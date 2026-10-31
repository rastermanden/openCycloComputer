# Stykliste

Priser tjekket **29. oktober 2026**. Kiwi Electronics viser priser ekskl. moms; der er lagt 25 % dansk moms på. Euro er omregnet med 7,4736 kr (ECB den dag). Fragt er ikke med. Butikkerne sender til Danmark: Kiwi fra Nederlandene, Opencircuit og Elektroshoppen fra Danmark. Antratek i København er nævnt hvor de havde en bedre pris, men varen var udsolgt.

Intet er bestilt.

## Anbefalet fase 1

| Del | Valg | Butik | Pris | Verificeret | Link |
| --- | --- | --- | --- | --- | --- |
| Dev-board | Adafruit Feather nRF52840 Sense | Kiwi Electronics (NL) | 336 kr | 35,99 EUR ekskl. moms, 5 på lager | [kiwi](https://www.kiwi-electronics.com/en/adafruit-feather-nrf52840-sense-10185) |
| Display | Adafruit Sharp Memory Display 2,7" 400×240 | Opencircuit.dk | 496 kr | 66,40 EUR inkl. moms, eksternt lager 10–12 dage | [opencircuit](https://opencircuit.dk/product/adafruit-sharp-memory-display-breakout-2.7) |
| GNSS | SparkFun MAX-M10S breakout (Qwiic) | Opencircuit.dk | 506 kr | 67,70 EUR inkl. moms, eksternt lager 5–7 dage | [opencircuit](https://opencircuit.dk/product/sparkfun-gnss-receiver-breakout-max-m10s-qwiic) |
| Batteri | LiPo 3,7 V 2000 mAh, JST-PH (LP803860) | Elektroshoppen.dk | 97 kr | 96,95 kr inkl. moms, 62 på lager | [elektroshoppen](https://elektroshoppen.dk/produkt/lipo-batteri-lithium-ion-polymer-batteri-37v-2000mah-med-jst-phr-2-stik-lp803860/) |
| Fuel gauge | Adafruit MAX17048 (STEMMA QT) | Kiwi Electronics (NL) | 53 kr | 5,69 EUR ekskl. moms, 39 på lager | [kiwi](https://www.kiwi-electronics.com/en/adafruit-max17048-lipoly-liion-fuel-gauge-battery-monitor-11061) |
| Knapper | Pushbutton 6 mm, 20 stk. | Kiwi Electronics (NL) | 19 kr | 1,99 EUR ekskl. moms, 179 på lager | [kiwi](https://www.kiwi-electronics.com/en/pushbutton-6mm-20-pack-404) |
| Buzzer | Piezo-buzzer | Kiwi Electronics (NL) | 12 kr | 1,29 EUR ekskl. moms, 37 på lager | [kiwi](https://www.kiwi-electronics.com/en/piezo-buzzer-565) |
| Kabler | 2× STEMMA QT / Qwiic til hanben, 150 mm | Kiwi Electronics (NL) | 18 kr | 0,95 EUR ekskl. moms pr. stk., 60 på lager | [kiwi](https://www.kiwi-electronics.com/en/stemma-qt-qwiic-jst-sh-4-pin-to-premium-male-headers-cable-150mm-long-10386) |
| Breadboard | 400 punkter, half-size | Kiwi Electronics (NL) | 28 kr | 2,99 EUR ekskl. moms, 24 på lager | [kiwi](https://www.kiwi-electronics.com/en/400pt-half-size-breadboard-clear-3007) |
| Debugger | Raspberry Pi Debug Probe (CMSIS-DAP) | Kiwi Electronics (NL) | 102 kr | 10,89 EUR ekskl. moms, 86 på lager | [kiwi](https://www.kiwi-electronics.com/en/raspberry-pi-debug-probe-11345) |
| USB-C | Adafruit USB-C breakout, downstream | Kiwi Electronics (NL) | 27 kr | 2,89 EUR ekskl. moms, 67 på lager | [kiwi](https://www.kiwi-electronics.com/en/adafruit-usb-c-breakout-board-downstream-connection-4312) |

| Sum | Pris |
| --- | --- |
| Kernedele, fra board til og med breadboard | 1.565 kr |
| Samme plus debugger og USB-C-breakout | 1.694 kr |
| Ikke med | Fragt fra to-tre butikker, GNSS-antenne, kabinet-dele og filament |

Anbefalet første ordre er rækken ovenfor, altså **1.694 kr** plus fragt og antenne. Debuggeren er med, fordi Zephyr-arbejdet bliver trægt uden SWD.

### Valgfrit i samme runde

| Del | Valg | Butik | Pris | Verificeret | Link |
| --- | --- | --- | --- | --- | --- |
| microSD | Adafruit MicroSD breakout+ | Kiwi | 68 kr | 7,29 EUR ekskl. moms, 7 på lager | [kiwi](https://www.kiwi-electronics.com/en/microsd-card-breakout-boardplus-3206) |
| Afstandsstykker | M2,5 nylon, skruer og standoffs, 380 stk. | Kiwi | 93 kr | 9,99 EUR ekskl. moms, 33 på lager | [kiwi](https://www.kiwi-electronics.com/en/m2-5-screw-and-stand-off-set-black-nylon-380-pieces-10252) |

Med de to valgfrie linjer oven i debugger og USB-C er summen **1.855 kr**. microSD er ikke nødvendig for v1. Afstandsstykker er rare på breadboardet og i fit-testen, men kabinettet bruger egne bosser.

### Skal med, men prisen er ikke i tabellen

- **GNSS-antenne.** SparkFun MAX-M10S-breakoutet har SMA og ingen chip-antenne. En lille aktiv eller passiv patch (omkring 25 × 25 mm) med kort SMA-kabel passer til lommen i kabinettet. Vælg en antenne til 3,3 V hvis den er aktiv, og tjek at den dækker GPS L1 / Galileo E1. Prisen var ikke en del af 29. oktober-tjekket.
- **Kabinet-forbrug.** 2 mm silikonesnor, M3-varmeindsatser, rustfri M3-skruer, 1 mm klar polycarbonat til vinduet, PETG eller ASA. Se [../enclosure/README.md](../enclosure/README.md). Priserne blev ikke genverificeret 29. oktober. En tidligere liste havde blandt andet silikonesnor 2 mm hos Carsten Holm (15,44 kr) og 1 mm polycarbonat hos Holmegaard Plast (fra 100 kr, skåret). Tjek UV-bestandig polycarbonat hvis vinduet skal ligge i sol.

### At holde øje med

- Antratek.dk havde MAX-M10S til 280 kr, udsolgt 29. oktober 2026: [antratek.dk](https://www.antratek.dk/gnss-receiver-breakout-max-m10s-qwiic).
- Opencircuit har gratis fragt fra 150 EUR. Display plus GNSS var 134 EUR den dag, så en lille ekstra vare kan udløse fri fragt.
- Budgetspor: L76K i stedet for MAX-M10S (107 kr hos Kiwi) bringer kernedelene ned på **1.166 kr**. Driftstiden bliver kortere. Link: [L76K](https://www.kiwi-electronics.com/en/l76k-multi-gnss-module-with-gps-bds-and-qzss-support-20602).
- E-paper som display-alternativ: Adafruit 2,9" gråtone FeatherWing, 261 kr hos Opencircuit. Ikke anbefalet. [opencircuit](https://opencircuit.dk/product/adafruit-2.9-inch-grayscale-eink-epaper).

**JST-polaritet.** Mål plus og minus på Elektroshoppens stik før det sættes i Featheren. Omvendt polaritet ødelægger laderen.

## Andre boards (sammenligning, samme dag)

| Board | Pris | Link |
| --- | --- | --- |
| Feather nRF52840 Express | 215 kr, Kiwi | [kiwi](https://www.kiwi-electronics.com/en/adafruit-feather-nrf52840-express-4259) |
| Seeed XIAO nRF52840 | 89 kr, Kiwi | [kiwi](https://www.kiwi-electronics.com/en/seeed-studio-xiao-nrf52840-11041) |

## Alternativ: Seeed XIAO-listen

Denne liste er den tidligere, billigere stykliste. Den er beholdt som alternativ, ikke som det der skal bestilles. Priserne er grovere og er ikke alle genverificeret 29. oktober. Den anbefalede kolonne ovenfor vinder, når de to siger noget forskelligt.

| Del | Valg | Note fra den tidligere liste |
| --- | --- | --- |
| MCU | Seeed XIAO nRF52840 | RS Danmark 112,76 kr. Seeed direkte 9,99 USD. Sense-udgaven 15,90 USD |
| MCU, større | Feather nRF52840 Express | Kiwi 22,99 EUR ekskl. moms |
| GNSS, dyr | SparkFun MAX-M10S | 45,95 USD. Ca. 7,5–10 mA i den gamle note |
| GNSS, billig | Seeed L76K til XIAO | 11,99 USD. Ca. 29–41 mA i den gamle note |
| Display | Sharp 2,7" hos Opencircuit | 65,90 EUR i den gamle note (66,40 EUR i oktober-tjekket) |
| Display, lille | Sharp 1,3" | 24,95 USD hos Adafruit |
| Display, billigt | Waveshare 2,9" e-paper | 18,90 EUR hos Welectron |
| Batteri | LP103450 2000 mAh hos Elektroshoppen | 73,95 kr. Andet mål end LP803860. Polaritet skal stadig måles |
| Batteri | Let Elektronik 2000 mAh | 125 kr |
| Barometer | Adafruit BMP390 | 10,95 USD, var udsolgt. Unødvendigt på Feather Sense, som har BMP280 |

XIAO-sporet ender et sted omkring 450–600 kr for en minimal opsætning og omkring 1.100–1.250 kr hvis Sharp 2,7" og MAX-M10S beholdes, plus kabinet. GPIO-loftet er grunden til at det ikke er anbefalingen. Se [hardware.md](hardware.md).

## Kabinet-materialer fra den tidligere note

Brug som indkøbsliste, og slå prisen op igen før bestilling:

| Del | Hvor den blev set |
| --- | --- |
| PETG, 3DO, 1 kg | 151,20 kr, [3do.dk](https://3do.dk/petg/505-3do-petg-1kg-transperant.html) |
| ASA, 3DJake, 1 kg | 306 SEK, [3djake.se](https://www.3djake.se/3djake/asa-svart) |
| TPU 95A | omkring 190 kr/kg, ikke verificeret |
| Silikonesnor 2,00 mm | Carsten Holm, 15,44 kr |
| Polycarbonat 1 mm | Holmegaard Plast, fra 100 kr, helst UV-stabil |
| IP67 USB-C-panelstik | Sinolec, omkring 7 GBP, hvis proppen ikke er tæt nok |
| Varmeindsatser M3 og rustfri M3×8 eller M3×10 | byggemarked eller elektronik-gros |

Printeren er en Bambu Lab P1S. Bambu PETG Basic og Bambu ASA er de profiler kabinet-noten tager udgangspunkt i. Filament fra en anden rulle kan bruges, hvis temperaturen følger producentens datablad.
