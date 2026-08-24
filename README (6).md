# Twój pierwszy projekt elektroniczny: mini płytka rozwojowa STM32F4

Cel: przejść **cały proces** projektowania elektroniki — od pomysłu, przez schemat i layout PCB, po zamówienie, montaż i uruchomienie działającej płytki. Narzędzie: **KiCad** teraz, z opcją przeniesienia tego samego projektu do **Altium** za miesiąc jako ćwiczenie porównawcze.

Masz już RPi5 i STM32F4 (tinkering), więc pomijamy teorię podstawową — od razu wchodzimy w praktykę projektowania płytki.

---

## 1. Zakres projektu

Minimalna, samodzielna płytka z mikrokontrolerem STM32F4, zasilana z USB-C, programowalna przez SWD. Nic ponad to, co niezbędne — celem jest przejście całego procesu, a nie zbudowanie skomplikowanego urządzenia.

**Funkcje płytki:**
- Zasilanie z USB-C (5V → 3.3V przez LDO)
- MCU: STM32F411CEU6 (**UFQFPN-48** 7x7mm — nie LQFP48, patrz `../../../docs/components-reference.md` — popularny, tani, dużo przykładów — "black pill" jest na nim oparty)
- Programowanie/debug: złącze SWD jako prosty 4-5 pin rządek 2.54mm (SWDIO, SWCLK, GND, 3V3, opcjonalnie NRST) — wycięty z taśmy 1x40, patrz baza komponentów (zamiast box headera 2x5 1.27mm, który okazał się słabo dostępny do montażu w JLCPCB)
- BOOT0 na przełączniku/jumperze (do wejścia w bootloader USB DFU)
- 1 LED użytkownika + 1 LED zasilania
- 1 przycisk RESET + 1 przycisk User
- Rezonator HSE 8MHz (opcjonalnie — F411 ma też wewnętrzny RC, można pominąć na v1 dla uproszczenia)
- Wyprowadzone GPIO na złączach goldpin (2x rządek, żeby można było wpinać płytkę stykową/przewody)

To celowo blisko "Blue Pill / Black Pill" — sprawdzony, dobrze udokumentowany układ, minimalne ryzyko, że coś nie zadziała z powodów, których nie rozumiesz.

---

## 2. Etapy pracy (checklist całego procesu)

### Faza A — Schemat (KiCad Schematic Editor)
1. Załóż nowy projekt w KiCad.
2. Zbuduj schemat blokowo: zasilanie → MCU → peryferia (LED/przyciski) → złącza (SWD, GPIO).
3. Dobierz konkretne komponenty:
   - LDO 3.3V: np. **AP2112K-3.3** (SOT-23-5, do 600mA, tani, powszechny w SMD hobby)
   - MCU: **STM32F411CEU6** (sprawdź dostępność na LCSC/Mouser)
   - Kondensatory odsprzęgające: 100nF przy każdej parze VDD/VSS MCU (F411 ma kilka par) + 1-4.7µF na wejściu/wyjściu LDO
   - Rezystory pull-up/pull-down: BOOT0 (pull-down 10k), NRST (pull-up 10k + kondensator 100nF), przyciski (pull-up wewnętrzny w MCU wystarczy, albo zewnętrzny 10k)
4. Przypisz footprinty (Footprint Assignment) — SOT-23-5, **QFN-48 (UFQFPN-48, z exposed pad)**, 0603 dla R/C.
5. Uruchom **ERC** (Electrical Rules Check) i wyczyść wszystkie błędy/ostrzeżenia.

### Faza B — Layout PCB (KiCad PCB Editor)
1. Zdefiniuj obrys płytki (Board Outline) — np. 40x25mm, mieści się w najtańszym progu produkcji.
2. Rozmieść komponenty: MCU centralnie, LDO blisko złącza USB-C, kondensatory odsprzęgające jak najbliżej pinów zasilania MCU.
3. Warstwy: 2-layer (top/bottom) w zupełności wystarczy na start. Górna warstwa = sygnały + częściowo GND, dolna = solidna płaszczyzna GND (pour).
4. Routing: zasilanie grubszymi ścieżkami (np. 0.4-0.5mm dla 3.3V), sygnały cyfrowe 0.2-0.25mm.
5. Dodaj plane GND (zalewkę) na obu warstwach, połącz przelotkami (via stitching).
6. Uruchom **DRC** (Design Rules Check) dopasowany do możliwości producenta (patrz niżej) i wyczyść wszystkie błędy.
7. Sprawdź silkscreen — opisy nie mogą nachodzić na pola lutownicze.
8. Dodaj otwory montażowe (opcjonalnie), tekst z nazwą/wersją projektu.

### Faza C — Pliki produkcyjne
1. Wygeneruj **Gerbery** (RS-274X) + pliki wierceń (Excellon).
2. Wygeneruj **BOM** (listę komponentów, z numerami LCSC) i **CPL/Pick&Place** — obowiązkowe przy zamawianiu montażu, nie opcjonalne.
3. Zweryfikuj Gerbery w przeglądarce online producenta przed wysłaniem zamówienia.

