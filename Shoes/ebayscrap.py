import requests
from bs4 import BeautifulSoup
import pandas as pd

# goal is to scrape ebay, the code will prompt the user to provide the SKU of the item
# they are searching for, then the size, condition, and any other speicifics they have
# then using that the  code will scrape ebay and provide the last sold item/date, volume of sales last 90 days
# average sale price, and the high/low sales price
# Define the base URL for the eBay search


# Define the eBay filters dictionary
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
        "Consumer Electronics": 9355,
        "Clothing, Shoes & Accessories": 11450,
        "Health & Beauty": 26395,
        "Home & Garden": 11700,
        "Sporting Goods": 382,
        "Toys & Hobbies": 220,
        "Books": 267,
        "Video Games & Consoles": 1249,
        "Collectibles": 1,
        "Business & Industrial": 12576,
        "Automotive": 6000, 
    },
    "categories": {
        "No Category": 0,
        "Cell Phones & Smartphones": 9355,
        "Laptops & Netbooks": 175673,
        "Watches": 31387,
        "Furniture": 3197,
        "Action Figures": 2605,
        "Jewelry & Watches": 281,
        "Cameras & Photo": 625,
        "Pet Supplies": 1281,
        "Crafts": 14339,
        "Computers/Tablets & Networking": 58058,
        "Cars & Trucks": 6001,  
        "Motorcycles": 6024,  
        "Car & Truck Parts": 6030,  
        "Motorcycle Parts": 10063,  
        "Automotive Tools & Supplies": 34998,  
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

url = "https://www.ebay.com/sch/i.html"

# Define the query parameters for the search request
params = {
    '_from': 'R40',
    '_nkw': 'iphone 13',
    'LH_ItemCondition': ebay_filters["item_conditions"]["Used"],  # Item condition; 'New'.
    'LH_PrefLoc': ebay_filters["item_locations"]["International"],
    '_udlo': '200',  # Minimum price.
    '_udhi': '400',  # Maximum price.
    '_dcat': ebay_filters["directories"]["No Directory"],  # Filter by directory ID; "Consumer Electronics".
    '_sacat': ebay_filters["categories"]["No Category"],  # Filter by category ID; "Cell Phones & Smartphones".
    '_sop': ebay_filters["sort_order"]["Time: newly listed"],  # Sort by "Time: newly listed"
    'LH_Sold': '1',  # Only sold listings (='1').
    'LH_Complete': '1',  # Only completed listings (='1').
    'LH_BIN': '0',  # Only Buy It Now listings (='1').
    'LH_Auction': '1',  # Only Auction Listings (='1').
    'LH_BO': '0',  # Only listings that accept offers (='1').
    'LH_FS': '0',  # Only Free Shipping listings (='1').
    '_ipg': '240',  # Number of items per page (='1'), Max is 240.
    'rt': 'nc'  # Result type; 'nc' indicates no cache to ensure the search results are fresh. 
    
}

request =requests.Requst('GET', url, params=params)
prepared_request = requests.prepare()
print(prepared_request.url)

#initialize variables

# Initialize variables
page_number = 0
items_list = []

# Loop over pages
while True:
    
    page_number += 1
    
    print(f'Scraping page: {page_number}')
          
    params['_pgn'] = page_number
    
    # Send GET request to eBay with the defined parameters
    response  = requests.get(url, params=params)
    html_content = response.text # Get the HTML content of the page
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
          
    # Find the next button
    next_button = soup.find('button', class_='pagination__next', type='next')

    # Check if the next button is disabled
    if next_button and next_button.get('aria-disabled') == 'true':
        print('No more pages pages to scrape')
        break
    else:
        # Extract items
        items = soup.find_all('div', class_='s-item__wrapper clearfix')

        # Extract Listings
        for item in items [2:]:
            title = item.find('div', class_='s-item__title').text
            price = item.find('span', class_='s-item__price').text
            link = item.find('a', class_='s-item__link')['href'].split('?')[0]
            image_url = item.find('div', class_='s-item__image-wrapper image-treatment').find('img').get('src','No image URL')

            # Define each item as a dictionary
            item_dict = {
                'Title': title,
                'Price': price,
                'Link': link,
                'Image Link': image_url
            }

            # Append the dictionary to the list
            items_list.append(item_dict)

            len(items_list)
            items_df = pd.DataFram(items_list)
            items_df


            forbidden_terms = [
                'refurbished',
                'iphone 12',
                'parts',
                'damaged',
                'locked',
                'pro',
                'mini',
                '256 gb',
                '512 gb',
                'verizon',
                'at&t', 
                't-mobile',
                'cricket',
                'metro',
                'boost',
                'read description'               
            ]

            # Create a boolean mask for filtering out forbidden terms
            mask = ~items_df['Title'].str.lower().str.contains(r'\b(?:' + '|'.join(forbidden_terms) + r')\b')

            # Apply the mask to filter the DataFrame
            filtered_df = items_df[mask]


            # Reset the index of the filtered DataFrame
            filtered_df = filtered_df.reset_index(drop=True)

                        
