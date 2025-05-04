import streamlit as st
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# --- Streamlit UI ---
st.set_page_config(page_title="Pak'nSave Price Checker", layout="centered")
st.title("🛒 Pak'nSave Product Price Checker")
st.markdown("Enter a product name to check prices across NZ stores (e.g. **Toblerone Milk Chocolate Bar 360g**)")

product_query = st.text_input("Enter product name")
search_button = st.button("Search Prices")

# --- Store URLs ---
store_urls = {
    'Botany': 'https://www.paknsave.co.nz/shop/online/botany',
    'Manukau': 'https://www.paknsave.co.nz/shop/online/manukau',
    'Mill Street': 'https://www.paknsave.co.nz/shop/online/mill-street',
    'Kilbirnie': 'https://www.paknsave.co.nz/shop/online/kilbirnie',
    'Moorhouse': 'https://www.paknsave.co.nz/shop/online/moorhouse',
    'Hornby': 'https://www.paknsave.co.nz/shop/online/hornby'
}

# --- Selenium Chrome options ---
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/chromium-browser"
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# Path to chromedriver on Streamlit Cloud
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

def search_product_in_stores(product_query):
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=chrome_options)
    results = []

    for store, url in store_urls.items():
        search_url = f"{url}/search?search={product_query.replace(' ', '+')}"
        st.write(f"🔍 Searching in **{store}**...")
        try:
            driver.get(search_url)
            time.sleep(4)  # wait for JavaScript to load

            product_title = driver.find_element(By.CLASS_NAME, "product-title").text
            price = driver.find_element(By.CLASS_NAME, "price").text

            results.append({
                "Store": store,
                "Product": product_title,
                "Price": price
            })
        except Exception:
            results.append({
                "Store": store,
                "Product": "Not Found",
                "Price": "N/A"
            })

    driver.quit()
    return pd.DataFrame(results)

# --- Trigger Search ---
if search_button and product_query.strip():
    st.info(f"Searching for: **{product_query}**")
    df = search_product_in_stores(product_query.strip())

    st.success("Search complete!")
    st.dataframe(df)

    st.download_button("📥 Download Results as CSV", df.to_csv(index=False), "paknsave_prices.csv", "text/csv")
elif search_button:
    st.error("Please enter a product name.")
