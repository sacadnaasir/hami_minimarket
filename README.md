
# Hami MiniMarket Inventory System

# Overview
The Hami MiniMarket Inventory System is a Python-based console application designed to help small shop owners or store managers track, organize, and manage their inventory efficiently.  
It allows users to add, update, delete, search, view, and export product data, all saved automatically to a CSV file for easy access in Excel or other spreadsheet tools.

This project was created as part of a Python Development Track, focusing on practical applications of file handling, loops, conditional logic, and clean code structuring.

---

# Idea Behind the Project
Small stores often rely on notebooks or memory to track stock, which leads to confusion, lost data, and inaccurate stock records.  
This system solves that by providing a simple, offline, and beginner-friendly inventory manager that:
- Keeps all products organized in one place.
- Automatically saves data to a file.
- Warns about low stock.
- Supports undoing accidental actions.
- Works perfectly on any computer with Python installed.

It’s built around clarity, reliability, and simplicity — no databases, no installations, just Python and CSV.

---

# Features and Their Explanations

| Feature                           | Description                                                                                |
|-----------------------------------|--------------------------------------------------------------------------------------------|
|  **Add Product**                  |Lets the user add new products (Name and Category required). Validates input for price and quantity. Prevents duplicates and offers to update if item exist|
|  **Update Product**               | Allows editing of any field (name, category, price, quantity). Blank fields mean “no change.” Confirms before saving changes.|
|  **View Products**                | Displays all products neatly in table format, showing stock level indicators: 🔴 Low, 🟡 Moderate, 🟢 Good Stock. Also shows total count, quantity, and value.|
|  **Delete Product**               | Removes a product completely after confirmation. Can be undone later.                      |
|  **Search Product**               | Finds products by part of their name (case-insensitive search).                            |
|  **Calculate Total Value**        | Calculates total worth of all items in stock.                                              |
|  **Save & Load Data (CSV)**       | Automatically saves all products into a `inventory.csv` file and reloads them on next run. |
|  **Export to CSV**                | Lets user export the inventory into a different CSV file (e.g., `export_inventory.csv`).   |
|  **Undo Last Change**             | Reverts the last action (Add, Delete, or Update) to restore data easily.                   |
|  **Cancel Anytime**               | Typing `cancel` during any input safely returns to the menu without breaking anything.     |
|  **Stock Status Alerts**          | Items are categorized by quantity levels:- `< 20` → 🔴 Low Stock - `20–99` → 🟡 Moderate Stock - `≥ 100` → 🟢 Good Stock|
|  **Clean & Non-Repetitive Code**  | The code uses helper functions for validation, cancel checking, pausing, and stock-level evaluation — making it easy to maintain and extend.|


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
   python Hamiminimarket.py
   ```
3. You’ll see a menu like this:
   ```
   ====== Hami MiniMarket Inventory System ======
   1. Add Product
   2. View Products
   3. Update Product
   4. Calculate Total Value
   5. Search Product
   6. Delete Product
   7. Undo Last Change
   8. Export to CSV
   9. Exit
   ==============================================
   ```

---

# Example Usage

# Adding a Product
```
--- Add New Product ---
Enter product name: Mango
Enter category: Fruit
Enter price: 2.5
Enter quantity: 50
✅ Mango added successfully!
💾 You can undo this addition from the main menu.
```

**Result in `inventory.csv`:**
```csv
name,category,price,quantity
Mango,Fruit,2.5,50
```

---

# Updating a Product
```
--- Update Existing Product ---
Enter the product name to update: Mango
New name: Mango
New category: Fruit
New price: 3
New quantity: 60
Save changes? (y/n): y
✅ Product 'Mango' updated successfully!
```

---

# Viewing Products
```
--- Product List ---
Name           Category       Price     Quantity  Status
--------------------------------------------------------------------
Mango          Fruit          3.0       60        🟡 MODERATE STOCK
--------------------------------------------------------------------
📊 Summary: 1 products | Total Qty: 60 | Value: $180.00
```

---

# Deleting a Product
```
--- Delete Product ---
Enter product name to delete: Mango
Are you sure you want to delete 'Mango'? (y/n): y
🗑️ 'Mango' deleted successfully.
```

Undo the deletion:
```
↩️ Deletion of 'Mango' undone.
```

---

# Exporting Inventory
```
Enter filename to export to (default: export_inventory.csv): exported.csv
✅ Inventory exported successfully to 'exported.csv'!
```

---

# Example Input & Output

| Action            | Input                                                  | Output                                 |
|-------------------|--------------------------------------------------------|----------------------------------------|
| Add Product       | Name: Milk<br>Category: Dairy<br>Price: 1.2<br>Qty: 10 | ✅ “Milk added successfully!”          |
| View Products     | (Select 2)                                             | Table showing all items + stock levels |
| Update Product    | New price: 1.5                                         | ✅ “Product updated successfully!”     |
| Delete Product    | Name: Milk                                             | 🗑️ “Milk deleted successfully.”        |
| Undo              | (Select 7)                                             | ↩️ “Deletion of ‘Milk’ undone.”        |
| Export            | Filename: shop_backup.csv                              | ✅ “Inventory exported successfully.”  |


# Behind the Scenes
- The program uses lists and dictionaries to store products.  
- Data is automatically saved and loaded from a CSV file named `inventory.csv`.  
- Input validation ensures no invalid data breaks the program.  
- `undo_last_change()` safely rolls back the most recent operation.

---

# Tech Stack
- Language: Python 3  
- Libraries Used:*  
  - `csv` → for saving and loading data  
  - `os` → for screen clearing  

---

# Conclusion
The Hami MiniMarket Inventory System is a small but powerful inventory management tool for local stores.  
It combines usability, data safety, and simplicity — ideal for small shop owners managing stock efficiently.
