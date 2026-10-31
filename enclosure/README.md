# Kabinet

Første udkast til et kabinet der kan printes på en Bambu Lab P1S og rettes i FreeCAD. Det er et fit-prototype, ikke et færdigt produkt: breakout-printene får lov at ligge ved siden af hinanden, så man kan komme til dem. Når elektronikken er målt, rykkes parametrene, og kabinettet kan skrumpe.

Modellen er bygget og eksporteret med FreeCAD 1.0.0 (`freecadcmd`). OpenSCAD bruges ikke.

## Dele

| Fil | Hvad det er | Print den |
| --- | --- | --- |
| `stl/insert_test_strip.stl` | Fire M3-huller, 3,8 / 4,0 / 4,2 / 4,4 mm. Prikker 1–4 | Først |
| `stl/tolerance_coupon.stl` | Fire Garmin-haner med forskellig luft. Prikker 1–4 | Først |
| `stl/garmin_gauge_socket.stl` | Printet hun, så hanen kan prøves uden en rigtig holder | Sammen med kuponen |
| `stl/garmin_mount.stl` | Hanen der skal i en rigtig Garmin-holder, med to M3-huller | Når luften er valgt |
| `stl/fit_test_frame.stl` | Kavitetens fodaftryk med hegn om hvert print | Før det store kabinet |
| `stl/gasket_coupon_body.stl` og `gasket_coupon_lid.stl` | Samme spor-tværsnit som kabinettet, én skrue | Før det store kabinet |
| `stl/case_body.stl` | Bund. Vindue, knapper, USB, vent, varmeindsatser, styretappe | Når fit og pakning er prøvet |
| `stl/case_lid.stl` | Låg, batteribakke, møtrikslommer til holderen | Sammen med bunden |
| `stl/usb_c_plug.stl` | Prop til USB-C-hullet, med spor til en lille snor | Sammen med bunden |
| `stl/baro_hood.stl` | Lille hætte der limes over vent-hullet | Sammen med bunden |
| `stl/window_sheet_blank.stl` | Emnet til 1 mm polycarbonat, ikke en printdel | Send målet til pladeleverandøren |

STEP-filer med samme navne ligger i `step/`. FreeCAD-dokumentet med regneark og PartDesign-kroppe ligger i `freecad/openCycloComputer_enclosure.FCStd`.

## Mål lige nu

Med standardparametrene, bygget 31. oktober 2026:

| | |
| --- | --- |
| Udvendig bund | 110 × 152 × 25,7 mm, inklusive styrekraven |
| Med låg | 28,4 mm fra frontflade til lågets yderside |
| Garmin-mount oveni | ca. 6 mm |
| Vinduesåbning | 55,6 × 34,1 mm |
| Polycarbonat | 59,6 × 38,1 × 1,0 mm |
| Knapmembran | 0,40 mm, to lag ved 0,20 mm laghøjde |

P1S' byggevolumen er 256 mm. Bunden passer på pladen med brim. Det er stort for en cykelcomputer, fordi Feather, Sharp-breakout, MAX-M10S med SMA og batteriet ikke er stablet som i et færdigt produkt. Det er et bevidst v1-valg.

Koordinater, set udefra med skærmen mod dig og USB nedad:

- X vokser mod højre, Y mod himlen (GPS-enden), Z fra frontfladen og bagud.
- Origo er bundens nederste venstre hjørne, på frontfladen.
- Feather ligger nederst, langside langs X, micro-USB mod venstre. USB-C-breakoutet trækkes med ledning til hullet i bundvæggen.
- Sharp-printet ligger over Featheren, centreret i X.
- MAX-M10S ligger øverst til venstre, SMA mod højre. Patch-antennen har en lav ramme til højre for den, mod frontvæggen, så den kigger samme vej som skærmen. På et styrmonteret computer vender den flade skråt op mod rytteren og har en del himmel.
- Batteriet ligger i en bakke på lågets inderside, ud for displayet.
- MAX17048 har et par mærker til højre for Featheren. Mål det rigtige print og ret `fuel_w` og `fuel_h`.

## Garmin quarter-turn

