# SPDX-License-Identifier: MIT
"""Parametric enclosure for openCycloComputer (FreeCAD 1.0).

Builds a first-draft bike-computer case for:
  * Adafruit Feather nRF52840 Sense
  * Adafruit Sharp Memory LCD 2.7" 400x240 breakout
  * SparkFun u-blox MAX-M10S (SMA) plus a 25 mm patch antenna
  * 2000 mAh LiPo (62 x 38.5 x 8.5 mm) and room for a MAX17048
  * Garmin quarter-turn male mount (community starting dimensions)

Units are millimetres. Edit PARAM_ROWS below, or create
enclosure/freecad/overrides.csv (``key,value``), then run:

    freecadcmd enclosure/freecad/build_enclosure.py

After editing the Parameters spreadsheet inside the FCStd file, rebuild
from those cells with:

    freecadcmd enclosure/freecad/build_enclosure.py --from-sheet

The spreadsheet is a mirror of the values used for the last build. The
Python table (plus overrides.csv) is the source of truth unless
--from-sheet is passed.

Garmin does not publish the quarter-turn interface. The tab numbers are
community order-of-magnitude starting values (two opposing ears, about
20-24 mm tip to tip, about 1.0-1.5 mm thick). Print the tolerance coupon
and measure a real cradle before trusting the fit. See enclosure/README.md.
"""

from __future__ import annotations

import csv
import math
import os
import sys

import FreeCAD as App
import Part

try:
    import MeshPart
except ImportError:  # pragma: no cover - freecadcmd should ship MeshPart
    MeshPart = None


# (key, default, unit, Danish description shown in the spreadsheet)
PARAM_ROWS = [
    # --- Garmin quarter-turn male (tune on a real mount) ---
    ("garmin_tab_count", 2, "n", "Antal tapper. 2 giver en rigtig 90-graders lås. 4 er jævnt fordelt og låser ved et halvt skridt."),
    ("garmin_tab_outer_d", 22.5, "mm", "Tip-til-tip over tapperne. Fællesskabsinterval ca. 20-24 mm. Ikke et officielt Garmin-mål."),
    ("garmin_neck_d", 16.0, "mm", "Navdiameter under tapperne."),
    ("garmin_tab_angle", 50.0, "deg", "Vinkelbredde af hver tap."),
    ("garmin_tab_t", 1.4, "mm", "Aksial tykkelse. Fællesskabsinterval ca. 1,0-1,5 mm."),
    ("garmin_undercut_h", 2.0, "mm", "Luft under tappen. Holderens læbe skal kunne gå ind her."),
    ("garmin_flange_d", 36.0, "mm", "Flange mod låget."),
    ("garmin_flange_t", 2.8, "mm", "Flangetykkelse."),
    ("garmin_clearance", 0.20, "mm", "Hvor meget den printede han krympes pr. side. Startværdi til P1S i PETG/ASA. Vælg ud fra tolerancekuponen."),
    ("garmin_chamfer", 0.35, "mm", "Lille affasning på tappens yderste top, så den finder ind i sprækken."),
    ("garmin_screw_pitch", 26.0, "mm", "Afstand mellem de to M3-huller i flangen."),
    ("garmin_screw_d", 3.4, "mm", "Frit hul til M3 i flangen."),
    ("female_allowance", 0.30, "mm", "Ekstra luft i den printede målesokkel. En rigtig Garmin-holder er stadig facit."),
    # --- Case envelope ---
    ("inner_w", 80.0, "mm", "Kavitet bredde (X, venstre mod højre)."),
    ("inner_h", 122.0, "mm", "Kavitet højde (Y). Y=0 er USB-siden, stor Y er himmel/GPS."),
    ("inner_d", 22.0, "mm", "Kavitet dybde (Z, fra indersiden af fronten til tætningsfladen)."),
    ("rim", 15.0, "mm", "Massiv kant hele vejen rundt til pakning, skruer og knapper."),
    ("front_wall", 2.4, "mm", "Frontvæg. Passer til 6 perimetre med 0,4 mm dyse."),
    ("corner_r", 8.0, "mm", "Udvendigt hjørneradius."),
    ("inner_corner_r", 4.0, "mm", "Hjørneradius i kaviteten."),
    ("lip_w", 2.0, "mm", "Bredde af styrekraven der holder låget på plads."),
    ("lip_h", 1.3, "mm", "Højde af styrekraven over tætningsfladen."),
    ("lid_t", 4.0, "mm", "Lågtykkelse."),
    ("lid_clearance", 0.30, "mm", "Luft mellem låg og styrekrave, pr. side."),
    # --- 2 mm silicone cord ---
    ("gasket_cord_d", 2.0, "mm", "Silikonesnorens diameter."),
    ("gasket_groove_w", 2.60, "mm", "Sporets bredde."),
    ("gasket_groove_d", 1.50, "mm", "Sporets dybde. Snoren stikker ca. 0,5 mm op og klemmes når låget skrues på."),
    ("gasket_inset", 5.0, "mm", "Afstand fra den ydre lige kant ind til sporets centerlinje."),
    ("gasket_corner_r", 20.0, "mm", "Centerlinjens hjørneradius. Stor radius fører sporet inden om hjørneskruerne."),
    # --- M3 heat-set inserts ---
    ("screw_inset", 6.2, "mm", "Skruecenter målt fra det ydre hjørne i både X og Y."),
    ("insert_hole_d", 4.0, "mm", "Hul til M3-varmeindsats. Tun med indsatstesten (3,8-4,4 mm)."),
    ("insert_depth", 5.5, "mm", "Huldybde fra tætningsfladen. Hullet er blindt."),
    ("screw_clear_d", 3.4, "mm", "Frit hul i låget til M3."),
    ("cbore_d", 6.6, "mm", "Forsænkning til M3-unbrakohoved."),
    ("cbore_dpth", 2.4, "mm", "Forsænkningsdybde i lågets yderside."),
    ("nut_af", 5.8, "mm", "Møtrikslomme til M3, mål over flader (møtrik 5,5 mm plus lidt luft)."),
    ("nut_depth", 2.6, "mm", "Dybde af møtrikslommen på lågets inderside."),
    # --- Sharp window ---
    ("active_w", 58.8, "mm", "LS027B7DH01 aktivt område, bredde."),
    ("active_h", 35.3, "mm", "LS027B7DH01 aktivt område, højde."),
    ("active_off_x", 0.0, "mm", "Vinduets center i forhold til display-printets center, X."),
    ("active_off_y", 0.0, "mm", "Vinduets center i Y. 0 antager at det aktive område sidder midt på printet. Ret det når modulet er målt."),
    ("aperture_shrink_x", 3.2, "mm", "Åbningen er smallere end det aktive område med dette. Nok til at styretappene i hjørnerne ikke skærer vinduet."),
    ("aperture_shrink_y", 1.2, "mm", "Åbningen er lavere end det aktive område med dette."),
    ("sheet_extra", 4.0, "mm", "Polycarbonatpladen er åbningen plus dette i både bredde og højde."),
    ("sheet_t", 1.0, "mm", "Polycarbonat, tykkelse."),
    ("sheet_rebate_extra", 0.20, "mm", "Falsen er dybere end pladen, så pladen ligger en anelse under frontfladen."),
    ("sheet_fit", 0.40, "mm", "Falsen er så meget større end pladen, så den kan lægges i og limes."),
    # --- Display PCB (Adafruit Eagle, 2.7 inch Sharp breakout) ---
    ("disp_pcb_w", 63.50, "mm", "Display-printets omrids, bredde."),
    ("disp_pcb_h", 55.88, "mm", "Display-printets omrids, højde. Der er et lille hak i den ene langside; lommen bruger omridset."),
    ("disp_hole_inset_x", 2.54, "mm", "Første monteringshul fra printets venstre kant."),
    ("disp_hole_inset_y", 2.54, "mm", "Første monteringshul fra printets bund."),
    ("disp_hole_pitch_x", 58.42, "mm", "Afstand mellem display-huller i X."),
    ("disp_hole_pitch_y", 50.80, "mm", "Afstand mellem display-huller i Y."),
    ("disp_pin_d", 2.0, "mm", "Styretap. Printets hul er 2,5 mm."),
    ("disp_boss_h", 2.2, "mm", "Højde under printet, så glasset ikke rammer frontens inderside."),
    ("disp_boss_od", 6.0, "mm", "Boss-diameter under displayet."),
    ("pin_raise", 2.4, "mm", "Hvor langt styretappen stikker op over bossen."),
    # --- Feather nRF52840 Sense (50.80 x 22.86 mm, long axis along X) ---
    ("feather_w", 50.80, "mm", "Feather-længde. Micro-USB sidder på den korte ende og peger til venstre; USB-C-breakoutet trækkes med ledning til bunden."),
    ("feather_h", 22.86, "mm", "Feather-bredde."),
    ("feather_hole_x0", 2.54, "mm", "Hul fra printets USB-ende."),
    ("feather_hole_x1", 48.26, "mm", "Hul fra printets USB-ende, modsat ende."),
    ("feather_hole_y0", 2.54, "mm", "Hul fra printets langkant."),
    ("feather_hole_y1", 20.32, "mm", "Hul fra printets langkant, modsat kant."),
    ("feather_pin_d", 2.0, "mm", "Styretap. Hullerne i Eagle er boret 2,54 mm."),
    ("feather_boss_h", 3.0, "mm", "Frihøjde under Feather for lodninger på bagsiden."),
    ("feather_boss_od", 5.5, "mm", "Boss-diameter under Feather."),
    # --- SparkFun MAX-M10S, inches converted: 1.50 x 1.20 in, SMA +0.24 in ---
    ("gps_pcb_w", 38.10, "mm", "GNSS-print uden SMA."),
    ("gps_pcb_h", 30.48, "mm", "GNSS-print, den korte side."),
    ("gps_sma_extra", 6.10, "mm", "SMA-stikket rager ud over printet langs X."),
    ("gps_hole_x0", 2.54, "mm", "GNSS-hul fra printets kant uden SMA."),
    ("gps_hole_x1", 35.56, "mm", "GNSS-hul, modsat kant (stadig på printet, ikke på SMA)."),
    ("gps_hole_y0", 2.54, "mm", "GNSS-hul fra kanten."),
    ("gps_hole_y1", 27.94, "mm", "GNSS-hul, modsat kant."),
    ("gps_pin_d", 2.8, "mm", "Styretap. Stand-off-hullerne er boret 3,30 mm."),
    ("gps_boss_h", 3.0, "mm", "Frihøjde under GNSS-printet."),
    ("gps_boss_od", 6.0, "mm", "Boss-diameter under GNSS-printet."),
    ("patch_w", 25.0, "mm", "Keramisk patch-antenne. Lommen er kun en pladsholder; vælg en rigtig antenne."),
    ("patch_h", 25.0, "mm", "Patch-antenne, den anden side."),
    # --- Battery and fuel gauge ---
    ("bat_w", 62.0, "mm", "LiPo som Elektroshoppen oplyser for LP803860."),
    ("bat_h", 38.5, "mm", "LiPo, den korte side."),
    ("bat_clear", 1.0, "mm", "Luft omkring posen i bakken på låget."),
    ("bat_wall_h", 3.0, "mm", "Højde af bakkekanten. Posen ligger løst; kanten er kun et stop."),
    ("bat_wall_t", 1.4, "mm", "Bakkekantens tykkelse."),
    ("fuel_w", 22.0, "mm", "Plads til Adafruit MAX17048. Mål det rigtige print og ret tallet."),
    ("fuel_h", 16.0, "mm", "Plads til fuel gauge, den korte side."),
    # --- Stacking ---
    ("zone_gap", 2.5, "mm", "Luft mellem Feather, display og GNSS i Y."),
    ("zone_margin", 2.0, "mm", "Luft fra kavitetens kant til nærmeste print."),
    # --- Buttons (side walls, tactile 6x6 behind a printed membrane) ---
    ("btn_dish_d", 11.0, "mm", "Fingerfordybning, diameter."),
    ("btn_dish_depth", 1.0, "mm", "Fingerfordybningens dybde fra ydersiden."),
    ("btn_membrane", 0.40, "mm", "Membran. Præcis to lag når laghøjden er 0,20 mm. Gør den tykkere hvis knappen er for stiv."),
    ("btn_pocket", 7.4, "mm", "Firkantet lomme til en 6x6 mm tactile switch."),
    ("btn_z", 8.0, "mm", "Knappernes center målt fra frontfladen. Hold den væk fra pakningssporet bagi."),
    ("btn_y1", 34.0, "mm", "Nederste knap-par, center Y i kabinettets koordinater."),
    ("btn_y2", 54.0, "mm", "Øverste knap-par, center Y."),
    # --- USB-C plug opening, bottom wall ---
    ("usbc_w", 10.4, "mm", "Udskæring til USB-C-stik, bredde."),
    ("usbc_h", 4.8, "mm", "Udskæring, højde."),
    ("usbc_z", 9.0, "mm", "Udskæringens center fra frontfladen."),
    ("usbc_seat_extra", 6.0, "mm", "Udvendig fals til proppens flange er hullet plus dette i begge led."),
    ("usbc_seat_d", 1.4, "mm", "Dybde af den udvendige fals."),
    ("plug_clearance", 0.25, "mm", "Proppens næse er så meget mindre end hullet, pr. side."),
    ("plug_nose", 6.0, "mm", "Hvor langt proppen stikker ind."),
    ("plug_flange_t", 2.4, "mm", "Proppens flange."),
    # --- Barometer vent ---
    ("vent_d", 2.4, "mm", "Hul gennem væggen, så BMP280 kan mærke lufttrykket."),
    ("vent_membrane_d", 8.0, "mm", "Rund fals til en lille åndbar membran (Gore-type)."),
    ("vent_membrane_depth", 0.7, "mm", "Faldens dybde."),
    ("vent_from_top", 18.0, "mm", "Vent-center under kavitetens øverste kant, i venstre væg."),
    ("vent_z", 10.0, "mm", "Vent-center fra frontfladen."),
]

