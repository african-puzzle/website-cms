# website-cms

The Sveltia CMS admin for africanpuzzle.com, served at https://admin.africanpuzzle.com. It is two files and some favicons:

- `config.yml`: the collections and fields editors see. Each field writes into the `african-puzzle/website-frontend` repo, not this one.
- `index.html`: loads Sveltia from unpkg (unpinned) and holds all admin branding and CSS.

There is no build, no package manager, and no test suite. Site content lives in `website-frontend`; this repo changes only what the admin lets editors do.

## Deploy

GitHub Pages serves `main` from the repo root. A merge to `main` is live in about a minute, for every editor.

CAUTION: A `config.yml` error locks every editor out of the admin. Do steps 2 and 3 below and get a PR review before any merge to `main`.

## Changing config.yml

1. Read the `sveltia-cms` skill before the edit.
2. After the edit, run the skill's validation gate check; done means it prints `OK`.
3. If a collection or field name, type, or path changed, run the `cms-schema-drift` agent. Fix every `break` finding before the PR.
4. In the PR, write `closes #N` for the issue it resolves.
