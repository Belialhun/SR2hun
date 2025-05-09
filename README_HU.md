# Belialhun/SR2hun – Python szkriptek technikai és dokumentációs áttekintése

Ez a projekt a **Legacy of Kain: Soul Reaver 2** videojáték magyarításához kapcsolódik, ahol a játék szöveges és grafikus elemeit kell átalakítani és a megfelelő formátumba konvertálni. A repó 3 fontos Python szkriptet és egy HTML-alapú segédeszközt tartalmaz, amelyek a lokalizáció technikai részét támogatják.

---

## ✨ **GeneratedPNG.py**

**Célja**: 
Ez a szkript a `.tpng` kiterjesztésű szöveges állományokat (amelyek párbeszédeket, narrációkat tartalmaznak formázási tagekkel) PNG képekké alakítja. Ezek a képek szolgálnak a játékban megjelenő feliratos szövegek vizuális megjelenítésére.

**Fő funkciók:**
- Feldolgozza a `.tpng` fájlokat, amelyek soron ként tartalmazzák a megjelenítendő szövegeket és vezérlő tageket, pl. `[title]`, `[dialogue]`, `[narrator]`, `[centered]`, `[pn]`, `[NLA]`, `[NRA]`.
- Automatikusan formázza a szöveget stílus szerint (betűtípus, szín, igazítás).
- A kimenet egy 512x448 pixeles PNG kép, amely tartalmazza:
  - A lefordított magyar szöveget
  - "Előző / Következő" nyilak ikonokkal
  - Oldalszámot (ha meg van adva `[pn]` taggel)
- A szkript a képbe beágyazza a teljes eredeti szöveget metaadatként ("Description" mező), így később ellenőrizhető, hogy a kép megfelel-e az eredeti szövegnek.
- Használja a Pillow (PIL) könyvtárat és Arial betűtípusokat a rajzoláshoz.

---

## 📁 **pngtoraw.py**

**Célja**:
A PNG képek konvertálása a Soul Reaver 2 saját `.raw` formátumába, amely 16 bites ARGB1555 (1 bit átlátszóság + 5-5-5 bites RGB színek) struktúrával rendelkezik. Ezt használja a játék textúraként.

**Fő funkciók:**
- Interaktív Tkinter alapú grafikus felület.
- A felhasználó megadhat:
  - Egy PNG fájlt (egyedi konvertáláshoz)
  - Egy teljes mappát PNG képekkel (tömeges konvertáláshoz)
  - Egy eredeti `.raw` fájlt, amelyből a 128 byte-os fejlecet másolja át
- A kimenet `.raw` fájl, amely a fejlec + konvertált képadatokat tartalmazza.
- A kimeneti fájlok fix hossza: 458 880 byte (ami egy 512x448-as képnek felel meg).
- Hasznos eszköz a lokalizált, szerkesztett képek visszacsomagolásához.

---

## 👁️ **rawtopng.py**

**Célja**:
A játék `.raw` fájljainak visszafejtése és PNG képek generálása azokból. Ez a folyamat segít a játék eredeti (pl. angol nyelvű) textúráinak megtekintésében, szerkesztésében.

**Fő funkciók:**
- Egyszerű Tkinter alapú GUI, amely lehetővé teszi egy teljes mappa `.raw` fájainak feldolgozását.
- A szkript feltételezi, hogy a `.raw` fájl:
  - 128 byte fejleccel kezdődik
  - Ezután 16 bites ARGB1555 pixeleket tartalmaz
  - A képméret fix: 512x448 pixel (229 376 pixel)
- Minden kimeneti kép PNG formátumban mentésre kerül az output mappába.
- Ha hibát észlel (pl. nem megfelelő fájlméret), logfájlba („conversion_errors.log”) írja a hibát.

---

## 🗃️ **DOCTYPE5.html**

**Célja**:
Ez egy HTML5-alapú, interaktív szövegkészítő eszköz, amellyel egyszerűen és vizuálisan generálhatók a `GeneratedPNG.py` által feldolgozható `.tpng` fájlok.

**Fő funkciók:**
- Szövegdobozok dinamikus létrehozása (10–20)
- Minden dobozhoz hozzárendelhető egy típus: `[dialogue]`, `[narrator]`, `[centered]`, `[title]`, stb.
- Oldalszám megadása `[pn]` taggel
- Két opcionális jelölőnégyzet: "Előző nyíl ne jelenjen meg" `[NLA]`, "Következő nyíl ne jelenjen meg" `[NRA]`
- Gomb: **Szöveg generálása** → kimenet megjelenítése
- Gomb: **Fájl generálása** → `.tpng` fájl mentése

**Használat:**
1. Nyisd meg a `DOCTYPE5.html` fájlt böngészőben
2. Válassz szövegdoboz-számot, írd be a szövegeket, add meg a stílust
3. Add meg az oldalszámot, pipáld ki a nyilakat ha kell
4. Kattints **Szöveg generálása**, ellenőrizd a kimenetet
5. Kattints **Fájl generálása**, a böngésző letölti a `.tpng` fájlt

---

## 🔧 Lokalizációs munkafolyamat áttekintése

1. **Eredeti képek visszafejtése**: `rawtopng.py`
   - Eredeti `.raw` textúrák átalakítása szerkeszthető PNG-vé.

2. **Szövegek szerkesztése és generálása**: `DOCTYPE5.html` + `GeneratedPNG.py`
   - HTML oldalon megadott szövegekből `.tpng` fájl, majd PNG generálás

3. **Képek átalakítása játékformátumba**: `pngtoraw.py`
   - PNG-ből RAW konvertálás, a játék által elfogadott formátumba

---

## 🔗 Függőségek
- Python 3.x
- Pillow (PIL)
- Tkinter (a Python standard GUI könyvtára)