HERE = os.path.dirname(os.path.abspath(__file__))
ENCL = os.path.dirname(HERE)
STL_DIR = os.path.join(ENCL, "stl")
STEP_DIR = os.path.join(ENCL, "step")
FCSTD_PATH = os.path.join(HERE, "openCycloComputer_enclosure.FCStd")
OVERRIDES = os.path.join(HERE, "overrides.csv")


def params_from_rows():
    values = {}
    for key, value, _unit, _desc in PARAM_ROWS:
        values[key] = float(value)
    return values


def apply_csv_overrides(values):
    if not os.path.isfile(OVERRIDES):
        return []
    applied = []
    with open(OVERRIDES, newline="", encoding="utf-8") as handle:
        for row in csv.reader(line for line in handle if not line.strip().startswith("#")):
            if not row or len(row) < 2 or row[0].strip() == "key":
                continue
            key = row[0].strip()
            if key not in values:
                raise SystemExit(f"overrides.csv: unknown parameter {key}")
            values[key] = float(row[1])
            applied.append(key)
    return applied


def apply_sheet_overrides(values):
    if not os.path.isfile(FCSTD_PATH):
        raise SystemExit(f"--from-sheet was set, but {FCSTD_PATH} does not exist yet")
    doc = App.openDocument(FCSTD_PATH)
    try:
        sheet = doc.getObject("Parameters")
        if sheet is None:
            raise SystemExit("The FCStd file has no Parameters spreadsheet")
        applied = []
        for key, _value, _unit, _desc in PARAM_ROWS:
            values[key] = float(sheet.get(key))
            applied.append(key)
        return applied
    finally:
        App.closeDocument(doc.Name)


def outer_size(p):
    return p["inner_w"] + 2 * p["rim"], p["inner_h"] + 2 * p["rim"]


def body_height(p):
    """Front face to the top of the alignment lip."""
    return p["front_wall"] + p["inner_d"] + p["lip_h"]


def mating_z(p):
    """Z of the gasket face (lip rises above this)."""
    return p["front_wall"] + p["inner_d"]


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------

def fuse_many(shapes):
    shapes = [s for s in shapes if s is not None]
    if not shapes:
        raise ValueError("nothing to fuse")
    if len(shapes) == 1:
        return shapes[0]
    return shapes[0].multiFuse(shapes[1:])


def cut_many(base, tools):
    tools = [t for t in tools if t is not None]
    if not tools:
        return base
    return base.cut(fuse_many(tools))


def _arc(cx, cy, a0_deg, a1_deg, radius):
    circle = Part.Circle(App.Vector(cx, cy, 0), App.Vector(0, 0, 1), radius)
    return Part.ArcOfCircle(circle, math.radians(a0_deg), math.radians(a1_deg)).toShape()


