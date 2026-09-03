# 01 — Mini płytka rozwojowa STM32F411

Status: 🟢 Wykonany layout PCB gotowe do zamówienia (etap: przygotowanie do schematu)

Pierwszy projekt w tym repo. Cel: przejść cały proces projektowania elektroniki — schemat → PCB → produkcja → montaż → uruchomienie — na małej, tanio produkowalnej płytce.

**Dodatkowa rola od projektu 02:** ta płytka służy też jako wielokrotnego użytku "carrier" MCU do testowania mniejszych modułów ([02-nrf24-radio-module](../02-nrf24-radio-module/), [03-audio-adc-frontend](../03-audio-adc-frontend/), [04-audio-dac-backend](../04-audio-dac-backend/)) — podpinasz je przewodami do jej złączy GPIO/SPI/I2S zamiast projektować osobny MCU na każdej mniejszej płytce. Zamów przynajmniej 2 sztuki w PCBA, jeśli chcesz testować link radiowy (potrzebujesz dwóch niezależnych carrierów).

## Zakres (v1)

- Zasilanie z USB-C (5V → 3.3V przez LDO)
- MCU: STM32F412CEU6 (UFQFPN-48)
- Programowanie/debug: złącze SWD jako prosty rządek 2.54mm (4-5 pin), pod montaż PCBA zamiast box headera
- BOOT0 na pull-downie (bez przełącznika na v1)
- Montaż: docelowo **zamawiany PCBA w JLCPCB** (nie ręczne lutowanie) — patrz baza komponentów po numery LCSC
- 1 LED użytkownika + 1 LED zasilania
- Przycisk RESET + przycisk User
- Kryształ HSE
- Wyprowadzone GPIO na goldpinach

Pełny opis etapów pracy, checklisty i zasady projektowe: patrz [`docs/plan-projektu.md`](docs/plan-projektu.md) oraz [`../../docs/components-reference.md`](../../docs/components-reference.md) w repo głównym.

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

### 2026-08-25 —  Schemat p. 1 Sekcja zasilania

**Co zrobiłem:**
    - ciąg dalszy zbierania dokumentacji ze strony jlcpcb i doboru komponentów 
    - nauka pracy z dokumentacją - wyszukiwania sekcji w datasheecie któe właściwie zaprezentują rozwiązanie możliwe do zaimplementowania w aplikacji
    - Sekcja zasilania płytki - dokończyłem
**Co nie zadziałało / problemy:**
    - Nie wykorzystywałem jeszcze na tamtym etapie net names i global labels - bardzo przydatne narzędzia 
**Czego się nauczyłem:**
    - Organizacja schematu w sekcje i wykorzystanie kondensatoró decapujących bardzo
**Następny krok:**
    - Połączenie z MCU

    
### 2026-08-26 — Schemat p. 2 MCU

**Co zrobiłem:**
    - Zestaw połaczeń z MCU z sekcji zasilania
    - Wybór komponentów do peryferiów zgodnych z planem projektu
    - Poznawanie alternate functions
**Co nie zadziałało / problemy:**
    -I2C i I2S to dwie inne rzeczy
**Czego się nauczyłem:**
    - Ten sam moduł może realizować dwie funkcje jednocześnie więc jeśli mają ze sobą rozmawiać to lepiej aby były z dwóch innych modułów
    - I2C i I2S to dwie inne rzeczy
**Następny krok:**
    - dokończyć schemat zacząć z pcb

### 2026-08-27 — Schemat p. 3 Peryferia

**Co zrobiłem:**
    - Sekcja peryferiów
    - Optymalizacja netów
    - Poprawki wizualne schematu
    - Dodane diody LED
    - Przyciski     
**Co nie zadziałało / problemy:**
    - Lepiej zmienić diodę na inny kolor niż niebieski niż nie zastosować żadnego rezystora ograniczającego prąd mimo że napięcie odpowiada napięciu pracy diody
**Czego się nauczyłem:**
    - Lepiej zmienić diodę na inny kolor niż niebieski niż nie zastosować żadnego rezystora ograniczającego prąd mimo że napięcie odpowiada napięciu pracy diody
**Następny krok:**
    - PCB Layout

    
### 2026-09-02 — PCB Layout p. 1 Initial Layout

**Co zrobiłem:**
    - initial PCB layout
    - Dodany kryształ HSE
    - Dobór kondensatorów do kryształu
**Co nie zadziałało / problemy:**
    - Pierwsze próby posegregowania komponentów - wymaga doświadczenia aby właściwie podzielić na sekcje lub parę iteracji
**Czego się nauczyłem:**
    - Kryształ może mieć różne Load capacitance w zależności od tego co się zamawia - należy zwrócić uwagę
    - dobór kondensatoró do kryształu
**Następny krok:**
    - dokończyć PCB layout


### 2026-09-03 — PCB Layout p. 2 Layout opcja A

**Co zrobiłem:**
    - pierwsza propozycja pcb layout
    - znikome wykorzystanie warstwy B.Cu - głównie skłąda się z ground plane
**Co nie zadziałało / problemy:**
    - Powinienem lepiej przemyśleć kolejność wykonywanie routingu - do wdrożenia w nastepnej wersji
**Czego się nauczyłem:**
    - Tworzenie obrysu PCB
    - Wylewanie Ground plane
    - Layout ścieżek w usb - c
**Następny krok:**
    - Powtórzyć drugi raz routing z wiedzą którą nabyłem przy tej próbie - zobaczymy co się da poprawić
