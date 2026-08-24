# Projekt 06: Bezprzewodowy link audio TX/RX dla pianina (2.4GHz, własny protokół) — integracja

> Ten dokument opisuje **całościową architekturę i uzasadnienie** systemu. Samą budowę i naukę rozbiłem na cztery mniejsze, samodzielnie testowalne moduły — zbuduj i przetestuj je najpierw osobno, zanim wrócisz tutaj do integracji:
> [02-nrf24-radio-module](../../02-nrf24-radio-module/) · [03-audio-adc-frontend](../../03-audio-adc-frontend/) · [04-audio-dac-backend](../../04-audio-dac-backend/) · [05-power-module](../../05-power-module/)
>
> Test punkty pod oscyloskop dla konkretnych sygnałów są opisane w README każdego modułu — ten dokument skupia się na architekturze całości, budżecie przepustowości i bezpieczeństwie, które dotyczą systemu jako całości.

## Cel i geneza

Problem do rozwiązania: cicha gra na pianinie w nocy wymaga słuchawek, ale komercyjne bezprzewodowe rozwiązania nie nadają się do monitorowania gry w czasie rzeczywistym:

- **AirPods (dowolny model):** tylko kodeki AAC/SBC, zmierzone opóźnienie **100–180ms na urządzeniu Apple, 220–290ms na innych** — twardy limit sprzętowy w samych AirPodsach, którego żaden nadajnik nie obejdzie.
- **Słuchawki z aptX Low Latency (np. Audio-Technica ATH-TWX7):** ~30-40ms — użyteczne, ale drogie (~800-900zł) i nadal zależne od implementacji kodeka w cudzym sprzęcie.

Rozwiązanie: **własny link radiowy 2.4GHz (nRF24L01+), gdzie Ty budujesz i nadajnik, i odbiornik.** Nie jesteś zależny od żadnego komercyjnego kodeka Bluetooth, masz pełną kontrolę nad opóźnieniem, a moduły radiowe kosztują ułamek ceny gotowych słuchawek. To też realny, osiągalny pierwszy projekt RF — w przeciwieństwie do próby zaprojektowania Bluetootha "od zera" (nierealne hobbystycznie — baseband BT to praca całych zespołów inżynierskich u producentów chipów).

## Architektura systemu

```
[Pianino, wyjście słuchawkowe]
        │ jack 6.3mm → przejściówka → 3.5mm TRS
        ▼
┌─────────────────────┐         2.4GHz          ┌─────────────────────┐
│   TX (przy pianinie)  │  ──────────────────►   │   RX (przy Tobie)     │
│  jack → ADC → MCU →   │     nRF24L01+           │  nRF24L01+ → MCU →    │
│  nRF24L01+             │                        │  DAC → wzmacniacz →   │
│  zasilanie: USB-C      │                        │  jack 3.5mm            │
│  (stale podłączony)    │                        │  zasilanie: bateria    │
└─────────────────────┘                        │  LiPo + ładowanie USB-C│
                                                   └─────────────────────┘
```

**TX (nadajnik, zostaje przy pianinie):**
- Wejście: gniazdo **3.5mm TRS** (używasz swojej przejściówki 6.3mm→3.5mm z wyjścia słuchawkowego pianina)
- **ADC:** PCM1808 (stereo, 24-bit, interfejs I2S) — konwertuje sygnał analogowy na cyfrowe próbki. Dużo lepsza jakość niż wewnętrzny ADC STM32 (12-bit, bez filtru antyaliasingowego).
- **MCU:** STM32F411CEU6 (ten sam co w projekcie 01 — reużywasz wiedzę o obudowie UFQFPN-48 i pinoutach) — odbiera audio przez I2S, pakietyzuje próbki, wysyła przez SPI do radia.
- **Radio:** nRF24L01+, **bare chip (QFN20)** — projektujesz dopasowanie anteny i layout RF samodzielnie (patrz sekcja niżej).
- **Zasilanie:** bezpośrednio z USB-C, bez baterii — TX stoi przy pianinie, nie musi być mobilny.

