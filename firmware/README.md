# Firmware

Der er ingen applikation i mappen endnu. Sporet er Zephyr via nRF Connect SDK, ikke Arduino-coren. Arduino kan bruges en aften på breadboardet, men den kan ikke bære ANT+ senere, og lavstrøms-arbejdet bliver sværere. Baggrunden står i [../docs/ant-plus.md](../docs/ant-plus.md).

## Board

| | |
| --- | --- |
| Board | Adafruit Feather nRF52840 Sense |
| Zephyr-target | `adafruit_feather_nrf52840/nrf52840/sense` |
| UF2, uden debugger | `adafruit_feather_nrf52840/nrf52840/sense/uf2` |
| SoC | nRF52840, Cortex-M4F, 1 MB flash, 256 KB RAM |
| Radio | BLE i første omgang. ANT kun med Garmins stak, se dokumentationen |
| Ekstern flash | 2 MB QSPI, til LittleFS og turfiler |

Navnet med skråstreger er Zephyrs nuværende board-kvalifikator. Ældre NCS-versioner brugte `adafruit_feather_nrf52840` og et Kconfig-symbol for Sense. Slå det op med `west boards | grep feather_nrf52840` i den version der installeres, og ret tabellen her hvis navnet er et andet. Pin-mux ligger i boardets devicetree. Opfind ikke en lokal pin-tabel før den første overlay er skrevet og prøvet.

## Værktøj

- nRF Connect SDK via nordic's toolchain manager, eller en vest-manifest der peger på en fast NCS-revision. Revisionen skrives ind her, når den er valgt. SDK'et vendres ikke ind i dette repo.
- `west init` / `west update` i en mappe ved siden af repoet, ikke inde i det.
- Debug: Raspberry Pi Debug Probe (CMSIS-DAP) på SWD-padsene på undersiden af Featheren. pyOCD eller OpenOCD, som NCS' `west flash` forventer.
- UF2 er fint til blink og til de første display-forsøg. Strømmåling og breakpoint kræver sonden.
- Sprog: C, med devicetree-overlays til Sharp, GNSS og knapper. C++ kun hvis et konkret bibliotek tvinger det.

Foreslået layout, når den første app oprettes:

```
firmware/
  app/            # én Zephyr-app indtil den skal deles
    src/
    boards/       # overlay for adafruit_feather_nrf52840 sense
    prj.conf
  README.md
```

## Rækkefølge

1. Blink på Sense-boardet, først UF2, så SWD.
2. Sharp LS027B7DH01 på SPI. Hele framen er 13,5 KB og skal ligge i RAM. Opdatering 1 Hz, plus den EXTCOMIN/VCOM-toggle displayet kræver. Adafruit-breakoutet har niveau-skift og 5 V-boost, så logikken kan være 3,3 V.
3. MAX-M10S på I²C (u-blox-adressen er 0x42, indtil den ændres). UBX frem for NMEA, så parseren ikke æder RAM. Første fix, så tid, position og fart på displayet. LED'en på breakoutet slukkes i samme omgang.
4. Knapper: start, stop, omgang, side. Interrupts, ikke polling i et travlt loop.
5. MAX17048 på I²C, adresse 0x36 på Adafruit-boardet. Procent på skærmen.
6. Turens tilstandsmaskine, derefter FIT til LittleFS på QSPI. GPX kan vente, eller laves på telefonen.
7. BLE-central: Heart Rate, Cycling Speed and Cadence, Cycling Power. Genforbindelse når en sensor forsvinder bag en bil.
8. Først derefter: søvn mellem samples, og de målinger [strømbudgettet](../docs/power-budget.md) mangler.

ANT+ er ikke på listen. Se M4 i [køreplanen](../docs/roadmap.md).

## Det der ikke skal ind endnu

- Eget HAL-lag oven på Zephyr.
- En telefon-app. Filen skal kunne hentes med det Zephyr allerede kan (USB mass storage eller en simpel BLE-overførsel), før der tegnes en protokol.
- OTA. Planen skrives når basen kører, den bygges ikke først.
