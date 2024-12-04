Inventory System 
Scripts Overview
1. inventory_app.py

    The main application script.
    Handles user interactions through a menu-based interface.
    Connects to the core functions of the system for managing inventories.

2. inventory.py

    Manages inventory-related logic.
    Functions:
        add_inventory(inventory_name): Creates a new inventory.
        add_item(inventory_name, sku): Adds an item to an inventory and fetches details via the SKU.
        get_inventory(): Retrieves all inventory data.

3. storage.py

    Handles JSON data storage and retrieval.
    Functions:
        load_inventory(): Loads inventory data from inventory.json.
        save_inventory(data): Saves inventory data to inventory.json.

4. csv_handler.py

    Manages CSV import and export.
    Functions:
        export_inventory_to_csv(inventory_name, inventory_data): Exports a specific inventory to a CSV file.
        export_all_inventories_to_csv(inventories): Exports all inventories, each to a separate