def rounded_rect_solid(x, y, w, h, radius, z0, height):
    """Solid rounded rectangle. (x, y) is the minimum corner. Extruded +Z."""
    radius = min(radius, w / 2.0 - 0.05, h / 2.0 - 0.05)
    if radius < 0.2:
        solid = Part.makeBox(w, h, height, App.Vector(x, y, z0))
        return solid
    edges = [
        Part.makeLine(App.Vector(x + radius, y, 0), App.Vector(x + w - radius, y, 0)),
        _arc(x + w - radius, y + radius, -90, 0, radius),
        Part.makeLine(App.Vector(x + w, y + radius, 0), App.Vector(x + w, y + h - radius, 0)),
        _arc(x + w - radius, y + h - radius, 0, 90, radius),
        Part.makeLine(App.Vector(x + w - radius, y + h, 0), App.Vector(x + radius, y + h, 0)),
        _arc(x + radius, y + h - radius, 90, 180, radius),
        Part.makeLine(App.Vector(x, y + h - radius, 0), App.Vector(x, y + radius, 0)),
        _arc(x + radius, y + radius, 180, 270, radius),
    ]
    wire = Part.Wire(edges)
    if not wire.isClosed():
        raise RuntimeError("rounded rectangle wire did not close")
    solid = Part.Face(wire).extrude(App.Vector(0, 0, height))
    solid.translate(App.Vector(0, 0, z0))
    return solid


def cylinder_z(cx, cy, z0, radius, height):
    return Part.makeCylinder(radius, height, App.Vector(cx, cy, z0))


def cylinder_x(x0, y, z, radius, length):
    return Part.makeCylinder(radius, length, App.Vector(x0, y, z), App.Vector(1, 0, 0))


def stadium_along_y(cx, y0, cz, length_x, height_z, depth_y):
    """Obround slot. length along X, height along Z, extruded +Y from y0."""
    radius = height_z / 2.0
    core = max(length_x - height_z, 0.2)
    box = Part.makeBox(core, depth_y, height_z, App.Vector(cx - core / 2.0, y0, cz - radius))
    c1 = Part.makeCylinder(radius, depth_y, App.Vector(cx - core / 2.0, y0, cz), App.Vector(0, 1, 0))
    c2 = Part.makeCylinder(radius, depth_y, App.Vector(cx + core / 2.0, y0, cz), App.Vector(0, 1, 0))
    return fuse_many([box, c1, c2])


def stadium_along_z(cx, cy, z0, length_x, height_y, depth_z):
    """Obround post/nose. length along X, height along Y, extruded +Z from z0."""
    radius = height_y / 2.0
    core = max(length_x - height_y, 0.2)
    box = Part.makeBox(core, height_y, depth_z, App.Vector(cx - core / 2.0, cy - radius, z0))
    c1 = Part.makeCylinder(radius, depth_z, App.Vector(cx - core / 2.0, cy, z0))
    c2 = Part.makeCylinder(radius, depth_z, App.Vector(cx + core / 2.0, cy, z0))
    return fuse_many([box, c1, c2])


def pie_solid(radius, angle_deg, z0, height, rot_deg):
    """Pie slice centered on rot_deg, extruded +Z."""
    half = math.radians(angle_deg / 2.0)
    p0 = App.Vector(0, 0, 0)
    p1 = App.Vector(radius * math.cos(-half), radius * math.sin(-half), 0)
    p2 = App.Vector(radius * math.cos(half), radius * math.sin(half), 0)
    circle = Part.Circle(App.Vector(0, 0, 0), App.Vector(0, 0, 1), radius)
    arc = Part.ArcOfCircle(circle, -half, half).toShape()
    wire = Part.Wire([Part.makeLine(p0, p1), arc, Part.makeLine(p2, p0)])
    solid = Part.Face(wire).extrude(App.Vector(0, 0, height))
    solid.translate(App.Vector(0, 0, z0))
    if abs(rot_deg) > 1e-6:
        solid.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), rot_deg)
    return solid


def hex_prism(cx, cy, z0, across_flats, height):
    """Regular hexagon. Flat-to-flat is across_flats. A flat is perpendicular to X."""
    radius = across_flats / math.sqrt(3.0)
    pts = []
    for i in range(6):
        ang = math.radians(30 + i * 60)
        pts.append(App.Vector(cx + radius * math.cos(ang), cy + radius * math.sin(ang), z0))
    pts.append(pts[0])
    face = Part.Face(Part.makePolygon(pts))
    return face.extrude(App.Vector(0, 0, height))


def largest_solid(shape):
    solids = list(shape.Solids)
    if not solids:
        return shape, 0
    solids.sort(key=lambda solid: solid.Volume, reverse=True)
    return solids[0], len(solids)


def volume_of_common(a, b):
    common = a.common(b)
    return common.Volume if common is not None else 0.0


# ---------------------------------------------------------------------------
# Layout: where each board sits in case coordinates (origin = front lower left)
# ---------------------------------------------------------------------------

def compute_layout(p):
    rim = p["rim"]
    fx = rim + p["zone_margin"]
    fy = rim + p["zone_margin"]
    dx = rim + (p["inner_w"] - p["disp_pcb_w"]) / 2.0
    dy = fy + p["feather_h"] + p["zone_gap"]
    gx = rim + p["zone_margin"]
    gy = dy + p["disp_pcb_h"] + p["zone_gap"]
    patch_x = gx + p["gps_pcb_w"] + p["gps_sma_extra"] + p["zone_gap"]
    patch_y = gy + (p["gps_pcb_h"] - p["patch_h"]) / 2.0
    fuel_x = fx + p["feather_w"] + p["zone_gap"]
    fuel_y = fy + (p["feather_h"] - p["fuel_h"]) / 2.0
    bat_x = dx + (p["disp_pcb_w"] - p["bat_w"]) / 2.0
    bat_y = dy + (p["disp_pcb_h"] - p["bat_h"]) / 2.0
    disp_cx = dx + p["disp_pcb_w"] / 2.0 + p["active_off_x"]
    disp_cy = dy + p["disp_pcb_h"] / 2.0 + p["active_off_y"]
    return {
        "feather": (fx, fy),
        "display": (dx, dy),
        "gps": (gx, gy),
        "patch": (patch_x, patch_y),
        "fuel": (fuel_x, fuel_y),
        "battery": (bat_x, bat_y),
        "window_c": (disp_cx, disp_cy),
    }


def check_layout(p, lay, errors):
    x1 = p["rim"] + p["inner_w"]
    y1 = p["rim"] + p["inner_h"]
    checks = [
        ("feather", lay["feather"], p["feather_w"], p["feather_h"]),
        ("display", lay["display"], p["disp_pcb_w"], p["disp_pcb_h"]),
        ("gps pcb", lay["gps"], p["gps_pcb_w"], p["gps_pcb_h"]),
        ("gps sma", (lay["gps"][0], lay["gps"][1]), p["gps_pcb_w"] + p["gps_sma_extra"], p["gps_pcb_h"]),
        ("patch", lay["patch"], p["patch_w"], p["patch_h"]),
        ("fuel", lay["fuel"], p["fuel_w"], p["fuel_h"]),
        ("battery", lay["battery"], p["bat_w"], p["bat_h"]),
    ]
    for name, (x, y), w, h in checks:
        if x < p["rim"] - 0.01 or y < p["rim"] - 0.01 or x + w > x1 + 0.01 or y + h > y1 + 0.01:
            errors.append(f"layout: {name} at ({x:.1f},{y:.1f}) size {w:.1f}x{h:.1f} does not fit the cavity")
    if lay["patch"][0] < lay["gps"][0] + p["gps_pcb_w"] + p["gps_sma_extra"] - 0.01:
        errors.append("layout: patch antenna overlaps the SMA connector")


# ---------------------------------------------------------------------------
# Garmin mount
# ---------------------------------------------------------------------------

def garmin_angles(p):
    count = int(round(p["garmin_tab_count"]))
    if count < 2:
        count = 2
    return [i * (360.0 / count) for i in range(count)]


