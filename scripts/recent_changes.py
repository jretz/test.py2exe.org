"""Keep publish-time history independent of the caller's checkout and timezone."""

import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from html import unescape
from itertools import chain, groupby, islice
from pathlib import Path, PurePosixPath
from textwrap import wrap
from types import MappingProxyType
from urllib.parse import quote


LIMIT = 20
REPOSITORY = "https://github.com/jretz/test.py2exe.org"
RELOCATION = "Move wiki pages and attachments into the Zensical layout"
CONVERSION = "Convert wiki pages to Markdown and add Zensical configuration"
GENERATED_PAGE = "content/recent-changes.md"
STATUSES = MappingProxyType(
    {
        "A": "added",
        "M": "updated",
        "R": "renamed",
        "D": "removed",
    },
)


@dataclass(frozen=True, kw_only=True)
class Commit:
    """UTC dates keep day boundaries independent of the publisher's timezone."""

    sha: str
    parent: str
    timestamp: datetime
    author: str
    subject: str


@dataclass(frozen=True, kw_only=True)
class FileChange:
    """An old path distinguishes renames from additions and removals."""

    status: str
    path: str
    old_path: str | None = None


@dataclass(frozen=True, kw_only=True)
class Entry:
    """Grouping by commit keeps a multi-page edit in one history slot."""

    commit: Commit
    pages: tuple[FileChange, ...]
    archived: bool


@dataclass(frozen=True, kw_only=True)
class Repository:
    """Pair a checkout with the environment used for local Git commands."""

    root: Path
    environment: Mapping[str, str]


@dataclass(frozen=True, kw_only=True)
class History:
    """Separate modern edits from archived wiki edits at the migration boundary."""

    modern: tuple[Commit, ...]
    archive: tuple[Commit, ...] = ()
    relocation: str | None = None


def git(repository: Repository, *arguments: str) -> bytes:
    """Run Git in the selected checkout without a shell.

    Returns:
        The command's standard output as bytes.

    Raises:
        FileNotFoundError: Git is unavailable in the selected environment.
    """
    executable = shutil.which("git", path=repository.environment.get("PATH"))
    if executable is None:
        msg = "Git is required to generate Recent Changes."
        raise FileNotFoundError(msg)
    return subprocess.run(
        (executable, *arguments),
        cwd=repository.root,
        env=repository.environment,
        stdout=subprocess.PIPE,
        check=True,
    ).stdout


def nul_fields(data: bytes) -> tuple[str, ...]:
    """Decode Git's NUL-delimited output.

    Returns:
        Decoded fields without the trailing record terminator.
    """
    if not data:
        return ()
    return tuple(data.removesuffix(b"\0").decode("utf-8", errors="replace").split("\0"))


def parse_commits(data: bytes) -> tuple[Commit, ...]:
    """Parse the five fields emitted for each commit by ``read_commits``.

    Returns:
        Commits in their original order with timestamps normalized to UTC.
    """
    fields = iter(nul_fields(data))
    return tuple(
        Commit(
            sha=sha,
            parent=parent,
            timestamp=datetime.fromisoformat(date).astimezone(UTC),
            author=author,
            subject=subject,
        )
        for sha, parent, date, author, subject in zip(
            fields,
            fields,
            fields,
            fields,
            fields,
            strict=True,
        )
    )


def read_commits(repository: Repository, head: str) -> tuple[Commit, ...]:
    """Read non-merge commits reachable from the selected revision.

    Returns:
        Commit metadata in Git's date order.
    """
    return parse_commits(
        git(
            repository,
            "log",
            "--no-merges",
            "--date-order",
            "--encoding=UTF-8",
            "-z",
            "--format=%H%x00%P%x00%aI%x00%an%x00%s",
            head,
        ),
    )


