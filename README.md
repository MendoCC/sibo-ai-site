# SIBO AI — webbplats

Statisk sajt för `siboai.app`, publicerad via GitHub Pages. **Engelska är primär**,
svenska och tyska är valbara.

## Struktur

| Sökväg | Roll |
|---|---|
| `/` | Startsida, engelska (primär) |
| `/sv/` | Startsida, svenska |
| `/de/` | Startsida, tyska |
| `/support.html` | Support, engelska |
| `/sv/support.html` | Support, svenska |
| `/de/support.html` | Support, tyska |
| `/privacy.html` | Integritetspolicy (engelska + svenska) — **genererad** |
| `/404.html` | Felsida (engelska, med länk till alla språk) |
| `/sitemap.xml`, `/robots.txt` | Sökmotorstöd |
| `/styles.css` | Hela designsystemet |
| `/img/` | Appens riktiga skärmdumpar, ikoner och delningsbild |
| `/tools/build_privacy.py` | Genererar `privacy.html` ur app-repots policy |

Språkväxlaren (`EN · SV · DE`) sitter i sidhuvudet **utanför** `<nav>`, eftersom
`nav` göms på smal skärm. Flytta den inte in i `nav` — då försvinner den på mobil.

Varje sida har `<link rel="alternate" hreflang=…>` för alla tre språk plus
`x-default`, och kanonisk URL till sig själv.

## Lägga till ett språk

1. Kopiera `sv/` till den nya koden (`es/`, `fr/` …).
2. Byt `<html lang>`, `<title>`, kanonisk URL, `og:locale` och all brödtext.
3. Lägg till språket i språkväxlaren i **alla** sidhuvuden och i sidfotens
   språkkolumn — och i `hreflang`-länkarna överst i varje sida.
4. Lägg till `aria-current="page"` på det nya språket och ta bort det från de andra.
5. Uppdatera `sitemap.xml`.

Kör `python3 /tmp/site_audit.py`-motsvarigheten (eller motsvarande kontroll) —
den verifierar att varje intern länk har ett mål, att `lang` stämmer och att
inga skript eller tredjepartsresurser smugit in.

## Inga tredjepartsresurser

Ingen analytics, inga cookies, **ingen JavaScript**, inga CDN:er eller externa
typsnitt. Det är ett hårt krav för det här projektet, inte en preferens. Därför
systemtypsnitt, egen CSS i en fil, `<a>` för all navigering och `<details>` för
utfällbara frågor (fungerar utan skript).

```bash
grep -cE '<script|fonts\.googleapis|cdn\.|unpkg|jsdelivr' *.html sv/*.html de/*.html   # ska ge 0
```

## Uppdatera integritetspolicyn

```bash
python3 tools/build_privacy.py
```

Skriptet skriver **bara** `privacy.html`. Startsidorna, `styles.css`,
`support.html` och `404.html` är handskrivna och rörs aldrig.

⚠️ **Policyn finns bara på engelska och svenska.** Källfilen
`docs/PRIVACY-POLICY.md` i app-repot har två språk. De tyska sidorna säger det
rakt ut i stället för att länka till en tyskspråkig policy som inte finns. En
tysk fassning måste läggas till i källfilen och granskas juridiskt innan
publicering — lägg den i så fall som en tredje del i samma fil.

Fälten `ATT FYLLA I` (kontakt-e-post, registrerad adress) och `ATT BEKRÄFTA`
(biträdesavtal, lagringstider, åldersgräns) är **medvetet synliga** tills de är
ifyllda: en policy med ofyllda fält ska se ofylld ut.

## Bilder

`img/` byggs ur app-repots `store-assets/` och innehåller appens egna
skärmdumpar — inga illustrationer eller påhittade gränssnitt.

- `1-dashboard.png`, `2-timeline.png`, `4-symptom.png`, `5-correlations.png` — iOS, skalade till 1400 px
- `ai-utdrag.png` — beskuret utsnitt ur AI-coachen. Beskärningen tar bort
  provperiodsräknaren (skärmdumpen är från ett äldre bygge än dagens 14 dagar)
  och tillskottslistan med dosering. Använd inte
  `store-assets/ios/shot-3-aicoach.png` oskalad i marknadsföring — den
  innehåller båda.
- `icon-192.png`, `apple-touch-icon.png`, `favicon-64.png`, `og.jpg`

Android-skärmdumparna i app-repot visar **"SIBO Coach"** i apphuvudet och ett
äldre gränssnitt — de används därför inte här förrän appen är omdöpt.

## Publicera

GitHub Pages bygger om automatiskt vid push till `main`. Verifiera:

```bash
curl -sI https://siboai.app/ | head -1
```