def garmin_male(p, clearance):
    """Male quarter-turn. Flange bottom on z=0, tabs point +Z.

    ``clearance`` shrinks the tabs (positive = looser in a real cradle,
    because a printed male comes out fat).
    """
    outer_r = p["garmin_tab_outer_d"] / 2.0 - clearance
    neck_r = max(p["garmin_neck_d"] / 2.0 - clearance, 3.0)
    tab_t = max(p["garmin_tab_t"] - clearance, 0.6)
    under = p["garmin_undercut_h"] + max(clearance, 0.0) * 0.5
    ang = p["garmin_tab_angle"] - math.degrees(2.0 * clearance / max(outer_r, 1.0))
    ang = max(min(ang, 80.0), 20.0)
    flange_h = p["garmin_flange_t"]
    z_tab = flange_h + under

    flange = cylinder_z(0, 0, 0, p["garmin_flange_d"] / 2.0, flange_h)
    # Neck runs up through the tabs so the ears are supported.
    neck = cylinder_z(0, 0, 0, neck_r, z_tab + tab_t)
    tabs = []
    for rot in garmin_angles(p):
        sector = pie_solid(outer_r, ang, z_tab, tab_t, rot)
        tabs.append(sector)
    shape = fuse_many([flange, neck] + tabs)
    # Drop anything of the pie that landed inside the neck; fuse already merged it.
    if p["garmin_chamfer"] > 0.05:
        chamfer = p["garmin_chamfer"]
        z_top = z_tab + tab_t
        triangle = Part.makePolygon([
            App.Vector(outer_r - chamfer, 0, z_top + 0.02),
            App.Vector(outer_r + 0.6, 0, z_top + 0.02),
            App.Vector(outer_r + 0.6, 0, z_top - chamfer),
            App.Vector(outer_r - chamfer, 0, z_top + 0.02),
        ])
        ring = Part.Face(triangle).revolve(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 360)
        shape = shape.cut(ring)
    # Screw holes through the flange only (outside the neck).
    half = p["garmin_screw_pitch"] / 2.0
    holes = [
        cylinder_z(half, 0, -0.2, p["garmin_screw_d"] / 2.0, flange_h + 0.4),
        cylinder_z(-half, 0, -0.2, p["garmin_screw_d"] / 2.0, flange_h + 0.4),
    ]
    # Witness notch on +Y so the tab axis is obvious on the printed part.
    notch = Part.makeBox(
        1.2, 3.0, flange_h + 0.4,
        App.Vector(-0.6, p["garmin_flange_d"] / 2.0 - 2.2, -0.2),
    )
    shape = cut_many(shape, holes + [notch])
    solid, _n = largest_solid(shape)
    return solid


def garmin_pips(count, z, y, radius=1.1, height=0.9):
    """1..4 raised dots in front of the flange, so the coupon can be told apart."""
    dots = []
    span = (count - 1) * 3.0
    for i in range(int(count)):
        dots.append(cylinder_z(-span / 2.0 + i * 3.0, y, z, radius, height))
    return dots


def tolerance_coupon(p):
    """Four males on one plate. Dot count is 1..4 as clearance grows."""
    clearances = (-0.05, 0.10, 0.20, 0.35)
    pitch = p["garmin_flange_d"] + 6.0
    margin = 6.0
    plate_w = margin * 2 + pitch * (len(clearances) - 1) + p["garmin_flange_d"]
    plate_h = p["garmin_flange_d"] + 16.0
    plate_t = 2.2
    plate = Part.makeBox(plate_w, plate_h, plate_t)
    mounts = [plate]
    for index, clearance in enumerate(clearances):
        cx = margin + p["garmin_flange_d"] / 2.0 + index * pitch
        cy = 8.0 + p["garmin_flange_d"] / 2.0
        male = garmin_male(p, clearance)
        male.translate(App.Vector(cx, cy, plate_t))
        mounts.append(male)
        # Dots sit on the plate, just in front of the flange (negative local Y).
        pip_y = -(p["garmin_flange_d"] / 2.0) - 3.2
        for dot in garmin_pips(index + 1, plate_t, pip_y):
            dot.translate(App.Vector(cx, cy, 0))
            mounts.append(dot)
    solid, _n = largest_solid(fuse_many(mounts))
    return solid, clearances


def garmin_gauge(p):
    """Printed female gauge.

    Slots line up with the tabs for insertion. With 2 tabs, a 90 degree
    turn carries them under the lip. This is a fit gauge, not a copy of
    a Garmin cradle (no spring, no detent).
    """
    allow = p["female_allowance"]
    outer_r = p["garmin_tab_outer_d"] / 2.0 + allow
    neck_r = p["garmin_neck_d"] / 2.0 + allow
    tab_t = p["garmin_tab_t"] + allow
    under = p["garmin_undercut_h"] + allow
    ang = p["garmin_tab_angle"] + 8.0
    floor = 2.6
    lip_t = tab_t
    total_h = floor + under + lip_t
    disk_r = outer_r + 6.0
    disk = cylinder_z(0, 0, 0, disk_r, total_h)
    # Open volume the tabs can sweep in.
    sweep = cylinder_z(0, 0, floor - 0.01, outer_r, under + lip_t + 0.5)
    neck = cylinder_z(0, 0, floor - 0.01, neck_r, under + lip_t + 0.5)
    shape = cut_many(disk, [sweep, neck])
    # Put the lip back, then cut the entry slots through it.
    lip = cylinder_z(0, 0, floor + under, disk_r, lip_t + 0.02)
    lip_hole = cylinder_z(0, 0, floor + under - 0.05, neck_r, lip_t + 0.2)
    lip = lip.cut(lip_hole)
    slots = []
    slot_h = lip_t + under + 0.4
    for rot in garmin_angles(p):
        slots.append(pie_solid(outer_r + 0.4, ang, floor + under - 0.05, slot_h, rot))
    lip = cut_many(lip, slots)
    shape = fuse_many([shape, lip])
    # Trim the lip fuse back to the disk radius (lip used disk_r already).
    solid, _n = largest_solid(shape)
    return solid


# ---------------------------------------------------------------------------
# Case
# ---------------------------------------------------------------------------

def gasket_tool(p):
    ow, oh = outer_size(p)
    inset = p["gasket_inset"]
    width = p["gasket_groove_w"]
    radius = p["gasket_corner_r"]
    z0 = mating_z(p) - p["gasket_groove_d"]
    depth = p["gasket_groove_d"] + 0.05
    outer = rounded_rect_solid(
        inset - width / 2.0,
        inset - width / 2.0,
        ow - 2 * (inset - width / 2.0),
        oh - 2 * (inset - width / 2.0),
        radius + width / 2.0,
        z0,
        depth,
    )
    inner = rounded_rect_solid(
        inset + width / 2.0,
        inset + width / 2.0,
        ow - 2 * (inset + width / 2.0),
        oh - 2 * (inset + width / 2.0),
        max(radius - width / 2.0, 0.5),
        z0 - 0.02,
        depth + 0.04,
    )
    return outer.cut(inner)


def screw_points(p):
    ow, oh = outer_size(p)
    m = p["screw_inset"]
    return [(m, m), (ow - m, m), (m, oh - m), (ow - m, oh - m)]


def board_posts(origin, holes, pin_d, boss_od, boss_h, pin_raise, z_floor):
    """Locating pins. A wide boss is omitted when boss_od is 0 (display side)."""
    ox, oy = origin
    posts = []
    for hx, hy in holes:
        cx, cy = ox + hx, oy + hy
        if boss_od > pin_d + 0.2 and boss_h > 0.2:
            posts.append(cylinder_z(cx, cy, z_floor, boss_od / 2.0, boss_h))
            posts.append(cylinder_z(cx, cy, z_floor + boss_h, pin_d / 2.0, pin_raise))
        else:
            posts.append(cylinder_z(cx, cy, z_floor, pin_d / 2.0, max(boss_h, 0.0) + pin_raise))
    return posts


