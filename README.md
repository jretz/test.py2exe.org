# py2exe Documentation

This is documentation for py2exe, built from Markdown with
[Zensical](https://zensical.org/) and hosted on
[test.py2exe.org](https://test.py2exe.org/) through GitHub Pages. The Git
history preserves the former
[MoinMoin](https://moinmo.in/) wiki's revisions, including edit dates and
authors.

## Making Changes

Fork and clone this repository, then edit the pages under `content/`. Use
relative `.md` links between pages and keep attachments in an `assets/`
directory beside the page that uses them. The generated site navigation follows
the directory structure, with each page's first heading supplying its title.

To preview the documentation, install [mise](https://mise.jdx.dev/), then run
this from the repository root:

```sh
mise run serve-preview
```

Mise installs the required tools, checks the Markdown, and serves a preview.
Stop it with Ctrl-C.
These commands work in Linux and macOS terminals, Windows PowerShell, and
Command Prompt.

Before committing your changes, run `mise run build` to check the Markdown and
ensure that the site can be built. Request that your changes be published by
opening a pull request in this repository.

GitHub Actions checks pull requests and publishes the site after pushes to
`main`. See [Publishing to GitHub Pages](publishing.md) for setup and deployment
details.
