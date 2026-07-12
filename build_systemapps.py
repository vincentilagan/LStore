#!/usr/bin/env python3
"""Regenerate systemapps.json by scanning system/*.vx VX headers.
These are the built-in Luci OS system/utility apps. Published so a user
can re-download (repair/update) one if it errors in the system — the
fresh copy lands in ~/.config/luci/apps and OVERRIDES the built-in."""
import os, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
SYSDIR = os.path.join(HERE, "system")
BASE = "https://raw.githubusercontent.com/vincentilagan/LStore/main/system"

# Friendly categories so the section can group utilities sensibly.
CATS = {
    "wifi": "Network", "bluetooth": "Network",
    "volume": "Hardware", "brightness": "Hardware", "audio": "Hardware",
    "camera": "Hardware",
    "appearance": "Settings", "settings": "Settings",
    "vinx_settings": "Settings", "vinx_model": "Settings",
    "terminal": "Tools", "manual": "Tools", "check": "Tools",
    "notification": "System", "lockscreen": "System", "log": "System",
    "sysinfo": "System", "systemhealth": "System", "crashcheck": "System",
    "cosmic_monitor": "System", "monitor": "System", "capture": "System",
    "trash": "Files", "diskcleaner": "Files", "diskImageViewer": "Files",
    "copying": "Files", "htmlview": "Files", "tuba": "Files",
    "launchpad": "Core", "LStore": "Core", "app": "Core",
    "sysApps": "Core", "appControl": "Core", "appProxy": "Core",
    "blackhole": "System",
}

apps = []
for fn in sorted(os.listdir(SYSDIR)):
    if not fn.endswith(".vx"):
        continue
    path = os.path.join(SYSDIR, fn)
    meta = {"name": os.path.splitext(fn)[0], "icon": "🧩",
            "version": "1.0", "author": "Vincent Ilagan"}
    signed = False
    with open(path, encoding="utf-8-sig", errors="ignore") as f:
        for line in f:
            s = line.strip()
            if s.startswith("# VX:sig="):
                signed = True
            if not s.startswith("# VX:"):
                # header block ends at first non-header line
                if s and not s.startswith("#"):
                    break
                continue
            kv = s[5:].split("=", 1)
            if len(kv) == 2:
                meta[kv[0].strip()] = kv[1].strip()
    _id = os.path.splitext(fn)[0]
    apps.append({
        "id": _id,
        "name": meta.get("name") or _id,
        "file": fn,
        "version": meta.get("version", "1.0"),
        "icon": meta.get("icon", "🧩"),
        "author": meta.get("author", "Vincent Ilagan"),
        "category": CATS.get(_id, "System"),
        "signed": signed,
        "system": True,
    })

cat = {
    "store": "LStore",
    "section": "System",
    "note": ("Built-in Luci OS system + utility apps. If one errors, "
             "re-download it here — the repaired copy lands in "
             "~/.config/luci/apps and OVERRIDES the broken built-in "
             "(no root needed; the immutable /usr/local/luci copy is "
             "never touched). Authored by Vincent Ilagan."),
    "base": BASE,
    "apps": apps,
}
with open(os.path.join(HERE, "systemapps.json"), "w", encoding="utf-8") as f:
    json.dump(cat, f, ensure_ascii=False, indent=2)
print("wrote systemapps.json with %d system app(s)" % len(apps))
for a in apps:
    print("  %-18s %-22s v%-5s %s %s" % (
        a["file"], a["name"], a["version"], a["icon"],
        "signed" if a["signed"] else "UNSIGNED"))
