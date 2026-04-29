# Releasing Dokmatiq DocGen SDKs

This document describes how the Dokmatiq DocGen SDKs are published, what
infrastructure is wired up, and what to do when you want to ship a new
version.

---

## TL;DR — How to ship a new release

1. Make code changes in the relevant SDK directory
2. Bump the version in that SDK's manifest file:

   | SDK        | File                            | Field            |
   | ---------- | ------------------------------- | ---------------- |
   | TypeScript | `typescript/package.json`       | `"version"`      |
   | Python     | `python/pyproject.toml`         | `version = "…"`  |
   | Java       | `java/pom.xml`                  | `<version>…</…>` |
   | .NET       | `dotnet/src/DocGen/DocGen.csproj` | `<Version>…</…>` |
   | PHP        | _(none — derived from git tag, see below)_ | — |

3. Commit and push to `main`
4. Tag and push the tag:

   ```bash
   git tag -a <sdk>-v<version> -m "<short release notes>"
   git push origin <sdk>-v<version>
   ```

   Tag patterns: `typescript-v0.1.2`, `python-v0.1.2`, `java-v0.1.2`,
   `dotnet-v0.1.2`. For PHP: `php-v0.1.2`.

5. The matching `.github/workflows/release-<sdk>.yml` workflow auto-runs
   and publishes to the registry. Watch the run at
   https://github.com/dokmatiq/docgen-sdks/actions

That's it for steady-state releases. The rest of this doc explains
what's behind the curtain.

---

## SDK distribution channels

| Language   | Registry         | Package name               | Install command                       |
| ---------- | ---------------- | -------------------------- | ------------------------------------- |
| TypeScript | npm              | `@dokmatiq/docgen`         | `npm install @dokmatiq/docgen`        |
| Python     | PyPI             | `dokmatiq-docgen`          | `pip install dokmatiq-docgen`         |
| Java       | Maven Central    | `com.dokmatiq:docgen-sdk`  | Maven/Gradle dependency               |
| .NET       | NuGet            | `Dokmatiq.DocGen`          | `dotnet add package Dokmatiq.DocGen`  |
| PHP        | Packagist        | `dokmatiq/docgen-sdk`      | `composer require dokmatiq/docgen-sdk`|

Plus auxiliary distributions:

| Artifact            | Channel                                       | Identifier                              |
| ------------------- | --------------------------------------------- | --------------------------------------- |
| MCP server (Python) | PyPI                                          | `dokmatiq-docgen-mcp`                   |
| MCP server          | Official MCP Registry                         | `io.github.dokmatiq/docgen`             |
| Claude Code plugin  | `dokmatiq/claude-plugins` marketplace repo    | `docgen@dokmatiq`                       |

---

## Per-channel reference

### npm — `@dokmatiq/docgen`

- **Account**: user `dokmatiq` on npmjs.com (created with `support@dokmatiq.com`)
- **Auth in CI**: repo secret `NPM_TOKEN` (Automation Token — bypasses 2FA)
- **Workflow**: `.github/workflows/release-typescript.yml`
- **Trigger**: push of tag `typescript-v*`
- **Behaviour**: `setup-node@v4` writes auth to `.npmrc` from
  `NODE_AUTH_TOKEN` env, then `npm publish`. `package.json` has
  `publishConfig.access = "public"` so the scoped package defaults to
  public.
- **Dry-run**: workflow has `workflow_dispatch` with `dry_run` input
  → runs `npm publish --dry-run`.

### PyPI — `dokmatiq-docgen` (and `dokmatiq-docgen-mcp`)

- **Account**: user `dokmatiq` on pypi.org (created with `support@dokmatiq.com`)
- **Auth in CI**: **OIDC Trusted Publisher** — _no token_, no secret.
  Configured at
  `pypi.org/manage/project/dokmatiq-docgen/settings/publishing/` to
  trust GitHub Actions runs of workflow `release-python.yml` from
  `dokmatiq/docgen-sdks`.
- **Workflow**: `.github/workflows/release-python.yml`
- **Trigger**: push of tag `python-v*`
- **Behaviour**: `python -m build` produces sdist + wheel, `twine check`,
  then the official `pypa/gh-action-pypi-publish` action exchanges a
  GitHub OIDC token for a short-lived PyPI publish token.
- **Dry-run**: same dispatch flow — builds and twine-checks but skips
  upload.

