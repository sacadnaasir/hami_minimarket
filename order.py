# Importing modules for file handling and JSON data operations
import json, os
from datetime import datetime, timedelta
from inventory import inventory, save_data, pause, get_valid_number

ORDERS_FILE = "orders.json"
RECEIPTS_DIR = "receipts"
TAX_RATE = 0.05
DISCOUNT_THRESHOLD = 20.0
DISCOUNT_RATE = 0.10
MODIFY_WINDOW_MINUTES = 60
os.makedirs(RECEIPTS_DIR, exist_ok=True)

def save_orders(orders):
    with open(ORDERS_FILE,"w",encoding="utf-8") as f:
        json.dump(orders,f,indent=2,ensure_ascii=False)

def load_orders():
    if not os.path.exists(ORDERS_FILE): return []
    with open(ORDERS_FILE,"r",encoding="utf-8") as f:
        data=json.load(f)
        for o in data:
            o["subtotal"]=float(o.get("subtotal",0))
            o["tax"]=float(o.get("tax",0))
            o["discount"]=float(o.get("discount",0))
            o["total"]=float(o.get("total",0))
        return data

def now_str(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def now_for_filename(): return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
def is_expired(ts): return datetime.now()-datetime.strptime(ts,"%Y-%m-%d %H:%M:%S") >= timedelta(minutes=MODIFY_WINDOW_MINUTES)
def minutes_remaining(ts): return max(0,int(MODIFY_WINDOW_MINUTES - (datetime.now()-datetime.strptime(ts,"%Y-%m-%d %H:%M:%S")).total_seconds()//60))

def next_order_id(orders):
    if not orders: return "ORD_001"
    nums=[int(o["order_id"].split("_")[1]) for o in orders if "_" in o.get("order_id","") and o["order_id"].split("_")[1].isdigit()]
    return f"ORD_{max(nums)+1:03d}" if nums else "ORD_001"

def write_receipt(order):
    path=os.path.join(RECEIPTS_DIR,order["receipt_file"])
    with open(path,"w",encoding="utf-8") as f:
        f.write("Hami MiniMarket - Receipt\n")
        f.write(f"Order ID: {order['order_id']}\nUser: {order['username']}\nTimestamp: {order['timestamp']}\n\n")
        f.write(f"{'Name':<15}{'Qty':<6}{'Price':<10}{'Line':<12}\n"); f.write("-"*50+"\n")
        for i in order["products"]:
            f.write(f"{i['name']:<15}{i['quantity']:<6}{i['price']:<10.2f}{i['price']*i['quantity']:<12.2f}\n")
        f.write("-"*50+"\n")
        f.write(f"Subtotal: ${order['subtotal']:.2f}\nTax: ${order['tax']:.2f}\nDiscount: ${order['discount']:.2f}\nTotal: ${order['total']:.2f}\n")
    return path

def make_order(username):
    orders=load_orders(); cart=[]
    if not inventory: print("No products."); pause(); return
    print("Available products:")
    for i,p in enumerate(inventory,1): print(f"{i}. {p['name']} - ${p['price']} ({p['quantity']} in stock)")
    while True:
        name=input("Enter product name to add (or 'done'/'cancel'): ").strip()
        if name.lower()=="done": break
        if name.lower()=="cancel": print("Cancelled."); return
        prod=next((p for p in inventory if p['name'].lower()==name.lower()),None)
        if not prod: print("Not found."); continue
        qty=get_valid_number(f"Enter quantity (available {prod['quantity']}): ", is_int=True)
        if qty=="cancel": return
        if qty>prod['quantity']: print("Not enough stock."); continue
        cart.append({'name':prod['name'],'price':prod['price'],'quantity':qty}); print(f"Added {qty} x {prod['name']}")
    if not cart: print("Empty order."); pause(); return
    subtotal=sum(i['price']*i['quantity'] for i in cart); tax=subtotal*TAX_RATE; disc=0.0
    if subtotal>DISCOUNT_THRESHOLD and input(f"Apply {int(DISCOUNT_RATE*100)}% discount? (y/n): ").strip().lower()=="y": disc=subtotal*DISCOUNT_RATE
    total=subtotal+tax-disc; print(f"Subtotal:${subtotal:.2f}\nTax:${tax:.2f}\nDiscount:${disc:.2f}\nTotal:${total:.2f}")
    if input("Confirm order and reduce inventory? (y/n): ").strip().lower()!="y": print("Cancelled."); pause(); return
    for item in cart:
        for p in inventory:
            if p['name'].lower()==item['name'].lower(): p['quantity']-=item['quantity']; break
    save_data()
    order={'order_id':next_order_id(orders),'username':username,'products':cart,'subtotal':subtotal,'tax':tax,'discount':disc,'total':total,'timestamp':now_str(),'receipt_file':f"receipt_{username}_{now_for_filename()}.txt"}
    orders.append(order); save_orders(orders); path=write_receipt(order); print(f"Receipt saved: {path}"); pause()

def view_orders():
    orders=load_orders()
    if not orders: print("No orders."); pause(); return
    for o in orders:
        print(f"\nID:{o['order_id']} | User:{o['username']} | Date:{o['timestamp']} | Total:${o['total']:.2f}")
        if is_expired(o['timestamp']): print("Status: Expired (cannot modify)")
        else: print(f"Time left: {minutes_remaining(o['timestamp'])} minutes")

def list_orders_summary():
    orders=load_orders()
    if not orders: print("No orders."); pause(); return []
    print("--- Existing Orders ---")
    for o in orders:
        prod_names = ", ".join([p['name'] for p in o.get('products',[])][:5])
        print(f"ID:{o['order_id']} | User:{o.get('username')} | Date:{o.get('timestamp')} | Products:{prod_names} | Total:${o.get('total',0):.2f}")
    return orders

def find_order_by_id(orders, oid): return next((o for o in orders if o['order_id']==oid), None)

def modify_order():
    orders=load_orders()
    if not orders: print("No orders."); pause(); return
    list_orders_summary()
    oid=input("Enter Order ID to modify (or 'cancel'): ").strip()
    if oid.lower()=="cancel" or not oid: print("Cancelled."); pause(); return
    o=find_order_by_id(orders, oid)
    if not o: print("Not found."); pause(); return
    if is_expired(o['timestamp']): print("Expired - cannot modify."); pause(); return
    for idx,i in enumerate(o['products'],1): print(f"{idx}. {i['name']} | Qty:{i['quantity']} | Price:${i['price']:.2f}")
    action=input("Type 'edit' to change quantity, 'delete' to cancel entire order, or 'cancel': ").lower()
    if action=="cancel": print("Cancelled."); pause(); return
    if action=="delete":
        if input("Confirm deletion (y/n): ").lower()=="y":
            for item in o['products']:
                for p in inventory:
                    if p['name'].lower()==item['name'].lower(): p['quantity']+=item['quantity']
            path=os.path.join(RECEIPTS_DIR,o['receipt_file'])
            if os.path.exists(path): os.remove(path)
            orders=[x for x in orders if x['order_id']!=oid]; save_orders(orders); save_data(); print("Order deleted."); pause(); return
        else: print("Cancelled."); pause(); return
    if action=="edit":
        idx_choice=get_valid_number("Enter item number to edit (or 'cancel'): ", is_int=True)
        if idx_choice=="cancel": print("Cancelled."); pause(); return
        if idx_choice<1 or idx_choice>len(o['products']): print("Invalid."); pause(); return
        item=o['products'][idx_choice-1]; print(f"Selected {item['name']} (current qty {item['quantity']})")
        new_qty=get_valid_number("Enter new quantity (leave blank to keep): ", allow_blank=True, is_int=True)
        if new_qty=="cancel": print("Cancelled."); pause(); return
        if new_qty is None: print("No change."); pause(); return
        for p in inventory:
            if p['name'].lower()==item['name'].lower():
                p['quantity'] += item['quantity']
                if new_qty > p['quantity']: print("Not enough stock."); p['quantity'] -= item['quantity']; pause(); return
                p['quantity'] -= new_qty; break
        item['quantity']=new_qty
        subtotal = sum(it['price']*it['quantity'] for it in o['products'])
        o['subtotal']=subtotal; o['tax']=subtotal*TAX_RATE; o['discount']=subtotal*DISCOUNT_RATE if subtotal>DISCOUNT_THRESHOLD else 0.0
        o['total']=o['subtotal']+o['tax']-o['discount']; o['timestamp']=now_str(); write_receipt(o); save_orders(orders); save_data(); print("Order updated."); pause(); return

def cleanup_expired_orders():
    orders=load_orders(); expired=[o for o in orders if is_expired(o['timestamp'])]
    if not expired: print("No expired."); pause(); return
    for o in expired:
        path=os.path.join(RECEIPTS_DIR,o['receipt_file'])
        if os.path.exists(path): os.remove(path)
        for item in o['products']:
            for p in inventory:
                if p['name'].lower()==item['name'].lower(): p['quantity']+=item['quantity']
    remaining=[o for o in orders if not is_expired(o['timestamp'])]; save_orders(remaining); save_data(); print(f"Cleaned {len(expired)} expired orders."); pause()
