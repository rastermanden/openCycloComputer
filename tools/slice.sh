#!/usr/bin/env bash
# Slice STL files for the Bambu Lab P1S with Bambu Studio's CLI (headless).
#
#   tools/slice.sh enclosure/stl/tolerance_coupon.stl [more.stl ...]
#
# Output: build/slice/<name>_P1S_<filament>.gcode.3mf (one file per STL) plus a summary.
# Override with env vars:
#   FILAMENT="Bambu PETG HF @BBL X1C"   PROCESS="0.20mm Standard @BBL X1C"
#   PLATE="Textured PEI Plate"          PRINTER="Bambu Lab P1S 0.4 nozzle"
#   OUT=build/slice
set -euo pipefail

FILAMENT="${FILAMENT:-Bambu PETG HF @BBL X1C}"
PROCESS="${PROCESS:-0.20mm Standard @BBL X1C}"
PLATE="${PLATE:-Textured PEI Plate}"
PRINTER="${PRINTER:-Bambu Lab P1S 0.4 nozzle}"
BBL="${BAMBU_SYSTEM_DIR:-$HOME/.config/BambuStudio/system/BBL}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${OUT:-$ROOT/build/slice}"
BAMBU="${BAMBU:-bambu-studio}"

[ $# -ge 1 ] || { sed -n '2,12p' "$0"; exit 1; }
command -v "$BAMBU" >/dev/null || { echo "bambu-studio not found"; exit 1; }
[ -f "$BBL/machine/$PRINTER.json" ] || { echo "printer preset missing: $BBL/machine/$PRINTER.json (open Bambu Studio once to download presets)"; exit 1; }

mkdir -p "$OUT"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
python3 "$ROOT/tools/bambu_presets.py" filament "$FILAMENT" "$TMP/filament.json" "$PRINTER"
python3 "$ROOT/tools/bambu_presets.py" process "$PROCESS" "$TMP/process.json" "$PRINTER" "curr_bed_type=$PLATE"
ftag="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["filament_type"][0])' "$TMP/filament.json")"

status=0
for stl in "$@"; do
  name="$(basename "${stl%.*}")"
  work="$TMP/$name"; mkdir -p "$work"
  out="${name}_P1S_${ftag}.gcode.3mf"
  "$BAMBU" --debug 1 --slice 0 --arrange 1 \
    --load-settings "$BBL/machine/$PRINTER.json;$TMP/process.json" \
    --load-filaments "$TMP/filament.json" \
    --export-3mf "$out" --outputdir "$work" "$(realpath "$stl")" >"$work/log.txt" 2>&1 || true
  if [ -f "$work/$out" ]; then
    cp "$work/$out" "$OUT/"
    python3 - "$work/result.json" "$name" "$OUT/$out" <<'PY'
import json,sys
r=json.load(open(sys.argv[1]));p=r["sliced_plates"][0]
g=sum(f["total_used_g"] for f in p["filaments"]);m=p["total_predication"]/60
print(f"OK   {sys.argv[2]:28s} {m:6.1f} min {g:6.1f} g  -> {sys.argv[3]}")
PY
  else
    echo "FAIL $name"; grep -E "\[error\]" "$work/log.txt" | grep -vi "osmesa\|glfw" | tail -3 || true
    status=1
  fi
done
exit $status