def parse_changes(data: bytes) -> tuple[FileChange, ...]:
    """Parse NUL-delimited name-status records, including paired rename paths.

    Returns:
        Changes in their original order without similarity scores.
    """
    fields = iter(nul_fields(data))
    changes = []
    for status in filter(None, fields):
        path = next(fields)
        changes.append(
            FileChange(status=status[0], path=next(fields), old_path=path)
            if status.startswith(("R", "C"))
            else FileChange(status=status[0], path=path),
        )
    return tuple(changes)


def read_changes(
    repository: Repository,
    sha: str,
    *,
    rename: str = "-M",
) -> tuple[FileChange, ...]:
    """Read a commit's file changes using the requested rename threshold.

    Returns:
        File statuses and paths from Git's tree comparison.
    """
    return parse_changes(
        git(
            repository,
            "diff-tree",
            "--root",
            "--no-commit-id",
            "--no-ext-diff",
            "--no-textconv",
            "--name-status",
            "-r",
            "-z",
            rename,
            sha,
        ),
    )


def is_page(path: str) -> bool:
    """Identify authored Markdown beneath the site's content directory.

    Returns:
        Whether the path is a page other than generated Recent Changes.
    """
    return (
        path.startswith("content/") and path.endswith(".md") and path != GENERATED_PAGE
    )


def modern_change(change: FileChange) -> FileChange | None:
    """Translate a file change into its effect on the site's pages.

    Returns:
        A page change, or None for paths and statuses outside the page history.
    """
    path_is_page = is_page(change.path)
    if change.status == "R" and change.old_path:
        if is_page(change.old_path):
            return (
                change if path_is_page else FileChange(status="D", path=change.old_path)
            )
        return FileChange(status="A", path=change.path) if path_is_page else None
    return change if path_is_page and change.status in STATUSES else None


def wiki_body(raw: bytes) -> tuple[bytes, ...]:
    """Remove only MoinMoin's leading access-control instructions.

    Returns:
        Page lines suitable for detecting changes beyond permissions.
    """
    # MoinMoin only interprets processing instructions at the start of a page.
    lines = raw.splitlines()
    start = 0
    while start < len(lines) and lines[start].startswith(b"#"):
        start += 1
    return (
        *[line for line in lines[:start] if not re.match(rb"#acl(?:\s|$)", line)],
        *lines[start:],
    )


def archive_change(
    change: FileChange,
    aliases: Mapping[str, str],
) -> FileChange | None:
    """Map a retained wiki edit to the page's modern path.

    Returns:
        The mapped change, or None when no retained page is affected.
    """
    path = aliases.get(change.path)
    if change.status == "R" and change.old_path:
        old_path = aliases.get(change.old_path)
        if path or old_path:
            return FileChange(
                status="R",
                path=path or old_path or "",
                old_path=old_path,
            )
    if path is None or change.status not in STATUSES:
        return None
    return FileChange(status=change.status, path=path)


def split_history(commits: tuple[Commit, ...]) -> History:
    """Locate the paired relocation and conversion commits.

    Returns:
        Modern and archived edits with migration commits omitted when found.
    """
    relocation_candidates = {c.sha for c in commits if c.subject == RELOCATION}
    conversion = next(
        (
            c
            for c in commits
            if c.subject == CONVERSION and c.parent in relocation_candidates
        ),
        None,
    )
    if conversion is None:
        return History(modern=commits)
    boundary = next(i for i, c in enumerate(commits) if c.sha == conversion.parent)
    return History(
        modern=tuple(c for c in commits[:boundary] if c != conversion),
        archive=commits[boundary + 1 :],
        relocation=conversion.parent,
    )


def page_aliases(changes: tuple[FileChange, ...]) -> Mapping[str, str]:
    """Collect the page renames recorded by the relocation commit.

    Returns:
        An immutable mapping from wiki filenames to Markdown paths.
    """
    return MappingProxyType(
        {
            change.old_path: change.path
            for change in changes
            if change.status == "R" and change.old_path and is_page(change.path)
        },
    )


