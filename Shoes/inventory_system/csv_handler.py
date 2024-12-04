import pandas as pd
import os

EXPORT_DIR = "exported"

def export_inventory_to_csv(inventory_name, inventory_data):
    """
    Export a single inventory to its own CSV file.
    
    Args:
        inventory_name (str): The name of the inventory.
        inventory_data (dict): The items and their details in the inventory.
    """
    # Ensure the export directory exists
    os.makedirs(EXPORT_DIR, exist_ok=True)

    # Prepare the CSV file path
    file_path = os.path.join(EXPORT_DIR, f"{inventory_name}.csv")

    # Flatten inventory data into a list of rows
    rows = []
    for sku, details in inventory_data.items():
        row = {
            "SKU": sku,
            "Name": details.get("name", ""),
            "Retail Price": details.get("retail_price", ""),
            "Average Price": details.get("avg_price", ""),
        }
        rows.append(row)

    # Create a DataFrame and export to CSV
    df = pd.DataFrame(rows)
    df.to_csv(file_path, index=False)
    print(f"Inventory '{inventory_name}' exported to {file_path}")
