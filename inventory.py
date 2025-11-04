# Importing modules for file handling and JSON data operations
import json, os 
INVENTORY_FILE = "inventory.json"
inventory = []
last_change = None

def pause(): input("\nPress Enter to continue...")

def get_valid_number(prompt, allow_blank=False, is_int=False):
    while True:
        v = input(prompt).strip()
        if v.lower() == "cancel": return "cancel"
        if v == "" and allow_blank: return None
        try:
            return int(v) if is_int else float(v)
        except:
            print("Please enter a valid number or 'cancel'.")

def stock_status(qty):
    if qty < 20: return "🔴 LOW STOCK"
    if qty < 100: return "🟡 MODERATE STOCK"
    return "🟢 GOOD STOCK"

def save_data(filename=INVENTORY_FILE):
    with open(filename,"w",encoding="utf-8") as f:
        json.dump(inventory,f,indent=2,ensure_ascii=False)

def load_data(filename=INVENTORY_FILE):
    global inventory
    inventory.clear()
    if not os.path.exists(filename): return
    with open(filename,"r",encoding="utf-8") as f:
        data = json.load(f)
        for row in data:
            row["price"] = float(row.get("price",0))
            row["quantity"] = int(row.get("quantity",0))
            inventory.append(row)

def add_product():
    global last_change
    print("Add product (type 'cancel' to abort)")
    while True:
        name = input("Name: ").strip()
        if name.lower()=="cancel": print("Cancelled."); return
        if not name: print("Name required."); continue
        break
    for p in inventory:
        if p["name"].lower()==name.lower():
            print("Exists. Use update instead."); return
    while True:
        cat = input("Category: ").strip()
        if cat.lower()=="cancel": print("Cancelled."); return
        if not cat: print("Category required."); continue
        break
    price = get_valid_number("Price: ")
    if price=="cancel": return
    qty = get_valid_number("Quantity: ", is_int=True)
    if qty=="cancel": return
    product={"name":name,"category":cat,"price":price,"quantity":qty}
    inventory.append(product); save_data(); last_change={"action":"add","product":product.copy()}
    print("✅ Added."); pause()

def update_existing_product(product):
    global last_change
    print(f"Updating product: {product['name']}")
    print(f"Category: {product['category']}\nPrice: {product['price']}\nQuantity: {product['quantity']}")
    print("Leave blank to keep current. Type 'cancel' to abort.")
    new_name = input("New name: ").strip()
    if new_name.lower()=="cancel": print("Cancelled."); return
    new_cat = input("New category: ").strip()
    if new_cat.lower()=="cancel": print("Cancelled."); return
    new_price = get_valid_number("New price: ", allow_blank=True)
    if new_price=="cancel": return
    new_qty = get_valid_number("New quantity: ", allow_blank=True, is_int=True)
    if new_qty=="cancel": return
    old=product.copy(); updated=old.copy()
    if new_name: updated["name"]=new_name
    if new_cat: updated["category"]=new_cat
    if new_price is not None: updated["price"]=new_price
    if new_qty is not None: updated["quantity"]=new_qty
    if updated==old:
        print("No changes."); pause(); return
    if input("Save changes? (y/n): ").strip().lower()!="y":
        print("Cancelled."); pause(); return
    product.update(updated); save_data(); last_change={"action":"update","old":old,"new":updated}
    print("✅ Updated."); pause()

def update_product():
    name = input("Enter product name to update (or 'cancel'): ").strip()
    if name.lower()=="cancel" or not name: print("Cancelled."); return
    for p in inventory:
        if p["name"].lower()==name.lower(): update_existing_product(p); return
    print("Not found."); pause()

def view_products():
    if not inventory: print("No products."); pause(); return
    print(f"{'Name':<20}{'Category':<15}{'Price':<10}{'Qty':<8}Status")
    print("-"*70)
    for p in inventory:
        print(f"{p['name']:<20}{p['category']:<15}{p['price']:<10}{p['quantity']:<8}{stock_status(p['quantity'])}")
    pause()

def delete_product():
    global last_change
    name = input("Enter product name to delete (or 'cancel'): ").strip()
    if name.lower()=="cancel" or not name: print("Cancelled."); return
    for p in inventory:
        if p["name"].lower()==name.lower():
            if input(f"Confirm delete {name}? (y/n): ").strip().lower()=="y":
                inventory.remove(p); save_data(); last_change={"action":"delete","product":p.copy()}; print("Deleted.")
            else:
                print("Cancelled.")
            pause(); return
    print("Not found."); pause()

def undo_last_change():
    global last_change
    if not last_change: print("No recent changes."); pause(); return
    a=last_change["action"]
    if a=="add":
        prod=last_change["product"]
        inventory[:] = [p for p in inventory if p['name'].lower()!=prod['name'].lower()]
        print("Undo add.")
    elif a=="delete":
        inventory.append(last_change["product"]); print("Undo delete.")
    elif a=="update":
        old=last_change["old"]
        for i,p in enumerate(inventory):
            if p["name"].lower()==old["name"].lower():
                inventory[i]=old; print("Undo update."); break
    save_data(); last_change=None; pause()

def search_product():
    term = input("Enter search keyword (or 'cancel'): ").strip()
    if term.lower()=="cancel" or not term: print("Cancelled."); return
    found = [p for p in inventory if term.lower() in p["name"].lower()]
    if not found: print("No matches."); pause(); return
    print(f"{'Name':<20}{'Category':<15}{'Price':<10}{'Qty':<8}Status")
    print("-"*70)
    for p in found:
        print(f"{p['name']:<20}{p['category']:<15}{p['price']:<10}{p['quantity']:<8}{stock_status(p['quantity'])}")
    pause()
