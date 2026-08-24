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
- Zebrałem dokumentację i potwierdziłem dostępność symboli/footprintów dla: STM32F411CEU6, AP2112K-3.3, złącze USB-C, złącze SWD, rezonator 8MHz (odłożony do Rev B)
- Założyłem strukturę repozytorium

**Co nie zadziałało / problemy:**
- —

**Czego się nauczyłem:**
- Dla większości popularnych komponentów nie trzeba rysować footprintów od zera — warto najpierw sprawdzić bibliotekę wbudowaną KiCad, potem SnapMagic/Ultra Librarian, dopiero na końcu rysować ręcznie
- USB-C wymaga rezystorów 5.1kΩ pull-down na CC1/CC2, inaczej port może nie podać zasilania

**Następny krok:**
- Zweryfikować pobrane/wbudowane symbole i footprinty 1:1 z datasheetami
- Zbudować schemat w KiCad (zasilanie → MCU → peryferia → złącza)

### 2026-08-24 — dobór komponentów pod montaż PCBA (JLCPCB)

**Co zrobiłem:**
- Sprawdziłem dostępność każdego komponentu w katalogu montażowym JLCPCB (LCSC) — bo docelowo płytka ma być zamawiana jako gotowo złożona (PCBA), a nie lutowana ręcznie
- Znalazłem konkretne numery LCSC dla MCU (`C60420`), LDO (`C51118`), złącza USB-C (`C2987385`), rządka pinów pod SWD/GPIO (`C2977586`), tact switcha (`C66637`) — szczegóły w `../../docs/components-reference.md`

**Co nie zadziałało / problemy:**
- Pierwotna rekomendacja złącza SWD (box header 2×5 1.27mm) okazała się mieć status "Extended" i zerowy aktualny stan magazynowy w JLCPCB — zmieniłem na prosty rządek 2.54mm ciachany z taśmy, dużo lepiej dostępny

**Czego się nauczyłem:**
- **Poprawka błędu:** oznaczenie `STM32F411CEU6` to obudowa **UFQFPN-48** (QFN, pady na spodzie + exposed pad), nie LQFP48 jak wcześniej założyłem — sprawdź to zawsze na karcie części u dostawcy, nie tylko po "podobieństwie" do innych projektów
- Footprint złącza USB-C jest specyficzny dla konkretnego producenta/modelu — nie ma jednego uniwersalnego footprintu na "USB-C 6-pin", trzeba dobrać dokładnie pod zamówioną część
- JLCPCB dzieli komponenty na Basic/Preferred/Extended — to wpływa i na koszt (opłata za feeder), i na ryzyko braku w magazynie; warto to sprawdzać przy każdym doborze części, nie tylko w tym projekcie
- Stan magazynowy zmienia się codziennie — numery LCSC to punkt startowy do BOM, ale wymagają weryfikacji tuż przed zamówieniem

**Następny krok:**
- Zbudować schemat w KiCad z tymi konkretnymi komponentami
- Pobrać/zweryfikować footprint złącza USB-C (`C2987385`) dopasowany dokładnie do tej części

### 2026-08-24 — konsolidacja repo (branch `1STM` → `main`)

**Co zrobiłem:**
- Znalazłem już założony projekt KiCad (`1STM.kicad_pro` + puste `.kicad_sch`/`.kicad_pcb`) na osobnym branchu `1STM` i przeniosłem go do docelowej struktury `projects/01-stm32-mini-devboard/hardware/kicad/` na `main`
- Dodałem `.gitignore` pod pliki tymczasowe/backupy KiCad (m.in. `1STM-backups/`, żeby nie śmiecić historii repo dużymi zipami)

**Co nie zadziałało / problemy:**
- —

**Czego się nauczyłem:**
- Trzymanie realnej pracy na osobnym branchu, którego nikt nie widzi z poziomu `main`, psuje repo jako portfolio — ktoś oglądający tylko główną gałąź zobaczy sam README. Warto pracować bezpośrednio na `main` (albo scalać branch roboczy regularnie), skoro celem jest też pokazywanie postępu.

**Następny krok:**
- Zbudować schemat w KiCad (Faza A z planu projektu)
