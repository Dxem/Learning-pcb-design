# 06 — Integracja: bezprzewodowy link audio TX/RX dla pianina

Status: 🟡 w toku — architektura i BOM gotowe; **czeka na potwierdzenie działania modułów 02-05 osobno**, zanim zaczniemy łączyć je w finalne płytki TX/RX

Cel: cicha gra na pianinie w nocy przez słuchawki bezprzewodowe z niskim opóźnieniem — bez polegania na Bluetooth (AirPods nie nadają się do tego strukturalnie, nawet aptX LL to kompromis). Własny link 2.4GHz (nRF24L01+), gdzie sam projektujesz i nadajnik (TX), i odbiornik (RX) — bez zależności od kodeków komercyjnych słuchawek.

## Ten projekt to synteza czterech mniejszych modułów

Zamiast projektować od razu dwie złożone, wieloukładowe płytki, rozbiłem to na osobne sesje nauki — każdy moduł testowalny samodzielnie, podpięty do carriera STM32 z [projektu 01](../01-stm32-mini-devboard/), zanim cokolwiek trafi na wspólną płytkę:

| Moduł | Czego uczy | Status |
|---|---|---|
| [02-nrf24-radio-module](../02-nrf24-radio-module/) | RF: antena, SPI, pomiar opóźnienia | 🟡 plan gotowy |
| [03-audio-adc-frontend](../03-audio-adc-frontend/) | Analog audio-in + ADC/I2S | 🟡 plan gotowy |
| [04-audio-dac-backend](../04-audio-dac-backend/) | I2S/DAC + wzmacniacz słuchawkowy | 🟡 plan gotowy |
| [05-power-module](../05-power-module/) | Bateria LiPo, ładowanie, ochrona | 🟡 plan gotowy |

**Kolejność pracy:** zbuduj i przetestuj każdy moduł osobno (każdy podpięty do płytki STM32 z projektu 01) → dopiero gdy wszystkie cztery działają samodzielnie i potwierdzone oscyloskopem → złóż TX (moduł 02 + 03 + 05 + MCU) i RX (moduł 02 + 04 + 05 + MCU) na dwóch finalnych płytkach.

Pełny opis architektury systemu, budżetu przepustowości i pełny BOM: [`docs/plan-projektu.md`](docs/plan-projektu.md) — te decyzje (dlaczego nie Bluetooth, kompromis jakości audio, bezpieczeństwo baterii) dotyczą całości i nie są powtarzane osobno w każdym module.

## Zakres finalny (v1)

- **TX** (przy pianinie): jack 3.5mm → PCM1808 (ADC) → STM32F411 → nRF24L01+ (bare chip, własna antena). Zasilanie z USB-C, bez baterii.
- **RX** (przy Tobie): nRF24L01+ → STM32F411 → PCM5102A (DAC) → NS4160 (wzmacniacz) → jack 3.5mm. Bateria LiPo + ładowanie USB-C.
- Audio v1: mono, 16-bit, ~22-32kHz (kompromis pod przepustowość nRF24L01+, ~350-512kbps) — stereo/wyższa jakość to Rev B.
- USB-C na obu płytkach: wyłącznie zasilanie/ładowanie, audio idzie osobnym torem analogowym przez jack 3.5mm.

## Dlaczego nie kupić gotowych słuchawek Bluetooth

- AirPods: tylko AAC/SBC, 100-180ms+ opóźnienia — twardy limit sprzętowy, nie do obejścia żadnym nadajnikiem
- aptX Low Latency (np. ATH-TWX7): ~30-40ms, ale drogie i nadal cudzy kodek
- Własny link 2.4GHz: potencjalnie pojedyncze-kilkanaście ms, tani (moduły ~1-2$), pełna kontrola nad protokołem

Szczegóły w [`docs/plan-projektu.md`](docs/plan-projektu.md).

## Struktura folderu

