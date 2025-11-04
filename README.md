
# Hami MiniMarket Inventory System

# Overview
Hami MiniMarket System is a Python-based console application that manages a small retail store’s inventory, orders, and user accounts with built-in security, data recovery, and automation features.

This project was created as part of a Python Development Track, focusing on practical applications of file handling, loops, conditional logic, and clean code structuring.

---

# Idea Behind the Project
Small stores often rely on notebooks or memory to track stock, which leads to confusion, lost data, and inaccurate stock records.  
This system solves that by providing a simple, offline, and beginner-friendly inventory manager that:
- Process and edit orders 🛒
- Automatically generate receipts 🧾
- Protect data with user accounts and recovery options 🔐
- Reset or restart the system safely ⚙️

---

# Features and Their Explanations
# 🧍 User Account & Security
- Create New Account – Register new users directly from the login screen.
- Login System – Secure login for each user.
- Forgot Password / Recovery
  - Uses security questions if available.
  - If not, challenges the user with fake product or fake feature quiz.
  - Escalating lock-out timer for repeated failures (5 min → 10 min → 30 min → 1 h → 8 h → … → century 😅).
- Manage Account Menu
  - Change password instantly.
  - Add or update security questions.
  - View account info.
- Erase All Data
  - Deletes every record (users, inventory, orders, receipts) and starts fresh.

# 📦 Inventory Management
- Add Products with name, category, price, and quantity.
- Update Products professionally (clean summary layout).
- Delete Products safely with confirmation.
- Undo Last Change for accidental edits.
- Search Products by name (shows full details).
- Low Stock Alerts
  - 🔴 Below 20 → Low
  - 🟡 20–99 → Moderate
  - 🟢 100 + → Good Stock
- Export Inventory to JSON (with cancel option).

# 🧾 Order Management
- Create Orders
  - View available products and add to cart. 
  - Optional 10 % discount for orders > $20.
  - Calculates subtotal, tax (5 %), discount, and total.
  - Generates text receipt file automatically.
- Order Management Menu
```
1. View Orders
2. Modify Order
3. Delete Order
4. Back
```
- Modify or Delete Orders
  - Shows order summaries (ID, user, date, products, total).
  - Allows edits within 1 hour of creation.
  - Displays time left or marks as Expired.
  - Updates or deletes receipt files automatically.
  - Automatic Cleanup of expired orders (if enabled).

# ⚙️ System Management
- Erase-All Function on both Login & Account menus.
- Instant Data Refresh – password or data changes apply immediately.
- Cancel Option in every major action.
- Auto Initialization – creates default admin (admin / 1234) on first run.

---
   
# How to Use (Step-by-Step)

# Setup
1. Make sure you have Python 3 installed.  
   To check, open a terminal or command prompt and run:
   ```bash
   python --version
   ```
2. Download or copy the file `Hamiminimarket.py` to your computer.
3. (Optional) Open it with any code editor like VS Code, PyCharm, or IDLE if you want to view or edit it.

---

# Running the Program
1. Open your terminal in the folder containing the file.  
2. Run the script:
   ```bash
   python main.py
   ```
3. Choose from login menu:
   ```
   1. Login
   2. Create New Account
   3. Forgot Password
   4. Erase All Data & Start Fresh
   5. Exit
   ```
4. Once logged in you will see:
   ```
   1. View Inventory
   2. Manage Inventory
   3. Make New Order
   4. Manage Orders
   5. Export Inventory
   6. Manage Account
   7. Exit
   ```
---

# Examples

# Creating an Order
```
Available products:
1. Milk - $10.0 (1000 in stock)
2. Mango - $1.0 (1000 in stock)

Enter product name to add (or 'done'): Milk
Enter quantity (available 1000): 4
✅ Added 4 x Milk to cart.

Enter product name to add (or 'done'): done
Apply 10% discount for orders over $20.0? (y/n): y

Order summary:
Subtotal: $40.00
Tax (5%): $2.00
Discount: $4.00
Total: $38.00

Confirm order and reduce inventory? (y/n): y
✅ Receipt saved: receipts/receipt_admin_2025-11-03_10-35-01.txt
```

---

# Password Recovery(no security questions)
```
Select the product that is NOT in stock:
1. Mango
2. Milk
3. Peach
Your choice (1-3): 3
✅ Password reset successful!
```

---

# File Structure
```
HamiMiniMarket/
│
├── main.py           # Main controller with helpers & account logic
├── inventory.py      # Inventory handling
├── order.py          # Order & receipt management
│
├── users.json        # Saved user accounts
├── inventory.json    # Product data
├── orders.json       # Order records
└── receipts/         # Generated receipts (text files)
```

# Tech Stack
- Python 3    
- JSON → for saving and loading data
- File system operations → for receipt & reset

---

# 🧩 Future Improvements
- Multi-user roles (Admin, Cashier, Viewer)
- Graphical UI using Tkinter or PyQt
- Database backend (SQLite/MySQL)
- Daily sales summary reports
