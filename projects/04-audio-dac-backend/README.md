# 04 — Wyjście audio: DAC + wzmacniacz słuchawkowy (samodzielna sesja nauki audio-out)

Status: 🟡 w toku — plan gotowy, schemat do zrobienia

Trzeci z modułów wydzielonych z [projektu integracyjnego 06](../06-piano-audio-integration/). Lustrzane odbicie modułu 03: **droga sygnału od cyfrowego I2S do dźwięku w słuchawkach.**

## Zakres

- Złącze/pady I2S (BCK, LRCK, DIN, 3V3, GND) — **do podpięcia do płytki STM32 z projektu 01**, tak jak w module 03
- **PCM5102A** — stereo DAC 24-bit, wejście I2S, wyjście analogowe
- **NS4160** — wzmacniacz słuchawkowy, steruje bezpośrednio słuchawkami
- Gniazdo **3.5mm TRS** na wyjściu (do dowolnych przewodowych słuchawek, w tym Twojej przejściówki 6.3mm)

## Test punkty pod oscyloskop

- **BCK, LRCK, DIN** wchodzące do PCM5102A — potwierdzenie, że MCU faktycznie wysyła poprawną ramkę I2S.
- **Wyjście analogowe PCM5102A, przed wzmacniaczem** — zobacz zrekonstruowany sygnał analogowy.
- **Wyjście NS4160, po wzmacniaczu** (tuż przed gniazdem 3.5mm) — porównaj z sygnałem przed wzmacniaczem, zobacz wzmocnienie i sprawdź, czy nie ma zniekształceń (clipping, szum).

Połącz to z modułem 03 na stole (bez radia pośrodku) — wejście audio → I2S → wyjście audio → DAC/wzmacniacz — i porównaj sygnał na wejściu jacka modułu 03 z sygnałem na wyjściu jacka modułu 04 na dwóch kanałach oscyloskopu jednocześnie. To pełny test łańcucha audio bez zmiennej "czy radio też działa poprawnie" — dobra kolejność debugowania.

## BOM

| Komponent | Część | LCSC/JLCPCB | Uwagi |
|---|---|---|---|
| DAC | PCM5102APWR | `C107671` | Stereo, 24-bit, I2S, TSSOP-20 |
| Wzmacniacz słuchawkowy | NS4160 | `C219017` | Stereo headphone driver |
| Gniazdo 3.5mm TRS | PJ-3537S-SMT | `C2689709` | Ten sam co w module 03 |
| Pady testowe | `TestPoint:TestPoint_Pad_D1.0mm` | — | Na BCK/LRCK/DIN + wyjście DAC + wyjście wzmacniacza |

## Struktura folderu

```
04-audio-dac-backend/
├── README.md               ← pełny plan modułu (ten plik zawiera wszystko: zakres, BOM, test punkty)
├── docs/                   ← na przyszłość: datasheety, notatki z bring-up, zdjęcia
└── hardware/
    └── kicad/
```

## Log postępu

### 2026-08-24 — wydzielenie modułu z projektu integracyjnego

**Co zrobiłem:**
- Rozbiłem "wireless-piano-audio-link" na moduły — ten to czyste wyjście audio: I2S → PCM5102A → NS4160 → jack, testowane przez podpięcie do carriera STM32 z projektu 01
- Zaplanowałem test punkty na liniach I2S wejściowych oraz na sygnale analogowym przed/po wzmacniaczu

**Następny krok:**
- Schemat w KiCad
- Zaplanować test "moduł 03 + moduł 04 na stole" jako weryfikację całego łańcucha audio przed dodaniem radia
