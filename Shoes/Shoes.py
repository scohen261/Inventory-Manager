from tkinter import messagebox
import requests

API_KEY = 'NYsXWV2Yk4JoLQIpda/lXw==MjudBjgujAQ76mEG'

def get_tax_rate(zip_code):
    api_url = f'https://api.api-ninjas.com/v1/salestax?zip_code={zip_code}'
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    
    if response.status_code == requests.codes.ok:
        data = response.json()
        
        # Check if the response is a list or a dictionary
        print("API Response:", data)  # Print the response to inspect it
        
        # If it's a list, access the first element
        if isinstance(data, list):
            if len(data) > 0:
                return float(data[0]['total_rate'])  # Use 'total_rate' and convert to float
            else:
                return None  # Handle case where list is empty
        elif isinstance(data, dict):
            return float(data['total_rate'])  # If it's a dictionary, use 'total_rate'
    else:
        messagebox.showwarning("Error", f"Failed to retrieve tax info for ZIP {zip_code}")
        return None

      
# Prompt user for retail price and discount information
retail = float(input("Enter the retail price: "))
discount_type = input("Enter the discount type (cash, percent, both, or none): ")

if discount_type == "cash" or discount_type == "both":
    cash_discount = float(input("Enter the cash discount: "))
    discounted_price = retail - cash_discount
elif discount_type == "percent" or discount_type == "both":
    percentage_discount = float(input("Enter the percentage discount: "))
    percentage_discount_amount = (percentage_discount / 100) * retail
    discounted_price = retail - percentage_discount_amount
else:
    discounted_price = retail  # Assuming no discount

# Ask user for ZIP code to calculate sales tax
zip_code = input("Enter your ZIP code for tax calculation: ")
tax = get_tax_rate(zip_code)

if tax is not None:
    total_price = discounted_price * (1 + tax / 100)
    print(f"The total price is: {total_price:.2f}")
else:
    print("Unable to calculate total price due to missing tax information.")

# Profit calculator (unchanged)
ebay_fee = 0.1325  # eBay fee percentage (13.25%)
final_value_fee = 0.30  # eBay final value fee for items under $150
stockx_fee = 0.09  # StockX fee percentage (9%)
stockx_shipping_fee = 4  # StockX shipping fee
goat_fee = 0.095  # Goat fee percentage (9.5%)
goat_cashout_fee = 0.029  # Goat cashout fee percentage (2.9%)
goat_seller_fee = 5  # Goat seller fee

def calculate_break_even_price_per_platform(total_price):
    # Calculate break-even price for eBay
    ebay_break_even = total_price / (1 - ebay_fee) + final_value_fee

    # Calculate break-even price for StockX
    stockx_break_even = (total_price + stockx_shipping_fee) / (1 - stockx_fee)

    # Calculate break-even price for Goat
    goat_break_even = (total_price + goat_seller_fee) / (1 - goat_fee - goat_cashout_fee)

    return ebay_break_even, stockx_break_even, goat_break_even

# Assuming total_price is already calculated from previous steps
ebay_break_even, stockx_break_even, goat_break_even = calculate_break_even_price_per_platform(total_price)

print("The minimum selling price to break even on eBay is:", ebay_break_even)
print("The minimum selling price to break even on StockX is:", stockx_break_even)
print("The minimum selling price to break even on Goat is:", goat_break_even)