def case_body(p, lay):
    ow, oh = outer_size(p)
    total_h = body_height(p)
    shell = rounded_rect_solid(0, 0, ow, oh, p["corner_r"], 0, total_h)
    cavity = rounded_rect_solid(
        p["rim"], p["rim"], p["inner_w"], p["inner_h"], p["inner_corner_r"],
        p["front_wall"], p["inner_d"] + p["lip_h"] + 1.0,
    )
    # Leave only the outer lip standing above the mating face.
    lip_cut = rounded_rect_solid(
        p["lip_w"], p["lip_w"], ow - 2 * p["lip_w"], oh - 2 * p["lip_w"],
        max(p["corner_r"] - p["lip_w"], 0.4),
        mating_z(p), p["lip_h"] + 1.0,
    )
    groove = gasket_tool(p)
    tools = [cavity, lip_cut, groove]

    # Window rebate (outside) and aperture (through).
    ap_w = p["active_w"] - p["aperture_shrink_x"]
    ap_h = p["active_h"] - p["aperture_shrink_y"]
    sheet_w = ap_w + p["sheet_extra"]
    sheet_h = ap_h + p["sheet_extra"]
    cx, cy = lay["window_c"]
    rebate_d = p["sheet_t"] + p["sheet_rebate_extra"]
    tools.append(rounded_rect_solid(
        cx - (sheet_w + p["sheet_fit"]) / 2.0,
        cy - (sheet_h + p["sheet_fit"]) / 2.0,
        sheet_w + p["sheet_fit"],
        sheet_h + p["sheet_fit"],
        2.0,
        -0.05,
        rebate_d + 0.05,
    ))
    tools.append(rounded_rect_solid(
        cx - ap_w / 2.0, cy - ap_h / 2.0, ap_w, ap_h, 1.5,
        -0.1, p["front_wall"] + 0.4,
    ))

    # Side buttons. The dish comes in from the outside, the switch pocket
    # comes in from the cavity, and `btn_membrane` of plastic is left between them.
    membrane_x = p["btn_dish_depth"] + p["btn_membrane"]
    pocket = p["btn_pocket"]
    for side in ("L", "R"):
        for by in (p["btn_y1"], p["btn_y2"]):
            if side == "L":
                tools.append(cylinder_x(-0.2, by, p["btn_z"], p["btn_dish_d"] / 2.0, p["btn_dish_depth"] + 0.2))
                tools.append(Part.makeBox(
                    p["rim"] + 0.4 - membrane_x,
                    pocket,
                    pocket,
                    App.Vector(membrane_x, by - pocket / 2.0, p["btn_z"] - pocket / 2.0),
                ))
            else:
                outer_start = ow - p["btn_dish_depth"]
                tools.append(cylinder_x(outer_start, by, p["btn_z"], p["btn_dish_d"] / 2.0, p["btn_dish_depth"] + 0.4))
                pocket_end = ow - membrane_x
                pocket_start = ow - p["rim"] - 0.4
                tools.append(Part.makeBox(
                    pocket_end - pocket_start,
                    pocket,
                    pocket,
                    App.Vector(pocket_start, by - pocket / 2.0, p["btn_z"] - pocket / 2.0),
                ))

    # USB-C slot through the bottom rim, plus a shallow seat for the plug flange.
    tools.append(stadium_along_y(
        ow / 2.0, -0.4, p["usbc_z"], p["usbc_w"], p["usbc_h"], p["rim"] + 0.8,
    ))
    seat_w = p["usbc_w"] + p["usbc_seat_extra"]
    seat_h = p["usbc_h"] + p["usbc_seat_extra"]
    tools.append(stadium_along_y(
        ow / 2.0, -0.2, p["usbc_z"], seat_w, seat_h, p["usbc_seat_d"] + 0.2,
    ))

    # Barometer vent in the left wall.
    vent_y = p["rim"] + p["inner_h"] - p["vent_from_top"]
    tools.append(cylinder_x(-0.2, vent_y, p["vent_z"], p["vent_d"] / 2.0, p["rim"] + 0.6))
    tools.append(cylinder_x(-0.2, vent_y, p["vent_z"], p["vent_membrane_d"] / 2.0, p["vent_membrane_depth"] + 0.2))

    # Blind heat-set holes from the mating face.
    for sx, sy in screw_points(p):
        tools.append(cylinder_z(sx, sy, mating_z(p) - p["insert_depth"], p["insert_hole_d"] / 2.0, p["insert_depth"] + 0.3))

    body = cut_many(shell, tools)

    posts = []
    posts += board_posts(
        lay["display"],
        [
            (p["disp_hole_inset_x"], p["disp_hole_inset_y"]),
            (p["disp_hole_inset_x"] + p["disp_hole_pitch_x"], p["disp_hole_inset_y"]),
            (p["disp_hole_inset_x"], p["disp_hole_inset_y"] + p["disp_hole_pitch_y"]),
            (p["disp_hole_inset_x"] + p["disp_hole_pitch_x"], p["disp_hole_inset_y"] + p["disp_hole_pitch_y"]),
        ],
        p["disp_pin_d"], 0.0, p["disp_boss_h"], p["pin_raise"], p["front_wall"],
    )
    posts += board_posts(
        lay["feather"],
        [
            (p["feather_hole_x0"], p["feather_hole_y0"]),
            (p["feather_hole_x1"], p["feather_hole_y0"]),
            (p["feather_hole_x0"], p["feather_hole_y1"]),
            (p["feather_hole_x1"], p["feather_hole_y1"]),
        ],
        p["feather_pin_d"], p["feather_boss_od"], p["feather_boss_h"], p["pin_raise"], p["front_wall"],
    )
    posts += board_posts(
        lay["gps"],
        [
            (p["gps_hole_x0"], p["gps_hole_y0"]),
            (p["gps_hole_x1"], p["gps_hole_y0"]),
            (p["gps_hole_x0"], p["gps_hole_y1"]),
            (p["gps_hole_x1"], p["gps_hole_y1"]),
        ],
        p["gps_pin_d"], p["gps_boss_od"], p["gps_boss_h"], p["pin_raise"], p["front_wall"],
    )
    # Patch-antenna fence: a low open frame so the ceramic has a home against the front wall.
    px, py = lay["patch"]
    fence_h = 2.0
    fence_t = 1.2
    posts.append(Part.makeBox(p["patch_w"] + 2 * fence_t, fence_t, fence_h, App.Vector(px - fence_t, py - fence_t, p["front_wall"])))
    posts.append(Part.makeBox(p["patch_w"] + 2 * fence_t, fence_t, fence_h, App.Vector(px - fence_t, py + p["patch_h"], p["front_wall"])))
    posts.append(Part.makeBox(fence_t, p["patch_h"], fence_h, App.Vector(px - fence_t, py, p["front_wall"])))
    posts.append(Part.makeBox(fence_t, p["patch_h"], fence_h, App.Vector(px + p["patch_w"], py, p["front_wall"])))
    # Fuel-gauge corner ticks (low L-marks, not a full frame).
    fux, fuy = lay["fuel"]
    tick = 4.0
    th = 1.6
    tt = 1.0
    posts.append(Part.makeBox(tick, tt, th, App.Vector(fux, fuy, p["front_wall"])))
    posts.append(Part.makeBox(tt, tick, th, App.Vector(fux, fuy, p["front_wall"])))
    posts.append(Part.makeBox(tick, tt, th, App.Vector(fux + p["fuel_w"] - tick, fuy + p["fuel_h"] - tt, p["front_wall"])))
    posts.append(Part.makeBox(tt, tick, th, App.Vector(fux + p["fuel_w"] - tt, fuy + p["fuel_h"] - tick, p["front_wall"])))

    body = fuse_many([body] + posts)
    solid, nsolids = largest_solid(body)
    return solid, nsolids, (sheet_w, sheet_h, ap_w, ap_h, vent_y)


def case_lid(p, lay):
    """Lid in print coordinates: z=0 is the outer face (bed), +Z points into the case."""
    ow, oh = outer_size(p)
    gap = p["lid_clearance"]
    x0 = p["lip_w"] + gap
    y0 = p["lip_w"] + gap
    lw = ow - 2 * x0
    lh = oh - 2 * y0
    lid = rounded_rect_solid(x0, y0, lw, lh, max(p["corner_r"] - p["lip_w"], 1.0), 0, p["lid_t"])
    tools = []
    for sx, sy in screw_points(p):
        tools.append(cylinder_z(sx, sy, -0.1, p["screw_clear_d"] / 2.0, p["lid_t"] + 0.2))
        tools.append(cylinder_z(sx, sy, -0.05, p["cbore_d"] / 2.0, p["cbore_dpth"] + 0.05))
    # Mount screws + nut traps. Nuts open on the inner face (+Z).
    mcx, mcy = lay["window_c"]
    half = p["garmin_screw_pitch"] / 2.0
    for mx in (mcx - half, mcx + half):
        tools.append(cylinder_z(mx, mcy, -0.1, p["screw_clear_d"] / 2.0, p["lid_t"] + 0.2))
        tools.append(hex_prism(mx, mcy, p["lid_t"] - p["nut_depth"], p["nut_af"], p["nut_depth"] + 0.05))
        tools.append(cylinder_z(mx, mcy, -0.05, p["cbore_d"] / 2.0, min(1.6, p["cbore_dpth"])))
    lid = cut_many(lid, tools)

    # Battery tray walls standing up from the inner face.
    bx, by = lay["battery"]
    wall_h = p["bat_wall_h"]
    wt = p["bat_wall_t"]
    clear = p["bat_clear"]
    tx = bx - clear - wt
    ty = by - clear - wt
    tw = p["bat_w"] + 2 * clear + 2 * wt
    th = p["bat_h"] + 2 * clear + 2 * wt
    outer = Part.makeBox(tw, th, wall_h, App.Vector(tx, ty, p["lid_t"]))
    inner = Part.makeBox(
        tw - 2 * wt, th - 2 * wt, wall_h + 0.2,
        App.Vector(tx + wt, ty + wt, p["lid_t"] - 0.1),
    )
    # Leave the tray open on +X so the pouch wire can leave.
    gate = Part.makeBox(wt + 0.2, 8.0, wall_h + 0.2, App.Vector(tx + tw - wt - 0.1, ty + th / 2.0 - 4.0, p["lid_t"] - 0.1))
    tray = outer.cut(fuse_many([inner, gate]))
    lid = fuse_many([lid, tray])
    solid, nsolids = largest_solid(lid)
    return solid, nsolids


