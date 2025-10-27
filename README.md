<div align="center">

<img src="https://emojicdn.elk.sh/📘" width="80"/>

# Daily Words

**An interactive web app for learning everyday English vocabulary**  
Search · Category Filter · IPA (BrE/AmE) · Example Sentences

🌍 **Live Site** 👉 https://rubbbyy.github.io/daily-words/

</div>

---

## ✨ Features

- ✅ Categorized vocabulary: Fruits 🍎 Vegetables 🥕 Daily Items 🧴
- ✅ Click a word to expand details
- ✅ Show **BrE/AmE IPA**
- ✅ English example sentences
- ✅ Search in English and Chinese
- ✅ Mobile-friendly UI
- ✅ Export current list to CSV

🚧 Coming soon…

- 🔊 Pronunciation (TTS)
- 🎮 Quiz mode — Multiple choice & spelling
- 🎯 Mark as mastered
- 🌙 Light/Dark theme switch
- 🖼️ Add images for visual memory
- 📚 More categories (Animal · Transportation · School · Clothing…)

---

## 📸 Preview

> (Screenshots of your app, coming soon!)

Example layout:

| List View | Expanded Word |
|----------|----------------|
| Word list with filters | IPA & example sentence |

---

## 🛠️ Tech Stack

| Part | Technology |
|------|------------|
| Generator | Python (`build_page.py`) |
| Vocabulary | `vocab_data.py` (Editable) |
| UI | HTML + CSS + JavaScript |
| Hosting | GitHub Pages |

---

## 📦 Local Build Instructions

```bash
python3 build_page.py
open site/index.html   # macOS, or double-click
