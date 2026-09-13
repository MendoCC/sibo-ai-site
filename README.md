# SIBO AI — webbplats

Statisk sajt för `siboai.app`, publicerad via GitHub Pages.

| Fil | Roll |
|---|---|
| `index.html` | Startsida — produktsida med hero, funktioner, analys, coach, galleri, integritet, pris, FAQ |
| `privacy.html` | Integritetspolicy (engelska + svenska) — **genererad**, se nedan |
| `support.html` | Kontakt, radering av uppgifter, prenumerationshantering |
| `404.html` | Felsida |
| `styles.css` | Hela designsystemet |
| `img/` | Appens riktiga skärmdumpar, ikoner och delningsbild |
| `tools/build_privacy.py` | Genererar `privacy.html` ur app-repots policy |
| `CNAME` | `siboai.app` |

## Inga tredjepartsresurser

Ingen analytics, inga cookies, **ingen JavaScript**, inga CDN:er eller externa
typsnitt. Det är ett hårt krav för det här projektet, inte en preferens. Därför
systemtypsnitt, egen CSS i en fil, `<a>` för all navigering och `<details>` för
utfällbara frågor (fungerar utan skript).

Kontroll innan publicering:

```bash
grep -cE '<script|fonts\.googleapis|cdn\.|unpkg|jsdelivr' *.html   # ska ge 0
```

## Uppdatera integritetspolicyn

Policyn får inte glida ifrån app-repots `docs/PRIVACY-POLICY.md`. Generera om:

```bash
python3 tools/build_privacy.py
```

Skriptet skriver **bara** `privacy.html`. `index.html`, `styles.css`,
`support.html` och `404.html` är handskrivna och rörs aldrig — en tidigare
version genererade hela sajten och skulle ha skrivit över designsystemet.

Fälten markerade `ATT FYLLA I` (kontakt-e-post, registrerad adress) och
`ATT BEKRÄFTA` (biträdesavtal, lagringstider, åldersgräns) är **medvetet synliga**
tills de är ifyllda: en policy med ofyllda fält ska se ofylld ut.

## Bilder

`img/` byggs ur app-repots `store-assets/` och innehåller appens egna
skärmdumpar — inga illustrationer eller påhittade gränssnitt.

- `1-dashboard.png` … `5-correlations.png`, `4-symptom.png` — iOS, skalade till 1400 px
- `ai-utdrag.png` — beskuret utsnitt ur AI-coachen. Beskärningen tar bort
  provperiodsräknaren (skärmdumpen är från ett äldre bygge än dagens 14 dagar)
  och tillskottslistan med dosering (medicinsk påståenderisk). Använd inte
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
