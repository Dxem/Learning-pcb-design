# 05 — Moduł zasilania: bateria LiPo + ładowanie + ochrona (samodzielna sesja nauki power)

Status: 🟡 w toku — plan gotowy, schemat do zrobienia

Czwarty z modułów wydzielonych z [projektu integracyjnego 06](../06-piano-audio-integration/). Ten moduł jest też **najbardziej samodzielnie użyteczny na przyszłość** — to ogólny "power brick" do zasilania batteryjnego dowolnego kolejnego projektu, nie tylko tego.

## Zakres

- Złącze **USB-C** (tylko zasilanie/ładowanie) — reużywasz tę samą część co w projekcie 01
- **TP4056** — ładowarka LiPo
- **DW01A + MOSFET (np. FS8205A)** — obwód ochronny baterii (nadładowanie, nadmierne rozładowanie, zwarcie). **Obowiązkowe, nie opcjonalne** — patrz sekcja bezpieczeństwa w [planie projektu 06](../06-piano-audio-integration/docs/plan-projektu.md#bezpieczeństwo-baterii-lipo-przeczytaj-przed-zamówieniem-ogniwa).
- Złącze baterii LiPo (JST-PH 2-pin, typowy standard dla hobby ogniw)
- **AP2112K-3.3** — LDO, wyjście regulowane 3.3V
- Złącze/pady wyjściowe: VBAT (niereg.), 3V3 (reg.), GND — do zasilania modułów 02/03/04 podczas testów, docelowo do płytek TX/RX w projekcie 06

## Test punkty pod oscyloskop/multimetr

- **VBAT** (napięcie baterii, niereg.) — obserwuj rozładowywanie w czasie, charakterystykę napięcia LiPo pod obciążeniem
- **Wyjście 3V3 (po LDO)** — sprawdź stabilność pod zmiennym obciążeniem (podłącz/odłącz inny moduł i patrz, czy napięcie "siada")
- **Punkt przed/po rezystorze sensu prądu** (jeśli dodasz mały rezystor szeregowy niskiej wartości na ścieżce ładowania lub zasilania) — dodatkowa, opcjonalna lekcja pomiaru prądu na oscyloskopie/multimetrze przez spadek napięcia na znanym rezystorze
- **Piny statusu ładowania z TP4056** (CHRG/STDBY) — zobacz logicznie, kiedy układ raportuje ładowanie vs pełne naładowanie

## BOM

| Komponent | Część | LCSC/JLCPCB | Uwagi |
|---|---|---|---|
| Złącze USB-C | CIKI Type-C-2.0-6Pin | `C2987385` | Ten sam co w projekcie 01 — tylko zasilanie |
| Ładowarka LiPo | TP4056 | `C382139` | Tylko ładowarka |
| Ochrona baterii | DW01A | `C436931` | + MOSFET (np. FS8205A) — obowiązkowe |
| LDO 3.3V | AP2112K-3.3TRG1 | `C51118` | Ten sam co w projekcie 01 |
| Złącze baterii | JST-PH 2-pin | do zweryfikowania w JLCPCB parts | Standard dla hobby ogniw LiPo |
| Pady testowe | `TestPoint:TestPoint_Pad_D1.0mm` | — | VBAT, 3V3, GND, CHRG/STDBY |

## Struktura folderu

```
05-power-module/
├── README.md               ← pełny plan modułu (ten plik zawiera wszystko: zakres, BOM, test punkty)
├── docs/                   ← na przyszłość: datasheety, notatki z bring-up, zdjęcia
└── hardware/
    └── kicad/
```

## Log postępu

### 2026-08-24 — wydzielenie modułu z projektu integracyjnego

**Co zrobiłem:**
- Rozbiłem "wireless-piano-audio-link" na moduły — ten to zasilanie: USB-C ładowanie → TP4056 → ochrona DW01A → LDO 3.3V, reużywalny w przyszłych projektach
- Zaplanowałem test punkty na VBAT, 3V3, statusie ładowania

**Następny krok:**
- Zweryfikować konkretne złącze baterii LiPo (JST-PH) w katalogu JLCPCB
- Schemat w KiCad
