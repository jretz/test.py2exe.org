"""Build and publish GitHub Pages in a disposable checkout."""

import argparse
import contextlib
import os
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
from collections.abc import Callable, Generator, Mapping
from pathlib import Path, PureWindowsPath
from types import FrameType, MappingProxyType


PAGES_DOMAIN = "test.py2exe.org"
PAGES_REF = "refs/heads/gh-pages"


class TaskInterruptedError(Exception):
    """Allow cleanup to finish before reporting a termination signal."""

    @property
    def number(self) -> int:
        """Use the signal number to preserve conventional exit statuses."""
        return self.args[0]


def termination_numbers() -> frozenset[int]:
    """Select the termination signals available on the current platform.

    Returns:
        Signal numbers that should trigger task cleanup.
    """
    return frozenset(
        number
        for name in ("SIGINT", "SIGTERM", "SIGHUP", "SIGBREAK")
        if (number := getattr(signal, name, None)) is not None
    )


def interrupt_task(number: int, frame: FrameType | None) -> None:
    """Interrupt the task once and ignore repeated signals during cleanup.

    Raises:
        TaskInterruptedError: The received signal requests task termination.
    """
    del frame  # The signal callback requires a frame argument; cleanup does not.
    for handled in termination_numbers():
        signal.signal(handled, signal.SIG_IGN)
    raise TaskInterruptedError(number)


@contextlib.contextmanager
def termination_signals() -> Generator[None]:
    """Defer repeated termination signals while resource cleanup runs."""
    previous = MappingProxyType(
        {number: signal.getsignal(number) for number in termination_numbers()},
    )
    try:
        for number in previous:
            signal.signal(number, interrupt_task)
        yield
    finally:
        for number, handler in previous.items():
            signal.signal(number, handler)


def signal_process_group(process: subprocess.Popen[str], number: int) -> None:
    """Signal the POSIX process group if it still exists."""
    with contextlib.suppress(ProcessLookupError):
        os.killpg(process.pid, number)


