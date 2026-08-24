# Baza wiedzy o komponentach — projekt 01: mini płytka STM32F411

Dla każdego komponentu: co to jest, skąd wziąć symbol/footprint w KiCad, i **czy da się go zamówić do automatycznego montażu (PCBA) w JLCPCB/PCBWay**. Cel projektu to zamówienie gotowo złożonej płytki, więc dobór komponentów jest podporządkowany temu, co te dwie firmy realnie mają w magazynie i potrafią wlutować maszynowo — nie samej dostępności datasheetu.

---

## Jak działa sourcing w JLCPCB/PCBWay (przeczytaj to przed wyborem komponentów)

**JLCPCB PCBA** jest zintegrowane z magazynem **LCSC** — każdy komponent w Twoim BOM musi mieć numer LCSC (`Cxxxxx`), a JLCPCB dzieli je na trzy kategorie:

- **Basic** — komponenty z maszyn szybkiego montażu, bez opłaty za ustawienie feedera, zwykle najtańsze i najlepiej zaopatrzone (rezystory, kondensatory, popularne diody/tranzystory w standardowych obudowach).
- **Preferred/Extended** — mniej standardowe części (np. konkretne MCU, złącza, przełączniki) — dokładalne maszynowo, ale z jednorazową opłatą za feeder (rzędu $3) i czasem mniejszym/zmiennym stanem magazynowym.
- Stan magazynowy **zmienia się codziennie** (niedobory komponentów są normalne) — numery LCSC poniżej to punkt startowy do BOM, ale **zawsze zweryfikuj aktualny stan na jlcpcb.com/parts tuż przed złożeniem zamówienia**, nie tygodnie wcześniej.

**PCBWay** też oferuje PCBA, ale ich katalog komponentów i system kategorii jest oddzielny od LCSC. Żeby nie komplikować sourcingu w dwie strony na raz: **na v1 celuj w JLCPCB jako główny dostawca montażu** (bo cały dobór poniżej jest zweryfikowany względem ich katalogu) i traktuj PCBWay jako opcję na samo gołe PCB (bez montażu) do porównania ceny/jakości laminatu, a nie jako drugie źródło BOM.

---

## 1. MCU — STM32F411CEU6

⚠️ **Ważna korekta względem poprzedniej wersji tego dokumentu:** sprawdziłem kartę części w JLCPCB i obudowa to **UFQFPN-48 (7×7mm)**, **nie LQFP48** jak napisałem wcześniej. Litera „U” w oznaczeniu `STM32F411C**E U**6` to właśnie kod obudowy UFQFPN (bez wyprowadzeń na bokach, tylko padów na spodzie + duży pad termiczny/masy na środku). To dokładnie ta sama obudowa, co w popularnym „Black Pill".

