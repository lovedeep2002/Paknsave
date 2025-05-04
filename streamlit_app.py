import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- Streamlit App Title ---
st.title("🛒 Pak'nSave Product Price Checker")

# --- Product Search Input ---
product_query = st.text_input("Enter product name (e.g., milk, butter, rice):")
search_button = st.button("Search Prices")

# --- Store List ---
store_urls = {
    'Botany': 'https://www.paknsave.co.nz/shop/online/botany',
    'Manukau': 'https://www.paknsave.co.nz/shop/online/manukau',
    'Mill Street': 'https://www.paknsave.co.nz/shop/online/mill-street',
    'Kilbirnie': 'https://www.paknsave.co.nz/shop/online/kilbirnie',
    'Moorhouse': 'https://www.paknsave.co.nz/shop/online/moorhouse',
    'Hornby': 'https://www.paknsave.co.nz/shop/online/hornby'
}

# --- Function to Scrape Prices ---
def get_prices(product):
    results = []
    for store, url in store_urls.items():
        search_url = f"{url}/search?search={product}"
        try:
            response = requests.get(search_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('div', class_='product-tile')
            for item in products[:3]:  # Limit to top 3 results per store
                name = item.find('span', class_='product-title').get_text(strip=True)
                price = item.find('span', class_='price').get_text(strip=True)
                results.append({'Store': store, 'Product': name, 'Price': price})
        except Exception as e:
            results.append({'Store': store, 'Product': 'Error', 'Price': str(e)})
    return pd.DataFrame(results)

# --- Trigger Search on Button Click ---
if search_button and product_query.strip() != "":
    st.write(f"🔍 Searching for: **{product_query}**")
    df = get_prices(product_query)
    
    if not df.empty:
        st.success(f"Found {len(df)} results!")
        st.dataframe(df)
        st.download_button("📥 Download Results as CSV", df.to_csv(index=False), "paknsave_prices.csv", "text/csv")
    else:
        st.warning("No products found. Try a different search term.")
elif search_button:
    st.error("Please enter a product name before searching.")
