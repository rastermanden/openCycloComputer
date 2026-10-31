# ANT+ og hvorfor BLE kommer først

nRF52840-radioen kan ANT. Softwarestakken kan den ikke af sig selv. Stakken og netværksnøglen ejes af Garmin. Det her er status som den blev læst 29. oktober 2026 på Garmins udviklersider. Læs siderne igen før der bruges penge på en licens, og før noget sælges. Tallene herunder er et referat, ikke en aftale.

- [ANT til nRF Connect SDK, licens og priser](https://developer.garmin.com/ant-program/nrf-connect-sdk/)
- [ANT-licensering](https://developer.garmin.com/ant-program/licensing/)

Til privat brug og evaluering er stakken gratis med en evalueringsnøgle. Sælges enheden, kræves en kommerciel licens. Den pris der stod på siden var 0,08 USD pr. enhed, med et minimum på 800 USD pr. halvår. Derudover skal ANT+ Adopter Agreement accepteres.

MIT-licensen på dette repo dækker vores egen kode og mekanik. Den dækker ikke Garmins stak, og en evalueringsnøgle må ikke bare lægges i et offentligt repo.

## Tre veje

1. **Kun BLE.** Næsten alle nye pulsbælter, fart/kadence-sensorer og wattmålere taler både BLE og ANT+. Det er vejen for prototype og for den første udgave der bliver brugt på cyklen. Ingen licens, ingen nøgle, og Zephyr har BLE-centralen.
2. **ANT+ i Zephyr.** Garmins tilføjelse til nRF Connect SDK (`ant-nrfconnect` på GitHub) med `CONFIG_ANT_EVALUATION_KEY` til eget brug. Det kræver at aftalen er accepteret, og at nøglen ikke committes. Først når BLE-sensorerne virker, og kun hvis en konkret sensor ikke findes på BLE.
3. **Ældre nRF5 SDK med SoftDevice S340**, som kan BLE og ANT samtidig. Den virker, men nRF5 SDK er i vedligehold. Den er ikke sporet her.

Adafruits Arduino-core kan ikke ANT+, fordi den er bygget på S140 (kun BLE). En prototype der starter i Arduino, kan ikke få ANT+ bagefter uden at flytte til Zephyr eller nRF5 SDK. Derfor ligger firmware-planen på Zephyr, også selv om de første sensorer er BLE.

## Rækkefølge i projektet

M4 er BLE: puls (Heart Rate Service), fart/kadence (Cycling Speed and Cadence) og watt (Cycling Power). ANT+ står som et notat i samme milepæl, ikke som en implementeringsopgave. Evalueringsnøgle og aftale tages først, når der er en sensor der ikke kan nås på BLE, eller når enheden skal kunne tale med en ældre træner.