**RX (odbiornik, przy Tobie — np. na pasku lub w kieszeni):**
- **Radio:** nRF24L01+ (bare chip, ta sama antena co w TX)
- **MCU:** STM32F411CEU6 — odbiera przez SPI, rekonstruuje strumień próbek, wysyła I2S do DAC.
- **DAC:** PCM5102A (stereo, I2S in, wyjście analogowe)
- **Wzmacniacz słuchawkowy:** NS4160 (steruje bezpośrednio słuchawkami przewodowymi)
- **Wyjście:** gniazdo **3.5mm TRS** — działa z dowolnymi przewodowymi słuchawkami, w tym Twoją przejściówką do 6.3mm.
- **Zasilanie:** bateria LiPo + ładowanie przez USB-C. **USB-C na RX to wyłącznie zasilanie/ładowanie — audio idzie osobnym, analogowym torem przez jack 3.5mm** (zgodnie z ustaloną decyzją: uczysz się projektować złącze USB-C bez wchodzenia w stos USB Host + UAC2, co byłoby osobnym, dużym projektem firmware samym w sobie).

## Budżet przepustowości i kompromis jakości audio — przeczytaj przed pisaniem firmware

nRF24L01+ ma twardy limit sprzętowy: **maks. 32 bajty payloadu na pakiet**, air data rate do 2Mbps (konfigurowalny: 250kbps / 1Mbps / 2Mbps), a realna przepustowość po narzucie protokołu (adresy, CRC, retransmisje) jest zauważalnie niższa niż nominalne 2Mbps.

Dla porównania: CD-quality stereo 16-bit/44.1kHz to **~1.41 Mbps surowego PCM** — praktycznie na granicy albo powyżej tego, co realistycznie przeciągniesz przez ten radio z zapasem na niezawodność łącza.

**Rekomendacja na v1:** mono, 16-bit, próbkowanie ~22-32kHz (~350-512 kbps) — zostawia solidny margines na narzut protokołu, a jakość w zupełności wystarczająca do monitorowania własnej gry (to nie ma być audiofilskie hi-fi, ma słychać siebie wyraźnie i bez opóźnienia). Stereo i wyższa jakość próbkowania — cel na Rev B, gdy już będziesz mieć działający, przetestowany łańcuch end-to-end. Traktuj te liczby jako punkt startowy, nie sztywną specyfikację — dostrój je eksperymentalnie.

## Kluczowa decyzja protokołowa: nie licz na Auto-ACK/Auto-Retransmit tak jak przy zwykłej transmisji danych

Domyślne mechanizmy nRF24L01+ (Auto-ACK + Auto-Retransmit) są dobre do niezawodnego przesyłania danych, ale przy audio w czasie rzeczywistym powodują **skoki opóźnienia** przy zgubionym pakiecie — radio czeka na retransmisję zamiast iść dalej ze strumieniem. W audio/wideo real-time (dokładnie jak w streamingu RTP/UDP, a nie TCP) lepiej zaakceptować sporadyczny zgubiony pakiet — czyli mikroskopijny "glitch" w dźwięku — niż stabilnie rosnące opóźnienie przy próbie retransmisji spóźnionych danych. Rozważ na v1: wyłączony Auto-ACK dla strumienia audio (tryb ShockBurst bez potwierdzeń) albo bardzo krótki, jednorazowy retry z małym opóźnieniem.

## Etapy pracy

**Zanim tu zaczniesz:** poniższe fazy zakładają, że moduły 02 (radio), 03 (ADC), 04 (DAC/wzmacniacz) i 05 (zasilanie) są już zbudowane i potwierdzone osobno na oscyloskopie. Ten dokument opisuje etapy **integracji** sprawdzonych bloków w dwie finalne płytki — nie zaczynaj tu od zera.

### Faza A — Schemat TX (KiCad)
1. Wejście audio: gniazdo 3.5mm TRS → kondensatory sprzęgające (DC blocking) → ewentualny dzielnik napięcia/dopasowanie poziomu do wejścia ADC (poziom z wyjścia słuchawkowego pianina może być głośniejszy niż nominalny line-level wejścia PCM1808 — sprawdź zakres wejściowy w datasheecie i dobierz dzielnik, żeby nie przesterować ADC).
2. PCM1808: zasilanie analogowe/cyfrowe (rozdzielone masy), konfiguracja trybu pracy (piny formatu I2S, master/slave clock) zgodnie z datasheetem.
3. STM32F411: I2S in (SPI2 lub SPI3 w trybie I2S) od PCM1808, SPI do nRF24L01+, standardowe obwiązanie (decoupling, BOOT0, NRST — jak w projekcie 01).
4. nRF24L01+: obwody zasilania (potrzebuje stabilnego, czystego 3.3V — radio jest wrażliwe na szum zasilania), SPI do MCU, linie IRQ/CE.
5. ERC.