### Faza D — Zamówienie (PCBA — montaż zamawiany, nie ręczny)
- Docelowo zamawiasz **gotowo złożoną płytkę** przez **JLCPCB SMT Assembly** (główny dostawca sourcingu — patrz `../../../docs/components-reference.md` po numery LCSC i kategorie Basic/Preferred/Extended dla każdego komponentu) lub **PCBWay Assembly**.
- To ma sens także dlatego, że MCU jest w obudowie **QFN (UFQFPN-48, exposed pad na spodzie)** — dużo trudniejszej do porządnego ręcznego lutowania niż LQFP, więc montaż maszynowy jest tu wręcz praktyczniejszy niż DIY.
- Przed złożeniem zamówienia PCBA: zweryfikuj aktualny stan magazynowy każdej pozycji BOM na jlcpcb.com — stan zmienia się codziennie.
- Jeśli mimo to chcesz mieć też kilka sztuk gołego PCB do własnego eksperymentowania/lutowania pozostałych, prostszych komponentów (LED, przyciski) ręcznie — zamów dodatkowe sztuki bez montażu przy tym samym zamówieniu (JLCPCB pozwala zamówić np. 5 szt. z PCBA + resztę panelu bez montażu).

### Faza E — Montaż i uruchomienie
1. Kontrola wzrokowa pod lupą/mikroskopem — zwarcia, brak lutu.
2. Test ciągłości multimetrem: GND-GND, brak zwarcia 3V3-GND.
3. Pierwsze zasilenie **przez zasilacz laboratoryjny z ogranicznikiem prądu** (nie bezpośrednio z USB) — sprawdź pobór prądu, zanim wpiszesz płytkę do komputera.
4. Zmierz napięcie na wyjściu LDO (powinno być ~3.3V).
5. Podłącz programator (ST-Link) do SWD, spróbuj wykryć MCU (STM32CubeProgrammer albo OpenOCD).
6. Wgraj prosty firmware "blink LED" — pierwszy dowód, że cały łańcuch działa.
7. Udokumentuj, co nie zadziałało za pierwszym razem (prawie zawsze coś jest) — to najcenniejsza część nauki.

---

## 3. Kluczowe zasady projektowe, o które warto zadbać

- **Decoupling**: kondensator 100nF jak najbliżej (dosłownie kilka mm) każdego pinu zasilania MCU, krótka ścieżka do GND.
- **Płaszczyzna GND**: solidna, nieprzerywana zalewka masy pod komponentami — kluczowe dla stabilności i EMI.
- **BOOT0**: musi mieć zdefiniowany stan (pull-down), inaczej MCU może losowo wchodzić w bootloader.
- **NRST**: pull-up + kondensator (opóźnienie/debounce), zgodnie z datasheetem STM32.
- **Szerokości ścieżek zasilania**: dla kilkuset mA przy 3.3V, 0.3-0.5mm to bezpieczny zakres na 1oz miedzi (użyj kalkulatora trace width, np. wbudowanego w KiCad).
- **Reguły DRC**: ustaw zgodnie z możliwościami producenta (JLCPCB standard: min. trace/spacing 0.127mm, min. via 0.3mm/0.15mm drill) — jeśli projektujesz w ich granicach, unikniesz kosztownych niespodzianek.

---

## 4. Zasoby do nauki (w kolejności przydatności)

1. **Phil's Lab (YouTube)** — projektowanie płytek ze STM32 w KiCad od zera, bardzo praktyczne, dokładnie Twój przypadek.
2. **KiCad Official "Getting Started" + "Learn KiCad"** — dokumentacja i tutoriale na kicad.org.
3. **Datasheet + Reference Manual STM32F411** — sekcje: Power supply scheme, Boot configuration, minimalna aplikacja (zwykle w Application Note AN nt. "Getting started with STM32F4 hardware development" od ST).
4. **JLCPCB "Capabilities" page** — żeby wiedzieć, jakie DRC ustawić.
5. **Contextual Electronics (kurs płatny, ale bardzo dobry)** — jeśli po tym projekcie zechcesz pogłębić temat systematycznie.

---

## 5. Co dalej po pierwszej wersji

- **Rev B**: dodaj USB do komunikacji (D+/D- do MCU, F411 ma natywny USB OTG FS) zamiast tylko zasilania — to naturalny kolejny krok trudności.
- **Przeniesienie do Altium**: gdy dostaniesz dostęp za miesiąc, odtworzenie tego samego, już zweryfikowanego projektu w Altium to świetne ćwiczenie porównawcze narzędzi bez ryzyka związanego z nowym projektem.
- **Integracja z RPi5**: kolejny projekt mógłby być płytką rozszerzeń (HAT) dla RPi5 — naturalne połączenie Twoich dwóch platform.

---

## Checklist przed wysłaniem do produkcji

- [ ] ERC bez błędów i ostrzeżeń (albo świadomie wyciszone)
- [ ] DRC bez błędów, zgodne z możliwościami producenta
- [ ] Wszystkie footprinty zweryfikowane wizualnie (3D viewer w KiCad)
- [ ] Silkscreen nie nachodzi na pady
- [ ] BOOT0 i NRST mają zdefiniowany stan
- [ ] Kondensatory odsprzęgające blisko pinów zasilania
- [ ] Płaszczyzna GND ciągła
- [ ] Sprawdzone Gerbery w viewerze producenta przed zamówieniem
