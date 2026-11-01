#!/usr/bin/env python3
"""Flatten a Bambu Studio system preset (resolve its 'inherits' chain) into one JSON file.

Bambu Studio's CLI ignores filament presets whose parents it cannot resolve and falls
back to PLA, so we flatten them first and mark them compatible with the target printer.

Usage: bambu_presets.py <filament|process> "<preset name>" <out.json> <printer> [key=value ...]
"""
import glob, json, os, sys

BBL = os.path.expanduser(os.environ.get("BAMBU_SYSTEM_DIR", "~/.config/BambuStudio/system/BBL"))

def main():
    kind, name, out, printer, *extra = sys.argv[1:]
    idx = {}
    for f in glob.glob(f"{BBL}/{kind}/*.json"):
        try:
            d = json.load(open(f))
            idx[d.get("name")] = d
        except Exception:
            pass
    if name not in idx:
        sys.exit(f"preset not found: {kind}/{name} (looked in {BBL})")

    def resolve(n):
        d = dict(idx[n])
        parent = d.get("inherits")
        if parent:
            r = resolve(parent)
            r.update(d)
            d = r
        return d

    d = resolve(name)
    d.pop("inherits", None)
    d["from"] = "system"
    d["name"] = name
    cp = d.get("compatible_printers", [])
    if printer not in cp:
        d["compatible_printers"] = cp + [printer]
    for kv in extra:
        k, v = kv.split("=", 1)
        d[k] = v
    json.dump(d, open(out, "w"), indent=1)

if __name__ == "__main__":
    main()
