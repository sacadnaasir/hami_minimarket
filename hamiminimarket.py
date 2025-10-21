import csv # To call Python’s built-in CSV module.
import os # To access to the operating system features (e.g clearing the terminal) 

# ===============================
# Hami Minimarket Inventory System 
# ===============================

inventory = []      # Stores all products
last_change = None  # Tracks last action for undo


# ==============================================
#  Helper Functions
# ==============================================
 
def pause():
    """Pause the program until user presses Enter."""
    input("\nPress Enter to continue...")


def check_cancel(value):
    """Check if the user typed 'cancel' to exit early."""
    if value.lower() == "cancel":
        print("🚫 Action cancelled. Returning to menu.")
        pause()
        return True
    return False


def get_valid_number(prompt, allow_blank=False, is_int=False):
    """
    Ask user for a valid number (price or quantity).
    Keep retrying until correct.
    """
    while True:
        value = input(prompt).strip()
        if value == "" and allow_blank:
            return None
        if check_cancel(value):
            return "cancel"
        try:
            num = int(value) if is_int else float(value)
            if num < 0:
                print("❌ Value cannot be negative.")
                continue
            return num
        except ValueError:
            print("❌ Please enter a valid number.")


def stock_status(qty):
    """Return stock level label based on quantity."""
    if qty < 20:
        return "🔴 LOW STOCK"
    elif qty < 100:
        return "🟡 MODERATE STOCK"
    else:
        return "🟢 GOOD STOCK"


# ==============================================
# CSV Save / Load / Export
# ==============================================

