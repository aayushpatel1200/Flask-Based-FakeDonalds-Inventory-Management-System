
"""
Inventory System with Per-Item Critical Stock Threshold

This system helps a burger shop (FakeDonald's) manage inventory efficiently by:
- Tracking current stock levels
- Alerting you when items are low
- Placing orders with GST included
- Logging product waste
- Saving all updates to the inventory.csv file
"""

"""
[BEFORE YOU START]:
                    1. Make sure you have a file called `inventory.csv` in the same folder as this Python file.
                    That file should include columns:
                    - name, quantity, price, units_per_box, critical_level

                    2. Open a terminal or code editor and run this Python file:
                    py mcd_inventory_critical_threshold.py

[MENU OPTIONS]:

            {View Inventory}  
            - Shows a list of all items, boxes in stock, price per box, and per-unit price.  
            - Also shows low stock alerts (if anything is below its critical level).

            {Daily Inventory Entry}
            - Use this at the start of the day to enter how many boxes are currently in stock for each item.  
            - This replaces the old numbers and updates the system.

            {Place Order (with GST)}
            - Use this to simulate ordering more boxes of products.  
            - You’ll pick a product number, enter how many boxes you want, and it adds it to stock.  
            - Shows a summary with subtotal, 5% GST, and total cost.

            {Log Wasted Products} 
            - If some food goes bad or is wasted, enter how many units (e.g., patties, buns, etc.) were wasted for each product.  
            - The system calculates how much money was lost.

            {Save and Exit}
            - Saves all the changes you made (new stock counts, orders, waste logs) back to the CSV file.  
            - Safely closes the program.

[DATA IS AUTO-SAVED]:
            - No need to manually update the CSV file — just press Option 5 to save your session.
            - Always save before closing the program to keep your changes.

[NOTES]:
            - Enter numbers only when asked (no letters or symbols).
            - If you type something wrong, the program will let you retry or skip that step.
            - Don’t delete or rename `inventory.csv` while the program is running.

"""


import csv

# GST rate used in final invoice
GST_RATE = 0.05

# This function loads the inventory from a CSV file.
# It also calculates the per-unit price based on how many items are in each box.
def load_inventory(filename):
    inventory = {}
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name'].lower()
                quantity = int(row['quantity'])  # Number of boxes
                price = float(row['price'])      # Price per box
                units = int(row['units_per_box'])  # Items per box
                critical = int(row['critical_level'])  # Alert level
                per_unit = price / units         # Calculate price per single item

                # Store all values in the inventory dictionary
                inventory[name] = {
                    'quantity': quantity,
                    'price': price,
                    'units_per_box': units,
                    'critical_level': critical,
                    'per_unit_price': per_unit
                }
    except FileNotFoundError:
        print("inventory.csv not found.")
    return inventory

# This function saves the updated inventory back to the CSV file
def save_inventory(inventory, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'quantity', 'price', 'units_per_box', 'critical_level'])
        writer.writeheader()
        for name, data in inventory.items():
            writer.writerow({
                'name': name,
                'quantity': data['quantity'],
                'price': data['price'],
                'units_per_box': data['units_per_box'],
                'critical_level': data['critical_level']
            })

# Displays the current inventory in a readable table format
def show_inventory(inventory):
    print("\n======================== INVENTORY ========================")
    print(f"{'No.':<3} {'Item':<20} {'Boxes':<8} {'Box Price':<10} {'Per Unit':<10}")
    for i, (name, item) in enumerate(inventory.items(), 1):
        print(f"{i:<3} {name.title():<20} {item['quantity']:<8} ${item['price']:<9.2f} ${item['per_unit_price']:<10.3f}")
    print("="*40)

# Checks if any item has dropped below its critical threshold and shows a warning
def show_low_stock_alerts(inventory):
    print("\n !!! LOW STOCK ALERTS !!!")
    found = False
    for name, item in inventory.items():
        if item['quantity'] < item['critical_level']:
            print(f"- {name.title()}: Only {item['quantity']} boxes left (Critical: {item['critical_level']})")
            found = True
    if not found:
        print("All products are sufficiently stocked.")

# Allows user to manually update the inventory for each product (e.g., during shift start)
def daily_inventory_entry(inventory):
    print("\n================= Daily Inventory Entry =================")
    for i, (name, item) in enumerate(inventory.items(), 1):
        try:
            new_qty = int(input(f"{i}. {name.title()} - Boxes on hand: "))
            inventory[name]['quantity'] = new_qty
        except ValueError:
            print("Invalid input, skipping.")

# Used to place new orders and automatically update stock levels
# Also calculates subtotal, GST, and total order cost
def place_order(inventory):
    show_inventory(inventory)
    print("\n================= Place Order =================")
    items = list(inventory.keys())
    order = {}

    while True:
        choice = input("Enter product number to order (or 'done'): ").strip().lower()
        if choice == 'done':
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(items)):
            print("Invalid choice.")
            continue

        idx = int(choice) - 1
        name = items[idx]
        try:
            qty = int(input(f"How many boxes of {name.title()} to order? "))
            if qty <= 0:
                print("Must be > 0")
                continue
            box_price = inventory[name]['price']
            order[name] = {
                'qty': qty,
                'unit_price': box_price,
                'subtotal': box_price * qty
            }
            inventory[name]['quantity'] += qty
        except ValueError:
            print("Invalid quantity.")

    if order:
        print("\n=== Order Summary ===")
        total = sum(item['subtotal'] for item in order.values())
        gst = total * GST_RATE
        grand_total = total + gst
        print(f"{'Item':<20} {'Boxes':<6} {'Unit Price':<12} {'Subtotal':<10}")
        for name, item in order.items():
            print(f"{name.title():<20} {item['qty']:<6} ${item['unit_price']:<11.2f} ${item['subtotal']:<10.2f}")
        print("-" * 50)
        print(f"Subtotal: ${total:.2f}")
        print(f"GST (5%): ${gst:.2f}")
        print(f"Total: ${grand_total:.2f}")

# Tracks how many units were wasted and calculates the financial loss
def waste_entry(inventory):
    print("\n=== Waste Tracking ===")
    total_waste_cost = 0
    for i, (name, item) in enumerate(inventory.items(), 1):
        try:
            units_wasted = int(input(f"{i}. {name.title()} - Units wasted: "))
            cost = units_wasted * item['per_unit_price']
            total_waste_cost += cost
        except ValueError:
            print("Invalid input, skipping.")
    print(f"Total cost of waste: ${total_waste_cost:.2f}")

# Main menu loop of the program — shows options and directs to appropriate functions
def main():
    filename = 'inventory.csv'
    inventory = load_inventory(filename)    
    show_low_stock_alerts(inventory)
    
    while True:
        print("""
========== MENU ==========
1. View Inventory
2. Daily Inventory Entry
3. Place Order (with GST)
4. Log Wasted Products
5. Save and Exit
==========================
""")
        option = input("Choose an option: ").strip()
        if option == '1':
            show_low_stock_alerts(inventory)
            show_inventory(inventory)
        elif option == '2':
            show_low_stock_alerts(inventory)
            daily_inventory_entry(inventory)
        elif option == '3':
            show_low_stock_alerts(inventory)
            place_order(inventory)
        elif option == '4':
            waste_entry(inventory)
        elif option == '5':
            save_inventory(inventory, filename)
            print("Saved and exiting.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
