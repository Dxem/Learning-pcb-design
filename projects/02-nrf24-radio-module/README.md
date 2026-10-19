# 02 — Moduł radiowy nRF24L01+ (samodzielna sesja nauki RF)

Status: 🟡 w toku — plan gotowy, schemat do zrobienia

Pierwszy z czterech mniejszych modułów, na które rozbiłem [projekt integracyjny 06](../06-piano-audio-integration/) (bezprzewodowy link audio TX/RX). Zamiast projektować od razu całą, złożoną płytkę TX/RX, uczysz się każdej dziedziny osobno na małej, testowalnej płytce. Ten moduł: **RF — dopasowanie anteny i cyfrowa komunikacja SPI z radiem.**

## Zakres

- **nRF24L01+** — bare chip QFN20, własny layout anteny wg referencji Nordica (bez modułu z gotową anteną — to jest właśnie ćwiczenie RF)
- Złącze/pady wyprowadzające SPI (SCK, MOSI, MISO, CSN, CE, IRQ) + 3V3 + GND — **do podpięcia przewodami do płytki z projektu 01** (Twój mini dev board STM32F411) zamiast projektowania osobnego MCU na tej płytce. Reużywasz już zbudowany sprzęt zamiast duplikować MCU w każdym module.
- Bez własnego zasilacza — 3.3V bierzesz z płytki STM32 (project 01 ma już regulator na pokładzie); dodaj tylko lokalny kondensator blokujący blisko radia (nRF24 jest czuły na szum na linii zasilania).

## Test punkty pod oscyloskop/analizator stanów logicznych

Dodaj wyprowadzone pady testowe (małe pady/via, opisane na sitodruku) na:

- **SCK, MOSI, MISO, CSN, CE, IRQ** — wszystkie sygnały cyfrowe SPI, idealne do oscyloskopu/analizatora logicznego. Zobaczysz realny protokół komunikacji z radiem, timing transakcji SPI, kiedy CE się aktywuje przy nadawaniu itd.
- **GPIO testowy z MCU, przełączany na początku/końcu wysyłki pakietu** — to jest Twój sposób na **zmierzenie realnego opóźnienia** transmisji: przełącz jeden GPIO na TX w momencie wysyłki, drugi GPIO na RX w momencie odbioru, i zmierz różnicę czasu na dwukanałowym oscyloskopie. To najważniejszy pomiar w całym projekcie 06 (uzasadnia, czy w ogóle warto grać na tym w czasie rzeczywistym).

**Ważne zastrzeżenie:** samego sygnału radiowego 2.4GHz **nie zobaczysz sensownie na typowym hobbystycznym oscyloskopie** — standardowa sonda pasywna (nawet 10x) ma pojemność rzędu 10-15pF, która przy 2.4GHz realnie rozstraja dopasowanie anteny i daje mylący odczyt, a większość hobbystycznych oscyloskopów ma pasmo 50-100MHz, dalece za mało na 2.4GHz. Do weryfikacji samego RF potrzebny byłby analizator widma albo sonda aktywna wysokiej impedancji. To nie problem — to, co realnie chcesz zobaczyć (protokół SPI i opóźnienie end-to-end), jest w pełni dostępne na zwykłym oscyloskopie.

## Plan budowy i testu

