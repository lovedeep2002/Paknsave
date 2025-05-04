import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# --- Title ---
st.title("Pak'nSave Nationwide Product Price Checker")
st.markdown("Check the price of a specific product in all major Pak'nSave stores across New Zealand.")

# --- Input ---
product_name = st.text_input("Enter **exact product name** (e.g., 'Toblerone Milk Chocolate Bar 360g'):")
search_button = st.button("Search Prices")

# --- Store List ---
store_urls = {
    'Botany': 'https://www.paknsave.co.nz/shop/online/botany',
    'Manukau': 'https://www.paknsave.co.nz/shop/online/manukau',
    'Mill Street': 'https://www.paknsave.co.nz/shop/online/mill-street',
    'Kilbirnie': 'https://www.paknsave.co.nz/shop/online/kilbirnie',
    'Moorhouse': 'https://www.paknsave.co.nz/shop/online/moorhouse',
    'Hornby': 'https://www.paknsave.co.nz/shop/online/hornby',
    'Albany': 'https://www.paknsave.co.nz/shop/online/albany',
    'Whangarei': 'https://www.paknsave.co.nz/shop/online/whangarei',
    'Rotorua': 'https://www.paknsave.co.nz/shop/online/rotorua',
    'Napier': 'https://www.paknsave.co.nz/shop/online/napier'
}

# --- Scraping Function ---
def get_product_prices_exact(product_query):
    results = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for store, url in store_urls.items():
        search_url = f"{url}/search?search={product_query.replace(' ', '+')}"
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            product_tiles = soup.find_all('div', class_='product-tile')

            found = False
            for item in product_tiles:
                title_tag = item.find('span', class_='product-title')
                price_tag = item.find('span', class_='price')

                if title_tag and product_query.lower() in title_tag.text.lower():
                    found = True
                    name = title_tag.text.strip()
                    price = price_tag.text.strip() if price_tag else "N/A"
                    results.append({'Store': store, 'Product': name, 'Price': price})
                    break  # Stop after first exact match

            if not found:
                results.append({'Store': store, 'Product': 'Not Found', 'Price': 'N/A'})
            time.sleep(1)  # polite delay

        except Exception as e:
            results.append({'Store': store, 'Product': 'Error', 'Price': str(e)})

    return pd.DataFrame(results)

# --- Run the Search ---
if search_button and product_name.strip():
    st.info(f"Searching for: **{product_name}** across all stores...")
    df = get_product_prices_exact(product_name.strip())
    st.success("✅ Search complete.")
    st.dataframe(df)

    # Download CSV
    st.download_button("📥 Download Results as CSV", df.to_csv(index=False), "paknsave_prices.csv", "text/csv")
elif search_button:
    st.error("Please enter a product name.")
