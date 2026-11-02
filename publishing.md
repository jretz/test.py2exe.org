# Publishing to GitHub Pages

GitHub Actions runs `mise run build` when a pull request opens, reopens, or
receives new commits. Each push to `main` queues `mise run publish`. The
publishing job checks out the current `main` with its full history so queued
runs and retries deploy the latest source. Both jobs use
[mise-action][mise-action] with a three-day minimum release age for mise.

## First deployment

1. Under the repository's **Settings → Environments**, create
   `pages-publishing`. Set **Deployment branches and tags** to **Selected
   branches and tags** and add a branch rule for `main`. See [Environments][env].
2. Create a fine-grained personal access token from a repository administrator
   account with a verified email. Limit it to `jretz/test.py2exe.org` and grant
   **Contents: Read and write**. Save it as the environment secret
   `PAGES_PUBLISH_TOKEN`. A push using the default Actions token cannot trigger
   a branch-based Pages deployment. See the [publishing source guide][source].
3. Verify `test.py2exe.org` in the `jretz` account's Pages settings using
   GitHub's DNS TXT record. See the [domain verification guide][verify].
4. Push the generated source history to `main`. Wait for the
   **Publish documentation** job to create `gh-pages` with the built site.
5. Under **Settings → Pages**, select **Deploy from a branch**, choose
   `gh-pages` and `/(root)`, and save. Set the custom domain to
   `test.py2exe.org`.
6. Set these two `CNAME` records in your DNS provider. See the
   [custom domain guide][domains].

   | Host | Target |
   | --- | --- |
   | `test.py2exe.org` | `jretz.github.io.` |
   | `www.test.py2exe.org` | `jretz.github.io.` |

7. After DNS propagates and GitHub provisions the certificate, select **Enforce
   HTTPS** in Pages settings. GitHub Pages serves
   <https://test.py2exe.org/> and redirects <https://www.test.py2exe.org/> to it.

## Require the build before merging

After **Build documentation** passes on a pull request, create an active branch
ruleset under **Settings → Rules → Rulesets** that targets `main`. Enable
**Require a pull request before merging** and **Require status checks to pass**.
Add **Build documentation** from GitHub Actions, require branches to be up to
date before merging, and leave the bypass list empty. See [Rulesets][rulesets].

## Publish manually

Maintainers can also run the task from a full checkout of `main` with their
configured Git identity and GitHub SSH credentials. Their account needs write
access to `gh-pages`.

```sh
mise run publish
```

The task builds the committed `HEAD` in a temporary checkout. It generates
[Recent Changes](https://test.py2exe.org/recent-changes/) from the latest 20
documentation commits, including imported wiki edits while they fit. It runs
the site's Markdown checks and build once, adds `.nojekyll` and `CNAME` to the
rendered site, then creates `gh-pages` or pushes a fast-forward update to it.
If the branch changes during publishing, rerun the task. The repository's
**Actions** tab shows the GitHub Pages deployment status.

The [Zensical redirects plugin][redirects] builds static redirect pages for
legacy wiki URLs from `zensical.toml`. These pages redirect in the browser and
preserve URL fragments when JavaScript is enabled. Requests with legacy
attachment queries follow the article's redirect. The custom 404 page handles
legacy aliases that differ from a current path only by case. Unknown paths and
removed pages without a destination show the normal 404 page.

[mise-action]: https://github.com/jdx/mise-action
[env]: https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments
[rulesets]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
[verify]: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
[source]: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
[domains]: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
[redirects]: https://zensical.org/docs/setup/redirects/