def save_data(filename="inventory.csv"):
    """Save all inventory data to CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "category", "price", "quantity"])
        writer.writeheader()
        writer.writerows(inventory)


def load_data(filename="inventory.csv"):
    """Load data from CSV file if it exists."""
    global inventory
    inventory.clear()
    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["price"] = float(row["price"])
                row["quantity"] = int(row["quantity"])
                inventory.append(row)
        print("📂 Data loaded successfully!")
    except FileNotFoundError:
        print("No saved data found. Starting fresh.")


def export_to_csv():
    """Export inventory to another CSV file."""
    filename = input("Enter filename to export to (default: export_inventory.csv or type 'cancel' to go back): ").strip()
    if check_cancel(filename):
        return
    filename = filename or "export_inventory.csv"
    save_data(filename)
    print(f"✅ Inventory exported successfully to '{filename}'!")
    pause()


# ==============================================
# Add Product
# ==============================================

def add_product():
    global last_change
    print("\n--- Add New Product (type 'cancel' anytime to go back) ---")

    # Require valid product name
    while True:
        name = input("Enter product name: ").strip()
        if check_cancel(name):
            return
        if not name:
            print("❌ Product name is required. Please enter a valid name.")
            continue
        break

    # Prevent duplicates
    for product in inventory:
        if product["name"].lower() == name.lower():
            print(f"⚠️ '{name}' already exists in inventory.")
            choice = input("Do you want to update its details instead? (y/n): ").strip().lower()
            if choice == "y":
                update_existing_product(product)
            else:
                print("🚫 No changes made.")
                pause()
            return

    # Require valid category
    while True:
        category = input("Enter category: ").strip()
        if check_cancel(category):
            return
        if not category:
            print("❌ Category is required. Please enter a valid category.")
            continue
        break

    price = get_valid_number("Enter price: ")
    if price == "cancel":
        return

    quantity = get_valid_number("Enter quantity: ", is_int=True)
    if quantity == "cancel":
        return

    product = {"name": name, "category": category, "price": price, "quantity": quantity}
    inventory.append(product)
    save_data()
    last_change = {"action": "add", "product": product.copy()}

    print(f"✅ {name} added successfully!")
    print("💾 You can undo this addition from the main menu.")
    pause()


# ==============================================
# Update Existing Product
# ==============================================

def update_existing_product(product):
    global last_change

    print("\n--- Update Existing Product ---")
    print(f"Current details for '{product['name']}':")
    print(f"Name: {product['name']}")
    print(f"Category: {product['category']}")
    print(f"Price: {product['price']}")
    print(f"Quantity: {product['quantity']}")
    print("\nEnter new details (leave blank to keep current value):")

    old_product = product.copy()
    updated_product = product.copy()

    new_name = input("New name: ").strip()
    if check_cancel(new_name):
        return
    if new_name:
        updated_product["name"] = new_name

    new_category = input("New category: ").strip()
    if check_cancel(new_category):
        return
    if new_category:
        updated_product["category"] = new_category

    new_price = get_valid_number("New price: ", allow_blank=True)
    if new_price == "cancel":
        return
    if new_price is not None:
        updated_product["price"] = new_price

    new_qty = get_valid_number("New quantity: ", allow_blank=True, is_int=True)
    if new_qty == "cancel":
        return
    if new_qty is not None:
        updated_product["quantity"] = new_qty

    if updated_product == old_product:
        print("\nℹ️ No changes were made.")
        pause()
        return

    print("\n📝 Review updated details:")
    print(f"Name: {updated_product['name']}")
    print(f"Category: {updated_product['category']}")
    print(f"Price: {updated_product['price']}")
    print(f"Quantity: {updated_product['quantity']}")

    confirm = input("\nSave changes? (y/n): ").strip().lower()
    if confirm == "y":
        product.update(updated_product)
        save_data()
        last_change = {"action": "update", "old": old_product, "new": updated_product}
        print(f"✅ Product '{product['name']}' updated successfully!")
    else:
        print("🚫 Update cancelled.")
    pause()


def update_product():
    """Find a product and update its details."""
    print("\n--- Update Product ---")
    name = input("Enter the product name to update (or type 'cancel' to go back): ").strip()
    if check_cancel(name):
        return
    for product in inventory:
        if product["name"].lower() == name.lower():
            update_existing_product(product)
            return
    print("❌ Product not found.")
    pause()


# ==============================================
# View Products
# ==============================================

def view_products():
    """Display all products neatly."""
    print("\n--- Product List ---")
    if not inventory:
        print("No products available.")
        pause()
        return

    print(f"{'Name':<15}{'Category':<15}{'Price':<10}{'Quantity':<10}Status")
    print("-" * 70)
    for product in inventory:
        status = stock_status(product["quantity"])
        print(f"{product['name']:<15}{product['category']:<15}{product['price']:<10}{product['quantity']:<10}{status}")
    print("-" * 70)

    total_items = len(inventory)
    total_quantity = sum(p["quantity"] for p in inventory)
    total_value = sum(p["price"] * p["quantity"] for p in inventory)
    print(f"\n📊 Summary: {total_items} products | Total Qty: {total_quantity} | Value: ${total_value:.2f}")
    pause()


# ==============================================
# Delete, Undo, Search, Value
# ==============================================

def delete_product():
    global last_change
    print("\n--- Delete Product ---")
    name = input("Enter product name to delete (or type 'cancel' to go back): ").strip()
    if check_cancel(name):
        return
    for product in inventory:
        if product["name"].lower() == name.lower():
            confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").lower()
            if confirm == "y":
                deleted_copy = product.copy()
                inventory.remove(product)
                save_data()
                last_change = {"action": "delete", "product": deleted_copy}
                print(f"🗑️ '{name}' deleted successfully.")
            else:
                print("🚫 Deletion cancelled.")
            pause()
            return
    print("❌ Product not found.")
    pause()


def undo_last_change():
    global last_change
    if not last_change:
        print("\n⚠️ No recent changes to undo.")
        pause()
        return

    action = last_change["action"]
    if action == "add":
        product = last_change["product"]
        inventory[:] = [p for p in inventory if p["name"].lower() != product["name"].lower()]
        print(f"↩️ Addition of '{product['name']}' undone.")
    elif action == "delete":
        product = last_change["product"]
        inventory.append(product)
        print(f"↩️ Deletion of '{product['name']}' undone.")
    elif action == "update":
        old = last_change["old"]
        for i, p in enumerate(inventory):
            if p["name"].lower() == old["name"].lower():
                inventory[i] = old
                print(f"↩️ Update to '{old['name']}' undone.")
                break
    else:
        print("❌ Unknown action.")

    save_data()
    last_change = None
    pause()


def calculate_total_value():
    """Calculate the total value of inventory."""
    total = sum(p["price"] * p["quantity"] for p in inventory)
    print(f"\n💰 Total inventory value: ${total:.2f}")
    pause()


def search_product():
    """Search products by name."""
    name = input("\nEnter product name to search (or type 'cancel' to go back): ").strip()
    if check_cancel(name):
        return
    found = [p for p in inventory if name.lower() in p["name"].lower()]
    if found:
        print(f"\nResults for '{name}':")
        print(f"{'Name':<15}{'Category':<15}{'Price':<10}{'Quantity':<10}")
        print("-" * 50)
        for p in found:
            print(f"{p['name']:<15}{p['category']:<15}{p['price']:<10}{p['quantity']:<10}")
    else:
        print("❌ No matching products found.")
    pause()


# ==============================================
# Main Menu
# ==============================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    load_data()

    while True:
        clear_screen()
        print("\n====== Hami MiniMarket Inventory System ======")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Calculate Total Value")
        print("5. Search Product")
        print("6. Delete Product")
        print("7. Undo Last Change")
        print("8. Export to CSV")
        print("9. Exit")
        print("==============================================")

        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            update_product()
        elif choice == "4":
            calculate_total_value()
        elif choice == "5":
            search_product()
        elif choice == "6":
            delete_product()
        elif choice == "7":
            undo_last_change()
        elif choice == "8":
            export_to_csv()
        elif choice == "9":
            save_data()
            print("👋 Exiting program. Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please enter a number between 1 and 9.")
            pause()


if __name__ == "__main__":
    main()
