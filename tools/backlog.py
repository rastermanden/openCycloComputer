#!/usr/bin/env python3
"""Source for the GitHub backlog.

Writes tools/issues.yaml and docs/roadmap.md. Creating the issues on GitHub
is a separate step: tools/create_github_issues.py.

The cloud agent that set the repo up could not create labels, milestones or
issues (GitHub App token, HTTP 403). The files are the backlog until someone
with write access runs the create script.
"""

from __future__ import annotations

import os
import textwrap

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LABELS = [
    ("hardware", "1D4E89", "Elektronik, mekanik og komponentvalg"),
    ("firmware", "5319E7", "Zephyr, nRF Connect SDK og applikationen"),
    ("enclosure/3d-print", "C75300", "FreeCAD, STEP/STL og print på P1S"),
    ("docs", "0075CA", "Dokumentation"),
    ("purchasing", "0E8A16", "Indkøb og leverandører"),
    ("ble", "1D76DB", "Bluetooth Low Energy"),
    ("ant+", "FBCA04", "Garmin ANT+. Licens kræves før det bruges kommercielt"),
    ("gps", "0052CC", "GNSS, MAX-M10S og antenne"),
    ("display", "0530AD", "Sharp Memory LCD"),
    ("power", "D93F0B", "Strøm, batteri og fuel gauge"),
    ("research", "F9D0C4", "Undersøgelse før der bygges"),
    ("good first step", "7057FF", "Afgrænset opgave med et tydeligt slutpunkt"),
]

MILESTONES = [
    (
        "M0 Projektopstart & indkøb",
        "Repo, stykliste og den første ordre. Ingen firmware og intet print der skal passe, før delene er bestilt og de små testprint er planlagt.",
    ),
    (
        "M1 Breadboard-prototype (board+display+GPS lever)",
        "Feather, Sharp-display og MAX-M10S virker på bordet, hver for sig og samtidig. Intet kabinet endnu.",
    ),
    (
        "M2 3D-print: mount & kabinet v1",
        "Garmin-holder, fit og pakning printes og rettes i FreeCAD, før det store kabinet får en chance for at være forkert.",
    ),
    (
        "M3 Firmware basis (Zephyr, display, GPS fix, knapper)",
        "Én Zephyr-app der viser tid, fart og position og kan starte og stoppe en tur. Endnu ingen fil.",
    ),
    (
        "M4 Sensorer (BLE HR/power/speed/cadence, senere ANT+)",
        "Cykelcomputeren er BLE-central for de sensorer man faktisk har. ANT+ er et notat, ikke en implementering.",
    ),
    (
        "M5 Turoptagelse (FIT/GPX, flash/SD)",
        "En tur bliver til en fil på QSPI-flashen og kan hentes ud af boksen.",
    ),
    (
        "M6 Strøm & batterilevetid",
        "Estimaterne i strømbudgettet skiftes ud med målinger, og firmware sover mellem prøverne.",
    ),
    (
        "M7 Navigation & sync",
        "Senere spor: rutevisning og en vej til telefon, Strava eller Garmin Connect. Kun skitser indtil M3–M5 sidder.",
    ),
    (
        "M8 Vandtæt felt-test",
        "Kabinettet og elektronikken udenfor, i vand, kulde og på en rigtig tur.",
    ),
]


def issue(title, milestone, labels, body):
    return {
        "title": title,
        "milestone": milestone,
        "labels": labels,
        "body": textwrap.dedent(body).strip() + "\n",
    }


