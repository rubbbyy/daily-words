
# Daily Words

A static site for everyday English vocabulary (Fruits / Vegetables / Daily items) with search, category filters, collapsible IPA (BrE/AmE) and example sentences, and CSV export.

## Edit data
Open `vocab_data.py` in PyCharm CE and extend `CATEGORIES`. Each entry is:
`(Chinese, English, IPA_BrE, IPA_AmE, ExampleSentenceEn)`

## Build
In PyCharm terminal (or macOS Terminal):

```bash
cd /path/to/daily-words
python3 build_page.py
```

The page is generated at `site/index.html`.

## Publish to GitHub Pages
1. Create a new public GitHub repo, e.g. `daily-words`.
2. In terminal:

```bash
cd /path/to/daily-words
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/daily-words.git
git push -u origin main
```

3. On GitHub -> Settings -> Pages:
   - Build and deployment: Choose **Deploy from a branch**
   - Branch: `main` and **/root**
   - Save.

URL will be: `https://<YOUR_USERNAME>.github.io/daily-words/`
(Your `index.html` is under `site/`, so either move files to root or set Pages to use `/root` and ensure `index.html` is at repository root. Easiest: move generated `site/index.html` to root and commit.)

### Option A (simple): keep site at repo root
Change build script to write `index.html` at repo root, or move it manually:
```bash
cp site/index.html index.html
git add index.html
git commit -m "Publish index at root"
git push
```
Then set Pages source: `main` / `/root`.

### Option B: use `docs/` folder
Change the build to `docs/index.html` and select `main` / `/docs` in Pages.

