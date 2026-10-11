"""Catch the config.yml errors that made Sveltia CMS refuse to load (login blocked).

Usage: uv run --with pyyaml python .claude/skills/sveltia-cms/check_config.py [config.yml]
Exit 0 = clean, 1 = errors printed. Not a full schema check; Sveltia's own validator is the authority.
"""
import re
import sys

import yaml

BAD_NAME = re.compile(r"[.\s*]")


def check_fields(fields, where, errors, json_file=False):
    seen = set()
    for f in fields or []:
        name = f.get("name")
        loc = f"{where} > {name}"
        if not name:
            errors.append(f"{where}: field without a name")
            continue
        if BAD_NAME.search(name):
            errors.append(f"{loc}: name has a dot, space, or asterisk")
        if name in seen:
            errors.append(f"{loc}: duplicate field name")
        seen.add(name)
        if json_file and name == "body":
            errors.append(f"{loc}: 'body' is reserved; in a JSON file it does not become a key")
        check_fields(f.get("fields"), loc, errors)
        if isinstance(f.get("field"), dict):
            check_fields([f["field"]], loc, errors)


def check(config):
    errors = []
    seen = set()
    for c in config.get("collections") or []:
        name = c.get("name")
        if name in seen:
            errors.append(f"{name}: duplicate collection name")
        seen.add(name)
        if ("folder" in c) == ("files" in c):
            errors.append(f"{name}: needs exactly one of 'folder' or 'files' (a bare 'file' is not valid)")
        check_fields(c.get("fields"), name, errors)
        file_names = set()
        for f in c.get("files") or []:
            if f.get("name") in file_names:
                errors.append(f"{name} > {f.get('name')}: duplicate file name")
            file_names.add(f.get("name"))
            check_fields(f.get("fields"), f"{name} > {f.get('name')}", errors, str(f.get("file", "")).endswith(".json"))
    return errors


def demo():
    bad = {"collections": [
        {"name": "a", "file": "x.json", "fields": [{"name": "site.name"}]},
        {"name": "a", "folder": "f", "fields": [{"name": "t"}, {"name": "t"}]},
        {"name": "s", "files": [
            {"name": "p", "file": "p.json", "fields": [{"name": "body"}]},
            {"name": "p", "file": "q.json", "fields": []},
        ]},
    ]}
    assert len(check(bad)) == 6, check(bad)
    assert check({"collections": [{"name": "ok", "folder": "f", "fields": [{"name": "body"}]}]}) == []


if __name__ == "__main__":
    demo()
    path = sys.argv[1] if len(sys.argv) > 1 else "config.yml"
    errs = check(yaml.safe_load(open(path)))
    print("\n".join(errs) or f"{path}: OK")
    sys.exit(1 if errs else 0)