def lid_to_assembly(lid, p):
    """Flip the print-oriented lid onto the back of the case."""
    mat = App.Matrix()
    mat.A11 = 1
    mat.A22 = 1
    mat.A33 = -1
    mat.A34 = mating_z(p) + p["lid_t"]
    placed = lid.copy()
    placed.transformShape(mat)
    return placed


def usb_plug(p):
    ow, _oh = outer_size(p)
    nose_w = p["usbc_w"] - 2 * p["plug_clearance"]
    nose_h = p["usbc_h"] - 2 * p["plug_clearance"]
    flange_w = p["usbc_w"] + p["usbc_seat_extra"] - 0.6
    flange_h = p["usbc_h"] + p["usbc_seat_extra"] - 0.6
    # z=0 is the outer face of the flange. Nose points +Z (into the case when assembled,
    # and up off the bed when printed).
    flange = stadium_along_z(0, 0, 0, flange_w, flange_h, p["plug_flange_t"])
    nose = stadium_along_z(0, 0, p["plug_flange_t"], nose_w, nose_h, p["plug_nose"])
    # Shallow cord groove around the nose, 2 mm back from the tip.
    groove_z = p["plug_flange_t"] + p["plug_nose"] * 0.55
    ring_outer = stadium_along_z(0, 0, groove_z, nose_w + 0.4, nose_h + 0.4, 1.3)
    ring_inner = stadium_along_z(0, 0, groove_z - 0.05, nose_w - 1.3, nose_h - 1.3, 1.4)
    groove = ring_outer.cut(ring_inner)
    grip = Part.makeBox(flange_w * 0.45, 1.4, 1.2, App.Vector(-flange_w * 0.225, -0.7, -1.2))
    shape = fuse_many([flange, nose, grip]).cut(groove)
    solid, _n = largest_solid(shape)
    return solid


def baro_hood(p):
    """Small glue-on drip hood for the side vent. Prints without supports."""
    width = p["vent_membrane_d"] + 4.0
    depth = 5.0
    height = 8.0
    wall = 1.4
    block = Part.makeBox(depth, width, height)
    cave = Part.makeBox(depth + 0.2, width - 2 * wall, height - wall, App.Vector(-0.1, wall, -0.1))
    hole = cylinder_x(-0.2, width / 2.0, height / 2.0, p["vent_d"] / 2.0 + 0.4, wall + 0.4)
    # Sit the hood so its back face (x=0) glues over the membrane recess.
    shape = block.cut(fuse_many([cave, hole]))
    solid, _n = largest_solid(shape)
    return solid


def window_blank(p, sheet_w, sheet_h):
    return rounded_rect_solid(0, 0, sheet_w, sheet_h, 2.0, 0, p["sheet_t"])


def fit_frame(p, lay):
    """Cavity-sized plate with fences. Drop the real boards in before printing the case."""
    base_t = 1.2
    wall_h = 5.0
    wt = 1.4
    plate = Part.makeBox(p["inner_w"], p["inner_h"], base_t)
    # Chamfer one corner so orientation is obvious (USB / bottom is Y=0).
    plate = plate.cut(Part.makeBox(8, 8, base_t + 1, App.Vector(-1, -1, -0.2)))
    fences = []

    def rect_fence(x, y, w, h):
        fences.append(Part.makeBox(w + 2 * wt, wt, wall_h, App.Vector(x - wt, y - wt, base_t)))
        fences.append(Part.makeBox(w + 2 * wt, wt, wall_h, App.Vector(x - wt, y + h, base_t)))
        fences.append(Part.makeBox(wt, h, wall_h, App.Vector(x - wt, y, base_t)))
        fences.append(Part.makeBox(wt, h, wall_h, App.Vector(x + w, y, base_t)))

    ox = p["rim"]
    oy = p["rim"]
    fx, fy = lay["feather"]
    rect_fence(fx - ox, fy - oy, p["feather_w"], p["feather_h"])
    dx, dy = lay["display"]
    rect_fence(dx - ox, dy - oy, p["disp_pcb_w"], p["disp_pcb_h"])
    gx, gy = lay["gps"]
    rect_fence(gx - ox, gy - oy, p["gps_pcb_w"] + p["gps_sma_extra"], p["gps_pcb_h"])
    px, py = lay["patch"]
    rect_fence(px - ox, py - oy, p["patch_w"], p["patch_h"])
    ux, uy = lay["fuel"]
    rect_fence(ux - ox, uy - oy, p["fuel_w"], p["fuel_h"])
    bx, by = lay["battery"]
    rect_fence(bx - ox, by - oy, p["bat_w"], p["bat_h"])
    shape = fuse_many([plate] + fences)
    solid, _n = largest_solid(shape)
    return solid


def gasket_coupon(p):
    """Small two-part coupon that uses the same groove section as the case."""
    width = 56.0
    height = 36.0
    body_t = 8.0
    lid_t = 4.0
    # Groove runs as a rounded rectangle inset from the coupon edge.
    inset = 7.0
    radius = 6.0
    gw = p["gasket_groove_w"]
    gd = p["gasket_groove_d"]
    body = Part.makeBox(width, height, body_t)
    outer = rounded_rect_solid(
        inset - gw / 2.0, inset - gw / 2.0,
        width - 2 * (inset - gw / 2.0), height - 2 * (inset - gw / 2.0),
        radius + gw / 2.0, body_t - gd, gd + 0.05,
    )
    inner = rounded_rect_solid(
        inset + gw / 2.0, inset + gw / 2.0,
        width - 2 * (inset + gw / 2.0), height - 2 * (inset + gw / 2.0),
        max(radius - gw / 2.0, 0.4), body_t - gd - 0.02, gd + 0.1,
    )
    groove = outer.cut(inner)
    screw_x, screw_y = width / 2.0, height / 2.0
    hole = cylinder_z(screw_x, screw_y, body_t - p["insert_depth"], p["insert_hole_d"] / 2.0, p["insert_depth"] + 0.2)
    body = cut_many(body, [groove, hole])
    lid = Part.makeBox(width - 1.0, height - 1.0, lid_t, App.Vector(0.5, 0.5, 0))
    lid = cut_many(lid, [
        cylinder_z(screw_x, screw_y, -0.1, p["screw_clear_d"] / 2.0, lid_t + 0.2),
        cylinder_z(screw_x, screw_y, -0.05, p["cbore_d"] / 2.0, p["cbore_dpth"]),
    ])
    body_s, _n = largest_solid(body)
    lid_s, _n = largest_solid(lid)
    return body_s, lid_s


def insert_strip(p):
    """Four M3 pilot holes so the heat-set diameter can be chosen before the case."""
    diameters = (3.8, 4.0, 4.2, 4.4)
    length = 16.0 * len(diameters) + 8.0
    bar = Part.makeBox(length, 14.0, 8.0)
    holes = []
    pips = []
    for i, dia in enumerate(diameters):
        cx = 12.0 + i * 16.0
        holes.append(cylinder_z(cx, 8.5, 8.0 - 6.0, dia / 2.0, 6.2))
        for pip in range(i + 1):
            pips.append(cylinder_z(cx - 3.0 + pip * 2.2, 1.8, 7.15, 0.7, 0.9))
    shape = fuse_many([cut_many(bar, holes)] + pips)
    solid, _n = largest_solid(shape)
    return solid, diameters


# ---------------------------------------------------------------------------
# Checks, document, export
# ---------------------------------------------------------------------------

def expect_one_solid(name, shape, errors):
    if shape is None or shape.isNull():
        errors.append(f"{name}: null shape")
        return None
    solid, count = largest_solid(shape)
    if not solid.isValid():
        errors.append(f"{name}: shape is not valid")
    if count != 1:
        errors.append(f"{name}: expected 1 solid, found {count}")
    if solid.Volume < 1.0:
        errors.append(f"{name}: volume {solid.Volume:.1f} mm^3 is implausible")
    return solid


def _inside(shape, x, y, z):
    return shape.isInside(App.Vector(x, y, z), 0.05, True)


