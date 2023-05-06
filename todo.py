import argparse
import sqlite3

DB_NAME = "todo.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
    result = c.fetchone()
    if result:
        print("Table 'items' already exists")
    else:
        c.execute("""CREATE TABLE items (
                        number INTEGER PRIMARY KEY,
                        text TEXT NOT NULL,
                        done INTEGER DEFAULT 0
                    )""")
        conn.commit()
        print("Created table 'items'")
    conn.close()

def add_strikethrough(item):
    return f"\x1b[9m{item}\x1b[0m"

def add_item(item_text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO items (text) VALUES (?)", (item_text,))
    conn.commit()
    conn.close()
    print(f"Added item: {item_text}")

def list_items():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("No items found.")
    else:
        for row in rows:
            item_number, item_text, item_done = row
            if item_done:
                item_text = add_strikethrough(item_text)
            print(f"{item_number}. {item_text}")

def mark_item_done(item_number):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE number = ?", (item_number,))
    row = c.fetchone()
    if not row:
        print("Invalid item number.")
        conn.close()
        return
    item_text = row[1]
    c.execute("UPDATE items SET done = 1 WHERE number = ?", (item_number,))
    conn.commit()
    conn.close()
    print(f"Marked item as done: {item_text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage your to-do list")
    parser.add_argument("action", choices=["add", "list", "done"], help="Action to perform")
    parser.add_argument("--item-text", help="Text of the item to add")
    parser.add_argument("--item-number", type=int, help="Number of the item to mark done")
    args = parser.parse_args()

    create_table()

    if args.action == "add":
        add_item(args.item_text)
    elif args.action == "done":
        mark_item_done(args.item_number)
    elif args.action == "list":
        list_items()