def terminate_process_tree(process: subprocess.Popen[str]) -> None:
    """Force the task's process tree to exit using native platform tools."""
    if os.name != "nt":
        # Kill the group even when its parent has exited or descendants ignore SIGTERM.
        signal_process_group(process, signal.SIGKILL)
        return
    system = PureWindowsPath(os.environ.get("SYSTEMROOT", r"C:\Windows"))
    subprocess.run(
        (
            str(system / "System32" / "taskkill.exe"),
            "/PID",
            str(process.pid),
            "/T",
            "/F",
        ),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def stop_process_tree(process: subprocess.Popen[str]) -> None:
    """Release child-owned files before removing their temporary checkout."""
    if os.name == "nt" and process.poll() is not None:
        return
    terminate_process_tree(process)
    try:
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        if os.name == "nt":
            process.kill()
        else:
            signal_process_group(process, signal.SIGKILL)
        process.wait()


def start_command(
    arguments: tuple[str, ...],
    *,
    cwd: Path | None,
    environment: Mapping[str, str] | None,
    capture: bool,
) -> subprocess.Popen[str]:
    """Start a command in a process group with the requested output capture.

    Returns:
        The running child process, ready for collection or termination.
    """
    executable = shutil.which(
        arguments[0],
        path=(environment if environment is not None else os.environ).get("PATH"),
    )
    return subprocess.Popen(
        (executable or arguments[0], *arguments[1:]),
        cwd=cwd,
        env=environment,
        stdout=subprocess.PIPE if capture else None,
        text=True,
        encoding="utf-8" if capture else None,
        start_new_session=os.name != "nt",
        creationflags=(subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0),
    )


def run_command(
    arguments: tuple[str, ...],
    *,
    cwd: Path | None = None,
    environment: Mapping[str, str] | None = None,
    capture: bool = False,
) -> str:
    """Run the command and stop its process tree on interruption.

    Returns:
        Captured stdout, when requested.

    Raises:
        CalledProcessError: A nonzero exit status prevents the task from continuing.
    """
    process = start_command(
        arguments,
        cwd=cwd,
        environment=environment,
        capture=capture,
    )
    try:
        output = process.communicate()[0]
    except BaseException:
        stop_process_tree(process)
        raise
    if process.returncode:
        raise subprocess.CalledProcessError(process.returncode, arguments)
    return output or ""


def remove_readonly(
    function: Callable[[str], object],
    path: str,
    error: BaseException,
) -> None:
    """Allow cleanup of Git's read-only Windows object files."""
    if not isinstance(error, PermissionError):
        raise error
    Path(path).chmod(stat.S_IREAD | stat.S_IWRITE)
    function(path)


@contextlib.contextmanager
def temporary_directory(prefix: str) -> Generator[Path]:
    """Use Windows-aware deletion even when a child task fails.

    Yields:
        A disposable path whose cleanup also handles Git's read-only files.
    """
    directory = Path(tempfile.mkdtemp(prefix=prefix))
    try:
        yield directory
    finally:
        shutil.rmtree(directory, onexc=remove_readonly)


def build_site(root: Path, environment: Mapping[str, str]) -> None:
    """Build the site and require the generated Recent Changes page.

    Raises:
        ValueError: The build did not render the homepage or Recent Changes.
    """
    run_command(("mise", "run", "build"), cwd=root, environment=environment)
    if not (root / "site" / "index.html").is_file():
        msg = "The build did not produce the homepage."
        raise ValueError(msg)
    if not (root / "site" / "recent-changes" / "index.html").is_file():
        msg = "The build did not produce /recent-changes/."
        raise ValueError(msg)


def existing_pages_tip(
    git: tuple[str, ...],
    origin: str,
    environment: Mapping[str, str],
) -> str:
    """Fetch the existing publishing branch into the disposable repository.

    Returns:
        The fetched commit or an empty string if the branch does not exist.
    """
    branches = run_command(
        (*git, "ls-remote", "--refs", "--heads", "--", origin, PAGES_REF),
        capture=True,
        environment=environment,
    )
    if not branches:
        return ""
    run_command(
        (*git, "fetch", "--quiet", "--depth=1", "--no-tags", "--", origin, PAGES_REF),
        environment=environment,
    )
    return run_command(
        (*git, "rev-parse", "--verify", "FETCH_HEAD"),
        capture=True,
        environment=environment,
    ).strip()


def deployment_identity(
    root: Path,
    environment: Mapping[str, str],
) -> Mapping[str, str]:
    """Read the identity from the caller's repository configuration.

    Returns:
        An environment that also supplies the Git identity for the deployment.
    """
    identity = run_command(
        ("git", "var", "GIT_COMMITTER_IDENT"),
        cwd=root,
        capture=True,
        environment=environment,
    ).strip()
    name, address_and_date = identity.rsplit(" <", maxsplit=1)
    email = address_and_date.split("> ", maxsplit=1)[0]
    return MappingProxyType({
        **environment,
        "GIT_AUTHOR_NAME": name,
        "GIT_AUTHOR_EMAIL": email,
        "GIT_COMMITTER_NAME": name,
        "GIT_COMMITTER_EMAIL": email,
    })


def build_checkout(
    root: Path,
    checkout: Path,
    commit: str,
    environment: Mapping[str, str],
) -> None:
    """Build committed source and its local history outside the caller's checkout.

    Raises:
        ValueError: The content directory is a symbolic link or junction.
    """
    run_command(
        (
            "git",
            "clone",
            "--quiet",
            "--no-checkout",
            "--no-hardlinks",
            "--no-tags",
            "--",
            str(root),
            str(checkout),
        ),
        environment=environment,
    )
    run_command(
        ("git", "checkout", "--quiet", "--detach", commit),
        cwd=checkout,
        environment=environment,
    )
    build_environment = MappingProxyType({
        **environment,
        "MISE_TRUSTED_CONFIG_PATHS": str(checkout),
    })
    recent_changes = run_command(
        (sys.executable, str(checkout / "scripts" / "recent_changes.py")),
        cwd=checkout,
        environment=build_environment,
        capture=True,
    )
    source = checkout / "content" / "recent-changes.md"
    if source.parent.is_symlink() or source.parent.is_junction():
        msg = "The content directory must not be a symbolic link or junction."
        raise ValueError(msg)
    with source.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(recent_changes)
    build_site(checkout, build_environment)


def stage_site(site: Path, deployment: Path) -> None:
    """Copy the GitHub Pages build and add its branch publishing metadata.

    Raises:
        ValueError: The build contains symlinks or other unsupported entries.
    """
    if site.is_symlink() or site.is_junction():
        msg = "The build directory must not be a symbolic link or junction."
        raise ValueError(msg)
    for path in site.rglob("*"):
        if (
            path.is_symlink()
            or path.is_junction()
            or path.name.casefold() == ".git"
            or not (path.is_file() or path.is_dir())
        ):
            msg = f"Unsupported entry in the built site: {path.relative_to(site)}"
            raise ValueError(msg)
    shutil.copytree(site, deployment, symlinks=True)
    (deployment / ".nojekyll").write_bytes(b"")
    (deployment / "CNAME").write_bytes(f"{PAGES_DOMAIN}\n".encode())


def push_deployment(
    git: tuple[str, ...],
    origin: str,
    parent: str,
    source: str,
    environment: Mapping[str, str],
) -> None:
    """Push only the Pages branch, and reject any concurrent change to its tip."""
    run_command((*git, "add", "--force", "--all"), environment=environment)
    tree = run_command(
        (*git, "write-tree"),
        capture=True,
        environment=environment,
    ).strip()
    if parent:
        published_tree = run_command(
            (*git, "rev-parse", f"{parent}^{{tree}}"),
            capture=True,
            environment=environment,
        ).strip()
        if tree == published_tree:
            print("GitHub Pages already has this build.", flush=True)
            return
    commit = run_command(
        (
            *git,
            "commit-tree",
            tree,
            *(("-p", parent) if parent else ()),
            "-m",
            f"Publish documentation from {source}",
        ),
        capture=True,
        environment=environment,
    ).strip()
    # The new commit descends directly from the expected tip; the lease guards
    # against deletion or rewinding as well as another publisher advancing it.
    run_command(
        (
            *git,
            "push",
            "--no-follow-tags",
            "--recurse-submodules=no",
            f"--force-with-lease={PAGES_REF}:{parent}",
            "--",
            origin,
            f"{commit}:{PAGES_REF}",
        ),
        environment=environment,
    )
    print(f"Published {commit} to GitHub Pages for {PAGES_DOMAIN}.", flush=True)


def publish(root: Path) -> None:
    """Build committed HEAD once and publish the result to origin's Pages branch."""
    local_variables = frozenset(
        run_command(
            ("git", "rev-parse", "--local-env-vars"),
            cwd=root,
            capture=True,
        ).splitlines(),
    )
    environment = MappingProxyType({
        key: value for key, value in os.environ.items() if key not in local_variables
    })
    origin = run_command(
        ("git", "remote", "get-url", "--push", "origin"),
        cwd=root,
        capture=True,
        environment=environment,
    ).strip()
    source = run_command(
        ("git", "rev-parse", "--verify", "HEAD"),
        cwd=root,
        capture=True,
        environment=environment,
    ).strip()
    identity = deployment_identity(root, environment)
    with temporary_directory("py2exe-publish-") as workspace:
        metadata = workspace / "deployment.git"
        deployment = workspace / "deployment"
        checkout = workspace / "source"
        run_command(
            ("git", "init", "--quiet", "--bare", "--template=", str(metadata)),
            environment=environment,
        )
        git = ("git", f"--git-dir={metadata}")
        parent = existing_pages_tip(git, origin, environment)
        build_checkout(root, checkout, source, environment)
        stage_site(checkout / "site", deployment)
        push_deployment(
            (
                *git,
                "-C",
                str(deployment),
                f"--work-tree={deployment}",
                "-c",
                "core.autocrlf=false",
            ),
            origin,
            parent,
            source,
            identity,
        )


def main() -> int:
    """Use conventional exit statuses so mise can report failures and interruptions.

    Returns:
        Zero for success, a child failure status, or 128 plus the termination signal.
    """
    parser = argparse.ArgumentParser(
        description="Build and publish the site to GitHub Pages.",
    )
    parser.add_argument("command", choices=("publish",))
    parser.parse_args()
    try:
        with termination_signals():
            publish(Path(__file__).resolve().parent.parent)
    except TaskInterruptedError as error:
        return 128 + error.number
    except subprocess.CalledProcessError as error:
        print(
            f"{error.cmd[0]} failed with exit status {error.returncode}",
            file=sys.stderr,
        )
        return error.returncode if error.returncode > 0 else 128 - error.returncode
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
