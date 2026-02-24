# 🤖 Portfolio Generator Bot

Telegram orqali avtomatik professional portfolio yaratuvchi bot.

## 📁 Fayl tuzilmasi

```
portfolio_bot/
├── bot.py          # Asosiy bot kodi
├── generator.py    # HTML portfolio generatori (3 ta template)
├── config.py       # Konfiguratsiya
├── requirements.txt
└── .env.example
```

## 🚀 Ishga tushirish

### 1. Bot token olish
1. Telegram'da [@BotFather](https://t.me/BotFather) ga boring
2. `/newbot` yozing
3. Botga nom bering
4. Token oling: `1234567890:ABCdef...`

### 2. O'rnatish

```bash
# Virtual environment yarating
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate     # Windows

# Kutubxonalarni o'rnating
pip install -r requirements.txt
```

### 3. Token qo'shish

**Usul 1 — .env fayli:**
```bash
cp .env.example .env
# .env faylni oching va token qo'ying
BOT_TOKEN=1234567890:ABCdef...
```

**Usul 2 — config.py da to'g'ridan-to'g'ri:**
```python
BOT_TOKEN = "1234567890:ABCdef..."
```

### 4. Ishga tushirish

```bash
python bot.py
```

## 🎨 Templatelar

| Template | Tavsif |
|----------|--------|
| 🌙 Dark Modern | Qora fon, violet accent, Space Mono font |
| ☀️ Light Clean | Oq fon, editorial dizayn, Fraunces serif |
| 🎨 Creative Bold | Qora fon, sariq/pink aksentlar, Bebas Neue |

## 📤 Portfolio'ni joylash

### Netlify (eng oson — 1 daqiqa)
1. [netlify.com](https://netlify.com) ga kiring
2. Faylni "drag & drop" qiling
3. Tayyor! Bepul link olasiz

### GitHub Pages (bepul domen)
1. GitHub'da yangi repo yarating
2. `portfolio.html` → `index.html` deb nomlang
3. Repo'ga yuklang
4. Settings → Pages → Branch: main → Save
5. Link: `https://username.github.io/repo-name`

## 🔧 Kelajak rejalar (2-bosqich)

- [ ] GitHub API orqali avtomatik deploy
- [ ] Rasm yuklash (avatar)
- [ ] Ko'proq templatelar
- [ ] PDF export
- [ ] Admin panel

---
Made with ❤️ using aiogram 3 + Jinja2
