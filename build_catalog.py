#!/usr/bin/env python3
"""Regenerate apps.json from the .vx files in apps/.

Each app describes itself in its own VX: headers — name, icon, version,
author, and (optional) summary / category / featured. Whether the file
carries a "# VX:sig=" line decides the Verified badge. Rich fields already
present in apps.json are kept when a header doesn't override them, so any
hand-tuned summaries survive.

Workflow: drop a signed .vx into apps/, run publish.ps1 (which runs this
then commits + pushes). Render.com redeploys from the new commit.
"""
import os, json, glob, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
APPS = os.path.join(ROOT, "apps")
OUT  = os.path.join(ROOT, "apps.json")
BASE = "https://raw.githubusercontent.com/vincentilagan/LStore/main"


def read_headers(path):
    """Return ({header:value}, signed_bool) from the top VX: block."""
    h, signed = {}, False
    with open(path, encoding="utf-8", errors="replace") as f:
        for _ in range(14):
            line = f.readline()
            if not line:
                break
            s = line.strip()
            if not s.startswith("# VX:"):
                if h:            # header block ended
                    break
                continue         # allow leading blank/shebang lines
            if s.startswith("# VX:sig="):
                signed = True
                continue
            kv = s[5:].split("=", 1)
            if len(kv) == 2:
                h[kv[0].strip().lower()] = kv[1].strip()
    return h, signed


def load_existing():
    try:
        with open(OUT, encoding="utf-8") as f:
            return {a["id"]: a for a in json.load(f).get("apps", [])}
    except Exception:
        return {}


def truthy(v):
    return str(v).lower() in ("1", "true", "yes", "on")


def main():
    existing = load_existing()
    apps = []
    for vx in sorted(glob.glob(os.path.join(APPS, "*.vx"))):
        fname = os.path.basename(vx)
        appid = fname[:-3].lower()
        h, signed = read_headers(vx)
        prev = existing.get(appid, {})
        summary = h.get("summary", prev.get("summary", ""))
        apps.append({
            "id": appid,
            "name": h.get("name", prev.get("name", appid.title())),
            "file": fname,
            "version": h.get("version", prev.get("version", "1.0")),
            "author": h.get("author", prev.get("author", "Vincent Ilagan")),
            "category": h.get("category", prev.get("category", "App")),
            "icon": h.get("icon", prev.get("icon", "\U0001F4E6")),
            "featured": truthy(h.get("featured", "")) or prev.get("featured", False),
            "summary": summary,
            "description": prev.get("description", summary),
            "install": "apps/" + fname,
            "signed": signed,
        })
    catalog = {
        "store": "LStore",
        "tagline": "The Luci OS App Store",
        "publisher": "Vincent Ilagan",
        "updated": datetime.date.today().isoformat(),
        "base": BASE,
        "apps": apps,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote apps.json with %d app(s):" % len(apps))
    for a in apps:
        print("  - %-12s v%-5s %s" % (
            a["name"], a["version"], "Verified" if a["signed"] else "developer"))


if __name__ == "__main__":
    main()
