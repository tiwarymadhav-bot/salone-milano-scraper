# 🪑 Salone Milano Exhibitor Scraper

A production-grade Python scraper that extracts **exhibitor data** from [Salone del Mobile Milano](https://www.salonemilano.it) — one of the world's largest furniture & design trade fairs.

---

## 🚀 Features

- 🔁 **Loops all 7 Manifestazione categories** separately
- 📧 **Email extraction** via automated "Contatta" button click (dynamic interaction)
- 📄 **Full pagination support** — scrapes all pages per category
- 💾 **Auto-save after each event** — no data loss
- 📦 **Dual output** — CSV + JSON formats
- 🧹 **Clean structured data** — ready for analysis or CRM import

---

## 📊 Data Fields Extracted

| Field | Description |
|-------|-------------|
| `manifestazione` | Event category (e.g. EuroCucina, S.Project) |
| `company_name` | Exhibitor company name |
| `country` | Country of origin |
| `stand_number` | Hall/stand number at the fair |
| `website` | Company website URL |
| `category` | Product/design category |
| `phone` | Contact phone number |
| `email` | Contact email (via Contatta button) |
| `profile_url` | Direct link to exhibitor page |

---

## 🎪 Manifestazione Categories

All 7 categories are scraped separately in a loop:

| Code | Event Name |
|------|-----------|
| SMI | Salone Internazionale del Mobile |
| CDA | Salone Internazionale del Complemento d'Arredo |
| EIM | Workplace 3.0 |
| S_P | S.Project |
| EUC | EuroCucina |
| FTK | FTK — Technology For the Kitchen |
| ARB | Salone Internazionale del Bagno |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| Selenium | Browser automation + dynamic clicks |
| Pandas | Data processing & CSV export |
| JSON | Structured output |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/tiwarymadhav-bot/salone-milano-scraper.git
cd salone-milano-scraper
```

### 2. Install dependencies
```bash
pip install selenium pandas
```

### 3. Download ChromeDriver
- Download from: https://chromedriver.chromium.org/downloads
- Match your Chrome browser version
- Update `DRIVER_PATH` in the script

---

## 🔧 Configuration

```python
OUTPUT_CSV    = "salone_milano_exhibitors.csv"
OUTPUT_JSON   = "salone_milano_exhibitors.json"
DRIVER_PATH   = "path/to/chromedriver.exe"
```

---

## ▶️ Usage

```bash
python salone_milano_scraper.py
```

The script will:
1. Loop through all 7 event categories
2. Paginate through every listing page
3. Visit each exhibitor profile
4. Click "Contatta" to extract email
5. Auto-save after each category completes
6. Deliver clean CSV + JSON output

---

## 📁 Output Structure

```
salone-milano-scraper/
│
├── salone_milano_scraper.py          # Main scraper
├── salone_milano_exhibitors.csv      # Output CSV
├── salone_milano_exhibitors.json     # Output JSON
└── README.md
```

### Sample Output (CSV)

| manifestazione | company_name | country | stand_number | website | category | phone | email |
|---------------|-------------|---------|-------------|---------|----------|-------|-------|
| EuroCucina | Boffi S.p.A | Italy | Hall 12 - C30 | boffi.com | Kitchen Systems | +39 02... | info@boffi.com |
| S.Project | Bolon AB | Sweden | Hall 9 - B14 | bolon.com | Flooring | +46 33... | sales@bolon.com |

---

## 💡 How It Works

```
Loop each Manifestazione category
    ↓
Paginate through listing pages
    ↓
Collect all exhibitor profile URLs
    ↓
Visit each profile
    ↓
Click "Contatta" → extract email
    ↓
Save to CSV + JSON
```

---

## 📌 Use Cases

- B2B lead generation for furniture/design industry
- Market research on exhibiting companies
- Trade fair competitive analysis
- CRM database building

---

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**. Always review a website's Terms of Service before scraping. The author is not responsible for any misuse.

---

## 👨‍💻 Author

**Madhav Tiwary**
Python Developer | Web Scraping & Data Engineering

- 💼 [Upwork Profile](https://www.upwork.com/freelancers/~01f57d319968afb3a8?mp_source=share)
- 🐙 [GitHub](https://github.com/tiwarymadhav-bot)

---

## ⭐ If this project helped you, give it a star!
