from inventory import add_inventory, add_item, get_inventory
from csv_handler import export_inventory_to_csv
from storage import save_inventory

def main():
    print("Welcome to the Hybrid Inventory System!")
    while True:
        print("\nOptions:")
        print("1. Create a new inventory")
        print("2. Add an item to inventory")
        print("3. View all inventories")
        print("4. Export a specific inventory to CSV")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter inventory name: ")
            add_inventory(name)
        elif choice == "2":
            inventory_name = input("Enter inventory name: ")
            sku = input("Enter the SKU of the item: ")
            add_item(inventory_name, sku)
        elif choice == "3":
            inventories = get_inventory()
            for name, items in inventories.items():
                print(f"\nInventory: {name}")
                for sku, details in items.items():
                    print(f"  SKU: {sku}, Details: {details}")
        elif choice == "4":
            inventories = get_inventory()
            inventory_name = input("Enter the inventory name to export: ")
            if inventory_name in inventories:
                export_inventory_to_csv(inventory_name, inventories[inventory_name])
            else:
                print(f"Inventory '{inventory_name}' does not exist.")
        elif choice == "5":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
