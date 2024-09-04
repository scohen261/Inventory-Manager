import math

#this is the cost calculator
ct = 6.35  # Set the sales tax rate for Connecticut
nola = 9.45  # Set the sales tax rate for New Orleans
 #prompt to enter your own tax rate
retail = float(input("Enter the retail price: "))

discount_type = input("Enter the discount type (cash, percent or both): ")

if discount_type == "cash" or discount_type =="both":
    cash_discount = float(input("Enter the cash discount: "))
    discounted_price = retail - cash_discount
elif discount_type == "percent" or discount_type == "percentage" or discount_type =="both":
    percentage_discount = float(input("Enter the percentage discount: "))
    percentage_discount_amount = (percentage_discount / 100) * retail
    discounted_price = retail - percentage_discount_amount
else:
    print("Invalid discount type. Assuming no discount.")
    discounted_price = retail

# Check for preset tax locations or user-entered tax rate
tax_location = input("Enter the tax location (ct, nola, or other): ")

if tax_location == "ct":
    tax = ct
elif tax_location == "nola":
    tax = nola
else:
        tax_location == "other"
        other = float(input("Enter the tax rate: "))
        tax = other

"""      tax= float(tax_location)  # Attempt to convert tax location to a float
    except ValueError:
        print("Invalid tax input. Assuming Connecticut tax rate.")
        tax = ct"""

def calculate_total_price(retail, discounted_price, tax):
    tax_amount = discounted_price * (tax / 100)
    total_price = discounted_price + tax_amount
    return total_price

total_price = calculate_total_price(retail, discounted_price, tax)
print("The total price is:", total_price)



#profit calculator eventually will just have the info automatically plugged in from ebay

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


