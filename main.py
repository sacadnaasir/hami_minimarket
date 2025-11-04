#Importing necessary Python modules for file handling, random generation, timing, and system operations
import os, json, random, shutil, time
#import inventory and order modules from the project folder
import inventory, order  

USERS_FILE = "users.json"

# ------------------ Utility helpers ------------------
def pause(): input("\nPress Enter to continue...")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def load_users():
    if not os.path.exists(USERS_FILE): return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def get_user(username, users): 
    return next((u for u in users if u["username"].lower()==username.lower()), None)

def init_system():
    """Initialize data files if missing or empty."""
    users = []
    # Load existing users if possible
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
                if not isinstance(users, list):  # corrupted file
                    users = []
        except (json.JSONDecodeError, IOError):
            users = []

    # If no users found, create default admin
    if not users:
        users = [{"username": "admin", "password": "1234", "security": [], "lock_until": 0}]
        save_users(users)
        print("✅ Default admin created (admin / 1234)")
        print("💡 You can manage your account in the 'User Management' option.\n")

    # Initialize other system files and folders
    if not os.path.exists(inventory.INVENTORY_FILE):
        with open(inventory.INVENTORY_FILE, "w") as f:
            json.dump([], f)
    if not os.path.exists(order.ORDERS_FILE):
        with open(order.ORDERS_FILE, "w") as f:
            json.dump([], f)
    os.makedirs(order.RECEIPTS_DIR, exist_ok=True)

# ------------------ Security & Recovery ------------------
SECURITY_QUESTIONS = [
    "What is your favorite color?",
    "What city were you born in?",
    "What is your favorite animal?",
    "What was your first school?",
    "What is your mother's maiden name?"
]

FAKE_FEATURES = [
    "Teleport Products", "AI Product Designer", "Space Delivery Mode",
    "Predict Customer Mood", "Auto Clone Receipt", "Voice-Based Shopping"
]

FAKE_PRODUCTS = [
    "Peach", "Pineapple", "Kiwi", "Cucumber", "Avocado",
    "Tomato", "Pear", "Guava", "Pumpkin", "Radish"
]

lock_durations = [5*60, 10*60, 30*60, 60*60, 8*3600, 24*3600, 7*86400, 30*86400, 365*86400, 10*365*86400, 100*365*86400]

def get_lock_time(user):
    return user.get("lock_until",0)

def lock_user(user):
    user.setdefault("fail_count",0)
    user["fail_count"] += 1
    lock_seconds = lock_durations[min(user["fail_count"]-1, len(lock_durations)-1)]
    user["lock_until"] = time.time() + lock_seconds
    return lock_seconds

def unlock_user(user):
    user["lock_until"] = 0
    user["fail_count"] = 0

def generate_fruit_challenge():
    inventory.load_data()
    real = [p["name"] for p in inventory.inventory]
    if len(real) < 2:
        return None
    in_stock = random.sample(real, 2)
    fake_candidates = [f for f in FAKE_PRODUCTS if f not in real]
    fake = random.choice(fake_candidates) if fake_candidates else random.choice(FAKE_PRODUCTS)
    options = in_stock + [fake]
    random.shuffle(options)
    return options, fake

def generate_feature_challenge():
    real_feats = [
        "View Inventory", "Manage Inventory", "Make New Order",
        "View/Modify/Delete Orders", "Export Inventory", "Manage Account"
    ]
    fake = random.choice(FAKE_FEATURES)
    options = random.sample(real_feats, 2) + [fake]
    random.shuffle(options)
    return options, fake

