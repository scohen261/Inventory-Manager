from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import traceback

def get_goat_price(sku):
    # Chrome options
    options = Options()
    # Commented out to make browser visible for debugging
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    print("🚀 Launching Chrome...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        search_url = f"https://www.goat.com/search?query={sku}"
        print(f"🔎 Navigating to: {search_url}")
        driver.get(search_url)

        # Wait for search results to appear
        wait = WebDriverWait(driver, 10)
        print("⏳ Waiting for search results...")
        product_link = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/sneakers/']"))
        )

        product_url = product_link.get_attribute("href")
        print(f"➡️ Found product link: {product_url}")
        driver.get(product_url)

        print("⏳ Waiting for price element on product page...")
        price_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3[class*='grid-title'] span"))
        )

        price = price_element.text
        print("✅ Price element found!")
        return price

    except Exception as e:
        print("❌ An error occurred:")
        traceback.print_exc()
        return f"Error: {str(e)}"

    finally:
        print("🧹 Closing browser...")
        driver.quit()

if __name__ == "__main__":
    sku_input = input("Enter Shoe SKU: ")
    price = get_goat_price(sku_input)
    print(f"\n💰 Current price on GOAT: {price}")
