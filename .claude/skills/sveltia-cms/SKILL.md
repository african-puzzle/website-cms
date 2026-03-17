---
name: sveltia-cms
description: >
  Use when working with Sveltia CMS configuration, theming, collections, widgets, i18n,
  or troubleshooting CMS errors. Triggers on config.yml changes for CMS admin panels,
  index.html with Sveltia/Netlify/Decap CMS script tags, or any CMS content modeling task.
user-invocable: false
---

# Sveltia CMS Development Guide

You are a Sveltia CMS expert. Apply this knowledge when editing CMS configuration, theming, collections, or troubleshooting CMS issues. Sveltia CMS is a Git-based headless CMS and direct replacement for Netlify CMS / Decap CMS, maintaining high compatibility with their config format.

**Docs reference**: https://sveltiacms.app/en/docs

---

## Field Name Rules (CRITICAL)

Field `name` values **MUST NOT** contain:
- Dots (`.`) — e.g., `site.name` is INVALID
- Spaces
- Asterisks (`*`)

**Allowed**: `snake_case` or `camelCase`. Examples: `site_name`, `navHome`, `hero_title`.

**Reserved names**:
- `title` — default `identifier_field`, used for entry title and slug
- `body` — main content placed after frontmatter

---

## Top-Level Config Options

```yaml
# Branding
logo:                          # Preferred (new format)
  src: /path/to/logo.svg
  show_in_header: true
logo_url: /path/to/logo.svg   # Deprecated but still works
app_title: "My CMS"           # Shown on login page and browser tab

# Backend
backend:
  name: github                 # github | gitlab | gitea | test
  repo: owner/repo
  branch: main
  base_url: https://...        # OAuth endpoint

# Site
site_url: https://example.com
display_url: https://example.com
logout_redirect_url: /

# Media
media_folder: public/images    # Relative to repo root
public_folder: /images         # URL prefix for media

# Workflow
publish_mode: simple           # simple | editorial_workflow

# Slug
slug:
  encoding: unicode            # unicode | ascii
  clean_accents: false
  sanitize_replacement: "-"

# Other
locale: en
search: true
show_preview_links: true
```

---

## Collection Types

### Entry Collections (folder-based)
```yaml
- name: posts
  label: Blog Posts
  folder: src/content/posts
  create: true
  extension: md
  format: yaml-frontmatter
  slug: "{{slug}}"
  fields:
    - { label: Title, name: title, widget: string }
    - { label: Body, name: body, widget: markdown }
```

### File Collections (specific files)
```yaml
- name: settings
  label: Settings
  files:
    - name: general
      label: General Settings
      file: src/content/settings.json
      fields:
        - { label: Site Name, name: site_name, widget: string }
```

### Singletons
```yaml
- name: homepage
  label: Homepage
  file: src/content/homepage.json
  fields:
    - { label: Hero Title, name: hero_title, widget: string }
```

### Common Collection Options
- `label`, `label_singular`, `description`
- `create: true/false` (folder collections only)
- `delete: true/false`, `publish: true/false`
- `hide: true/false`
- `sortable_fields: [field1, field2]`
- `identifier_field: title` (default)
- `summary: "{{title}} — {{date}}"`
- `filter: { field: status, value: published }`
- `view_filters`, `view_groups`
- `editor: { preview: false }`

---

## Widget Types

| Widget | Data Type | Key Options |
|--------|-----------|-------------|
| `string` | String | `default` |
| `text` | String (multiline) | `default` |
| `number` | String/Int/Float | `value_type: int\|float`, `min`, `max`, `step` |
| `boolean` | Boolean | `default: true\|false` |
| `datetime` | Date string | `format`, `date_format`, `time_format`, `picker_utc` |
| `select` | String/Array | `options` (required), `multiple`, `min`, `max` |
| `relation` | Referenced value | `collection`, `value_field`, `search_fields` (all required), `display_fields`, `multiple` |
| `object` | Nested fields | `fields` (required), `collapsed`, `summary` |
| `list` | Array | `field`/`fields`, `allow_add`, `collapsed`, `summary`, `min`, `max`, `add_to_top` |
| `markdown` | Markdown | `minimal`, `buttons`, `editor_components`, `modes` |
| `image` | File path | `media_folder`, `allow_multiple`, `choose_url` |
| `file` | File path | Same as image but any file type |
| `color` | Color string | `allowInput`, `enableAlpha` |
| `code` | Code string | `default_language`, `allow_language_selection`, `output_code_only` |
| `hidden` | Any | `default` (only supports `name`, `widget`, `default`, `i18n`) |
| `map` | GeoJSON | `type: Point\|LineString\|Polygon`, `decimals` |
| `uuid` | UUID string | Auto-generated, `readonly: true` by default |
| `compute` | Computed value | Sveltia-specific |
| `keyvalue` | Key-value pairs | Sveltia-specific |
| `richtext` | Rich text | Sveltia-specific, Lexical-based editor |

### Common Field Options (all widgets)
```yaml
- label: Display Name
  name: field_name          # snake_case or camelCase, NO dots/spaces/asterisks
  widget: string
  required: true            # Boolean or array of locale codes
  default: ""
  hint: "Helper text (markdown)"
  comment: "Description above input (markdown)"
  pattern: ["^[a-z]+$", "Must be lowercase"]
  readonly: false
  preview: true
  i18n: true                # true | translate | duplicate | (omit)
```

---

