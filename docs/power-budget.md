# Strømbudget

Alle tal er estimater ud fra datablade og typiske værdier pr. 29. oktober 2026. De skal måles på prototypen og skrives ind her bagefter. Indtil da er det her loftet vi designer efter, ikke et løfte.

Batteri: 2000 mAh. Der regnes med 85 % brugbar kapacitet, så kulde, alder og tab i regulatoren er trukket fra.

```
driftstid (timer) = 2000 mAh × 0,85 / gennemsnitlig strøm (mA)
```

## Skarp Memory LCD (anbefalet)

| Komponent | Optimistisk (mA) | Realistisk (mA) | Pessimistisk (mA) | Antagelse |
| --- | --- | --- | --- | --- |
| GNSS (MAX-M10S) | 6 | 12 | 25 | Strømspare-tilstand / fire systemer kontinuerligt / ingen strømspare |
| nRF52840 + BLE | 0,6 | 1,0 | 2,0 | Puls, fart og telefon. CPU sover mellem opgaverne |
| Board-overhead | 0,3 | 1,0 | 3,0 | Regulator, sensorer på Feather Sense, LED'er |
| Logning, fuel gauge, buzzer | 0,1 | 0,3 | 0,6 | QSPI-skrivning én gang i sekundet, MAX17048, korte bip |
| Display | 0,2 | 0,5 | 1,0 | Opdatering 1 Hz plus VCOM-toggle |
| **I alt** | **7,2** | **14,8** | **31,6** | Gennemsnit, ikke spids |
| **Driftstid** | **236 timer** | **115 timer** | **54 timer** | 1700 mAh delt med strømmen |

115 timer er en lang uge med pendling, eller et brevet, hvis det realistiske scenarie holder. 54 timer rækker stadig til en hård weekend. Det pessimistiske scenarie er "GPS for fuld kraft og intet der sover", ikke en fejltilstand der skal designes hen imod.

## Hvis displayet var e-paper

Samme elektronik, men display-posten skiftet til delvis opdatering hvert sekund: 1 / 2 / 4 mA. Totalerne bliver 8,0 / 16,3 / 34,6 mA, og driftstiden 213 / 104 / 49 timer. E-paper er ikke valgt. Forskellen er reel, men mindre end det GNSS-tilstanden flytter, og opdateringen er dårligere til et sekund-tal.

## Hvad der faktisk flytter tallet

1. GNSS-tilstand. Fra 6 til 25 mA er hele budgettets spænd. Fire konstellationer kontinuerligt er det dyre valg. Én eller to, med u-blox' strømspare-tilstand, er det billige.
2. LED'en på GPS-breakoutet. Den skal fra.
3. Hvor ofte radioen er tændt mod sensorer og telefon.
4. Om Featherens sensorer (IMU, magnetometer, barometer) får lov at sove. Barometeret skal samples, ikke ligge tændt.
5. Displayet. Det er med vilje en lille post.

## Sådan skal det måles

- Breadboard først: USB-strømmåler eller et serie-milliamperemeter på batteribenet, med kendt LiPo eller en laboratorieforsyning sat ind som cellen. Ikke kun USB-strømmen ind i Featheren, for laderen og USB-forbruget blander sig.
- Senere: Nordics Power Profiler Kit, hvis det bliver nødvendigt at se sovetilstandene.
- Skriv de målte tal ind i tabellen her, med dato og firmware-commit, og lad estimaterne stå så man kan se hvad der rykkede sig.

Målepunkter der skal findes, før kabinettet lukkes: GPS slukket og tændt, display 1 Hz, BLE-annonce fra et pulsbælte tilsluttet, QSPI-skrivning, og dyb søvn mellem samples.