### Faza B — Schemat RX (KiCad)
1. nRF24L01+ → STM32F411 (SPI) — analogicznie do TX.
2. STM32F411 → PCM5102A (I2S out).
3. PCM5102A → NS4160 (wzmacniacz słuchawkowy) → gniazdo 3.5mm TRS.
4. Zasilanie: bateria LiPo → TP4056 (ładowanie z USB-C) → **obwód zabezpieczający (DW01A + MOSFET)** → AP2112K-3.3 (LDO do 3.3V) → reszta układu. Patrz sekcja bezpieczeństwa niżej — to nie jest opcjonalne.
5. ERC.

### Faza C — Layout PCB (obie płytki)
1. Osobne płytki dla TX i RX (różne zastosowania, różne wymiary — TX może być większy/stacjonarny, RX ma być noszony).
2. **Antena nRF24L01+:** podąrzaj referencyjny layout Nordica 1:1 — kształt śladu anteny, wymiary, keep-out (brak miedzi/GND pod śladem anteny i w jej pobliżu) zgodnie z ich dokumentacją referencyjną. To jest dokładnie ten rodzaj "RF od zera", który jest osiągalny bez analizatora sieci (VNA), pod warunkiem trzymania się referencji co do milimetra — nie improwizuj kształtu anteny.
3. Rozdziel masy analogowe/cyfrowe wokół ADC (TX) i DAC (RX) — typowa praktyka w projektach audio, ogranicza przenikanie szumu cyfrowego (zegary MCU, radio) do sygnału audio.
4. Trzymaj radio i jego antenę z dala od hałaśliwych cyfrowo ścieżek (zegary, szybkie sygnały SPI) i od krawędzi płytki zgodnie z zaleceniami producenta.
5. DRC.

### Faza D — Pliki produkcyjne i zamówienie PCBA
Analogicznie do projektu 01 — Gerbery, BOM z numerami LCSC, CPL, zamówienie w JLCPCB. Dwie osobne płytki (TX + RX) można zamówić w jednym zamówieniu.

### Faza E — Bring-up i firmware (kolejność ma znaczenie)
1. **Najpierw sam link radiowy**, bez audio: wyślij prosty licznik/wzorzec testowy z TX do RX, zweryfikuj że pakiety dochodzą i zmierz realne opóźnienie (np. przez GPIO toggle + oscyloskop/logic analyzer, albo prostszy pomiar czasowy w firmware).
2. Dopiero potem podłącz ADC/DAC i zamknij pełny łańcuch audio.
3. Zmierz subiektywne opóźnienie end-to-end (np. klaśnięcie przy mikrofonie telefonu + słuchawka jednocześnie, porównanie na nagraniu wideo w slow-motion) — to najbardziej wiarygodny test "czy da się na tym grać".

## Kluczowe zasady projektowe (specyficzne dla tego projektu)

- **Antena nRF24L01+:** trzymaj się referencyjnego layoutu producenta co do milimetra — to jedyny sposób na działającą antenę bez sprzętu pomiarowego RF.
- **Separacja mas analog/cyfra:** wokół PCM1808 (TX) i PCM5102A (RX) — inaczej usłyszysz szum cyfrowy w audio.
- **Czyste zasilanie radia:** nRF24L01+ jest wrażliwy na szum na linii 3.3V — dedykowany kondensator blokujący blisko pinu zasilania, rozważ dodatkowy kondensator elektrolityczny/tantalowy większej wartości blisko radia.
- **Bateria LiPo (RX) — patrz osobna sekcja bezpieczeństwa poniżej, to nie jest szczegół do pominięcia.**

## Bezpieczeństwo baterii LiPo — przeczytaj przed zamówieniem ogniwa

**Sam TP4056 to WYŁĄCZNIE ładowarka — nie ma wbudowanej ochrony przed nadmiernym rozładowaniem, zwarciem czy przegrzaniem ogniwa.** Do noszonego na sobie urządzenia z baterią litową to nie jest miejsce na skróty. Dwie sensowne opcje:

