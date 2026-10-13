---
name: sveltia-cms
description: Sveltia CMS rules for this repo's config.yml and index.html. Use when adding or changing a collection or field, restyling the admin UI, or when the admin shows a config error or blank login.
user-invocable: false
---

# Sveltia CMS

Sveltia CMS is a browser-only, Git-based CMS that reads the Netlify/Decap `config.yml` format with stricter validation. Official docs: https://sveltiacms.app/en/docs. When a rule below and the docs disagree, the docs win.

## The validation gate

Sveltia validates the whole `config.yml` before it draws the login screen. One error anywhere shows an error page and locks every editor out of the admin. Four of this repo's past fixes were this failure. Run the check after every `config.yml` edit; done means it prints `OK`:

```bash
uv run --with pyyaml python .claude/skills/sveltia-cms/check_config.py
```

It catches the errors this repo has hit. It does not replace Sveltia's own validator, so open the admin after deploy to confirm the login screen loads.

## Field names

- Write `name` in camelCase or snake_case. A dot, space, or asterisk fails validation (`site.name` broke all 225 translation fields once).
- `title` is the default `identifier_field` (entry title and slug).
- `body` is the text after the frontmatter in a Markdown entry. In a JSON file collection it does not become a JSON key, so name the field after the key the frontend reads (`countries`, `posts`).
- The field `name` is the key written to the frontend repo. It must match the Zod schema in `website-frontend/src/content.config.ts`, or the frontend build fails. For a cross-repo check, use the `cms-schema-drift` agent.

## Collection shapes

Every collection has exactly one of `folder` or `files`.

- **Folder collection**: one Markdown file per entry (`team`, `features`, `privacy`). Uses `folder`, `create`, `extension: md`, `format: yaml-frontmatter`, `fields`.
- **Files collection**: fixed files, each listed under `files` with its own `name`, `label`, `file`, `fields` (`countries`, `site-settings`, `contact`, `translations`). A single settings file is still a one-item `files` list; a bare `file:` at collection level is invalid.
- File names inside one `files` list must be unique; a duplicate `about-page` entry once blocked login.

The frontend's Astro `file()` loader decides the JSON shape it accepts. Check the loader's `parser` option before you change a list field's wrapper key.

## Multilingual content

The site has three locales: `fr` (source), `en`, `pcm` (Pidgin). This config does not use Sveltia's `i18n` option. It uses two patterns:

- An `object` field with `fr`, `en`, `pcm` subfields (`team.role`).
- One file per locale (`translations` > `fr`/`en`/`pcm`, `privacy` entries with a `locale` select).

When you add a translatable field, add it for all three locales.

## Sveltia-only widgets

Beyond the Decap widget set: `uuid`, `compute`, `keyvalue`, `richtext`. `hidden` accepts only `name`, `widget`, `default`, `i18n`.

## Admin UI styling

All styling and branding lives in `index.html`.

- Brand colors and fonts go through the `--sui-*` custom properties in `:root`; they cross Sveltia's Shadow DOM.
- The `[class*="..."]` selectors target Sveltia's internal class names. A Sveltia release can rename them with no warning, because `index.html` loads the latest build from unpkg with no version pin. After a style breaks, inspect the live DOM before you edit selectors.
- Sveltia overwrites `document.title` and shows "Sveltia CMS" text; the inline `MutationObserver` script restores the African Puzzle brand. Keep it when you edit `index.html`.
- Keep text at 16px minimum; uppercase field labels are the one 14px exception (issue #15).