def feature_checks(p, lay, body, errors):
    """Point samples that catch a cut which closed up or a boss in the window."""
    ow, oh = outer_size(p)
    cx, cy = lay["window_c"]
    ap_w = p["active_w"] - p["aperture_shrink_x"]
    ap_h = p["active_h"] - p["aperture_shrink_y"]
    mz = mating_z(p)
    if _inside(body, cx, cy, p["front_wall"] / 2.0):
        errors.append("window aperture is solid")
    if not _inside(body, cx, cy + ap_h / 2.0 + 1.6, p["front_wall"] / 2.0):
        errors.append("front wall beside the window is missing")
    if _inside(body, cx, cy, p["front_wall"] + 8.0):
        errors.append("cavity is solid at the display center")
    membrane_c = p["btn_dish_depth"] + p["btn_membrane"] / 2.0
    if not _inside(body, membrane_c, p["btn_y1"], p["btn_z"]):
        errors.append("left button membrane is missing")
    if _inside(body, p["btn_dish_depth"] / 2.0, p["btn_y1"], p["btn_z"]):
        errors.append("left button dish was not cut")
    if _inside(body, p["rim"] * 0.55, p["btn_y1"], p["btn_z"]):
        errors.append("left button pocket was not cut")
    if not _inside(body, ow - membrane_c, p["btn_y1"], p["btn_z"]):
        errors.append("right button membrane is missing")
    if _inside(body, ow - p["btn_dish_depth"] / 2.0, p["btn_y1"], p["btn_z"]):
        errors.append("right button dish was not cut")
    if _inside(body, ow - p["rim"] * 0.55, p["btn_y1"], p["btn_z"]):
        errors.append("right button pocket was not cut")
    sx, sy = screw_points(p)[0]
    if _inside(body, sx, sy, mz - p["insert_depth"] / 2.0):
        errors.append("heat-set hole is not open")
    if not _inside(body, sx, sy, mz - p["insert_depth"] - 2.5):
        errors.append("heat-set hole broke through toward the front")
    if _inside(body, ow / 2.0, p["rim"] * 0.5, p["usbc_z"]):
        errors.append("USB-C slot is solid")
    vent_y = p["rim"] + p["inner_h"] - p["vent_from_top"]
    if _inside(body, p["rim"] * 0.5, vent_y, p["vent_z"]):
        errors.append("barometer vent is solid")
    if _inside(body, ow / 2.0, p["gasket_inset"], mz - p["gasket_groove_d"] / 2.0):
        errors.append("gasket groove was not cut")
    if not _inside(body, p["lip_w"] / 2.0, oh / 2.0, mz + p["lip_h"] / 2.0):
        errors.append("alignment lip is missing")
    dx, dy = lay["display"]
    if not _inside(body, dx + p["disp_hole_inset_x"], dy + p["disp_hole_inset_y"], p["front_wall"] + 1.2):
        errors.append("display locating pin is missing")
    if _inside(body, cx - ap_w / 2.0 + 0.6, cy - ap_h / 2.0 + 0.6, p["front_wall"] / 2.0):
        errors.append("a display pin blocks the window aperture")
    # Open at the back, above the mating face, inside the cavity.
    if _inside(body, cx, cy, mz + p["lip_h"] * 0.5):
        errors.append("case is not open at the back")


def run_checks(p, lay, body, groove, errors):
    ow, oh = outer_size(p)
    bb = body.BoundBox
    if abs(bb.XLength - ow) > 0.2 or abs(bb.YLength - oh) > 0.2:
        errors.append(f"case bbox {bb.XLength:.2f} x {bb.YLength:.2f}, expected {ow:.2f} x {oh:.2f}")
    # Insert cylinders must sit fully in the corner mass, clear of the groove.
    guard_r = p["insert_hole_d"] / 2.0 + 1.0
    for sx, sy in screw_points(p):
        guard = cylinder_z(sx, sy, mating_z(p) - p["gasket_groove_d"] - 0.2, guard_r, p["gasket_groove_d"] + 0.4)
        if volume_of_common(guard, groove) > 0.5:
            errors.append(f"screw at ({sx:.1f},{sy:.1f}) intersects the gasket groove")
    # Window center should fall on the display PCB.
    dx, dy = lay["display"]
    cx, cy = lay["window_c"]
    if not (dx - 2 < cx < dx + p["disp_pcb_w"] + 2 and dy - 2 < cy < dy + p["disp_pcb_h"] + 2):
        errors.append("window center is not on the display PCB")
    # Buttons stay on the flat side, clear of the rounded corner and of each other.
    if min(p["btn_y1"], p["btn_y2"]) < p["corner_r"] + p["btn_dish_d"] / 2.0:
        errors.append("a button dish hits the rounded corner")
    if abs(p["btn_y1"] - p["btn_y2"]) < p["btn_dish_d"] + 1.0:
        errors.append("button dishes overlap")
    mz = mating_z(p)
    if p["btn_z"] + p["btn_pocket"] / 2.0 > mz - p["gasket_groove_d"] - 2.0:
        errors.append("button pocket is close to the gasket groove")
    if p["usbc_z"] + p["usbc_h"] / 2.0 > mz - p["gasket_groove_d"] - 2.0:
        errors.append("USB-C cutout is close to the gasket groove")


def write_spreadsheet(doc, p, derived):
    sheet = doc.addObject("Spreadsheet::Sheet", "Parameters")
    sheet.set("A1", "Parameter")
    sheet.set("B1", "Vaerdi")
    sheet.set("C1", "Enhed")
    sheet.set("D1", "Beskrivelse")
    sheet.set("E1", "ret denne celles alias via scriptet; --from-sheet laeser kolonne B")
    row = 2
    for key, _default, unit, desc in PARAM_ROWS:
        sheet.set(f"A{row}", key)
        sheet.set(f"B{row}", f"{p[key]:.6g}")
        sheet.setAlias(f"B{row}", key)
        sheet.set(f"C{row}", unit)
        sheet.set(f"D{row}", desc)
        row += 1
    row += 1
    sheet.set(f"A{row}", "Afledte maal (ikke input)")
    row += 1
    for key, value, unit, desc in derived:
        sheet.set(f"A{row}", key)
        sheet.set(f"B{row}", f"{value:.4g}" if isinstance(value, float) else str(value))
        sheet.set(f"C{row}", unit)
        sheet.set(f"D{row}", desc)
        row += 1
    return sheet


def add_part(doc, name, shape):
    feature = doc.addObject("Part::Feature", name + "_Shape")
    feature.Shape = shape
    body = doc.addObject("PartDesign::Body", name)
    body.BaseFeature = feature
    try:
        feature.Visibility = False
    except Exception:
        pass
    return body


def export_shape(name, shape, errors):
    os.makedirs(STL_DIR, exist_ok=True)
    os.makedirs(STEP_DIR, exist_ok=True)
    step_path = os.path.join(STEP_DIR, name + ".step")
    stl_path = os.path.join(STL_DIR, name + ".stl")
    shape.exportStep(step_path)
    if MeshPart is not None:
        mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.12, AngularDeflection=0.4)
        mesh.write(stl_path)
    else:
        shape.exportStl(stl_path)
    for path in (step_path, stl_path):
        size = os.path.getsize(path)
        if size < 200:
            errors.append(f"{path} is only {size} bytes")
    # Re-read the STEP and compare volume.
    reread = Part.Shape()
    reread.read(step_path)
    if reread.isNull() or not reread.Solids:
        errors.append(f"{name}: STEP re-read produced no solids")
    else:
        got = sum(solid.Volume for solid in reread.Solids)
        if abs(got - shape.Volume) / shape.Volume > 0.02:
            errors.append(f"{name}: STEP volume {got:.1f} differs from model {shape.Volume:.1f}")
    return step_path, stl_path


def place(shape, x, y, z):
    moved = shape.copy()
    moved.translate(App.Vector(x, y, z))
    return moved