1. **Kup gotowe ogniwo LiPo z wbudowaną płytką ochronną (protection PCB)** — wiele popularnych ogniw pouch/18650 sprzedawanych hobbystycznie ma to już wlutowane. Sprawdź w opisie produktu przed zakupem.
2. **Dodaj własny obwód ochronny:** DW01A (kontroler ochrony) + podwójny MOSFET (np. FS8205A) między ogniwem a resztą układu — standardowy, dobrze udokumentowany układ, chroni przed przeładowaniem, nadmiernym rozładowaniem i zwarciem.

Nie polegaj wyłącznie na softwarowym monitorowaniu napięcia w firmware jako jedynej ochronie — to dodatkowa warstwa, nie zamiennik sprzętowej ochrony.

## BOM — kluczowe komponenty (numery LCSC/JLCPCB zweryfikowane pod PCBA)

| Komponent | Rola | Część | LCSC/JLCPCB | Uwagi |
|---|---|---|---|---|
| MCU (TX i RX) | Sterowanie, protokół | STM32F411CEU6 | `C60420` | Ten sam co w projekcie 01, UFQFPN-48 |
| Radio (TX i RX) | Link 2.4GHz | NRF24L01P-R | `C8791` | Bare chip QFN20 — własny layout anteny |
| ADC (TX) | Analog → cyfra | PCM1808PWR | `C55513` | Stereo, 24-bit, I2S, TSSOP-14 |
| DAC (RX) | Cyfra → analog | PCM5102APWR | `C107671` | Stereo, 24-bit, I2S, TSSOP-20 |
| Wzmacniacz słuchawkowy (RX) | Napędza słuchawki | NS4160 | `C219017` | Stereo headphone driver |
| LDO 3.3V (TX i RX) | Regulacja zasilania | AP2112K-3.3TRG1 | `C51118` | Ten sam co w projekcie 01 |
| Złącze USB-C (TX i RX) | Zasilanie/ładowanie | CIKI Type-C-2.0-6Pin | `C2987385` | Ten sam co w projekcie 01 — tylko zasilanie |
| Ładowarka LiPo (RX) | Ładowanie baterii | TP4056 | `C382139` | Tylko ładowarka — patrz sekcja bezpieczeństwa |
| Ochrona baterii (RX) | Zabezpieczenie ogniwa | DW01A | `C436931` | + MOSFET (np. FS8205A) — obowiązkowe |
| Gniazdo 3.5mm TRS (TX i RX) | Wejście/wyjście audio | PJ-3537S-SMT | `C2689709` | Zweryfikuj liczbę styków (TRS = 3-biegunowe) przed finalizacją BOM |

Rezystory/kondensatory 0603, LED, przycisk — jak w projekcie 01 (Basic Parts / `C66637` dla tact switcha).

**Jak zawsze:** zweryfikuj aktualny stan magazynowy każdej pozycji na jlcpcb.com tuż przed zamówieniem.

## Zasoby

- [RF24Audio (biblioteka referencyjna do streamingu audio przez nRF24L01)](https://github.com/nRF24/RF24Audio)
- [stm32f401cdu6_nrf_audio (precedens: STM32F4 + nRF24 audio na GitHubie)](https://github.com/sdima1357/stm32f401cdu6_nrf_audio)
- Nordic nRF24L01+ Product Specification — sekcja PCB antenna reference design (do dokładnego odwzorowania w layoucie)
- [PCM1808 Datasheet (TI)](https://www.ti.com/lit/ds/symlink/pcm1808.pdf)
- [DW01A Datasheet](https://uelectronics.com/wp-content/uploads/2021/05/Datasheet-DW01A.pdf)

## Status / dalsze kroki

- [ ] Zweryfikować footprinty wszystkich nowych komponentów (PCM1808, PCM5102A, NS4160, nRF24L01+, TP4056, DW01A) względem datasheetów
- [ ] Zbudować schemat TX
- [ ] Zbudować schemat RX
- [ ] Layout PCB z referencyjną anteną nRF24
- [ ] Firmware: najpierw goły link radiowy + pomiar opóźnienia, dopiero potem audio
