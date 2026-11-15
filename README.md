# Mallu's Design Tool

Selaimessa toimiva suunnitteluohjelma remontteihin ja sisustukseen: 2D-pohjapiirros, 3D-näkymä, kävelytila, materiaalikirjasto, laatoitus, keittiökalusteet, valaistus ja varjot, ulkoympäristö sekä PDF-, DXF- ja tekoälykuvavienti.

## Käyttö

Avaa sivu: https://henryo124.github.io/mallus-design-tool/

`index.html` toimii myös sellaisenaan ilman nettiyhteyttä: lataa tiedosto ja avaa se selaimessa. Projektit tallentuvat vain omaan selaimeesi (IndexedDB / localStorage) – niitä ei lähetetä mihinkään. Varmuuskopion saa Projekti-välilehdeltä JSON-tiedostona.

## Rakenne

- `index.html` – valmis, itsenäinen sovellus (Three.js r128 ja jsPDF upotettuina)
- `src/src.html` – lähdekoodi
- `src/build.py` – kokoaa `index.html`:n (tarvitsee `lib/`-kansioon Three.js 0.128.0 -paketin ja jsPDF 2.5.1:n)
- `src/smoke.py` – Playwright-savutestit