ISSUES = [
    issue(
        "Køb fase 1-komponenter",
        MILESTONES[0][0],
        ["purchasing", "hardware"],
        """
        Bestil den anbefalede fase 1 fra docs/bom.md. Priserne er fra 29. oktober 2026 og skal skæves til, ikke bruges i blinde hvis en vare er udsolgt. Fragt er ikke med i summen på 1.694 kr.

        ## Tjekliste
        - [ ] Kiwi: Feather nRF52840 Sense (336 kr), MAX17048 (53 kr), 6 mm knapper (19 kr), piezo (12 kr), to STEMMA QT-kabler (18 kr), breadboard (28 kr), Debug Probe (102 kr), USB-C-breakout (27 kr)
        - [ ] Opencircuit: Sharp 2,7" 400×240 (496 kr) og SparkFun MAX-M10S (506 kr). Tjek om en lille ekstra vare udløser fri fragt over 150 EUR
        - [ ] Elektroshoppen: LiPo 2000 mAh JST-PH, den der er listet som LP803860 (97 kr)
        - [ ] Skriv ordre-numre og forventet levering i byggeloggen
        - [ ] microSD og afstandsstykker kun hvis de stadig er ønsket. De er ikke en del af de 1.694 kr

        ## Acceptkriterier
        - Ordrerne er afgivet hos de tre butikker, eller en bevidst erstatning er noteret med link og pris
        - docs/bom.md er rettet hvis en pris eller et varenummer var forkert den dag der blev købt
        - Intet andet board (XIAO, Feather Express) er købt som erstatning uden at hardware-noten er opdateret
        """,
    ),
    issue(
        "Afklar GNSS-antenne og JST-polaritet før delene sættes sammen",
        MILESTONES[0][0],
        ["purchasing", "hardware", "gps", "power"],
        """
        To ting der kan ødelægge den første aften, og som ikke står som linjer med pris i den verificerede stykliste.

        SparkFun MAX-M10S-breakoutet har SMA og ingen chip-antenne. Uden antenne kommer der ikke et fix. Kabinettet har en 25 × 25 mm lomme til en patch, mod fronten, ved siden af printet.

        Elektroshoppens JST-PH kan have plus og minus byttet i forhold til Adafruit. Det slår laderen ihjel.

        ## Tjekliste
        - [ ] Vælg en GNSS-antenne til L1/E1, med SMA, der kan ligge i 25 × 25 mm lommen eller i et kort kabel der kan
        - [ ] Aktiv antenne: den skal kunne fødes med 3,3 V. Passiv: tjek at MAX-M10S-breakoutet er glad for den (SparkFuns note)
        - [ ] Bestil antennen sammen med fase 1
        - [ ] Når batteriet er fremme: mål JST-stikket med et multimeter, uden at sætte det i Featheren
        - [ ] Skriv polariteten (hvilken side der er plus, set ind i stikket) i docs/hardware.md

        ## Acceptkriterier
        - Antennen er bestilt, og lommens mål i FreeCAD er rettet hvis antennen ikke er 25 × 25 mm
        - Polariteten er målt og skrevet ned før stikket har været i nærheden af boardet
        """,
    ),
    issue(
        "Bestil filament, O-ring, indsatser og polycarbonat",
        MILESTONES[0][0],
        ["purchasing", "enclosure/3d-print"],
        """
        Kabinet-delene var ikke med i pristjekket 29. oktober. De skal være i huset før M2, men de behøver ikke vente på elektronikken. Printeren er en P1S. PETG til de første print, ASA når noget skal sidde på cyklen.

        ## Tjekliste
        - [ ] PETG der kører godt på P1S (Bambu PETG Basic eller en rulle du allerede stoler på), tørret
        - [ ] ASA til den senere udgave, hvis den ikke allerede ligger på hylden
        - [ ] Silikonesnor, rund, 2,0 mm. Nok til kupon plus kabinet plus en reserve (et par meter)
        - [ ] M3-varmeindsatser, kort type, og rustfri M3-skruer (unbrako, hoved der passer i 6,6 mm forsænkning)
        - [ ] Klar polycarbonat 1,0 mm, skåret til ca. 60 × 38 mm, helst UV-stabil. Det præcise emne er enclosure/step/window_sheet_blank.step
        - [ ] En lille åndbar membran til barometer-hullet (8 mm fals)

        ## Acceptkriterier
        - Materialerne er i huset, eller der er en ordre med dato
        - docs/bom.md har den faktiske pris og butik, så næste gang ikke starter forfra
        """,
    ),
    issue(
        "Sæt Zephyr og nRF Connect SDK op",
        MILESTONES[0][0],
        ["firmware", "good first step"],
        """
        Værktøjskæden kan installeres mens delene er undervejs. SDK'et skal ikke vendres ind i repoet. Pin en NCS-revision og skriv den i firmware/README.md.

        ## Tjekliste
        - [ ] Installer NCS-toolchain (nordic's installer eller et west-manifest ved siden af repoet)
        - [ ] `west boards | grep feather_nrf52840` og ret board-navnet i firmware/README.md hvis det ikke er `adafruit_feather_nrf52840/nrf52840/sense`
        - [ ] Bekræft at Debug Probe ses som CMSIS-DAP
        - [ ] Byg et af Zephyrs samples for boardet, også selv om du endnu ikke kan flashe det

        ## Acceptkriterier
        - En sample linker for Sense-boardet
        - README siger hvilken NCS-revision og hvilket præcise board-navn der blev brugt
        """,
    ),
    issue(
        "Læs dokumentationen igennem og ret det der allerede er forkert",
        MILESTONES[0][0],
        ["docs", "good first step"],
        """
        README, stykliste, strømbudget, ANT-noten, byggeloggen og kabinet-noten er skrevet ud fra hardwareforslaget 29. oktober 2026 og CAD-udkastet 31. oktober. De skal være til at stole på, før der linkes til dem udefra.

        ## Tjekliste
        - [ ] Følg links i docs/bom.md. Notér dem der er døde
        - [ ] Tjek at summerne 1.565 / 1.694 / 1.855 stadig stemmer med rækkerne
        - [ ] Læs enclosure/README.md op mod de STL-filer der faktisk ligger i mappen
        - [ ] Skriv en linje i byggeloggen hvis noget blev rettet

        ## Acceptkriterier
        - Enten er der ingen rettelser, og det er sagt i issue-tråden, eller rettelserne er merget
        - Ingen hemmelighed (ANT-evalueringsnøgle, token) er landet i repoet
        """,
    ),
    issue(
        "Få Feather Sense til at boote og blinke",
        MILESTONES[1][0],
        ["firmware", "hardware", "good first step"],
        """
        Første livstegn. UF2 er nok. Debug Probe må gerne vente til næste issue.

        ## Tjekliste
        - [ ] Dobbeltklik reset, så BOOT-drevet kommer frem
        - [ ] Læg en UF2-fil bygget til `adafruit_feather_nrf52840/nrf52840/sense/uf2` (eller den variant `west boards` viste)
        - [ ] Den røde LED på ben 13 blinker i et tempo du selv har valgt, ikke bootloaderens standard

        ## Acceptkriterier
        - Et andet menneske kan flashe den samme UF2 og se blinket
        - Commit-id på firmwaren er noteret, også hvis appen stadig kun bor på maskinen og ikke i repoet
        """,
    ),
    issue(
        "Flash og debug over SWD med Debug Probe",
        MILESTONES[1][0],
        ["firmware", "hardware"],
        """
        SWD-padsene sidder på undersiden af Feather Sense. Uden den vej bliver de næste issues langsomme, og strømmåling med breakpoint er umulig.

        ## Tjekliste
        - [ ] Lod eller hold sonden på SWDIO, SWCLK, GND og gerne RESET. Tjek Adafruits pinout, gæt ikke
        - [ ] `west flash` med pyOCD eller OpenOCD rammer boardet
        - [ ] Et breakpoint i main stopper CPU'en, og continue lader den køre videre

        ## Acceptkriterier
        - Blink fra forrige issue kan flashes uden UF2
        - firmware/README.md siger hvilken probe-opsætning der virkede
        """,
    ),
    issue(
        "Vis et testmønster på Sharp 2,7\"",
        MILESTONES[1][0],
        ["display", "firmware", "hardware"],
        """
        Displayet er write-only. Hele 400×240-framen, 13,5 KB, skal ligge i RAM. Adafruit-breakoutet har boost og niveau-skift, så 3,3 V logik er i orden. SPI, plus den VCOM/EXTCOMIN-toggle databladet kræver, ellers falmer billedet.

        ## Tjekliste
        - [ ] Ledninger efter breakoutets silketryk, skrevet ned i et devicetree-overlay
        - [ ] Skakbræt eller en fuld sort/hvid frame, så døde rækker kan ses
        - [ ] Opdatering hvert sekund i et minut uden at billedet falmer
        - [ ] Mål at header-kanten og det aktive område stemmer med active_off_x/y i FreeCAD. Ret parametrene

        ## Acceptkriterier
        - Et stillbillede står skarpt i lampelys og kan opdateres på 1 Hz
        - Overlayet er committet, med de ben der faktisk blev brugt
        """,
    ),
    issue(
        "Få first fix fra MAX-M10S",
        MILESTONES[1][0],
        ["gps", "firmware", "hardware"],
        """
        I²C, u-blox-adresse 0x42 indtil den ændres. Brug UBX, ikke en NMEA-parser, så RAM ikke ædes. Power-LED'en på breakoutet skal kunne slukkes med jumperen. Antennen skal pege mod himmel, ikke ned i bordet.

        ## Tjekliste
        - [ ] Qwiic-kablet sidder, og et scan finder 0x42
        - [ ] Koldstart udendørs eller i et vindue giver et 3D-fix. Notér tiden
        - [ ] Positionen er i nærheden af det sted du står, ikke 0,0
        - [ ] LED'en er slukket, og det er noteret om fixet stadig kommer

        ## Acceptkriterier
        - Tid til første fix og hvilken konstellations-opsætning der blev brugt, er skrevet i byggeloggen
        - Modulet kan slukkes fra firmware, ikke kun med jumperen
        """,
    ),
    issue(
        "Læs batteriprocent fra MAX17048",
        MILESTONES[1][0],
        ["power", "firmware", "hardware"],
        """
        Adafruit-boardet ligger på I²C-adresse 0x36. Det skal have batteriledningerne forbi sig, ikke kun SDA/SCL. Følg Adafruits diagram. Gør det efter polariteten er målt.

        ## Tjekliste
        - [ ] Procent og spænding læses mens batteriet er tilsluttet Featherens JST
        - [ ] Tallet falder lidt når display og GPS er tændt, og står ikke fast på 0 eller 100
        - [ ] Boardet deler bussen med MAX-M10S uden adressekollision

        ## Acceptkriterier
        - En udskrift eller en linje på displayet viser procent og volt
        - Koblingen er tegnet eller fotograferet, så den kan laves igen
        """,
    ),
    issue(
        "Knapper og buzzer på breadboard",
        MILESTONES[1][0],
        ["hardware", "firmware"],
        """
        Fire 6×6 mm knapper og piezoen. I kabinettet bliver det til membraner, men elektrisk er det de samme switches. Vælg ben der ikke ligger i vejen for SPI til displayet og I²C til GNSS og fuel gauge.

        ## Tjekliste
        - [ ] Hver knap giver et interrupt, med debounce, og kan skelnes fra de andre
        - [ ] Buzzeren kan give et kort bip uden at blokere GPS-tråden i et halvt sekund
        - [ ] Benene er skrevet i overlayet

        ## Acceptkriterier
        - Et tryk skifter en tilstand på skærmen (eller i en log, hvis skærmen ikke er med i samme build endnu)
        - Overlayet er committet
        """,
    ),
    issue(
        "Grov strømmåling af breadboardet",
        MILESTONES[1][0],
        ["power", "research"],
        """
        Ikke det endelige budget. Bare et tal, så vi ved om vi er i nærheden af 15 mA eller 80 mA før kabinettet lukkes.

        Mål på batteribenet, ikke på USB ind i Featheren. Laderen blander sig i USB-tallet.

        ## Tjekliste
        - [ ] GPS slukket, display slukket
        - [ ] Display 1 Hz, GPS slukket
        - [ ] GPS med fix, den konstellations-opsætning du faktisk vil bruge
        - [ ] GPS-LED fra
        - [ ] Skriv tallene ind i docs/power-budget.md under estimaterne, med dato

        ## Acceptkriterier
        - Mindst de tre første rækker er målt og skrevet ind
        - Det står tydeligt at det er breadboard, ikke kabinet
        """,
    ),
    issue(
        "Import i FreeCAD og tilpas",
        MILESTONES[2][0],
        ["enclosure/3d-print", "good first step"],
        """
        Modellen er enclosure/freecad/build_enclosure.py plus FCStd-filen ved siden af. STEP er dum geometri og følger ikke med når et mål ændres. Byg igen fra scriptet.

        Åbn FCStd, se regnearket Parameters, og ret det der allerede er forkert når du har delene (antenne, batteriets rigtige mål, vinduets offset). Kør derefter:

        ```
        freecadcmd enclosure/freecad/build_enclosure.py --from-sheet
        ```

        Uden `--from-sheet` vinder tabellen i Python-filen, medmindre freecad/overrides.csv findes.

        ## Tjekliste
        - [ ] FCStd åbner i din FreeCAD, og Parameters viser de danske forklaringer
        - [ ] Et ændret tal (fx garmin_clearance) kan bygges om til en ny STL
        - [ ] PartDesign-kroppene kan få en ekstra lomme uden at scriptet sletter den ved næste kørsel, eller du har noteret at næste kørsel bygger kroppene forfra og at lommer derfor skal ligge i scriptet
        - [ ] Skriv i enclosure/README.md hvis arbejdsgangen på din maskine afviger (FreeCAD-version, MCP)

        ## Acceptkriterier
        - Du har bygget STL'erne lokalt én gang, ikke kun hentet dem fra repoet
        - De mål du ved er forkerte, er rettet i PARAM_ROWS eller overrides.csv og committet
        """,
    ),
    issue(
        "Print Garmin-tolerancekupon og prøv den i en rigtig holder",
        MILESTONES[2][0],
        ["enclosure/3d-print"],
        """
        Print ikke kabinettet først. Tappernes mål er et startgæt (to tapper, 22,5 mm tip til tip, 1,4 mm tykke), og P1S lægger lidt til.

        ## Tjekliste
        - [ ] Print tolerance_coupon.stl og garmin_gauge_socket.stl i PETG, 0,12 mm lag, 100 % infill, flange mod pladen
        - [ ] Support under tappens underside (almindelig support, ikke kun fra byggepladen), og fjern den så låsefladen er plan
        - [ ] Notér hvilken prik-han (1 = −0,05 mm, 2 = 0,10, 3 = 0,20, 4 = 0,35) der drejer i den printede sokkel
        - [ ] Prøv den samme han i en rigtig Garmin quarter-turn-holder. Soklen er ikke facit
        - [ ] Sæt garmin_clearance til den værdi holderen kunne lide, byg garmin_mount.stl igen, og print den

        ## Acceptkriterier
        - Et mount sidder i en rigtig holder, drejer kvart omgang og falder ikke ud når kassen rystes
        - Den valgte clearance og filament/laghøjde er skrevet i enclosure/README.md eller byggeloggen
        - Hvis holderen har fire tapper og ikke to, er garmin_tab_count og vinklerne rettet ud fra dine mål, ikke ud fra gættet
        """,
    ),
    issue(
        "Print fit-test-rammen og læg printene i",
        MILESTONES[2][0],
        ["enclosure/3d-print", "hardware"],
        """
        fit_test_frame.stl er kavitetens fodaftryk (80 × 122 mm i standardmodellen), med hegn om Feather, Sharp, MAX-M10S inkl. SMA, patch, batteri og fuel gauge. Den er ikke hele kabinettet og skal være hurtig at printe om.

        ## Tjekliste
        - [ ] Sharp-printet lander i hegnet, og hakket i langkanten er noteret hvis det generer
        - [ ] Feather lander, hullerne passer på de steder scriptet tror de sidder
        - [ ] MAX-M10S og SMA er indenfor, og den rigtige antenne passer i patch-rammen
        - [ ] Batteriposen passer. Ret bat_w/bat_h/bat_t hvis Elektroshoppens pose ikke er 62 × 38,5 × 8,5 mm
        - [ ] Ret inner_w, inner_h eller zone-målene og print rammen igen, hvis noget stødte

        ## Acceptkriterier
        - Alle fase 1-dele ligger i rammen samtidig uden at bøje et hegn
        - De rettede mål er committet, og en ny STL er bygget
        """,
    ),
    issue(
        "Pakningstest med silikonesnor",
        MILESTONES[2][0],
        ["enclosure/3d-print"],
        """
        gasket_coupon_body.stl og gasket_coupon_lid.stl bruger samme spor som kabinettet: 2,60 × 1,50 mm til en 2,0 mm snor, plus ét M3-hul. Det er billigere at tage fejl her end på 150 mm kabinet.

        ## Tjekliste
        - [ ] Varmeindsats i det hul diameter-testen pegede på
        - [ ] Snoren ligger i sporet uden at vride sig i hjørnerne (centerlinjens radius er stor i kabinettet, mindre i kuponen)
        - [ ] Låget kan skrues i bund, og snoren er klemt, ikke skåret over
        - [ ] Kupon under en hane i et minut. Tør indersiden af med papir bagefter
        - [ ] Ret gasket_groove_w eller gasket_groove_d hvis den drypper eller ikke kan lukkes, og print kuponen igen

        ## Acceptkriterier
        - En kupon er tæt under hanen, med den snor og det filament der skal bruges til kabinettet
        - De endelige spormål er dem scriptet har, ikke et mundtligt "den var fin"
        """,
    ),
    issue(
        "Print kabinet v1: bund, låg og USB-prop",
        MILESTONES[2][0],
        ["enclosure/3d-print"],
        """
        Først når holder, fit-ramme og pakningskupon er accepteret. Orientering og profil står i enclosure/README.md. Bund: vindue mod pladen. Låg: yderside mod pladen, så tætningsfladen er opad og ikke får elefantfod.

        ## Tjekliste
        - [ ] 6 vægge, 0,20 mm lag, PETG, seam væk fra pakningsfladen
        - [ ] Membranen er faktisk to lag og ikke et hul. Tryk på den før switches loddes
        - [ ] Låget lægger sig i styrekraven uden vold
        - [ ] USB-proppen går i hullet og kan tages ud igen
        - [ ] Holderen kan skrues på lågets møtrikslommer og stadig passe i Garmin-holderen

        ## Acceptkriterier
        - Bund, låg, prop og holder er samlet uden elektronik, og skruerne trækker låget ned på snoren
        - Kendte afvigelser (et hul der er for småt, en membran der er for stiv) er enten rettet i parametrene eller skrevet som opfølgning
        """,
    ),
    issue(
        "Sæt varmeindsatser og saml skruerne",
        MILESTONES[2][0],
        ["enclosure/3d-print", "hardware"],
        """
        Fire M3-indsatser i bunden, blinde huller fra bagsiden. To møtrikker i låget hører til holderen og er ikke varmeindsatser.

        ## Tjekliste
        - [ ] Brug den diameter indsatstesten valgte
        - [ ] Indsatserne sidder under pakningsfladen, ikke over den, så låget kan ligge an
        - [ ] Ingen indsats er gået igennem til fronten
        - [ ] Skruerne kan tages ud igen efter et døgn, uden at indsatsen drejer med

        ## Acceptkriterier
        - Låget kan spændes og løsnes tre gange
        - Hvis en indsats fejlede, er huldiameteren rettet og det ene hjørne boret op eller printet om. Ikke "godt nok" med lim
        """,
    ),
    issue(
        "Barometer-vent og åndbar membran",
        MILESTONES[2][0],
        ["enclosure/3d-print", "hardware"],
        """
        Uden hul måler BMP280 på Featheren trykket inde i en kasse, ikke vejret. Hullet sidder i venstre væg, øverst, 2,4 mm, med en 8 mm fals. Hætten er baro_hood.stl og limes udenpå, så væggen ikke har et udhæng.

        ## Tjekliste
        - [ ] Hullet er åbent ind i kaviteten og ikke dækket af GNSS-printet
        - [ ] Membranen dækker falsen og er limet i kanten, ikke tværs over hullet i et tykt lag
        - [ ] Hætten peger sådan at vand nedefra ikke løber ind i hullet
        - [ ] Med låg på: sug eller pust forsigtigt, og se at trykket på BMP280 flytter sig (når firmwaren kan læse det). Indtil da er et manuelt tjek nok: membranen er ikke en massiv limklat

        ## Acceptkriterier
        - Ventilen er monteret, og dens placering er den der er i CAD, eller CAD er rettet
        - Det er noteret hvilken membran der blev brugt
        """,
    ),
    issue(
        "Opret Zephyr-appen for Feather Sense",
        MILESTONES[3][0],
        ["firmware"],
        """
        Én app under firmware/, som beskrevet i firmware/README.md. Ikke et HAL-lag og ikke en kopiering af SDK'et ind i repoet.

        ## Tjekliste
        - [ ] prj.conf og et board-overlay der bygger med den pin'ede NCS-revision
        - [ ] `west build` for Sense-target, og `west flash` over SWD
        - [ ] Appen starter uden USB tilsluttet, på batteri

        ## Acceptkriterier
        - En ren klon plus den dokumenterede NCS-opsætning kan bygge appen
        - Board-navnet i build-kommandoen er det README siger
        """,
    ),
    issue(
        "Sharp-display i Zephyr, opdateret hvert sekund",
        MILESTONES[3][0],
        ["display", "firmware"],
        """
        Flyt testmønsteret fra breadboard-forsøget ind i appen. Framebuffer 13,5 KB. VCOM-toggle må ikke gå i stå når CPU'en sover. Det er en kendt måde at få et Sharp-display til at falme på.

        ## Tjekliste
        - [ ] Driver eller port der kan tegne tekst og en simpel boks
        - [ ] 1 Hz i ti minutter, billede stadig der
        - [ ] SPI-benene kommer fra overlayet, ikke fra magiske tal spredt i koden

        ## Acceptkriterier
        - Skærmen viser et tal der tæller, læsbart i dagslys ved et vindue
        - Strømmen til display-opdateringen er ikke en busy-wait der holder CPU'en vågen hele sekundet
        """,
    ),
    issue(
        "GPS-fix på skærmen",
        MILESTONES[3][0],
        ["gps", "firmware", "display"],
        """
        Tid, position og fart fra MAX-M10S, via UBX. Vis dem når der er fix, og vis "intet fix" når der ikke er. Opfind ikke en fart ud fra nul.

        ## Tjekliste
        - [ ] Koldstart og varmstart, tid noteret
        - [ ] Fart står stille når modulet ligger stille (støj på under en rimelig grænse, skriv grænsen)
        - [ ] GNSS kan slukkes fra appen

        ## Acceptkriterier
        - En tur ned ad gaden giver en fart der ligner virkeligheden
        - Konstellations-opsætningen er den du vil måle strøm på i M6, og den er skrevet ned
        """,
    ),
    issue(
        "Knapper: start, stop, omgang og side",
        MILESTONES[3][0],
        ["firmware"],
        """
        Fire funktioner, også hvis to af dem foreløbig kun skifter side. Debounce i firmware. Langt tryk må gerne være reserveret, men skal ikke være påkrævet for at starte en tur.

        ## Tjekliste
        - [ ] Start og stop kan ikke forveksles ved et enkelt prel
        - [ ] Omgang noteres (i en log er nok, FIT kommer i M5)
        - [ ] Side skifter mellem mindst to skærmbilleder
        - [ ] Bip ved omgang, kort nok til at det ikke blokerer

        ## Acceptkriterier
        - Man kan starte, markere omgang og stoppe uden at kigge i koden
        - Tilstandene overlever ikke et reset endnu. Det er i orden, og det er sagt
        """,
    ),
    issue(
        "Grundlayout på displayet",
        MILESTONES[3][0],
        ["display", "firmware"],
        """
        400×240 er nok til store tal. Første layout: fart stort, tid og distance mindre, puls/watt som pladsholdere indtil M4. Ingen dekoration der koster framebuffer-tid.

        ## Tjekliste
        - [ ] Fart kan læses på en arms længde
        - [ ] Der er en tydelig forskel på "kører" og "stoppet"
        - [ ] Layoutet flimrer ikke ved 1 Hz

        ## Acceptkriterier
        - Et foto i dagslys hvor fart, tid og en status kan læses
        - Pladsholderne for puls og watt er tomme felter, ikke tal der lyver
        """,
    ),
    issue(
        "Tur-tilstand uden filformat",
        MILESTONES[3][0],
        ["firmware"],
        """
        Tilstandsmaskinen skal findes før FIT gør den svær at ændre. Tilstande: klar, kører, stoppet. Omgang er en hændelse, ikke en tilstand.

        ## Tjekliste
        - [ ] Ulovlige hop (omgang mens den er klar) ignoreres
        - [ ] Distance og tid fryser når turen er stoppet
        - [ ] Et punkt i sekundet ligger i en ringbuffer i RAM, også selv om den ikke gemmes endnu

        ## Acceptkriterier
        - Maskinen er dækket af en lille test eller af en kommenteret log fra en rigtig kørsel på bordet
        - M5 kan lægge FIT ovenpå uden at starte forfra med tilstandene
        """,
    ),
    issue(
        "BLE-central: scan og vis enheder",
        MILESTONES[4][0],
        ["ble", "firmware"],
        """
        Computeren er central, ikke peripheral, når den taler med sensorer. Telefon-synk er et andet spor (M7) og må ikke blokere denne opgave.

        ## Tjekliste
        - [ ] Scan viser navn og RSSI for det der er i rummet
        - [ ] Filtrér så listen ikke er alle høretelefoner i nabolaget, men gem muligheden for at se dem mens du debugger
        - [ ] Scan slutter og forbindelsen kan etableres uden at GPS-tråden sulter

        ## Acceptkriterier
        - Mindst én kendt sensor dukker op med et navn du genkender
        - Det er dokumenteret hvilke connection-parametre der blev brugt
        """,
    ),
    issue(
        "Pulsbælte over BLE",
        MILESTONES[4][0],
        ["ble", "firmware", "display"],
        """
        Heart Rate Service. Vis pulsen i det felt grundlayoutet reserverede. Mistet forbindelse skal vises, ikke fryse det sidste tal som om det stadig gjaldt.

        ## Tjekliste
        - [ ] Forbind til dit eget bælte
        - [ ] Tallet følger når du holder vejret eller løber på stedet
        - [ ] Bæltet slukkes: UI viser at pulsen er væk inden for et aftalt antal sekunder
        - [ ] Genforbinder når bæltet tændes igen, uden genstart af computeren

        ## Acceptkriterier
        - Puls på skærmen under en kort tur på cyklen eller løbebåndet
        - Batteri-niveau fra sensoren vises hvis den udsender det, ellers er manglen noteret
        """,
    ),
    issue(
        "Fart og kadence fra en CSC-sensor",
        MILESTONES[4][0],
        ["ble", "firmware"],
        """
        Cycling Speed and Cadence. Hjulomkreds skal kunne sættes uden at rekompilere, også selv om det foreløbig er en konstant i en header med en kommentar om hvor den senere skal bo.

        ## Tjekliste
        - [ ] Kadence bevæger sig når kranken drejes
        - [ ] Sensor-fart og GPS-fart kan ses samtidig, så et forkert hjulmål opdages
        - [ ] Manglende sensor falder tilbage til GPS-fart, tydeligt markeret

        ## Acceptkriterier
        - En kort tur hvor de to farter er inden for noget du vil stå på mål for, og afvigelsen er noteret
        - Hjulomkredsen står ét sted i koden
        """,
    ),
    issue(
        "Wattmåler over BLE",
        MILESTONES[4][0],
        ["ble", "firmware", "display"],
        """
        Cycling Power Service. Effekt på skærmen. Ikke alle målere sender det samme sæt felter. Tag det din måler faktisk sender, og lad være med at regne watt ud fra en kadence der ikke findes.

        ## Tjekliste
        - [ ] Forbind til måleren
        - [ ] Watt følger når du træder
        - [ ] 0 W når du frihjulet, inden for målerens egen opførsel
        - [ ] Hvis måleren også er kadence-kilde, så dobbelt-tæl ikke kadence med CSC-sensoren. Vælg én og skriv valget ned

        ## Acceptkriterier
        - Watt synlig sammen med fart på grundlayoutet
        - Kendte mangler ved netop denne måler er noteret
        """,
    ),
    issue(
        "Genforbindelse når flere sensorer er med",
        MILESTONES[4][0],
        ["ble", "firmware"],
        """
        Puls, CSC og watt samtidig. nRF52840 kan flere centrale forbindelser. Det er her det skal bevises, ikke i hver sin demo.

        ## Tjekliste
        - [ ] Alle tre forbundet på én gang, GPS stadig med fix
        - [ ] Sluk én sensor. De to andre bliver hængende
        - [ ] Tænd den igen. Den kommer tilbage uden at de andre tabes
        - [ ] Notér hvor mange forbindelser og hvilke interval-parametre der blev brugt

        ## Acceptkriterier
        - En tur med de sensorer du ejer, hvor et bevidst slukket bælte kommer igen
        - UI viser hvilke sensorer der mangler
        """,
    ),
    issue(
        "Notat om ANT+ evalueringsnøgle, uden at implementere det",
        MILESTONES[4][0],
        ["ant+", "research", "docs"],
        """
        BLE er vejen. Denne opgave er kun et notat, så licensen ikke bliver en overraskelse den dag en gammel sensor ikke findes på BLE.

        Læs docs/ant-plus.md og Garmins sider igen. Læg ikke en evalueringsnøgle i repoet.

        ## Tjekliste
        - [ ] Bekræft om prisen (evaluering gratis, kommercielt 0,08 USD pr. enhed, minimum 800 USD pr. halvår, som læst 29. oktober 2026) stadig står på siden
        - [ ] Skriv afvigelser ind i docs/ant-plus.md med dato
        - [ ] Beslut om nogen sensor du faktisk ejer, kræver ANT. Hvis nej, lukkes sporet her

        ## Acceptkriterier
        - docs/ant-plus.md er genlæst og dateret
        - Ingen nøgle, ingen binær stak og ingen vendoring af ant-nrfconnect er committet
        """,
    ),
    issue(
        "Skriv FIT for en tur",
        MILESTONES[5][0],
        ["firmware"],
        """
        Én fil pr. tur. Punkter fra ringbufferen i M3, plus de sensorer M4 har. FIT frem for at opfinde et format. Et bibliotek der kan bygges på Zephyr, vælges bevidst. Hvis det ikke findes i en form vi vil eje, skrives de records vi faktisk bruger, ikke hele spec'en.

        ## Tjekliste
        - [ ] En kort tur bliver til en fil der kan åbnes i et FIT-værktøj eller en viewer
        - [ ] Tid, position og fart er der. Puls og watt er der hvis sensoren var med
        - [ ] En tom tur (start og stop med det samme) giver ikke en korrupt fil

        ## Acceptkriterier
        - En fil fra en rigtig tur er gemt som prøve (uden private spor, eller med et spor du vil have liggende) og kan åbnes
        - Format-versionen er noteret
        """,
    ),
    issue(
        "Filsystem på QSPI-flashen",
        MILESTONES[5][0],
        ["firmware"],
        """
        Feather Sense har 2 MB QSPI. LittleFS er udgangspunktet. 100–150 KB pr. time er tommelfingerreglen fra hardware-noten. Mål den på de filer du faktisk skriver.

        ## Tjekliste
        - [ ] Filer overlever reboot
        - [ ] Fuld flash håndteres (ældste tur slettes, eller skrivning stopper med en fejl på skærmen, vælg én)
        - [ ] Sluk under skrivning giver ikke en fil der crasher vieweren. LittleFS' egen garanti skal prøves, ikke antages

        ## Acceptkriterier
        - To ture efter hinanden ligger som to filer efter en strømafbrydelse imellem dem
        - Den målte størrelse pr. time er skrevet ind ved siden af estimatet
        """,
    ),
    issue(
        "GPX som eksport",
        MILESTONES[5][0],
        ["firmware"],
        """
        GPX kan laves på telefonen senere. Denne opgave er kun værd at tage på enheden hvis det er lettere end at vente. Vælg ét sted.

        ## Tjekliste
        - [ ] Beslut: GPX på enheden, eller GPX i telefonen ud fra FIT
        - [ ] Hvis på enheden: en fil der importeres i noget der kan vise et spor
        - [ ] Hvis på telefonen: skriv beslutningen i docs, og luk opgaven

        ## Acceptkriterier
        - Et spor kan ses på et kort, et sted i kæden, og stedet er dokumenteret
        """,
    ),
    issue(
        "Hent turfilen ud af boksen",
        MILESTONES[5][0],
        ["firmware", "ble"],
        """
        USB mass storage er den korte vej. BLE-overførsel må gerne være et eksperiment, men USB skal virke først, så en tur ikke sidder fast i kassen.

        ## Tjekliste
        - [ ] Når computeren sættes i en USB-port, kan filen kopieres af
        - [ ] Det ødelægger ikke den tur der stadig optages, eller optagelse er stoppet og det kan ses
        - [ ] Filen er den samme FIT som vieweren kunne åbne

        ## Acceptkriterier
        - En fil er kopieret til en laptop og åbnet, uden serie-konsol som mellemled
        - Begrænsninger (skal være stoppet, må ikke være på batteri alene, osv.) er skrevet i README
        """,
    ),
    issue(
        "Distance og tid ud fra GPS-punkterne",
        MILESTONES[5][0],
        ["gps", "firmware"],
        """
        Distance på skærmen og i filen skal være den samme. Filtrér punkter uden fix, så et hop til 0,0 ikke lægger en tur til ækvator oven i søndagsturen.

        ## Tjekliste
        - [ ] En kendt strækning (mål den på et kort) rammes inden for en afvigelse du skriver ned
        - [ ] Stå stille i to minutter. Distancen må ikke kravle
        - [ ] Tid er tur-tid, ikke væg-ur, og den pauser når turen er stoppet

        ## Acceptkriterier
        - Afvigelsen på testsstrækningen er noteret i byggeloggen
        - Samme tal står på skærmen og i FIT-filen
        """,
    ),
    issue(
        "Mål strøm i de GNSS-tilstande du faktisk bruger",
        MILESTONES[6][0],
        ["power", "gps"],
        """
        Erstat estimaterne. Samme metode som den grove breadboard-måling, men nu med den firmware der skal på cyklen, og med LED'en slukket.

        ## Tjekliste
        - [ ] Den valgte konstellations-opsætning, med fix, display 1 Hz, ingen BLE
        - [ ] Samme, plus de sensorer du kører med
        - [ ] GPS slukket, display 1 Hz
        - [ ] Skriv tallene i docs/power-budget.md med dato, commit og målemetode

        ## Acceptkriterier
        - Tabellen har en målt kolonne ved siden af de tre estimater
        - Det er tydeligt om tallet er gennemsnit over et minut eller en spids
        """,
    ),
    issue(
        "Sammenlign målingen med strømbudgettet",
        MILESTONES[6][0],
        ["power", "docs"],
        """
        115 timer var det realistiske estimat ved 14,8 mA. Regn den målte driftstid ud med samme formel (2000 mAh × 0,85 / målt mA) og sig om estimatet holdt.

        ## Tjekliste
        - [ ] Regnestykket står i docs/power-budget.md
        - [ ] Hvis målingen er mere end ca. det dobbelte af estimatet, er den sandsynlige synder navngivet (GPS-tilstand, LED, sensor der ikke sover, USB der var tilsluttet)
        - [ ] Ingen ny feature startes for at "fixe" tallet før synderen er navngivet

        ## Acceptkriterier
        - Et afsnit i strømbudgettet med målt driftstid og én sætning om hvad der skal ændres, eller at intet skal
        """,
    ),
    issue(
        "Sluk det der ikke skal være tændt",
        MILESTONES[6][0],
        ["power", "firmware"],
        """
        GPS-LED, IMU og magnetometer når de ikke bruges, displayets bus mellem frame-opdateringer, radioens duty cycle. BMP280 skal samples, ikke ligge i kontinuerlig mode hvis det koster.

        ## Tjekliste
        - [ ] Hver slukket blok er en commit eller et afsnit, så man kan se hvad der rykkede tallet
        - [ ] Fix og puls virker stadig bagefter
        - [ ] Ny måling ind i tabellen

        ## Acceptkriterier
        - Den målte strøm er lavere end før denne opgave, eller der er en forklaring på at den ikke kunne blive det
        - Ingen "optimering" der slukker GPS så der ikke længere er et fix
        """,
    ),
    issue(
        "Batteriprocent på skærmen under en tur",
        MILESTONES[6][0],
        ["power", "display", "firmware"],
        """
        MAX17048 er allerede læst på breadboardet. Her skal tallet være til at stole på en time inde i en tur, ikke kun ved et fuldt batteri på bordet.

        ## Tjekliste
        - [ ] Procent vises på grundlayoutet
        - [ ] Den falder monotont på en tur, inden for gauge'ens egen støj
        - [ ] Lav batteristand giver et bip én gang, ikke et bip hvert sekund

        ## Acceptkriterier
        - Foto eller note fra en tur hvor procenten ved start og slut er skrevet ned sammen med den målte spænding
        """,
    ),
    issue(
        "Driftstid på en rigtig tur",
        MILESTONES[6][0],
        ["power"],
        """
        Ikke en laboratorie-ekstrapolation. En tur der er lang nok til at tallet betyder noget, eller flere ture på samme opladning med procenten skrevet ned.

        ## Tjekliste
        - [ ] Start ved en kendt procent
        - [ ] Kør med den opsætning M4 endte på (de sensorer du har)
        - [ ] Notér varighed, distance og procent ved slut
        - [ ] Sammenlign med formlen

        ## Acceptkriterier
        - Mindst to timer er logget, med vejret og ca. temperatur, fordi kulde flytter kapaciteten
        - Resultatet står i byggeloggen
        """,
    ),
    issue(
        "Lavstrøm mellem GPS-samples",
        MILESTONES[6][0],
        ["power", "firmware"],
        """
        CPU og radio skal sove mellem de prøver turen faktisk gemmer. 1 Hz på displayet og 1 Hz i filen betyder ikke at kernen skal køre et busy-loop.

        ## Tjekliste
        - [ ] Strømprofilen viser søvn mellem samples, ikke en flad linje på det aktive forbrug
        - [ ] VCOM på Sharp-displayet kører stadig
        - [ ] Knapper vækker med det samme

        ## Acceptkriterier
        - Et plot eller en række tal fra Power Profiler eller måleren, committet eller lagt i byggeloggen
        - Ingen mistet knap eller mistet fix som pris for søvnen
        """,
    ),
    issue(
        "Skitsér navigation: pil eller brødkrumme",
        MILESTONES[7][0],
        ["research", "firmware", "display"],
        """
        Ikke en implementering. 400×240 kan vise en pil og et gadenavn, ikke et rasterkort, medmindre kortet kommer udefra. Skriv hvad v1 af navigation må være.

        ## Tjekliste
        - [ ] Vælg: kun brødkrumme af den optagede tur, eller en rute der er lagt ind udefra
        - [ ] Sig hvor ruten kommer fra (GPX ind på flashen, BLE, eller ikke endnu)
        - [ ] En papirskitse eller et billede af skærmlayoutet

        ## Acceptkriterier
        - Et kort afsnit i docs, der siger hvad der ikke bygges endnu
        - Ingen halv navigation i firmwaren der lyver om et sving
        """,
    ),
    issue(
        "Udkast til hvordan en tur kommer over på telefonen",
        MILESTONES[7][0],
        ["ble", "research", "docs"],
        """
        USB virker fra M5. Denne opgave er den trådløse vej, som udkast. Protokol før app.

        ## Tjekliste
        - [ ] Hvad der sendes (hele FIT-filen, eller punkter)
        - [ ] Hvem der er central når telefonen er med. Det kan stride mod sensor-rollen. Skriv konflikten
        - [ ] Om det overhovedet skal være BLE, eller om USB er nok til v1

        ## Acceptkriterier
        - En side i docs med beslutningen, inklusive "vi lader være indtil videre" hvis det er svaret
        """,
    ),
    issue(
        "Undersøg companion-app, uden at starte en",
        MILESTONES[7][0],
        ["research"],
        """
        En app er et produkt ved siden af cykelcomputeren. Kig på hvad der allerede findes (import af FIT, eksisterende åbne projekter) før der oprettes et nyt repo.

        ## Tjekliste
        - [ ] Kan en eksisterende app eller et script tage vores FIT-fil?
        - [ ] Hvis ja: dokumentér vejen. Hvis nej: skriv de tre ting appen skulle kunne, og lad være med at bygge den her

        ## Acceptkriterier
        - Beslutningen står i docs, med links
        """,
    ),
    issue(
        "Eksport til Strava eller Garmin Connect",
        MILESTONES[7][0],
        ["research", "docs"],
        """
        Vejen er næsten sikkert "FIT-fil ud, og så et værktøj der allerede findes". Bekræft det med én fil fra M5. Garmin Connect og ANT-licensen er ikke det samme problem. At uploade en FIT kræver ikke at enheden selv taler ANT+.

        ## Tjekliste
        - [ ] En rigtig fil er uploadet eller importeret et sted du bruger
        - [ ] Hvad der gik tabt (puls, watt, omgange) er noteret
        - [ ] Ingen API-nøgler i repoet

        ## Acceptkriterier
        - Byggeloggen siger hvor filen landede, og hvad der manglede
        """,
    ),
    issue(
        "Plan for firmware-opdatering, ikke selve opdateringen",
        MILESTONES[7][0],
        ["firmware", "research"],
        """
        UF2 og SWD virker allerede som udviklervej. OTA er først interessant når kabinettet er skruet sammen og du ikke vil åbne det. Skriv vejen, byg den ikke her.

        ## Tjekliste
        - [ ] UF2 gennem USB-C-hullet: virker det med proppen af og kablet i breakoutet?
        - [ ] Skal MCUboot med senere, ja eller nej, og hvorfor
        - [ ] Hvad der må ikke gå galt (en halv opdatering på en tur)

        ## Acceptkriterier
        - Et afsnit i firmware/README.md
        - Ingen MCUboot-opsætning merget "fordi den var i nærheden"
        """,
    ),
    issue(
        "Bruser-test af det samlede kabinet",
        MILESTONES[8][0],
        ["enclosure/3d-print", "hardware"],
        """
        Elektronikken skal kunne tåle at være i kassen, eller kassen testes tom først og derefter med elektronik hvis du tør. Start tom. Pakningskuponen var kun kuponen.

        ## Tjekliste
        - [ ] Snor, skruer, prop, membran og vindue monteret
        - [ ] Bruser eller vandkande i nogle minutter, derefter papir i hjørnerne
        - [ ] Hvis det drypper: find stedet (spor, prop, membran, vindueslim, en skrue der gennemborede noget) før der printes et nyt kabinet i blinde
        - [ ] Ret CAD hvis tætningen krævede et andet mål, og notér det

        ## Acceptkriterier
        - Tom kasse er tør indeni efter testen, eller utætheden er identificeret og der er en opfølgning
        - Elektronik har ikke været med i en test der ikke var tæt
        """,
    ),
    issue(
        "Barometer mod en kendt stigning",
        MILESTONES[8][0],
        ["hardware", "firmware"],
        """
        Kør eller gå en bakke du kender højden på, med ventilen monteret. Sammenlign med GPS-højde og med kortet. De tre er ikke ens. Skriv forskellen.

        ## Tjekliste
        - [ ] Samme bakke op og ned
        - [ ] Med og uden at proppen sidder i, hvis du mistænker at kassen er for tæt et andet sted
        - [ ] Temperatur noteret

        ## Acceptkriterier
        - Højdeforskellen er i byggeloggen, med hvilken kilde du stoler mest på bagefter
        - Hvis barometeret ikke flyttede sig, er ventilen fejlfindingspunktet, ikke filteret i firmwaren
        """,
    ),
    issue(
        "Kvalitet af GPS-sporet",
        MILESTONES[8][0],
        ["gps", "firmware"],
        """
        Et spor i skov, et spor mellem huse, et spor i det åbne. Antennens placering i toppen af kassen er et gæt indtil dette er kørt.

        ## Tjekliste
        - [ ] Tre miljøer, samme firmware
        - [ ] Hvor sporet hopper, og om det er antennen, vinduet eller en metalholder under kassen
        - [ ] Ret antennens placering i CAD hvis sporet kræver det

        ## Acceptkriterier
        - Tre FIT-filer eller et sammendrag med den værste afvigelse
        - Beslutning: antenneplaceringen bliver, eller den flyttes
        """,
    ),
    issue(
        "Kulde og batteri",
        MILESTONES[8][0],
        ["power", "hardware"],
        """
        0,85-faktoren i budgettet er et gæt på kulde og alder. En tur omkring frysepunktet, eller kassen i en kold bil en time før start, siger mere.

        ## Tjekliste
        - [ ] Startprocent efter kulde, sammenlignet med samme opladning indendørs
        - [ ] Om displayet stadig opdaterer (Sharp bør være ligeglad, e-paper ville ikke være det)
        - [ ] Om proppen og snoren stadig sidder når plasten er kold

        ## Acceptkriterier
        - En note i strømbudgettet: holdt faktoren, eller den skal være lavere
        """,
    ),
    issue(
        "Vibration: brosten eller grus",
        MILESTONES[8][0],
        ["hardware", "enclosure/3d-print"],
        """
        Holderen og skruerne. En kvart omgang der bakker ud på brosten, er en forkert clearance eller en manglende fjeder, ikke "printet var pænt".

        ## Tjekliste
        - [ ] En tur på dårlig belægning med computeren monteret
        - [ ] Bagefter: er holderen stadig låst, er skruerne stramme, er noget raslet løs inde i kassen
        - [ ] Switches sidder stadig bag membranerne

        ## Acceptkriterier
        - Enten overlevede den, og det er sagt med hvilken holder og hvilket underlag
        - Eller den gjorde ikke, og næste ændring i CAD er navngivet
        """,
    ),
    issue(
        "Samlet felttur og noter",
        MILESTONES[8][0],
        ["hardware", "firmware", "docs"],
        """
        Mindst to timer, med de sensorer der virker, filen hentet ud bagefter, og en ærlig note om hvad der var irriterende. Det er den note næste runde af CAD og firmware skal starte fra.

        ## Tjekliste
        - [ ] Turen ligger som FIT og kan åbnes
        - [ ] Procent ved start og slut
        - [ ] Hvad du kiggede efter på skærmen og ikke kunne finde
        - [ ] Hvad der tog vand, raslede eller mistede fix
        - [ ] Skriv det i docs/buildlog.md som næste nummer

        ## Acceptkriterier
        - Byggeloggen har feltturen, med commit-id på firmwaren og hvilken STL-revision kabinettet var
        - Mindst én konkret næste ændring er nævnt, ikke kun "det virkede fint"
        """,
    ),
]