def is_editorial(repository: Repository, sha: str, change: FileChange) -> bool:
    """Distinguish wiki edits from changes only to access-control instructions.

    Returns:
        Whether the change affects page content, existence, or location.
    """
    if change.status != "M":
        return True
    before = git(repository, "show", f"{sha}^:{change.path}")
    after = git(repository, "show", f"{sha}:{change.path}")
    return wiki_body(before) != wiki_body(after)


def read_pages(
    repository: Repository,
    commit: Commit,
    aliases: Mapping[str, str] | None,
) -> tuple[FileChange, ...]:
    """Select documentation changes from a modern or archived commit.

    Returns:
        Page changes with archived paths mapped and permission-only edits omitted.
    """
    changes = read_changes(repository, commit.sha)
    if aliases is None:
        return tuple(page for change in changes if (page := modern_change(change)))
    return tuple(
        page
        for change in changes
        if (page := archive_change(change, aliases))
        and is_editorial(repository, commit.sha, change)
    )


def read_history_entries(
    repository: Repository,
    commits: tuple[Commit, ...],
    aliases: Mapping[str, str] | None = None,
) -> Iterator[Entry]:
    """Collect commits that contain at least one documentation change.

    Yields:
        Entries in descending UTC author-date order.
    """
    for commit in sorted(commits, key=lambda commit: commit.timestamp, reverse=True):
        if pages := read_pages(repository, commit, aliases):
            yield Entry(commit=commit, pages=pages, archived=aliases is not None)


def read_entries(repository: Repository, head: str) -> tuple[Entry, ...]:
    """Fill the Recent Changes limit from modern edits and then archived edits.

    Returns:
        At most LIMIT documentation entries for the selected revision.
    """
    history = split_history(read_commits(repository, head))
    aliases = page_aliases(
        read_changes(repository, history.relocation, rename="-M100%")
        if history.relocation
        else (),
    )
    return tuple(
        islice(
            chain(
                read_history_entries(repository, history.modern),
                read_history_entries(repository, history.archive, aliases),
            ),
            LIMIT,
        ),
    )


def page_title(path: str, source: str) -> str:
    """Choose a display title from the page heading or its path.

    Returns:
        Home for the front page, or the page's heading or readable filename.
    """
    if path == "content/index.md":
        return "Home"
    if heading := re.match(r"\s*#\s+([^\n]+)", source):
        return unescape(heading[1].strip())
    article = PurePosixPath(path)
    label = article.parent.name if article.stem == "index" else article.stem
    return label.replace("-", " ").capitalize()


def public_text(value: str) -> str:
    """Escape metadata for display as literal Markdown text.

    Returns:
        A single line with markup punctuation encoded as character references.
    """
    # Treat Git metadata as display text, including markup and autolink syntax.
    return re.sub(
        r"[\\`*_{}\[\]<>()~!&$^+=:#@]",
        lambda match: f"&#{ord(match[0])};",
        " ".join(value.split()),
    )


def render_page(page: FileChange, titles: Mapping[str, str]) -> str:
    """Describe one page change, linking only to pages present in the snapshot.

    Returns:
        A Markdown label with a status suffix for additions, renames, and removals.
    """
    label = public_text(titles.get(page.path) or page_title(page.path, ""))
    if page.status != "D" and page.path in titles:
        destination = quote(page.path.removeprefix("content/"))
        label = f"[{label}]({destination})"
    if page.status != "M":
        label = f"{label} ({STATUSES[page.status]})"
    return label


def change_summary(pages: tuple[FileChange, ...]) -> str:
    """Summarize the number of pages affected by each kind of change.

    Returns:
        A compact status summary for the entry's details panel.
    """
    counts = Counter(page.status for page in pages)
    if len(counts) == 1:
        status, count = counts.most_common()[0]
        return f"{count} {'page' if count == 1 else 'pages'} {STATUSES[status]}"
    return " · ".join(
        f"{count} {STATUSES[status]}"
        for status in STATUSES
        if (count := counts[status])
    )