Garmin publicerer ikke målene. Det der cirkulerer, er andres skydelære, og de er uenige om hvorvidt der er to eller fire tapper. Modellen bruger **to tapper over for hinanden**, fordi det er den geometri der faktisk låser ved en kvart omgang: tapperne går ind i holderens sprækker og drejes 90 grader ind under læben.

Startværdier, bevidst midt i det interval der beskrives offentligt:

| Parameter | Værdi | Betydning |
| --- | --- | --- |
| `garmin_tab_outer_d` | 22,5 mm | Tip til tip. Intervallet der nævnes, er ca. 20–24 mm |
| `garmin_neck_d` | 16,0 mm | Navet under tapperne |
| `garmin_tab_angle` | 50° | Hvor bred hver tap er |
| `garmin_tab_t` | 1,4 mm | Tykkelse. Intervallet der nævnes, er ca. 1,0–1,5 mm |
| `garmin_undercut_h` | 2,0 mm | Luft under tappen, til holderens læbe |
| `garmin_clearance` | 0,20 mm | Hvor meget den printede han er krympet, pr. side |

`garmin_clearance` er den knap der skal drejes på. En printet han bliver tykkere og bredere end tegningen. På P1S i PETG eller ASA er 0,20 mm pr. side et sted at starte, ikke et facit.

Tolerancekuponen har fire haner:

| Prikker | `clearance` |
| --- | --- |
| 1 | −0,05 mm (tæt, næsten nominel) |
| 2 | 0,10 mm |
| 3 | 0,20 mm |
| 4 | 0,35 mm |

`garmin_gauge_socket.stl` er en printet hun med 0,30 mm ekstra luft (`female_allowance`), så man kan se om en han overhovedet kan drejes, før man har holderen i hånden. En rigtig Garmin-holder er stadig facit. Soklen har ingen fjeder og intet klik. Når en kupon-han drejer pænt i soklen, prøves den samme clearance i den rigtige holder, og først da sættes `garmin_clearance` og printes `garmin_mount.stl`.

Sæt `garmin_tab_count` til 4 hvis din holder helt tydeligt har fire ens tapper. Så står de med 90 grader, og låsen i målesoklen ligger halvvejs mellem dem (45 grader), ikke efter en fuld kvart omgang. Mål vinklerne før du bruger den indstilling.

Flangen har to M3-huller med 26 mm afstand og et lille hak på +Y, så man kan se hvordan tapperne vender uden at kigge ind under dem. Låget har tilsvarende huller og sekskantede lommer til M3-møtrikker på indersiden.

## At bygge modellen igen

Kilden er `freecad/build_enclosure.py`. Alle mål står i `PARAM_ROWS` øverst, med en dansk forklaring der også skrives ind i regnearket `Parameters` i FCStd-filen. Scriptet lægger hvert solid ind som BaseFeature i en PartDesign-krop, så der kan lægges en lomme eller en pad ovenpå i FreeCAD bagefter.

```bash
freecadcmd enclosure/freecad/build_enclosure.py
```

Scriptet skriver FCStd, STEP og STL. Det kræver FreeCAD 1.0 (testet med 1.0.0). `freecadcmd` skal være på PATH. På en maskine med FreeCAD AppImage kan den pakkes ud og kaldes som `squashfs-root/usr/bin/freecadcmd`.

Vil du ikke rette i Python, så kopier `freecad/overrides.csv.example` til `freecad/overrides.csv`:

```csv
garmin_clearance,0.15
insert_hole_d,4.2
```

De linjer vinder over tabellen i scriptet.

Vil du rette tallene i FreeCAD i stedet: åbn FCStd-filen, ret kolonne B i `Parameters`, gem, og kør

```bash
freecadcmd enclosure/freecad/build_enclosure.py --from-sheet
```

Uden `--from-sheet` bliver regnearket overskrevet med tabellen fra scriptet (plus overrides.csv), så et glemt tal i GUI'en ikke ændrer det næste print i smug. STEP-filerne er dum geometri. De er gode at importere og skære i, men de følger ikke med når en parameter ændres. Byg igen fra scriptet.

FCStd-filen viser også delene samlet: låg og holder sidder på bunden, og de små printdele ligger ved siden af, så de ikke skærer kabinettet.