def password_reset_flow(users):
    username = input("Enter your username (or 'cancel'): ").strip()
    if username.lower()=="cancel": print("Cancelled."); return
    user = get_user(username, users)
    if not user: print("User not found."); pause(); return
    if time.time() < user.get("lock_until",0):
        remain=int((user["lock_until"]-time.time())//60)
        print(f"Account locked. Try again in {remain} minutes."); pause(); return

    if user.get("security"):
        print("Answer your security questions:")
        correct=0
        for q in user["security"]:
            ans=input(f"{q['question']}: ").strip().lower()
            if ans == q["answer"].lower(): correct+=1
        if correct==len(user["security"]):
            new_pass=input("Enter new password: ").strip()
            user["password"]=new_pass; unlock_user(user); save_users(users)
            print("✅ Password reset successful! You can now log in."); pause(); return
        else:
            secs=lock_user(user); save_users(users)
            print(f"Incorrect. Locked for {secs//60} minutes."); pause(); return

    # No security Qs
    challenge = generate_fruit_challenge()
    if challenge:
        options, fake = challenge
        print("\nSelect the product that is NOT in stock:")
        for i,opt in enumerate(options,1): print(f"{i}. {opt}")
        ch=input("Your choice (1-3): ").strip()
        if ch in ["1","2","3"] and options[int(ch)-1]==fake:
            new_pass=input("Enter new password: ").strip()
            user["password"]=new_pass; unlock_user(user); save_users(users)
            print("✅ Password reset successful!"); pause(); return
        else:
            secs=lock_user(user); save_users(users)
            print(f"Incorrect. Locked for {secs//60} minutes."); pause(); return
    else:
        # fallback feature challenge
        options, fake = generate_feature_challenge()
        print("\nSelect the fake feature:")
        for i,opt in enumerate(options,1): print(f"{i}. {opt}")
        ch=input("Your choice (1-3): ").strip()
        if ch in ["1","2","3"] and options[int(ch)-1]==fake:
            new_pass=input("Enter new password: ").strip()
            user["password"]=new_pass; unlock_user(user); save_users(users)
            print("✅ Password reset successful!"); pause(); return
        else:
            secs=lock_user(user); save_users(users)
            print(f"Incorrect. Locked for {secs//60} minutes."); pause(); return

def erase_all_data_flow(logged_in=False):
    print("\n⚠️ WARNING: This will permanently delete all users, inventory, orders, and receipts.")
    confirm=input("Type 'YES' to confirm or 'cancel' to abort: ").strip()
    if confirm.lower()=="cancel":
        if logged_in: print("Operation cancelled. Returning to menu...")
        else: print("Cancelled.")
        pause(); return
    if confirm!="YES": print("Cancelled."); pause(); return
    for f in [USERS_FILE, inventory.INVENTORY_FILE, order.ORDERS_FILE]:
        if os.path.exists(f): os.remove(f)
    if os.path.exists(order.RECEIPTS_DIR): shutil.rmtree(order.RECEIPTS_DIR)
    init_system()
    print("✅ System restarted successfully.")
    pause()

# ------------------ Account Management ------------------
def manage_account(user, users):
    while True:
        clear_screen()
        print("--- User Account Management ---")
        print("1. Change Password")
        print("2. Set/Update Security Questions")
        print("3. View My Info")
        print("4. Erase All Data & Start Fresh")
        print("5. Back")
        c=input("Choose (1-5): ").strip()
        if c=="1":
            old=input("Enter old password: ").strip()
            if old!=user["password"]: print("Incorrect password."); pause(); continue
            new=input("Enter new password: ").strip()
            user["password"]=new; save_users(users)
            print("✅ Password changed."); pause()
        elif c=="2":
            print("Choose two security questions:")
            for i,q in enumerate(SECURITY_QUESTIONS,1): print(f"{i}. {q}")
            qs=[]
            for i in range(2):
                idx=input(f"Select question {i+1}: ").strip()
                if not idx.isdigit() or not (1<=int(idx)<=len(SECURITY_QUESTIONS)): print("Invalid."); break
                ans=input("Your answer: ").strip()
                qs.append({"question":SECURITY_QUESTIONS[int(idx)-1],"answer":ans.lower()})
            if len(qs)==2:
                user["security"]=qs; save_users(users); print("✅ Saved security questions.")
            pause()
        elif c=="3":
            print(f"Username: {user['username']}")
            print(f"Has security questions: {'Yes' if user.get('security') else 'No'}")
            pause()
        elif c=="4":
            erase_all_data_flow(logged_in=True)
        elif c=="5": return
        else: print("Invalid."); pause()

# ------------------ Main Menu ------------------
def main_menu(user):
    while True:
        clear_screen()
        if not user.get("security"):
            print("⚠️ Add security questions in User Management for easier password recovery.\n")
        print("====== Hami MiniMarket System ======")
        print("1. View Inventory")
        print("2. Manage Inventory (Add/Update/Delete/Undo/Search)")
        print("3. Make New Order")
        print("4. View/Modify/Delete Orders")
        print("5. Export Inventory")
        print("6. Manage Account")
        print("7. Logout")
        print("====================================")
        choice=input("Choose (1-7): ").strip()
        if choice=="1": inventory.view_products()
        elif choice=="2":
            while True:
                clear_screen()
                print("--- Inventory Management ---")
                print("1. Add Product\n2. Update Product\n3. Delete Product\n4. Undo Last Change\n5. Search Product\n6. Back")
                sub=input("Choose (1-6): ").strip()
                if sub=="1": inventory.add_product()
                elif sub=="2": inventory.update_product()
                elif sub=="3": inventory.delete_product()
                elif sub=="4": inventory.undo_last_change()
                elif sub=="5": inventory.search_product()
                elif sub=="6": break
                else: print("Invalid."); pause()
        elif choice=="3": order.make_order(user["username"])
        elif choice=="4":
            while True:
                clear_screen()
                print("--- Order Management ---")
                print("1. View Orders")
                print("2. Modify Order")
                print("3. Delete Order")
                print("4. Back")
                sub = input("Choose (1-4): ").strip()
                if sub == "1":
                    order.view_orders()
                elif sub == "2":
                    order.modify_order()
                elif sub == "3":
                    order.modify_order()  # internally supports delete choice
                elif sub == "4":
                    break
                else:
                    print("Invalid option.")
                    pause()

        elif choice=="5":
            name=input("Enter export filename (or 'cancel'): ").strip()
            if name.lower()=="cancel" or not name: print("Cancelled."); pause(); continue
            data=inventory.inventory
            with open(name if name.endswith(".json") else name+".json","w",encoding="utf-8") as f:
                json.dump(data,f,indent=2)
            print(f"✅ Exported to {name}.json"); pause()
        elif choice=="6": manage_account(user, load_users())
        elif choice=="7": print("Goodbye!"); break
        else: print("Invalid."); pause()

# ------------------ Login ------------------
def login_flow():
    users = load_users()
    while True:
        clear_screen()
        print("====== Welcome to Hami MiniMarket ======")
        print("1. Login")
        print("2. Create New Account")
        print("3. Forgot Password")
        print("4. Erase All Data & Start Fresh")
        print("5. Exit")
        ch = input("Choose (1-5): ").strip()

        if ch == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            u = get_user(username, users)
            if not u or u["password"] != password:
                print("Invalid credentials."); pause(); continue
            if time.time() < u.get("lock_until", 0):
                print("Account locked temporarily."); pause(); continue
            unlock_user(u); save_users(users)
            inventory.load_data()
            main_menu(u)

        elif ch == "2":
            # Create New Account
            print("--- Create New Account ---")
            while True:
                username = input("Choose a username (or 'cancel'): ").strip()
                if username.lower() == "cancel": print("Cancelled."); pause(); break
                if not username:
                    print("Username cannot be blank."); continue
                if get_user(username, users):
                    print("Username already taken."); continue
                password = input("Choose a password: ").strip()
                if not password:
                    print("Password cannot be blank."); continue
                new_user = {"username": username, "password": password, "security": [], "lock_until": 0}
                users.append(new_user)
                save_users(users)
                print("✅ Account created successfully!")
                print("💡 You can manage your account and add security questions later from User Management.")
                pause()
                break

        elif ch == "3":
            password_reset_flow(users)

        elif ch == "4":
            erase_all_data_flow(logged_in=False)

        elif ch == "5":
            print("Exiting..."); break

        else:
            print("Invalid."); pause()

# ------------------ Entry ------------------
if __name__=="__main__":
    init_system()
    login_flow()

