# 01 — Mini płytka rozwojowa STM32F411

Status: 🟡 w toku — zbieranie dokumentacji komponentów (etap: przygotowanie do schematu)

Pierwszy projekt w tym repo. Cel: przejść cały proces projektowania elektroniki — schemat → PCB → produkcja → montaż → uruchomienie — na małej, tanio produkowalnej płytce.

**Dodatkowa rola od projektu 02:** ta płytka służy też jako wielokrotnego użytku "carrier" MCU do testowania mniejszych modułów ([02-nrf24-radio-module](../02-nrf24-radio-module/), [03-audio-adc-frontend](../03-audio-adc-frontend/), [04-audio-dac-backend](../04-audio-dac-backend/)) — podpinasz je przewodami do jej złączy GPIO/SPI/I2S zamiast projektować osobny MCU na każdej mniejszej płytce. Zamów przynajmniej 2 sztuki w PCBA, jeśli chcesz testować link radiowy (potrzebujesz dwóch niezależnych carrierów).

## Zakres (v1)

- Zasilanie z USB-C (5V → 3.3V przez LDO)
- MCU: STM32F411CEU6 (**UFQFPN-48**, nie LQFP48 — patrz korekta w logu poniżej)
- Programowanie/debug: złącze SWD jako prosty rządek 2.54mm (4-5 pin), pod montaż PCBA zamiast box headera
- BOOT0 na pull-downie (bez przełącznika na v1)
- Montaż: docelowo **zamawiany PCBA w JLCPCB** (nie ręczne lutowanie) — patrz baza komponentów po numery LCSC
- 1 LED użytkownika + 1 LED zasilania
- Przycisk RESET + przycisk User
- Bez kryształu HSE na v1 (wewnętrzny RC MCU) — kryształ do Rev B
- Wyprowadzone GPIO na goldpinach

Pełny opis etapów pracy, checklisty i zasady projektowe: patrz [`docs/plan-projektu.md`](docs/plan-projektu.md) oraz [`../../docs/components-reference.md`](../../docs/components-reference.md) w repo głównym.

Projekt KiCad już założony: `hardware/kicad/1STM.kicad_pro` (na razie pusty — brak symboli i komponentów na płytce, gotowy do rozpoczęcia Fazy A ze schematem).

## Dokumentacja komponentów

Zebrana w [`../../docs/components-reference.md`](../../docs/components-reference.md) — datasheety, źródła symboli/footprintów, decyzje projektowe dla każdego komponentu.

## Struktura folderu

```
01-stm32-mini-devboard/
├── README.md               ← ten plik
├── docs/
│   └── plan-projektu.md    ← pełny plan: etapy, zasady projektowe, checklisty
└── hardware/
    └── kicad/
        ├── 1STM.kicad_pro
        ├── 1STM.kicad_sch
        ├── 1STM.kicad_pcb
        └── 1STM.kicad_prl
```

## Log postępu

### 2026-08-24 — start projektu, dobór komponentów

**Co zrobiłem:**
- Ustaliłem zakres v1 płytki (patrz wyżej)
- Zebrałem dokumentację i potwierdziłem dostępność symboli/footprintów dla: STM32F411CEU6, złącze USB-C
- Założyłem strukturę repozytorium
- Stworzyłem sekcję zasilania do mcu 
**Co nie zadziałało / problemy:**
- —

**Czego się nauczyłem:**
- Dla większości popularnych komponentów nie trzeba rysować footprintów od zera — warto najpierw sprawdzić bibliotekę wbudowaną KiCad, potem SnapMagic/Ultra Librarian, dopiero na końcu rysować ręcznie
- USB-C wymaga rezystorów 5.1kΩ pull-down na CC1/CC2, inaczej port może nie podać zasilania

**Następny krok:**
- Zweryfikować pobrane/wbudowane symbole i footprinty 1:1 z datasheetami
- Zbudować schemat w KiCad (zasilanie → MCU → peryferia → złącza)