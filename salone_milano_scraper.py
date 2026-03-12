import time
import json
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==============================
# CONFIG
# ==============================

OUTPUT_CSV = "salone_milano_exhibitors.csv"
OUTPUT_JSON = "salone_milano_exhibitors.json"
SAVE_INTERVAL = 50
DRIVER_PATH = "chromedriver.exe"  # Update this path

# All Manifestazione event codes
EVENTS = {
    "Salone Internazionale del Mobile": "SMI",
    "Salone Internazionale del Complemento d'Arredo": "CDA",
    "Workplace 3.0": "EIM",
    "S.Project": "S_P",
    "EuroCucina": "EUC",
    "FTK - Technology For the Kitchen": "FTK",
    "Salone Internazionale del Bagno": "ARB",
}

BASE_URL = "https://www.salonemilano.it/it/exhibitors"


# ==============================
# DRIVER SETUP
# ==============================

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Uncomment for headless mode:
    # chrome_options.add_argument("--headless=new")

    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# ==============================
# GET TOTAL PAGES
# ==============================

def get_total_pages(driver):
    try:
        pagination = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".pagination"))
        )
        pages = pagination.find_elements(By.TAG_NAME, "a")
        page_numbers = []
        for p in pages:
            try:
                page_numbers.append(int(p.text.strip()))
            except:
                pass
        return max(page_numbers) if page_numbers else 1
    except:
        return 1


# ==============================
# GET EMAIL VIA CONTATTA BUTTON
# ==============================

def get_email(driver):
    try:
        contatta_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'contatta') or contains(@class,'contatta')]"))
        )
        contatta_btn.click()
        time.sleep(2)

        email_elem = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='mailto:']"))
        )
        email = email_elem.get_attribute("href").replace("mailto:", "").strip()
        return email
    except:
        return ""


# ==============================
# SCRAPE ONE EXHIBITOR PAGE
# ==============================

def scrape_exhibitor_detail(driver, url, event_name):
    try:
        driver.get(url)
        time.sleep(2)

        data = {
            "manifestazione": event_name,
            "company_name": "",
            "country": "",
            "stand_number": "",
            "website": "",
            "category": "",
            "phone": "",
            "email": "",
            "profile_url": url,
        }

        # Company Name
        try:
            data["company_name"] = driver.find_element(
                By.CSS_SELECTOR, "h1.exhibitor-name, h1.company-name, h1"
            ).text.strip()
        except:
            pass

        # Country
        try:
            data["country"] = driver.find_element(
                By.XPATH, "//*[contains(@class,'country') or contains(@class,'nazione')]"
            ).text.strip()
        except:
            pass

        # Stand Number
        try:
            data["stand_number"] = driver.find_element(
                By.XPATH, "//*[contains(@class,'stand') or contains(@class,'padiglione')]"
            ).text.strip()
        except:
            pass

        # Website
        try:
            website_elem = driver.find_element(
                By.CSS_SELECTOR, "a.website-link, a[href*='http']:not([href*='salonemilano'])"
            )
            data["website"] = website_elem.get_attribute("href")
        except:
            pass

        # Category
        try:
            data["category"] = driver.find_element(
                By.XPATH, "//*[contains(@class,'categoria') or contains(@class,'category')]"
            ).text.strip()
        except:
            pass

        # Phone
        try:
            data["phone"] = driver.find_element(
                By.CSS_SELECTOR, "a[href^='tel:']"
            ).get_attribute("href").replace("tel:", "").strip()
        except:
            pass

        # Email via Contatta button
        data["email"] = get_email(driver)

        return data

    except Exception as e:
        print(f"  Error scraping {url}: {e}")
        return None


# ==============================
# SCRAPE ONE EVENT LISTING
# ==============================

def scrape_event(driver, event_name, event_code):
    print(f"\n{'='*50}")
    print(f"Scraping: {event_name} ({event_code})")
    print(f"{'='*50}")

    exhibitor_urls = []
    page = 1

    while True:
        url = f"{BASE_URL}?anno=2026&evento={event_code}&pageNumber={page}"
        print(f"  Listing page {page}: {url}")

        driver.get(url)
        time.sleep(3)

        # Get all exhibitor links
        try:
            cards = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    By.CSS_SELECTOR, "a.exhibitor-card, a.card-link, .exhibitor-item a"
                )
            )
            links = [c.get_attribute("href") for c in cards if c.get_attribute("href")]
            if not links:
                break
            exhibitor_urls.extend(links)
            print(f"  Found {len(links)} exhibitors on page {page}")
        except:
            print(f"  No more exhibitors found on page {page}")
            break

        # Check if next page exists
        try:
            next_btn = driver.find_element(
                By.CSS_SELECTOR, "a.next-page, a[aria-label='Next'], .pagination .next"
            )
            if not next_btn.is_enabled():
                break
            page += 1
        except:
            break

    print(f"  Total exhibitors found: {len(exhibitor_urls)}")

    # Scrape each exhibitor detail
    results = []
    for i, url in enumerate(exhibitor_urls):
        print(f"  [{i+1}/{len(exhibitor_urls)}] {url}")
        detail = scrape_exhibitor_detail(driver, url, event_name)
        if detail:
            results.append(detail)
        time.sleep(1.5)

    return results


# ==============================
# MAIN
# ==============================

def main():
    driver = create_driver()
    all_results = []

    try:
        for event_name, event_code in EVENTS.items():
            event_results = scrape_event(driver, event_name, event_code)
            all_results.extend(event_results)

            # Auto-save after each event
            save_data(all_results)
            print(f"  Saved {len(event_results)} records for {event_name}")

    except Exception as e:
        print(f"Fatal error: {e}")

    finally:
        save_data(all_results)
        driver.quit()
        print(f"\n✅ Scraping Complete! Total records: {len(all_results)}")


# ==============================
# SAVE DATA
# ==============================

def save_data(results):
    if not results:
        return

    # Save JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    # Save CSV
    df = pd.DataFrame(results)
    cols = ["manifestazione", "company_name", "country", "stand_number",
            "website", "category", "phone", "email", "profile_url"]
    df = df[[c for c in cols if c in df.columns]]
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print(f"  💾 Saved {len(results)} total records")


if __name__ == "__main__":
    main()