def render_entry(entry: Entry, titles: Mapping[str, str]) -> Iterator[str]:
    """Render a commit with its author, UTC time, diff link, and changed pages.

    Yields:
        Markdown lines for the entry and its collapsible page list.
    """
    commit = entry.commit
    subject = public_text(commit.subject or "Documentation update")
    subject_lines = wrap(f"**{subject}**", width=76, break_on_hyphens=False)
    yield from subject_lines[:-1]
    yield f"{subject_lines[-1]}  "
    author = public_text(commit.author or "Anonymous")
    yield from wrap(f"{commit.timestamp:%H:%M} · {author} ·", width=80)
    yield f"[Diff][diff-{commit.sha}]"
    yield ""
    yield f'??? info "{change_summary(entry.pages)}"'
    yield ""
    for page in entry.pages:
        yield from wrap(
            render_page(page, titles),
            width=80,
            initial_indent="    - ",
            subsequent_indent="      ",
            break_long_words=False,
            break_on_hyphens=False,
        )
    yield ""


def render_days(
    entries: tuple[Entry, ...],
    titles: Mapping[str, str],
    heading: str,
) -> Iterator[str]:
    """Group adjacent entries by their UTC calendar date.

    Yields:
        Markdown date headings at the requested level followed by their entries.
    """
    for day, changes in groupby(
        entries,
        key=lambda entry: entry.commit.timestamp.date(),
    ):
        yield f"{heading} {day:%B} {day.day}, {day.year}"
        yield ""
        for change in changes:
            yield from render_entry(change, titles)


def read_titles(
    repository: Repository,
    head: str,
    entries: tuple[Entry, ...],
) -> Mapping[str, str]:
    """Read display titles for changed pages that still exist in the snapshot.

    Returns:
        An immutable mapping from current page paths to their titles.
    """
    current_pages = frozenset(
        nul_fields(git(repository, "ls-tree", "-r", "--name-only", "-z", head)),
    )
    displayed_pages = {page.path for entry in entries for page in entry.pages}
    return MappingProxyType(
        {
            path: page_title(
                path,
                git(repository, "show", f"{head}:{path}").decode(
                    "utf-8",
                    errors="replace",
                ),
            )
            for path in sorted(current_pages & displayed_pages)
        },
    )


def render_history(
    entries: tuple[Entry, ...],
    titles: Mapping[str, str],
) -> str:
    """Assemble the generated page with separate modern and imported history.

    Returns:
        Markdown with generation metadata and repository diff references.
    """
    lines = [
        "---",
        "generated_recent_changes: true",
        "---",
        "",
        "# Recent Changes",
        "",
        "[Commit history][commit-history]",
        "",
    ]
    if not entries:
        lines.extend(["No documentation changes yet.", ""])
    modern = tuple(entry for entry in entries if not entry.archived)
    archive = tuple(entry for entry in entries if entry.archived)
    lines.extend(render_days(modern, titles, "##"))
    if archive:
        lines.extend(["## Imported wiki history", ""])
        lines.extend(render_days(archive, titles, "###"))
    lines.append(f"[commit-history]: {REPOSITORY}/commits/main/")
    lines.extend(
        f"[diff-{entry.commit.sha}]: {REPOSITORY}/commit/{entry.commit.sha}"
        for entry in entries
    )
    return "\n".join(lines).rstrip() + "\n"


def render_recent_changes(
    root: Path,
    *,
    environment: Mapping[str, str] | None = None,
) -> str:
    """Use one HEAD snapshot so titles and diffs remain consistent.

    Returns:
        Markdown whose relative links resolve from the content root.
    """
    repository = Repository(
        root=root,
        environment=MappingProxyType(
            {
                **(os.environ if environment is None else environment),
                "GIT_NO_LAZY_FETCH": "1",
            },
        ),
    )
    head = git(repository, "rev-parse", "--verify", "HEAD").decode("ascii").strip()
    entries = read_entries(repository, head)
    return render_history(entries, read_titles(repository, head, entries))


if __name__ == "__main__":
    sys.stdout.buffer.write(
        render_recent_changes(Path(__file__).resolve().parent.parent).encode("utf-8"),
    )
