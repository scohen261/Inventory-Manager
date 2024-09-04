import json

# File to store the inventory data
inventory_file = "inventory_data.json"

# Function to load existing inventory data from a file
def load_inventory_data():
    try:
        with open(inventory_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save inventory data to a file
def save_inventory_data(data):
    with open(inventory_file, 'w') as file:
        json.dump(data, file, indent=2)

# Define a dictionary to store inventories (initialize with loaded data)
all_inventories = load_inventory_data()

def add_inventory(inventory_name):
    # Check if the inventory already exists
    if inventory_name not in all_inventories:
        all_inventories[inventory_name] = {}
        print(f"Inventory '{inventory_name}' created successfully.")
        save_inventory_data(all_inventories)
    else:
        print(f"Inventory '{inventory_name}' already exists.")

def add_shoe_to_inventory(inventory_name, shoe_name, size, color, price, condition):
    # Check if the inventory exists
    if inventory_name in all_inventories:
        # Add or update the details of the shoe in the specified inventory
        all_inventories[inventory_name][shoe_name] = {'size': size, 'color': color, 'price': price, 'condition': condition}
        print(f"Shoe '{shoe_name}' added to '{inventory_name}' successfully.")
        save_inventory_data(all_inventories)
    else:
        print(f"Inventory '{inventory_name}' not found.")

def get_shoe_details(inventory_name, shoe_name):
    # Check if the inventory exists
    if inventory_name in all_inventories:
        inventory = all_inventories[inventory_name]

        # Check if the shoe name exists in the inventory
        if shoe_name in inventory:
            details = inventory[shoe_name]
            print(f"Details for {shoe_name} in {inventory_name}:")
            print(f"Size: {details['size']}")
            print(f"Color: {details['color']}")
            print(f"Price: {details['price']}")
            print(f"Condition: {details['condition']}")
        else:
            print(f"Shoe '{shoe_name}' not found in {inventory_name}.")
    else:
        print(f"Inventory '{inventory_name}' not found.")

# Ask the user if they want to access an existing inventory or create a new one
user_choice = input("Do you want to (1) access an existing inventory or (2) create a new one? Enter 1 or 2: ")

if user_choice == '1':
    # User wants to access an existing inventory
    existing_inventory_name = input("Enter the name of the existing inventory: ")

    # Ask the user if they want to look up a shoe or add a new one
    operation_choice = input("Do you want to (1) look up a shoe or (2) add a new one? Enter 1 or 2: ")

    if operation_choice == '1':
        # User wants to look up a shoe
        user_shoe_input = input("Enter the name of the shoe: ")
        get_shoe_details(existing_inventory_name, user_shoe_input)
    elif operation_choice == '2':
        # User wants to add a new shoe
        user_shoe_name = input("Enter the name of the shoe: ")
        user_shoe_size = input("Enter the size of the shoe: ")
        user_shoe_color = input("Enter the color of the shoe: ")
        user_shoe_price = input("Enter the price of the shoe: ")
        user_shoe_condition = input("Enter the condition of the shoe: ")
        add_shoe_to_inventory(existing_inventory_name, user_shoe_name, user_shoe_size, user_shoe_color, user_shoe_price, user_shoe_condition)
    else:
        print("Invalid choice. Please enter either 1 or 2.")

elif user_choice == '2':
    # User wants to create a new inventory
    new_inventory_name = input("Enter the name for the new inventory: ")

    # Add the new inventory
    add_inventory(new_inventory_name)

    # Ask the user if they want to look up a shoe or add a new one
    operation_choice = input("Do you want to (1) look up a shoe or (2) add a new one? Enter 1 or 2: ")

    if operation_choice == '1':
        # User wants to look up a shoe
        user_shoe_input = input("Enter the name of the shoe: ")
        get_shoe_details(new_inventory_name, user_shoe_input)
    elif operation_choice == '2':
        # User wants to add a new shoe
        user_shoe_name = input("Enter the name of the shoe: ")
        user_shoe_size = input("Enter the size of the shoe: ")
        user_shoe_color = input("Enter the color of the shoe: ")
        user_shoe_price = input("Enter the price of the shoe: ")
        user_shoe_condition = input("Enter the condition of the shoe: ")
        add_shoe_to_inventory(new_inventory_name, user_shoe_name, user_shoe_size, user_shoe_color, user_shoe_price, user_shoe_condition )
    else:
        print("Invalid choice. Please enter either 1 or 2.")

else:
    print("Invalid choice. Please enter either 1 or 2.")


"""
#This is an example Inventory
# Define a dictionary to store details of each shoe
selling_inventory = {
    'Nike Air Max': {'condition': 'New', 'size': '10', 'color': 'Black', 'price': '$120'},
    'Adidas Superstar': {'condition': 'New','size': '9', 'color': 'White', 'price': '$80'},
    'Puma RS-X': {'condition': 'New','size': '11', 'color': 'Red', 'price': '$100'},
    # Add more shoes and details as needed
}

def get_shoe_details(shoe_name):
    # Check if the shoe name exists in the inventory
    if shoe_name in selling_inventory:
        details = selling_inventory[shoe_name]
        print(f"Details for {shoe_name}:")
        print(f"Condition: {details['size']}")
        print(f"Size: {details['size']}")
        print(f"Color: {details['color']}")
        print(f"Price: {details['price']}")
        
    else:
        print(f"Shoe '{shoe_name}' not found in the inventory.")

# Get user input for the shoe name
user_input = input("Enter the name of the shoe: ")

# Call the function to get and display details
get_shoe_details(user_input)


#Another Example inventory
#Can have one for inventory, then in the interface have a button to add more collecitons so one could be wants, personals etc

personal_inventory = {
    'Nike Air Max': {'condition': 'New', 'size': '10', 'color': 'Black', 'price': '$120'},
    'Adidas Superstar': {'condition': 'New','size': '9', 'color': 'White', 'price': '$80'},
    'Puma RS-X': {'condition': 'New','size': '11', 'color': 'Red', 'price': '$100'},
    # Add more shoes and details as needed
}

def get_shoe_details(shoe_name):
    # Check if the shoe name exists in the inventory
    if shoe_name in personal_inventory:
        details = personal_inventory[shoe_name]
        print(f"Details for {shoe_name}:")
        print(f"Condition: {details['size']}")
        print(f"Size: {details['size']}")
        print(f"Color: {details['color']}")
        print(f"Price: {details['price']}")
        
    else:
        print(f"Shoe '{shoe_name}' not found in the inventory.")

# Get user input for the shoe name
user_input = input("Enter the name of the shoe: ")

# Call the function to get and display details
get_shoe_details(user_input)



"""

