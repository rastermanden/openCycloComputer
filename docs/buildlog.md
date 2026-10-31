# Byggelog

## 1 — 29. oktober 2026. Hardwareforslag og stykliste

Valgt til første prototype: Adafruit Feather nRF52840 Sense, Sharp Memory LCD 2,7" 400×240, u-blox MAX-M10S og LiPo 2000 mAh med MAX17048.

Priser og links blev tjekket samme dag hos Kiwi Electronics, Opencircuit og Elektroshoppen. Eurokurs 7,4736. Kernedelene landede på 1.565 kr, og 1.694 kr med debugger og USB-C-breakout. Et strømbudget med Sharp-displayet gav omkring 115 timer i det realistiske scenarie (54–236 timer i yderpunkterne).

Besluttet at firmware-sporet er Zephyr/nRF Connect SDK, med BLE først og ANT+ senere, fordi ANT-stakken er Garmins. XIAO nRF52840 blev vurderet og stillet som det billigere alternativ, ikke som det der bygges.

Intet blev bestilt.

## 2 — 31. oktober 2026. Repo, indkøb forberedes, print starter snart

Repoet `openCycloComputer` er oprettet, offentligt, MIT, med den danske dokumentation fra hardwareforslaget. Fase 1-delene er skrevet sammen som indkøbsliste. Der er stadig ikke bestilt noget.

Kabinettet er modelleret parametrisk i FreeCAD (Part og PartDesign, med et regneark over alle mål) til en Bambu Lab P1S. Modellen har Garmin quarter-turn-han, bund og låg med O-ringspor, vinduesfals, knap-membraner, USB-C-prop, barometer-vent og en fit-test-ramme. STEP og STL er eksporteret og ligger i `enclosure/`. Målene på quarter-turn er fællesskabets størrelsesorden, ikke et officielt Garmin-mål, og skal tunes på en rigtig holder før kabinettet printes i den endelige udgave.

Næste konkrete skridt er at bestille fase 1 og at printe tolerancekupon og fit-ramme, så FreeCAD-målene kan rettes mens elektronikken er undervejs. Printeren er en P1S (lukket, 256 mm i alle led, 0,4 mm dyse). PETG og ASA kører begge godt på den. Martin tegner selv videre i FreeCAD.
