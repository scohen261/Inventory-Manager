import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import re

# Restored eBay filters dictionary
ebay_filters = {
    "item_conditions": {
        "New": 1000,
        "Open box": 1500,
        "Used": 3000,
        "Certified Refurbished": 2000,
        "Excellent - Refurbished": 2500,
        "Very Good": 3000,
        "Good": 4000,
        "For Parts or Not Working": 7000
    },
    "item_locations": {
        "Domestic": 1,
        "International": 2,
        "Continent": 3,
    },
    "directories": {
        "No Directory": 0,
        "Clothing, Shoes & Accessories": 11450,
    },
    "subdirectories": {
        "Men's Shoes": 93427,
        "Women's Shoes": 3034,
    },
    "sort_order": {
        "Best Match": 12,
        "Time: ending soonest": 1,
        "Time: newly listed": 10,
        "Price + Shipping: lowest first": 15,
        "Price + Shipping: highest first": 16,
        "Distance: nearest first": 7
    }
}

def clean_price(price_str):
    """Convert price string to float"""
    try:
        price = re.sub(r'[^\d.]', '', price_str)
        return float(price)
    except:
        return 0.0

def parse_date(date_str):
    """Convert eBay date string to datetime object"""
    try:
        date_str = date_str.replace('Sold', '').strip()
        return pd.to_datetime(date_str)
    except:
        return None

def calculate_metrics(df):
    """Calculate sales metrics"""
    if df.empty:
        return None
    
    df['Price_Clean'] = df['Price'].apply(clean_price)
    
    metrics = {
        'average_price': round(df['Price_Clean'].mean(), 2),
        'last_sale_price': round(df['Price_Clean'].iloc[0], 2),
        'highest_price': round(df['Price_Clean'].max(), 2),
        'lowest_price': round(df['Price_Clean'].min(), 2),
        'total_sales': len(df),
        'last_90_days_sales': len(df[df['Date'] >= (datetime.now() - timedelta(days=90))]) if 'Date' in df.columns else 'N/A'
    }
    return metrics

def search_shoes(sku=None, brand=None, model=None, size=None, condition="Used"):
    """Enhanced eBay search function prioritizing SKU and handling pagination more robustly."""
    url = "https://www.ebay.com/sch/i.html"
    
    # Construct search query using SKU, size, and additional details
    search_query = f"{sku} {size}" if sku and size else f"{sku}"

    # Set search parameters including directory and subdirectory for better filtering
    params = {
        '_from': 'R40',
        '_nkw': search_query,
        'LH_Sold': '1',
        'LH_Complete': '1',
        '_ipg': '100',  # Adjust items per page to maximum for fewer requests
        '_dcat': ebay_filters["directories"]["Clothing, Shoes & Accessories"],
        '_sacat': 0,  # Adjust this based on men's or women's shoes if needed
        'LH_ItemCondition': ebay_filters["item_conditions"].get(condition, ''),
    }
    
    items_list = []
    page_number = 1  # Start from the first page

    while True:
        params['_pgn'] = page_number
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for items in the current page
        items = soup.find_all('div', class_='s-item__wrapper clearfix')
        if not items:
            break  # Exit loop if no items found

        for item in items:
            title = item.find('h3', class_='s-item__title').text if item.find('h3', class_='s-item__title') else 'No title'
            price = item.find('span', class_='s-item__price').text if item.find('span', class_='s-item__price') else '0'
            link = item.find('a', class_='s-item__link')['href'] if item.find('a', class_='s-item__link') else 'No link'
            
            # Append only if title matches the SKU to ensure accuracy
            if sku.lower() in title.lower():
                items_list.append({
                    'Title': title,
                    'Price': price,
                    'Link': link
                })

        # Check for the next page
        next_button = soup.find('a', attrs={'aria-label': 'Next page'})
        if next_button and 'disabled' not in next_button.attrs:
            page_number += 1
        else:
            break  # Stop if there is no next page

    return pd.DataFrame(items_list)


def main():
    print("eBay Shoe Sales Analyzer")
    print("-----------------------")
    
    # Get user input
    sku = input("Enter SKU (primary search term): ")
    brand = input("Enter brand (optional, press enter to skip): ") or None
    model = input("Enter model (optional, press enter to skip): ") or None
    size = input("Enter size (optional, press enter to skip): ") or None
    condition = input("Enter condition (New/Used, default=Used): ") or "Used"

    # Search for shoes
    print("\nSearching eBay for sales data...")
    df = search_shoes(sku, brand, model, size, condition)
    
    if df is None or df.empty:
        print("No results found")
        return

    # Calculate metrics
    metrics = calculate_metrics(df)
    
    if metrics:
        print("\nSales Metrics:")
        print(f"Average Sale Price: ${metrics['average_price']}")
        print(f"Last Sale Price: ${metrics['last_sale_price']}")
        print(f"Highest Sale Price: ${metrics['highest_price']}")
        print(f"Lowest Sale Price: ${metrics['lowest_price']}")
        print(f"Total Sales: {metrics['total_sales']}")
        if metrics['last_90_days_sales'] != 'N/A':
            print(f"Sales in Last 90 Days: {metrics['last_90_days_sales']}")
    

    def main():
        print("eBay Shoe Analyzer")
        print("-----------------")

            # Get user input
    sku = input("Enter SKU (primary search term): ")
    brand = input("Enter brand (optional, press enter to skip): ") or None
    model = input("Enter model (optional, press enter to skip): ") or None
    size = input("Enter size (optional, press enter to skip): ") or None
    condition = input("Enter condition (New/Used, default=Used): ") or "Used"

    # Search for shoes
    print("\nSearching eBay for sales data...")
    df = search_shoes(sku, brand, model, size, condition)

    if df is None or df.empty:
        print("No results found")
        return

    # Calculate metrics
    metrics = calculate_metrics(df)

    if metrics:
        print("\nSales Metrics:")
        print(f"Average Sale Price: ${metrics['average_price']}")
        print(f"Last Sale Price: ${metrics['last_sale_price']}")
        print(f"Highest Sale Price: ${metrics['highest_price']}")
        print(f"Lowest Sale Price: ${metrics['lowest_price']}")
        print(f"Total Sales: {metrics['total_sales']}")
        if metrics['last_90_days_sales'] != 'N/A':
            print(f"Sales in Last 90 Days: {metrics['last_90_days_sales']}")


    # Save to CSV
    output_file = f"{sku}_sales_data.csv"
    df.to_csv(output_file, index=False)
    print(f"\nDetailed sales data saved to {output_file}")

if __name__ == "__main__":
    main()