```
06-piano-audio-integration/
├── README.md                  ← ten plik
├── docs/
│   └── plan-projektu.md       ← architektura, BOM, etapy, bezpieczeństwo baterii
└── hardware/
    ├── kicad-tx/               ← finalny projekt KiCad nadajnika (po zweryfikowaniu modułów)
    └── kicad-rx/               ← finalny projekt KiCad odbiornika (po zweryfikowaniu modułów)
```

## Log postępu

### 2026-08-24 — zmiana trajektorii, architektura i BOM

**Co zrobiłem:**
- Przeanalizowałem opóźnienie AirPods (100-180ms+, tylko AAC/SBC, brak aptX) — stwierdziłem, że to strukturalnie wyklucza granie w czasie rzeczywistym niezależnie od jakości nadajnika
- Zdecydowałem o własnym linku 2.4GHz (nRF24L01+) zamiast Bluetooth — taniej, więcej kontroli, realny pierwszy projekt RF
- Zaprojektowałem architekturę TX/RX (ADC PCM1808 → MCU → radio, i odwrotnie po stronie RX z DAC PCM5102A + wzmacniaczem NS4160)
- Ustaliłem, że USB-C na obu płytkach to tylko zasilanie/ładowanie (nie pełny USB Host + UAC2)
- Zebrałem BOM z numerami LCSC/JLCPCB pod PCBA
- Zidentyfikowałem budżet przepustowości nRF24L01+ (32B/pakiet, ~2Mbps max) jako twarde ograniczenie — v1 celuje w mono 16-bit ~22-32kHz

**Czego się nauczyłem:**
- Kodek słuchawek (nie sam nadajnik) jest tu wąskim gardłem opóźnienia — AirPods mają twardy limit sprzętowy niezależny od tego, jak dobry zbudujesz nadajnik
- nRF24L01+ ma twardy limit 32 bajty/pakiet — CD-quality stereo audio praktycznie nie mieści się z zapasem na niezawodność
- Domyślny Auto-ACK/Auto-Retransmit w nRF24L01+ jest zły do audio real-time (powoduje skoki opóźnienia)
- Bare TP4056 to tylko ładowarka, nie ochrona baterii — obowiązkowy osobny obwód ochronny (DW01A + MOSFET)

**Następny krok:**
- —

### 2026-08-24 — rozbicie na moduły + test punkty pod oscyloskop

**Co zrobiłem:**
- Na Twoją prośbę rozbiłem projekt na cztery mniejsze, samodzielnie testowalne moduły (02-05) — każdy to osobna sesja nauki jednej dziedziny (RF, audio-in, audio-out, power), zamiast projektowania od razu dwóch złożonych płytek
- Każdy moduł podpina się do już zbudowanej płytki STM32 z projektu 01 zamiast duplikować MCU na każdej płytce
- Dodałem pady testowe pod oscyloskop na kluczowych sygnałach w każdym module (SPI, I2S, węzły analogowe, zasilanie)

**Co nie zadziałało / problemy:**
- —

**Czego się nauczyłem:**
- Sygnał radiowy 2.4GHz nie nadaje się do bezpośredniego podglądu na typowym hobbystycznym oscyloskopie (pojemność sondy rozstraja antenę, za wąskie pasmo) — ale cyfrowa strona protokołu (SPI) i pomiar opóźnienia GPIO-to-GPIO są w pełni dostępne i to one faktycznie odpowiadają na pytanie o użyteczność linku
- Rozbicie złożonego projektu na mniejsze, niezależnie weryfikowalne moduły znacząco obniża ryzyko utknięcia — każdy moduł można debugować w izolacji, zanim skumulują się niewiadome z kilku podsystemów naraz

**Następny krok:**
- Zbudować i przetestować moduły 02-05 osobno (patrz ich README)
- Wrócić tutaj dopiero po potwierdzeniu, że wszystkie cztery działają — wtedy integracja TX/RX