1. Zbuduj **dwie sztuki** tej samej płytki (rola TX/RX ustalana firmware'em, nie sprzętem) — potrzebujesz dwóch egzemplarzy do przetestowania linku. Jeśli zamówiłeś ≥2 sztuki płytki z projektu 01 w PCBA, masz już dwa carriery MCU do tego celu.
2. Podłącz oba moduły do dwóch płytek STM32 z projektu 01.
3. Firmware: najprostszy możliwy — jeden wysyła licznik/wzorzec testowy, drugi odbiera i zapala LED przy poprawnym odbiorze.
4. Zmierz opóźnienie GPIO-to-GPIO na oscyloskopie (patrz wyżej).
5. Dopiero po potwierdzeniu działającego linku i sensownego opóźnienia — przechodzisz do modułu 03/04 (audio).

## BOM

| Komponent | Część | LCSC/JLCPCB | Uwagi |
|---|---|---|---|
| Radio | NRF24L01P-R | `C8791` | Bare chip QFN20 |
| Kondensator blokujący | 100nF + większy elektrolityczny/tantalowy blisko radia | Basic Parts | Zasilanie radia musi być czyste |
| Pady testowe | np. `TestPoint:TestPoint_Pad_D1.0mm` w KiCad | — | Na każdej linii SPI + CE + IRQ |

## Struktura folderu

```
02-nrf24-radio-module/
├── README.md               ← pełny plan modułu (ten plik zawiera wszystko: zakres, BOM, test punkty)
├── docs/                   ← na przyszłość: datasheety, notatki z bring-up, zdjęcia
├── hardware/
|    └── kicad/
└── simulation/
```

## Log postępu

### 2026-09-28 — Rozpoczęcie prac

**Co zrobiłem:**
-  Przeczytałem datasheet modułu nrf24l01p 
- zdecydowałem się nie wykorzystywać nowszego modułu nrf54l01 ponieważ wymaga on obudowy qfn 48 co bezpośrednio wpływa na rozrośnięcie się płytki do mniej więcej wielkości devboarda. Moduł radiowy ma mieć postać shielda a do nauki nowszego modułu poświęcę oddzielny projekt

**Czego się nauczyłem:**
- Standardowy oscyloskop hobbystyczny nie nadaje się do bezpośredniego podglądu sygnału 2.4GHz (pojemność sondy rozstraja antenę, pasmo za wąskie) — ale cyfrowa strona (SPI, timing pakietów) jest w pełni dostępna i to ona faktycznie odpowiada na pytanie "czy to działa wystarczająco szybko"
- romiar obudów komponentów w sekcji dopasowującej wyjście do antenowego 50 ohm ma znaczenie ze względu na efekty pasożytnicze

**Następny krok:**
- Schemat w KiCad: nRF24L01+ + referencyjna antena + złącze do carriera STM32
- zmiana dotychczasowo dobranych komponentó na mniejszy footprint w miejscach gdzie ma to szczególne znaczenie.

### 2026-10-16 — Początek dopasowania anteny

**Co zrobiłem:**
-  Wyprowadziłem piny do fizycznej weryfikacji sygnałów 
- rozpoczęto budowę modelu do dopasowania anteny - wzorując się na application notes Nordic semiconductors, jednak w mojej aplikacji może się okazać że wartości konkretnych elementów mogą się różnić - z tego względu warto zrobić symulację

**Czego się nauczyłem:**
- Pomimo faktu, że nordic semiconductors sprawdziło konkretne dopasowanie do anteny - jest ono sprawdzone jedynie dla ich konkretnego layoutu - dla customowych rozwiązań należy stosować customowe dopasowania.
- Wykorzystywanie biblioteki scikit-rf - rozpocząłem naukę i postawiłem pierwsze kroki

**Następny krok:**
- zrealizować symulację
- dobrać komponenty do wyników symulacji
  
### 2026-10-18 — Początek dopasowania anteny

**Co zrobiłem:**
-  Wybrałem gotowe rozwiązanie anteny na 2.4 GHz zoptymalizowaną przez Texas Instruments 2.4-GHz Inverted F Antenna (Rev. D)
-  Dobrałem Oscylator kwarcowy oraz kondensatory obciążeniowe

**Czego się nauczyłem:**
- niektóre rozwiązania takie jak na przykład konkretny kształt anteny są publicznie i powszechnie dostępne - są zoptymalizowane i udokumentowane do takich właśnie projektów jak ten
- kondensatory w okolicach rezonatorów kwarcowych powinny mieć dielektryk taki jak NP0 lub C0G - nie zmieniać swojej pojemności pod wpływem różnic temperatury

**Następny krok:**
- zrealizować symulację
- dobrać komponenty do wyników symulacji
- pcb layout

### 2026-10-19 — Początek dopasowania anteny

**Co zrobiłem:**
-  Wykonano wstępną analizę symulacyjną dla układu proponowanego przez Nordic Semiconductors w nocie aplikacyjnej
-  Oceniono tolerancje na efekty pasożytnicze dla układu zaproponowanego przez Nordic
-  Analiza Smith Chart i SWR

**Czego się nauczyłem:**
- Nota aplikacyjna proponuje 15+j88Ω jednak z symulacji wynika 19 + j30 Ω, czyli brakuje 1.9nH na każdy pin - różnice mogą wynikać zarówno z obudowy jak i samych długości ścieżek
- Budżet na dodatkowe ścieżki przy ANT1/ANT2 to tylko ok. 0,25 nH, czyli ułamek milimetra. Dopasowanie jest ciasne, bo część rzeczywista impedancji to ok. 10–20 Ω
- Antyrezonans C3–C4 w węźle VDD_PA. Jeśli gałąź C3 ma więcej niż ok. 0,5 nH, węzeł przestaje być masą dla w.cz. i balun przestaje działać. (Prawdziwy kondensator to tak naprawdę cewka z kondensatorem w szeregu)

**Następny krok:**
- pcb layout
- rozbudować symulację po layoucie - teraz już wiem czego się teoretycznie spodziewać
- dobrać komponenty do wyników symulacji
