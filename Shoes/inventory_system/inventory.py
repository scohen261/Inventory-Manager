from storage import load_inventory, save_inventory
import sys
import os

# Get the absolute path of the parent directory where `stockxcaller.py` resides
current_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of inventory.py
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))  # One level up
sys.path.append(parent_dir)  # Add parent directory to sys.path

# Now try to import
from stockxcaller import SneakerAPI

def add_inventory(inventory_name):
    data = load_inventory()
    if inventory_name not in data:
        data[inventory_name] = {}
        save_inventory(data)
        print(f"Inventory '{inventory_name}' created.")
    else:
        print(f"Inventory '{inventory_name}' already exists.")

def add_item(inventory_name, sku):
    """Add a new item to the inventory using SKU and fetch additional details."""
    data = load_inventory()
    if inventory_name not in data:
        print(f"Inventory '{inventory_name}' does not exist.")
        return

    # Fetch details from StockX using the SKU
    api = SneakerAPI()
    products = api.search_products(sku)
    product = products[0]

    if not product:
        print(f"Failed to fetch product details for SKU '{sku}'.")
        return

    # Populate item details
    item_details = {
        "sku": sku,
        "name": product.name,
        "retail_price": product.retail_price,
        "avg_price": product.avg_price
    }

    # Add the item to the inventory
    data[inventory_name][sku] = item_details
    save_inventory(data)
    print(f"Item with SKU '{sku}' added to inventory '{inventory_name}'.")
    print(f"Details: {item_details}")

def get_inventory():
    return load_inventory()
