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
└── hardware/
    └── kicad/
```

## Log postępu

### 2026-08-24 — wydzielenie modułu z projektu integracyjnego

**Co zrobiłem:**
- Rozbiłem pierwotny projekt "wireless-piano-audio-link" na mniejsze, osobno testowalne moduły — ten moduł to czysto RF: antena + SPI, bez audio, bez zasilania na pokładzie
- Zaplanowałem test punkty na wszystkich liniach SPI + pomiar opóźnienia GPIO-to-GPIO

**Czego się nauczyłem:**
- Standardowy oscyloskop hobbystyczny nie nadaje się do bezpośredniego podglądu sygnału 2.4GHz (pojemność sondy rozstraja antenę, pasmo za wąskie) — ale cyfrowa strona (SPI, timing pakietów) jest w pełni dostępna i to ona faktycznie odpowiada na pytanie "czy to działa wystarczająco szybko"

**Następny krok:**
- Schemat w KiCad: nRF24L01+ + referencyjna antena + złącze do carriera STM32