## Hvad modellen indeholder

- **Bund.** Rundet kasse, åben bagtil. Frontvæg 2,4 mm, så seks perimetre med 0,4 mm dyse er massive. Fals til polycarbonat-vinduet på ydersiden, åbning igennem. Fire styretappe til Sharp-printet (uden bred boss, så de ikke dækker vinduet), bosser med tappe til Feather og GNSS, en lav ramme til patch-antennen og to mærker til fuel gauge.
- **Pakning.** Spor til 2,0 mm silikonesnor, 2,60 mm bredt og 1,50 mm dybt, så snoren stikker ca. 0,5 mm op og klemmes når låget skrues i bund. Sporet går i en stor bue uden om hjørneskruerne. En 2 mm krave styrer låget.
- **Skruer.** Fire blinde huller til M3-varmeindsatser, fra bagsiden, diameter 4,0 mm og dybde 5,5 mm. Låget har frihuller og forsænkning til unbrako. Hullet er et startgæt. Indsatstesten er der for at vælge diameteren før kabinettet printes.
- **Knapper.** To i hver sidevæg. Fordybning udefra, lomme til en 6×6 mm switch indefra, 0,40 mm membran imellem. De sidder i Z et stykke fra pakningssporen, så sporet ikke bliver brudt.
- **USB-C.** Stadium-hul i bundvæggen, 10,4 × 4,8 mm, plus en lav fals til proppens flange. Proppen har et spor til en tynd snor.
- **Barometer.** Hul 2,4 mm gennem venstre væg, øverst, med en 8 mm fals til en åndbar lap (Gore-typen eller en lille ePTFE-mærkat). Hætten er en separat del, så bundens sidevæg ikke skal have et udhæng der kræver support. BMP280 sidder på Featheren nede i kassen. Hullet munder ud i samme hulrum, så trykket kan udligne. Uden hullet måler barometeret kabinettets stivhed, ikke vejen.
- **Låg.** Batteribakke med et hul i den ene væg til ledningen. To møtrikslommer til holderen, placeret ud for displayets center, så skærmen og ikke hele den høje kasse sidder over styret.

Sharp-printets monteringshuller ligger tæt på det aktive områdes langkanter. Åbningen er derfor 3,2 mm smallere end de 58,8 mm, så tappe ikke stikker ind i vinduet. Det beskærer et par pixel-rækker i siderne. `active_off_x` og `active_off_y` er 0 og antager at glasset sidder midt på printet. Mål det, og flyt vinduet. Der er et hak i printets ene langside som lommen ikke følger. Fit-rammen bruger det rektangulære omrids.

## Print på Bambu Lab P1S

Printer: P1S, lukket kammer, 256 × 256 × 256 mm, 0,4 mm dyse. Slicer: Bambu Studio. PETG og ASA kører begge godt. PLA gør ikke. Den bliver blød på et sort styr i sol.

Tør rullen. Både PETG og ASA optager vand, og en våd rulle giver porøse vægge der ikke holder tæt.

### Materiale

**PETG** til tolerancekupon, fit-ramme, pakningskupon og det første kabinet. Tag Bambu Studio-profilen for den rulle du har (Bambu PETG Basic er udgangspunktet: dyse omkring 240–255 °C, tekstureret PEI 70 °C). Kammeret lukket. Emneblæser 20–40 %. Aux-blæser lav eller fra, den trækker holderens flange skæv. Rør ikke ved profilens volumetriske loft for at få den hurtigere.

**ASA** når noget skal bo på cyklen. Bambu ASA-profilen: dyse omkring 260 °C, seng 90 °C, kammer lukket og varmt før første lag, blæser 0–10 % undtagen på udhæng. Brim 6 mm på holder og kabinet. ASA slår sig mere end PETG. P1S' lukkede kammer er grunden til at det kan lade sig gøre. Print ikke ASA med døren åben.

### Profil

