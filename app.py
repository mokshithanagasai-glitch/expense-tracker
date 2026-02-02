import tkinter as tk
import sqlite3
from tkinter import ttk

# ---------- DATABASE ----------
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exp_date TEXT,
    category TEXT,
    amount REAL
)
""")
conn.commit()

# ---------- GUI WINDOW ----------
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("500x400")

# ---------- INPUT FIELDS ----------
tk.Label(root, text="Date").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Category").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

# ---------- TABLE ----------
table_frame = tk.Frame(root)
table_frame.pack(pady=20)

columns = ("ID", "Date", "Category", "Amount")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack()

# ---------- FUNCTIONS ----------
def load_expenses():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM expenses")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def show_data():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()

    try:
        amount = float(amount)
    except ValueError:
        print("Amount must be a number")
        return

    cursor.execute(
        "INSERT INTO expenses (exp_date, category, amount) VALUES (?, ?, ?)",
        (date, category, amount)
    )
    conn.commit()
    load_expenses()

    print("Expense saved!")

    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# ---------- BUTTON ----------
tk.Button(root, text="Add Expense", command=show_data).pack()

# ---------- START ----------
load_expenses()
root.mainloop()
conn.close()