- **LCSC/JLCPCB:** `C60420` — [karta części JLCPCB](https://jlcpcb.com/partdetail/STM32F411CEU6/C60420)
- Obudowa: **UFQFPN-48, 7×7mm**, rozstaw pinów 0.5mm, z eksponowanym padem termicznym pod spodem
- Assembly: SMT, PCBA Economic i Standard, MSL3 (przed montażem trzymany w suchym opakowaniu — nie problem przy zamówieniu przez JLCPCB, oni to obsługują)
- Datasheet (ST, oficjalny): https://www.st.com/resource/en/datasheet/stm32f411ce.pdf
- Pinout / przegląd: https://www.heisener.com/TechnologyDetail/STM32F411CEU6-Microcontroller-Pinout-Diagram-and-Features

**Symbol/footprint:** ponieważ to QFN (nie QFP), footprint w KiCad to `Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.6x5.6mm` (nazwa może się nieznacznie różnić wersją KiCad — **zweryfikuj wymiar exposed pad z datasheetem**, sekcja mechaniczna/"Package information"). Symbol STM32F411 z wbudowanej biblioteki `MCU_ST_STM32F4` pasuje niezależnie od obudowy (to tylko schemat elektryczny) — ale footprint musisz dobrać poprawnie pod QFN, inaczej DRC/3D viewer to wyłapie, ale lepiej wiedzieć od razu.

**Na co uważać przy schemacie:**
- Kilka par VDD/VSS (nie jedna) — każda potrzebuje własnego kondensatora 100nF blisko pinu.
- VDDA/VSSA (zasilanie analogowe) — osobna para, filtrowana (ferryt/dławik + kondensator), nawet jeśli na v1 nie używasz ADC.
- BOOT0 — pull-down 10kΩ do GND (stan domyślny = boot z Flash).
- NRST — pull-up 10kΩ + kondensator ~100nF (debounce), zgodnie z Reference Manual.
- **Exposed pad (EP) na spodzie QFN musi być połączony z GND** i mieć przelotki termiczne (thermal vias) w layoucie — bez tego montaż JLCPCB będzie ok, ale odprowadzanie ciepła i odniesienie masy będzie gorsze.

---

## 2. Regulator 3.3V — AP2112K-3.3TRG1

- **LCSC/JLCPCB:** `C51118` — [karta części JLCPCB](https://jlcpcb.com/partdetail/AP2112K-3.3TRG1/C51118)
- Obudowa: **SOT-23-5** (JLCPCB czasem etykietuje to jako „SOT-25-5" — to ta sama obudowa, inna konwencja nazewnictwa)
- Assembly: SMT, PCBA Economic i Standard, MSL1 (brak specjalnych wymagań wilgotnościowych)
- Datasheet (Diodes Inc., oficjalny): https://www.diodes.com/assets/Datasheets/AP2112.pdf

**Symbol/footprint:** generyczny footprint SOT-23-5 jest w standardowej bibliotece KiCad, ale **mapowanie pinów jest specyficzne dla tego układu** (kolejność: GND, EN, NC, VOUT, VIN — sprawdź dokładnie w datasheecie). Zweryfikuj ręcznie generyczny symbol SOT-23-5 i przepisz numerację pinów zgodnie z datasheetem — dla tego konkretnego, dobrze udokumentowanego układu to szybsze niż szukanie gotowego symbolu.

**Na co uważać:** pin EN (enable) musi być podciągnięty do VIN (pull-up), inaczej regulator nie włączy wyjścia. Kondensatory: ~1µF na wejściu, ~1µF (do 4.7µF wg datasheetu) na wyjściu, ceramiczne X5R/X7R — te akurat to typowe Basic Parts w JLCPCB, więc dobierzesz konkretny numer LCSC dopiero przy finalizacji BOM (zależnie od dostępnego rozmiaru obudowy).

---

## 3. Złącze USB-C (tylko zasilanie na v1)

Na v1 potrzebujesz tylko VBUS + GND + rezystorów CC — **nie musisz routować pary danych D+/D-** (to upraszcza layout, zostaw sobie USB-data jako zadanie na Rev B).

**Rekomendowana część (dostępna do montażu w JLCPCB):**
- **CIKI Type-C-2.0-6Pin**, `C2987385` — [karta części JLCPCB](https://jlcpcb.com/partdetail/CIKI-Type_C_2_06Pin/C2987385) — złącze 6-pinowe (tylko zasilanie, bez pinów danych/SBU), montaż SMD, prąd 5A/20V, przystosowane pod PCBA (nie THT — nie trzeba dodatkowo lutować ręcznie wzmocnień mechanicznych).

**Ważna zasada przy wyborze złącza USB-C pod PCBA:** w przeciwieństwie do MCU czy rezystora, **footprint złącza USB-C jest specyficzny dla konkretnego producenta/modelu** — nie ma jednego uniwersalnego "footprintu 6-pin USB-C". Musisz pobrać footprint dopasowany dokładnie do `C2987385` (np. przez eksport z EasyEDA — JLCPCB/LCSC linkują karty EasyEDA dla większości części, skąd można wyeksportować footprint do KiCad, albo poszukać go po numerze LCSC na SnapMagic Search), **a nie** wziąć losowy footprint USB-C ze społecznościowego repo, bo pozycje padów i otworów mechanicznych mogą się nie zgadzać z zamówioną częścią.

**Kluczowa zasada elektryczna:** piny **CC1 i CC2** muszą mieć rezystory **5.1kΩ pull-down do GND** — to jest to, co mówi hostowi USB-C "tu jest urządzenie, daj domyślne 5V/max 3A (albo 5V/1.5A wg reguł USB-PD)". Bez tego port może nie podać napięcia w ogóle.

Ogólny przegląd typów złącz i pinów (kontekst): https://www.lcsc.com/blog/usb-c-connector-types-explained-a-complete-guide-to-pins-protocols-and-power/

---

## 4. Złącze programujące — SWD

⚠️ **Zmiana rekomendacji względem poprzedniej wersji:** sprawdziłem dostępność w JLCPCB — typowe zwarte złącze box header 2×5 1.27mm (ARM Cortex Debug) okazało się mieć **status "Extended" i zerowy aktualny stan magazynowy** przy sprawdzeniu. Dla hobbystycznej płytki, którą i tak będziesz programować przez proste przewody/goldpiny, to niepotrzebne ryzyko i koszt.

**Rekomendacja: prosty rządek pinów 2.54mm (1×4 lub 1×5), przecięty z taśmy.**
- Część: **ZHOURI 2.54mm 1×40 pin header** (taśma do przycięcia na żądaną długość), `C2977586` — [karta części JLCPCB](https://jlcpcb.com/partdetail/ZHOURI-2_54_140/C2977586) — montaż THT, bardzo popularna, tania część, jedna pozycja BOM obsługuje jednocześnie: SWD (4-5 pinów: GND, SWCLK, SWDIO, 3V3, opcjonalnie NRST) i wszystkie wyprowadzenia GPIO.
- To dokładnie ten sam typ złącza, którego używają Blue Pill / Black Pill do SWD — pasuje do standardowych przewodów Dupont i typowego kabla ST-Link V2 (klony ST-Linka zwykle i tak mają zakończenie 4-pinowe 2.54mm, nie pełne 10-pinowe 1.27mm ARM).

Tag-Connect (pogo-pin, bez lutowanego złącza) zostaw jako opcję na przyszłość, gdy będzie Ci zależało na miniaturyzacji — na v1 niepotrzebnie komplikuje sourcing.

---

## 5. Rezonator HSE 8MHz (opcjonalny na v1)

**Decyzja projektowa (bez zmian):** STM32F411 ma wewnętrzny oscylator RC — na **v1 pomijasz kryształ całkowicie** i taktujesz MCU wewnętrznie. To dodatkowo upraszcza sourcing na pierwszy raz (jeden mniej komponent do dopasowania pod PCBA).

Gdy w Rev B będzie potrzebny dokładny zegar (np. USB): filtruj katalog JLCPCB bezpośrednio pod frazą "crystal 8MHz" w ich [bibliotece części do montażu](https://jlcpcb.com/parts/2nd/Crystals_Oscillators_Resonators/Crystals_3043) i wybierz pozycję ze statusem Basic/Preferred i realnym stanem magazynowym w danym momencie — nie ma sensu przypinać się teraz do konkretnego numeru, bo to zadanie na później.

---

## 6. Przycisk RESET i User — tact switch SMD

- **LCSC 6×6×12mm SMD Tactile Switch**, `C66637` — [karta części JLCPCB](https://jlcpcb.com/partdetail/LCSC-6_6_12/C66637) — status **Preferred**, obsługiwany przez montaż Economic i Standard PCBA, footprint `KEY-SMD` (symbol i footprint dostępne od razu w EasyEDA, do przeniesienia/zweryfikowania w KiCad).

---

## 7. LED, rezystory, kondensatory

Rezystory i kondensatory 0603 w standardowych wartościach (10kΩ, 100nF, 1µF itd.) oraz zwykłe diody LED 0603 to klasyczne **Basic Parts** w JLCPCB — najlepiej zaopatrzone, bez opłaty za feeder. Konkretny numer LCSC dobierzesz dopiero przy finalizacji BOM (zależy od wartości wynikającej ze schematu i koloru LED), filtrując bezpośrednio [bibliotekę Basic Parts](https://jlcpcb.com/parts/basic_parts) na stronie JLCPCB. Footprinty w KiCad: `LED_SMD`, `Resistor_SMD`, `Capacitor_SMD` (rozmiar 0603) — bez potrzeby dodatkowej weryfikacji poza rozmiarem obudowy.

---

## Metoda pracy (żeby to było powtarzalne przy kolejnych projektach)

1. Znajdź oficjalny datasheet producenta (nie dystrybutora) — to jedyne wiarygodne źródło numeracji pinów.
2. **Sprawdź dostępność w katalogu montażowym dostawcy (JLCPCB Parts Library / LCSC), zanim wybierzesz konkretny model** — zwłaszcza dla złączy i przełączników, gdzie footprint różni się między producentami tej samej "kategorii" części.
3. Zanotuj numer LCSC (`Cxxxxx`) i kategorię (Basic/Preferred/Extended) przy każdej pozycji BOM — to Ci ułatwi późniejsze porównanie kosztu i ryzyka niedoboru.
4. Sprawdź, czy KiCad ma gotowy symbol/footprint w bibliotece standardowej — jeśli tak, użyj go i zweryfikuj 1:1 z datasheetem.
5. Jeśli nie ma — sprawdź kartę EasyEDA/LCSC danej części (JLCPCB/LCSC linkują ją bezpośrednio) albo SnapMagic Search / Ultra Librarian po numerze katalogowym, zanim zaczniesz rysować ręcznie.
6. Jeśli i tam nie ma (rzadkie/nietypowe komponenty) — rysuj ręcznie w KiCad Symbol/Footprint Editor, z datasheetem otwartym obok, i zawsze zweryfikuj w widoku 3D przed zamówieniem.
7. **Tuż przed złożeniem zamówienia PCBA** — zweryfikuj aktualny stan magazynowy każdej pozycji BOM na jlcpcb.com, bo dane sprzed tygodni mogą już nie być aktualne.
