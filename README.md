# Learning-pcb-design

Im learning pcb design - so everything i do in this repo is open source and you are free to use this designs

Dziennik nauki projektowania elektroniki — od schematu, przez layout PCB, po zamówienie, montaż i uruchomienie. Repo służy jednocześnie jako log postępu i portfolio kolejnych projektów.

## Struktura repozytorium

```
Learning-pcb-design/
├── README.md                          ← ten plik
├── LICENSE                            ← Apache 2.0
├── docs/
│   ├── components-reference.md        ← baza wiedzy o komponentach projektu 01 (symbole, footprinty, dostępność do montażu PCBA)
│   └── project-log-template.md        ← szablon wpisu do logu postępu (kopiuj do każdego projektu)
└── projects/
    ├── 01-stm32-mini-devboard/        ← mini płytka dev STM32F411 — też reużywalny "carrier" MCU do testowania modułów 02-05
    ├── 02-nrf24-radio-module/         ← moduł: radio 2.4GHz (nRF24L01+), antena, SPI
    ├── 03-audio-adc-frontend/         ← moduł: wejście audio (jack → PCM1808 → I2S)
    ├── 04-audio-dac-backend/          ← moduł: wyjście audio (I2S → PCM5102A → wzmacniacz → jack)
    ├── 05-power-module/               ← moduł: bateria LiPo, ładowanie USB-C, ochrona, LDO
    └── 06-piano-audio-integration/    ← integracja modułów 02-05 w finalne płytki TX/RX
```

Każdy projekt ma tę samą strukturę wewnętrzną: `README.md` (cel, zakres, BOM, log postępu), `docs/` (plan/architektura, notatki), `hardware/kicad*/` (pliki KiCad). Dzięki temu repo skaluje się bez przebudowy, a każdy projekt jest samodzielnie czytelny — także dla kogoś oglądającego to jako portfolio.

**Wzorzec "carrier + moduły":** od projektu 02 każdy nowy, mniejszy moduł (radio, audio-in, audio-out, zasilanie) projektowany jest bez własnego MCU — podpina się przewodami do płytki z projektu 01, która pełni rolę wielokrotnego użytku platformy testowej. To pozwala uczyć się każdej dziedziny (RF, audio, power) osobno, zweryfikować ją oscyloskopem w izolacji, i dopiero potem łączyć sprawdzone bloki w finalną, złożoną płytkę (projekt integracyjny, np. 06).

Uwaga: `docs/components-reference.md` w repo głównym dotyczy konkretnie projektu 01 — każdy kolejny projekt trzyma własną dokumentację komponentów w swoim `README.md`/`docs/`, żeby nie mieszać BOM-ów różnych projektów w jednym pliku.

## Konwencja logu postępu

Każdy projekt ma w swoim `README.md` sekcję **Log postępu** — krótkie, datowane wpisy (co zrobiłem, co nie zadziałało, czego się nauczyłem). To najcenniejsza część repo z punktu widzenia nauki i najbardziej wiarygodna dla kogoś czytającego portfolio — pokazuje proces, nie tylko efekt końcowy.

## Konwencja commitów (proponowana)

Prosty prefiks + krótki opis, np.:

- `schem: dodaj obwod zasilania LDO`
- `pcb: routing plaszczyzny GND`
- `docs: notatki z bring-up rev A`
- `fix: popraw pull-down na BOOT0`

Nie jest to sztywna zasada — chodzi o czytelną historię, którą łatwo przejrzeć za pół roku.

## Status projektów

| Projekt | Status | Opis |
|---|---|---|
| [01-stm32-mini-devboard](projects/01-stm32-mini-devboard/) | 🟡 w toku — dobór komponentów zakończony, schemat 🟢, pcb layout 🟡  | Minimalna płytka dev ze STM32F411, USB-C, SWD; też carrier testowy dla modułów 02-05 |
| [02-nrf24-radio-module](projects/02-nrf24-radio-module/) | 🟡 w toku — plan gotowy, schemat do zrobienia | Moduł radiowy nRF24L01+ (bare chip), własna antena, test punkty na SPI |
| [03-audio-adc-frontend](projects/03-audio-adc-frontend/) | 🟡 w toku — plan gotowy, schemat do zrobienia | Wejście audio: jack 3.5mm → PCM1808 (ADC) → I2S |
| [04-audio-dac-backend](projects/04-audio-dac-backend/) | 🟡 w toku — plan gotowy, schemat do zrobienia | Wyjście audio: I2S → PCM5102A (DAC) → NS4160 (wzmacniacz) → jack 3.5mm |
| [05-power-module](projects/05-power-module/) | 🟡 w toku — plan gotowy, schemat do zrobienia | Bateria LiPo + ładowanie USB-C + ochrona (DW01A) + LDO 3.3V |
| [06-piano-audio-integration](projects/06-piano-audio-integration/) | 🟡 w toku — architektura i BOM gotowe, czeka na moduły 02-05 | Integracja sprawdzonych modułów w finalne płytki TX/RX do cichej gry na pianinie w nocy |