| | Kabinet, låg, fit-ramme, pakningskupon | Holder, kupon, målesokkel |
| --- | --- | --- |
| Laghøjde | 0,20 mm | 0,12 mm |
| Linjebredde | 0,42 mm | 0,42 mm |
| Vægge | 6, så 2,4 mm frontvæg er massiv | 8, eller bare 100 % infill |
| Infill | 40 % gyroid | 100 % |
| Top og bund | 5 lag | 5 lag |
| Elefantfod | 0,10–0,15 mm | 0,10–0,15 mm |

Slå *Detect thin wall* til, så 0,40 mm membranen bliver til to lag og ikke til ingenting. Hvis knappen er for stiv, sæt `btn_membrane` til 0,60 mm (tre lag) og byg igen. Hvis den er for slap, er 0,40 mm allerede minimum der er værd at stole på.

Seam: *Aligned*, og mal den hen i et baghjørne. Ikke hen over pakningsfladen og ikke langs O-ringens spor. På låget, som printes med tætningsfladen opad, ligger sømmen på kanten. Det er fint.

Hul-kompensation: start med X-Y hole compensation på 0, og vælg indsats-diameteren ud fra teststrimlen i stedet for at gætte en kompensation. P1S printer huller en smule små. 4,0 mm i modellen er derfor ikke automatisk 4,0 mm på emnet.

### Orientering og support

| Del | På pladen | Support |
| --- | --- | --- |
| Indsatstest, fit-ramme, pakningskupon | Flad, som den er eksporteret | Nej |
| Tolerancekupon og holder | Flange mod pladen, tapper opad | Ja, almindelig support (ikke kun fra pladen) under tappens underside. Top Z-afstand 0,16–0,20 mm. Mal supporten, så skruehullerne ikke fyldes |
| Målesokkel | Bunden mod pladen, åbning op | Nej, hvis sprækkerne er åbne opad. Tjek i sliceren |
| Bund | Vinduet mod pladen, åbning op | Nej. Knappernes fordybninger og USB-falsen ligger mod pladen og klarer sig |
| Låg | Ydersiden mod pladen (z = 0 i STL), tætningsflade og batteribakke op | Nej |
| USB-prop | Flange mod pladen, næse op | Nej |
| Barometer-hætte | Bagsiden mod pladen | Nej |

Tappens underside er et udhæng på omkring 3 mm. Uden support bliver låsefladen ru, og holderen føles slap. Fjern supporten forsigtigt, så fladen der skal ligge an mod holderens læbe, stadig er plan. 100 % infill i tapperne, så de ikke knækker når computeren drejes på plads.

### Rækkefølge

1. `insert_test_strip`. Varm en M3-indsats i det hul der sidder, uden at plasten vælter. Sæt `insert_hole_d` til den diameter. Prikkerne er 3,8, 4,0, 4,2 og 4,4 mm.
2. `tolerance_coupon` og `garmin_gauge_socket` i 0,12 mm. Find den prik-han der går i og drejer uden slør. Gentag den clearance i en rigtig Garmin-holder. Opdater `garmin_clearance`, og print `garmin_mount` først når den rigtige holder siger god for det.
3. `fit_test_frame`. Læg Sharp-print, Feather, MAX-M10S, patch, batteri og fuel gauge ned i hegnet. Hegnet er kaviteten, ikke hele kabinettet. Ret `inner_w`, `inner_h`, zone-målene og antennens mål, hvis noget ikke lander.
4. `gasket_coupon_*` med den rigtige 2 mm silikonesnor og én M3-indsats. Spænd låget, og hold kuponen under en hane. Ret `gasket_groove_w` og `gasket_groove_d` hvis snoren ikke klemmes, eller hvis låget ikke kan komme i bund. Først derefter er det værd at printe 150 mm kabinet.
5. Bund, låg, prop og hætte. Sæt indsatser i bunden mens plasten fra printet stadig er til at arbejde med, men ikke så varm at hullet driver. Skru låget på uden elektronik, og tjek at styrekraven går fri (`lid_clearance` er 0,30 mm pr. side).
6. Polycarbonat i falsen, limet med klar silikone eller UV-lim. Membranen over vent-hullet, så hætten. Holderen på låget med to M3-skruer og møtrikker i lommerne.

Bruser-testen af hele kabinettet hører til milepæl M8, ikke til det første print. En utæt kupon skal ikke gentages i fuld størrelse.