def dump():
    labels = [
        {"name": name, "color": color, "description": desc}
        for name, color, desc in LABELS
    ]
    milestones = [{"title": title, "description": desc} for title, desc in MILESTONES]
    doc = {"labels": labels, "milestones": milestones, "issues": ISSUES}
    yaml_path = os.path.join(ROOT, "tools", "issues.yaml")
    with open(yaml_path, "w", encoding="utf-8") as handle:
        handle.write(
            "# Backlog for openCycloComputer.\n"
            "# Kilden til teksten er tools/backlog.py. Kør den for at genskabe denne fil\n"
            "# og docs/roadmap.md. Opret issues med tools/create_github_issues.py\n"
            "# når du har en GitHub-token der må skrive til repoet.\n"
        )
        yaml.safe_dump(doc, handle, allow_unicode=True, sort_keys=False, width=100)
    write_roadmap(doc)
    print(f"wrote {yaml_path} and docs/roadmap.md ({len(ISSUES)} issues)")


def write_roadmap(doc):
    lines = []
    lines.append("# Køreplan")
    lines.append("")
    lines.append(
        "GitHub-labels, milepæle og issues blev ikke oprettet. Cloud-agentens token "
        "fik HTTP 403 (`Resource not accessible by integration`) da den prøvede at "
        "oprette en label på `rastermanden/openCycloComputer`. Den kan læse repoet "
        "og skubbe commits, men ikke skrive i issue-trackeren."
    )
    lines.append("")
    lines.append(
        "Backloggen ligger derfor her og i den maskinlæsbare fil "
        "[../tools/issues.yaml](../tools/issues.yaml). Når du er logget ind med en "
        "konto der må oprette issues, kør:"
    )
    lines.append("")
    lines.append("```bash")
    lines.append("python3 tools/create_github_issues.py")
    lines.append("```")
    lines.append("")
    lines.append(
        "Scriptet springer labels, milepæle og issues over, hvis de allerede findes, "
        "så det kan køres igen. Teksten vedligeholdes i `tools/backlog.py`. Kør den "
        "fil uden argumenter for at genskabe yaml og denne side."
    )
    lines.append("")
    lines.append("## Labels")
    lines.append("")
    lines.append("| Label | Farve | Betydning |")
    lines.append("| --- | --- | --- |")
    for label in doc["labels"]:
        lines.append(
            f"| `{label['name']}` | `#{label['color']}` | {label['description']} |"
        )
    lines.append("")
    lines.append("## Milepæle")
    lines.append("")
    for milestone in doc["milestones"]:
        count = sum(1 for item in doc["issues"] if item["milestone"] == milestone["title"])
        lines.append(f"### {milestone['title']}")
        lines.append("")
        lines.append(milestone["description"])
        lines.append("")
        lines.append(f"{count} opgaver.")
        lines.append("")
        for item in doc["issues"]:
            if item["milestone"] != milestone["title"]:
                continue
            labels = ", ".join(f"`{name}`" for name in item["labels"])
            lines.append(f"#### {item['title']}")
            lines.append("")
            lines.append(f"Labels: {labels}")
            lines.append("")
            lines.append(item["body"].rstrip())
            lines.append("")
    path = os.path.join(ROOT, "docs", "roadmap.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")


if __name__ == "__main__":
    dump()
