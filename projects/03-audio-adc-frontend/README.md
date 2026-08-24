# 03 — Wejście audio: kondycjonowanie + ADC (samodzielna sesja nauki audio-in)

Status: 🟡 w toku — plan gotowy, schemat do zrobienia

Drugi z modułów wydzielonych z [projektu integracyjnego 06](../06-piano-audio-integration/). Ten moduł: **droga sygnału od jacka 3.5mm do cyfrowego strumienia I2S.** Bez radia, bez baterii — czysto analog-front-end + konwersja A/C.

## Zakres

- Gniazdo **3.5mm TRS** (wejście z przejściówki 6.3mm z pianina)
- Kondensatory sprzęgające (DC blocking) na wejściu
- Dzielnik/dopasowanie poziomu — wyjście słuchawkowe pianina może być głośniejsze niż nominalne wejście line-level PCM1808, dobierz dzielnik żeby nie przesterować ADC (sprawdź zakres wejściowy w datasheecie PCM1808)
- **PCM1808** — stereo ADC 24-bit, wyjście I2S
- Złącze/pady I2S (BCK, LRCK, DOUT, SCK jeśli PCM1808 pracuje jako slave, 3V3, GND) — **do podpięcia do płytki STM32 z projektu 01** (piny SPI2/SPI3 w trybie I2S), zamiast własnego MCU na tej płytce

## Test punkty pod oscyloskop

To jest moduł, w którym oscyloskop daje najwięcej satysfakcji — sygnały są w paśmie akustycznym (do ~20kHz), więc każdy oscyloskop je pokaże bez problemu:

- **Sygnał analogowy przed kondensatorem sprzęgającym** (surowe wyjście z pianina) — zobacz realny kształt fali z instrumentu.
- **Sygnał analogowy po dzielniku/dopasowaniu poziomu, tuż przed wejściem ADC** — porównaj amplitudę, sprawdź czy nie ucinasz szczytów (clipping).
- **BCK (bit clock), LRCK (word select), DOUT** z PCM1808 — zobacz cyfrową stronę: jak wygląda ramka I2S, jak zmienia się DOUT względem LRCK. To bezpośrednie potwierdzenie, że ADC faktycznie koduje to, co widzisz na wejściu analogowym.

Świetne ćwiczenie: graj pojedynczy dźwięk na pianinie i porównaj kształt fali analogowej (kanał 1 oscyloskopu) z aktywnością na DOUT (kanał 2) — namacalny most między światem analogowym a cyfrowym.

## BOM

| Komponent | Część | LCSC/JLCPCB | Uwagi |
|---|---|---|---|
| ADC | PCM1808PWR | `C55513` | Stereo, 24-bit, I2S, TSSOP-14 |
| Gniazdo 3.5mm TRS | PJ-3537S-SMT | `C2689709` | Zweryfikuj liczbę styków (TRS = 3-biegunowe) |
| Kondensatory sprzęgające, dzielnik | 0603 R/C | Basic Parts | Wartości dobierz po zmierzeniu realnego poziomu z pianina |
| Pady testowe | `TestPoint:TestPoint_Pad_D1.0mm` | — | Na wej. analogowym (2 punkty) + BCK/LRCK/DOUT |

## Struktura folderu

```
03-audio-adc-frontend/
├── README.md               ← pełny plan modułu (ten plik zawiera wszystko: zakres, BOM, test punkty)
├── docs/                   ← na przyszłość: datasheety, notatki z bring-up, zdjęcia
└── hardware/
    └── kicad/
```

## Log postępu

### 2026-08-24 — wydzielenie modułu z projektu integracyjnego

**Co zrobiłem:**
- Rozbiłem "wireless-piano-audio-link" na moduły — ten to czyste wejście audio: jack → kondycjonowanie → PCM1808 → I2S, testowane przez podpięcie do carriera STM32 z projektu 01
- Zaplanowałem test punkty na sygnale analogowym (przed/po kondycjonowaniu) i na liniach I2S

**Następny krok:**
- Zmierzyć realny poziom sygnału z wyjścia słuchawkowego pianina multimetrem/oscyloskopem, żeby dobrać dzielnik wejściowy
- Schemat w KiCad