## i18n Configuration

### Top-level
```yaml
i18n:
  structure: multiple_folders  # multiple_folders | multiple_files | single_file
  locales: [en, fr, es]
  default_locale: en
```

### Collection-level
```yaml
- name: posts
  i18n: true                   # Inherit top-level i18n config
  # OR
  i18n:
    structure: single_file     # Override structure for this collection
    locales: [en, fr]
```

### Field-level
- `i18n: true` (or `i18n: translate`) — field is translatable
- `i18n: duplicate` — field is copied from default locale
- No `i18n` — field excluded from translations

### File collections
- Only `structure: single_file` is supported for file collections
- i18n must be enabled at both collection AND file level

---

## Theming & Branding

Sveltia CMS exposes internal `--sui-*` CSS custom properties. Override them in the `<style>` tag of your `index.html`:

```css
:root {
  /* Primary accent color */
  --sui-primary-accent-color-light: #f3e8ff;
  --sui-primary-accent-color: #8C30F5;
  --sui-primary-accent-color-dark: #6b21a8;
  --sui-primary-accent-color-inverted: #ffffff;

  /* Typography */
  --sui-primary-font-family: 'Montserrat', system-ui, sans-serif;
  --sui-primary-heading-font-family: 'Nunito', system-ui, sans-serif;

  /* Secondary accent */
  --sui-secondary-accent-color: #1a7a6d;
}
```

### Login page branding
- Set `logo.src` (or `logo_url`) in config for the logo on the login screen
- Set `app_title` for custom title text
- Target login elements with `[class*="login"], [class*="auth"]` CSS selectors
- Add Google Fonts via `<link>` in `index.html` `<head>`
- Favicons via standard `<link rel="icon">` tags

### Additional CSS targets
```css
/* Sidebar / navigation */
[class*="sidebar"], [class*="nav-bar"], nav[role="navigation"] { }

/* Header accent line */
header::after { content: ''; height: 2px; background: linear-gradient(...); }

/* Collection list hover */
[class*="list-item"]:hover { background-color: #f3e8ff; }

/* Save/publish buttons */
button[class*="publish"], button[class*="save"] { }
```

---

## Backends

### GitHub (recommended — uses GraphQL for best performance)
```yaml
backend:
  name: github
  repo: owner/repo
  branch: main
  base_url: https://your-oauth-server.example.com  # External OAuth
```

### GitLab
```yaml
backend:
  name: gitlab
  repo: owner/repo
  auth_type: pkce
  app_id: your-app-id
```

### Commit Message Templates
```yaml
backend:
  commit_messages:
    create: "Create {{collection}} "{{slug}}""
    update: "Update {{collection}} "{{slug}}""
    delete: "Delete {{collection}} "{{slug}}""
    uploadMedia: "Upload "{{path}}""
    deleteMedia: "Delete "{{path}}""
```

Template tags: `{{slug}}`, `{{collection}}`, `{{path}}`, `{{message}}`, `{{author-login}}`, `{{author-name}}`

---

## Common Patterns & Best Practices

### Translation files (flat JSON via file collections)
Use underscore-delimited field names that map to JSON keys:
```yaml
- name: translations
  label: Translations
  files:
    - name: en
      label: English
      file: src/i18n/en.json
      fields:
        - { label: 'Site Name', name: site_name, widget: string }
        - { label: 'Nav Home', name: nav_home, widget: string }
```
This produces `{"site_name": "...", "nav_home": "..."}` in the JSON file.

### Grouped settings with object widgets
```yaml
fields:
  - label: Site
    name: site
    widget: object
    fields:
      - { label: Name, name: name, widget: string }
      - { label: Tagline, name: tagline, widget: string }
```
This produces `{"site": {"name": "...", "tagline": "..."}}`.

### Multilingual content fields
```yaml
- label: Role
  name: role
  widget: object
  fields:
    - { label: French, name: fr, widget: string }
    - { label: English, name: en, widget: string }
```

---

## Troubleshooting

### Config validation errors block login
Sveltia CMS validates the entire config before rendering the login screen. ANY validation error will show an error page and prevent access. Common causes:
- Field names with dots, spaces, or asterisks
- Duplicate collection or field names
- Invalid relation references
- Mutually exclusive options

### Logo not showing on login
- Ensure `logo.src` (or `logo_url`) points to an accessible URL
- If using external URL, verify CORS headers allow loading
- Config errors prevent the CMS from initializing, which also hides the logo

### Custom CSS not applying
- CSS in `index.html` `<style>` tags loads before the CMS JS
- The CMS renders inside Shadow DOM for some elements — `--sui-*` variables work because they cascade through
- Use `!important` sparingly for button overrides
- Google Fonts must be loaded via `<link>` in `<head>`

---

## Key Differences from Netlify/Decap CMS

1. **Stricter field name validation** — dots are rejected (Netlify CMS was more lenient)
2. **Additional widgets**: `uuid`, `compute`, `keyvalue`, `richtext`
3. **GraphQL API** for GitHub backend (faster)
4. **Built-in asset management** with multiple storage providers
5. **No separate server** — runs entirely in-browser
6. **`logo` object** preferred over `logo_url` (deprecated)
7. **`app_title`** config option for custom login page title
8. **Stock photo integrations** (Pexels, Pixabay, Unsplash)
9. **Translation service integrations** (DeepL, Google Translate)
10. **Single SPA** under 600KB (minified + brotli)