def build():
    os.makedirs(STL_DIR, exist_ok=True)
    os.makedirs(STEP_DIR, exist_ok=True)
    values = params_from_rows()
    from_sheet = "--from-sheet" in sys.argv
    if from_sheet:
        used = apply_sheet_overrides(values)
        print(f"Loaded {len(used)} parameters from spreadsheet")
    else:
        used = apply_csv_overrides(values)
        if used:
            print("overrides.csv applied:", ", ".join(used))

    errors = []
    lay = compute_layout(values)
    check_layout(values, lay, errors)

    print("Building Garmin mount...")
    mount = expect_one_solid("garmin_mount", garmin_male(values, values["garmin_clearance"]), errors)
    print("Building tolerance coupon and gauge...")
    coupon, clearances = tolerance_coupon(values)
    coupon = expect_one_solid("tolerance_coupon", coupon, errors)
    gauge = expect_one_solid("garmin_gauge_socket", garmin_gauge(values), errors)
    print("Building case body...")
    body, body_solids, window_info = case_body(values, lay)
    sheet_w, sheet_h, ap_w, ap_h, vent_y = window_info
    if body_solids != 1:
        errors.append(f"case_body fuse produced {body_solids} solids before cleanup")
    body = expect_one_solid("case_body", body, errors)
    print("Building lid, plug, hood, fit frame, coupons...")
    lid, lid_solids = case_lid(values, lay)
    if lid_solids != 1:
        errors.append(f"case_lid fuse produced {lid_solids} solids before cleanup")
    lid = expect_one_solid("case_lid", lid, errors)
    plug = expect_one_solid("usb_c_plug", usb_plug(values), errors)
    hood = expect_one_solid("baro_hood", baro_hood(values), errors)
    blank = expect_one_solid("window_sheet_blank", window_blank(values, sheet_w, sheet_h), errors)
    frame = expect_one_solid("fit_test_frame", fit_frame(values, lay), errors)
    gasket_body, gasket_lid = gasket_coupon(values)
    gasket_body = expect_one_solid("gasket_coupon_body", gasket_body, errors)
    gasket_lid = expect_one_solid("gasket_coupon_lid", gasket_lid, errors)
    strip, diameters = insert_strip(values)
    strip = expect_one_solid("insert_test_strip", strip, errors)

    groove = gasket_tool(values)
    if body is not None:
        run_checks(values, lay, body, groove, errors)
        feature_checks(values, lay, body, errors)
    if mount is not None:
        tab_z = values["garmin_flange_t"] + values["garmin_undercut_h"] + values["garmin_tab_t"] * 0.5
        if not _inside(mount, 8.0, 0.0, tab_z):
            errors.append("garmin tab is missing on the +X ear")
        if _inside(mount, values["garmin_screw_pitch"] / 2.0, 0.0, values["garmin_flange_t"] / 2.0):
            errors.append("garmin flange screw hole is solid")

    ow, oh = outer_size(values)
    mz = mating_z(values)
    derived = [
        ("outer_w", ow, "mm", "Udvendig bredde."),
        ("outer_h", oh, "mm", "Udvendig hoejde."),
        ("body_h", body_height(values), "mm", "Bund fra frontflade til top af styrekrave."),
        ("overall_with_lid", mz + values["lid_t"], "mm", "Frontflade til laagets yderside, uden Garmin-mount."),
        ("mount_height", values["garmin_flange_t"] + values["garmin_undercut_h"] + values["garmin_tab_t"], "mm", "Mount over flangens bund, foer krympning."),
        ("aperture_w", ap_w, "mm", "Vinduesaabning."),
        ("aperture_h", ap_h, "mm", "Vinduesaabning."),
        ("sheet_w", sheet_w, "mm", "Anbefalet polycarbonat-emne."),
        ("sheet_h", sheet_h, "mm", "Anbefalet polycarbonat-emne."),
        ("window_cx", lay["window_c"][0], "mm", "Vinduescenter i kabinettets koordinater."),
        ("window_cy", lay["window_c"][1], "mm", "Vinduescenter i kabinettets koordinater."),
        ("vent_y", vent_y, "mm", "Barometer-vent, center Y."),
        ("feather_x", lay["feather"][0], "mm", "Feather, min-hjoerne."),
        ("feather_y", lay["feather"][1], "mm", "Feather, min-hjoerne."),
        ("display_x", lay["display"][0], "mm", "Display-print, min-hjoerne."),
        ("display_y", lay["display"][1], "mm", "Display-print, min-hjoerne."),
        ("gps_x", lay["gps"][0], "mm", "GNSS-print, min-hjoerne (SMA peger mod +X)."),
        ("gps_y", lay["gps"][1], "mm", "GNSS-print, min-hjoerne."),
        ("patch_x", lay["patch"][0], "mm", "Patch-antenne, min-hjoerne."),
        ("patch_y", lay["patch"][1], "mm", "Patch-antenne, min-hjoerne."),
        ("battery_x", lay["battery"][0], "mm", "Batteribakke, posens min-hjoerne."),
        ("battery_y", lay["battery"][1], "mm", "Batteribakke, posens min-hjoerne."),
    ]

    parts = []
    if not any(s.startswith("null") or "not valid" in s or "volume" in s for s in errors):
        parts = [
            ("garmin_mount", mount),
            ("garmin_gauge_socket", gauge),
            ("tolerance_coupon", coupon),
            ("case_body", body),
            ("case_lid", lid),
            ("usb_c_plug", plug),
            ("baro_hood", hood),
            ("window_sheet_blank", blank),
            ("fit_test_frame", frame),
            ("gasket_coupon_body", gasket_body),
            ("gasket_coupon_lid", gasket_lid),
            ("insert_test_strip", strip),
        ]

    doc = App.newDocument("openCycloComputer_enclosure")
    write_spreadsheet(doc, values, derived)
    # Assembly: case at origin, lid flipped on, mount on the lid, plug and hood nearby.
    if body is not None:
        add_part(doc, "CaseBody", body)
    if lid is not None:
        add_part(doc, "CaseLid", lid_to_assembly(lid, values))
    if mount is not None:
        cx, cy = lay["window_c"]
        add_part(doc, "GarminMount", place(mount, cx, cy, mz + values["lid_t"]))
    if plug is not None:
        # Nose +Z in the print frame. Rotate so the nose points +Y into the bottom wall.
        moved = plug.copy()
        moved.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), -90)
        # After Rx -90: print +Z (nose) becomes +Y, print +Y becomes +Z? 
        # Rx(-90): (x, y, z) -> (x, z, -y). Nose +Z -> +Y. Flange thickness was -Z grip / +Z nose.
        # Translate so the flange outer face sits just outside y=0.
        bb = moved.BoundBox
        moved.translate(App.Vector(ow / 2.0, -bb.YMax, values["usbc_z"]))
        add_part(doc, "UsbPlug", moved)
    if hood is not None:
        moved = hood.copy()
        # Hood local X is its depth; glue face x=0 should land on the case's left face (x=0),
        # opening facing out (-X). Rotate 180 around Z so the cave points -X, then translate.
        moved.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 180)
        bb = moved.BoundBox
        moved.translate(App.Vector(-bb.XMin, vent_y - (bb.YMin + bb.YMax) / 2.0, values["vent_z"] - (bb.ZMin + bb.ZMax) / 2.0))
        add_part(doc, "BaroHood", moved)
    # Loose parts parked to the right so they are visible and not intersecting the case.
    park_x = ow + 12.0
    parked = [
        ("FitTestFrame", frame, park_x, 0, 0),
        ("ToleranceCoupon", coupon, park_x, oh + 10, 0),
        ("GarminGauge", gauge, park_x + 160, 0, 0),
        ("GasketCouponBody", gasket_body, park_x, -50, 0),
        ("GasketCouponLid", gasket_lid, park_x + 70, -50, 0),
        ("InsertTestStrip", strip, park_x, -70, 0),
        ("WindowSheet", blank, park_x, oh - 20, 30),
    ]
    for name, shape, x, y, z in parked:
        if shape is not None:
            add_part(doc, name, place(shape, x, y, z))
    doc.recompute()
    doc.saveAs(FCSTD_PATH)
    print(f"Saved {FCSTD_PATH}")

    if errors:
        print("NOT EXPORTING step/stl because geometry checks failed:")
        for msg in errors:
            print(" -", msg)
        return 1

    print("Exporting STEP and STL...")
    for name, shape in parts:
        export_shape(name, shape, errors)
        print(f"  {name}: volume {shape.Volume:.0f} mm^3")

    print(
        f"Case outer {ow:.1f} x {oh:.1f} mm, body height {body_height(values):.1f} mm, "
        f"with lid {mz + values['lid_t']:.1f} mm (mount extra)."
    )
    print(f"Window aperture {ap_w:.1f} x {ap_h:.1f} mm, polycarbonate blank {sheet_w:.1f} x {sheet_h:.1f} x {values['sheet_t']:.1f} mm.")
    print("Tolerance coupon clearances (dots 1..4):", ", ".join(f"{c:+.2f}" for c in clearances))
    print("Insert-strip hole diameters (pips 1..4):", ", ".join(f"{d:.1f}" for d in diameters))
    if errors:
        print("EXPORT CHECKS FAILED:")
        for msg in errors:
            print(" -", msg)
        return 1
    print("OK")
    return 0


# freecadcmd executes the file under its module name, not always "__main__".
# Guard so a double-exec in the same process only builds once.
if os.environ.get("OCC_BUILD_ONCE") != "1":
    os.environ["OCC_BUILD_ONCE"] = "1"
    raise SystemExit(build())