The MCP server package (`dokmatiq-docgen-mcp`) does **not** have a
release workflow yet. Currently published manually:

```bash
cd mcp
# bump version in pyproject.toml first
rm -rf dist build && pyproject-build
twine check dist/*
read -rs PYPI_TOKEN && \
  TWINE_USERNAME=__token__ TWINE_PASSWORD="$PYPI_TOKEN" twine upload dist/* && \
  unset PYPI_TOKEN
```

Local `.pypirc` (chmod 600) holds tokens for both prod PyPI and
TestPyPI for manual flows.

### Java — Maven Central via Sonatype Central Portal

- **Account**: `support@dokmatiq.com` on central.sonatype.com
- **Namespace**: `com.dokmatiq` — verified via DNS TXT record for
  `dokmatiq.com`
- **GPG key**: `C12EACF57D4E37EBCB5036C05947C16DB5496929` (RSA 4096, no
  expiry). Public key uploaded to `keyserver.ubuntu.com`.
- **Auth in CI** — four repo secrets:
  - `SONATYPE_USERNAME` / `SONATYPE_PASSWORD` (User Token from
    Sonatype's account page, not the Sonatype password)
  - `GPG_PRIVATE_KEY` (armored ASCII export, includes BEGIN/END lines)
  - `GPG_PASSPHRASE`
- **Workflow**: `.github/workflows/release-java.yml`
- **Trigger**: push of tag `java-v*`
- **Behaviour**:
  1. Verifies `pom.xml` `<version>` matches the tag (refuses to deploy
     on mismatch)
  2. Imports GPG key into the runner's keyring
  3. Writes `~/.m2/settings.xml` using `${env.SONATYPE_USERNAME}`
     placeholders so secret values never appear as literals in the
     filesystem
  4. Runs `mvn -B -P release deploy`. The `release` profile activates
     `bestPractices=true` on `maven-gpg-plugin`, which uses loopback
     pinentry and reads the passphrase from `MAVEN_GPG_PASSPHRASE`
     env var
  5. `central-publishing-maven-plugin` uploads the bundle.
     `<autoPublish>true</autoPublish>` in `pom.xml` makes Sonatype
     publish to Maven Central immediately after validation passes
- **Local interactive `mvn deploy`**: still works unchanged.
  pinentry-mac handles the passphrase via Keychain. The `release`
  profile is **not** activated for local builds.
- **Dry-run**: `workflow_dispatch` with `dry_run=true` runs
  `mvn -P release verify` — signs all artifacts but skips upload.

### NuGet — `Dokmatiq.DocGen`

- **Account**: Microsoft account at nuget.org (login as `Dokmatiq`)
- **Auth in CI**: repo secret `NUGET_API_KEY` — scoped to the glob
  `Dokmatiq.*`, expires in 1 year (NuGet maximum)
- **Workflow**: `.github/workflows/release-dotnet.yml`
- **Trigger**: push of tag `dotnet-v*`
- **Behaviour**: `dotnet pack` builds the `.nupkg` into `dist/`, then
  `dotnet nuget push dist/*.nupkg --api-key …`. `--skip-duplicate` is
  set so re-running an already-published version doesn't fail the
  workflow loudly.
- The `.csproj` has `<PackageReadmeFile>README.md</PackageReadmeFile>`
  + a matching `<None Include="../../README.md" Pack="true" …/>` so
  the README is embedded in the package and rendered on
  nuget.org/packages/Dokmatiq.DocGen.
- **Dry-run**: workflow_dispatch — packs only, doesn't push. NuGet
  validates the package internally for ~10 minutes after upload
  before listing it under "Published Packages" (until then it's
  under "Unlisted Packages" — that's normal during validation).

### Packagist — `dokmatiq/docgen-sdk` (PHP)

PHP is the odd one out because Packagist clones a Git repo and looks
for `composer.json` at the **root**, but our monorepo has it at
`php/composer.json`. So we maintain a **second** repo
(`dokmatiq/docgen-php`) that contains only the PHP SDK at root, and
Packagist consumes that.

- **Source of truth**: `php/` directory of this monorepo
- **Mirror repo**: github.com/dokmatiq/docgen-php (auto-synced)
- **Sync workflow**: `.github/workflows/sync-php-subtree.yml` —
  triggered on every push to `main` that touches `php/**`. Uses
  `git subtree split --prefix=php main`, then force-pushes the
  result to `dokmatiq/docgen-php`.
  - Auth: secret `DOCGEN_PHP_PUSH_TOKEN` — fine-grained PAT scoped
    to `dokmatiq/docgen-php` only with `Contents: read+write`
  - Important: `actions/checkout` is configured with
    `persist-credentials: false` so the GitHub-injected
    `extraheader` doesn't override our PAT-based push
- **Release flow**: tag in this monorepo with `php-v<version>` triggers
  the sync, then a Packagist webhook on the mirror repo notifies
  Packagist immediately.
- **Packagist webhook**: configured at
  `github.com/dokmatiq/docgen-php/settings/hooks` with URL
  `https://packagist.org/api/update-package?username=OliverLieven&apiToken=<safe-token>`.
  Uses Packagist's **Safe API Token** (not the Main Token) — limited
  to update operations only, lower blast radius if leaked.
- **Auto-update verified**: webhook returns 202; package gets
  refreshed within seconds of a tag push.

---

## Auxiliary CI

### Per-SDK build CI (every push, every PR)

`.github/workflows/ci-typescript.yml`, `ci-python.yml`, `ci-java.yml`,
`ci-dotnet.yml`, `ci-php.yml` — each runs only when its SDK directory
or its own workflow file changes (`paths:` filter).

What they cover:

| SDK        | Matrix             | Steps                                           |
| ---------- | ------------------ | ----------------------------------------------- |
| TypeScript | Node 18, 20, 22    | `npm ci` → `npm run typecheck` → `npm run build` |
| Python     | Python 3.11, 3.12, 3.13 | `pip install -e ".[dev]"` → smoke import → `mypy src` (strict) |
| Java       | JDK 17, 21         | `mvn -B compile`                                |
| .NET       | .NET 8.0           | `dotnet restore` → `dotnet build` (Release)     |
| PHP        | PHP 8.1, 8.2, 8.3, 8.4 | `composer validate` → `composer install` → `php -l` lint |

Status badges in the root README and per-SDK READMEs link to the
respective workflow runs page.

### PHP subtree sync (described above)

`.github/workflows/sync-php-subtree.yml` — fires on `php/**` changes.

---

## MCP server distribution

The MCP server (`mcp/` directory) is a separate concern from the SDKs.

### Channels and current state

| Channel                        | State                                  | Notes                                |
| ------------------------------ | -------------------------------------- | ------------------------------------ |
| **PyPI** `dokmatiq-docgen-mcp` | live (currently 0.1.2)                 | manual upload; no release workflow yet |
| **Official MCP Registry**      | `io.github.dokmatiq/docgen` v0.1.2     | submitted via `mcp-publisher` CLI    |
| **Glama.ai**                   | review submitted directly + auto from punkpeye list | Frank Fiegel runs both        |
| **PulseMCP**                   | auto-ingests from official Registry weekly | no manual submit needed          |
| **punkpeye/awesome-mcp-servers** | PR open                              | merge → auto-syncs to Glama          |
| **appcypher/awesome-mcp-servers** | not submitted                       | repo owner has disabled PRs entirely; skip |
| **Smithery.ai**                | not submitted                          | their submit form expects a hosted HTTP server, ours is stdio-only |

### Submitting an update to the Official MCP Registry

1. Bump version in `mcp/pyproject.toml` and `mcp/server.json` (must
   match)
2. Build + upload to PyPI (manual command above)
3. From the `mcp/` directory:

   ```bash
   mcp-publisher login github     # token cached locally; expires periodically
   mcp-publisher publish
   ```

The Registry will validate that the matching PyPI package contains
the literal string `mcp-name: io.github.dokmatiq/docgen` somewhere
in the README (HTML comment or visible). This is the ownership proof
— don't remove it from `mcp/README.md`.

### Authentication for the Registry

`mcp-publisher login github` uses GitHub OAuth and grants access to
the `io.github.<org>/*` namespace if the user is a **public** member
of that org. If publish fails with "permission to publish:
io.github.OliverLieven/*" instead of `io.github.dokmatiq/*`, the
membership visibility is set to private — change at
github.com/orgs/dokmatiq/people.

---

## Claude Code plugin

The plugin has been moved out of this monorepo into a dedicated
marketplace repo: **github.com/dokmatiq/claude-plugins**.

```
/plugin marketplace add dokmatiq/claude-plugins
/plugin install docgen@dokmatiq
```

The copy under `plugin/` in this repo is kept temporarily for
backward-compat and will be removed in a future release.

The plugin bundles:
- `skills/docgen/SKILL.md` with proper YAML frontmatter (name +
  trigger description) — without the frontmatter Claude Code's
  matcher cannot see the skill at all
- `.mcp.json` that auto-configures the `docgen` MCP server when the
  plugin is installed (reads `DOCGEN_API_KEY` from the user's env)

---

## Brand assets for marketplace listings

Public URLs:

| URL                                     | Format    | Use                          |
| --------------------------------------- | --------- | ---------------------------- |
| `https://dokmatiq.com/favicon.svg`      | SVG 512²  | preferred — small inline icons in markdown listings (`<img height="14"…/>`) |
| `https://raw.githubusercontent.com/dokmatiq/docgen-sdks/main/assets/dokmatiq-icon.png` | PNG 1024² | when SVG is not supported    |
| `https://raw.githubusercontent.com/dokmatiq/docgen-sdks/main/assets/dokmatiq-logo.svg` | SVG       | wordmark logo                |

The `assets/` folder contains copies of the canonical brand files
from `~/Entwicklung/Dokmatiq/brand/`. Update there first, then sync
into `assets/` if the branding changes.

---

## Common operations cheatsheet

### Cut a TypeScript release v0.1.3

```bash
cd typescript
# edit src/, run tests
sed -i '' 's/"version": "0.1.2"/"version": "0.1.3"/' package.json
cd ..
git add typescript/
git commit -m "Release TypeScript SDK v0.1.3"
git push origin main
git tag -a typescript-v0.1.3 -m "Release notes here"
git push origin typescript-v0.1.3
# Watch: https://github.com/dokmatiq/docgen-sdks/actions
```

### Cut a Maven Central release v0.1.3

```bash
cd java
# edit src/, run tests
# bump <version>0.1.3</version> in pom.xml
cd ..
git add java/
git commit -m "Release Java SDK v0.1.3"
git push origin main
git tag -a java-v0.1.3 -m "Release notes here"
git push origin java-v0.1.3
# Workflow takes ~10-30 min; check Maven Central with
# https://repo1.maven.org/maven2/com/dokmatiq/docgen-sdk/0.1.3/
```

### Validate a release workflow without publishing

GitHub UI → Actions → pick the workflow → "Run workflow" →
`dry_run = true` → "Run workflow". Catches GPG / token / settings
issues without burning a version.

### Update the MCP server description in the registry

Description changes only propagate via a new version (PyPI doesn't
allow re-uploading the same version, and the Registry pulls the
description from the published version). So:

1. Bump `mcp/pyproject.toml` version and `mcp/server.json` version
   together
2. Update description string in both files
3. Re-build, re-upload to PyPI (manual)
4. `mcp-publisher publish` from `mcp/`

---

## Troubleshooting

### `mcp-publisher publish` returns 401 "token expired"

Token is short-lived. Re-login:

```bash
mcp-publisher login github
mcp-publisher publish
```

### `mcp-publisher publish` returns 403 "permission to publish: io.github.OliverLieven/*"

Your dokmatiq org membership is private. Make it public at
github.com/orgs/dokmatiq/people, then re-login the publisher.

### Java release fails with "gpg: signing failed: Bad passphrase"

The `GPG_PASSPHRASE` secret value doesn't match the actual passphrase
of the imported GPG key. Locally test:

```bash
read -rs PHRASE && echo "test" | gpg --batch --pinentry-mode loopback \
  --passphrase "$PHRASE" --clearsign \
  --local-user C12EACF57D4E37EBCB5036C05947C16DB5496929 > /dev/null \
  && echo OK || echo FAIL
unset PHRASE
```

If OK: the secret value is wrong (often trailing whitespace from
copy-paste) — re-set carefully. If FAIL: the passphrase you have is
wrong; check 1Password again or ramp the worst-case path of
generating a new GPG key.

### npm publish fails with "402 payment required"

Scoped package is being published as private. Verify
`package.json` has:

```json
"publishConfig": { "access": "public" }
```

### PyPI returns 403 on first upload of a new package

The token in `~/.pypirc` is project-scoped and can only push to a
specific existing package. To push a new package, generate an
account-scoped ("Entire account") token for the first upload, then
revoke it and create a project-scoped one for ongoing use.
