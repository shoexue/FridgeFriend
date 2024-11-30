import sqlite3

DB_NAME = 'foods.db'

def init_db():
    print("hi\n")
    """Initialize the SQLite database with a table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS foods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        expiration_date TEXT
    )
    ''')
    conn.commit()
    conn.close()

def add_food(name, expiration_date):
    """Insert a new food item into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO foods (name, expiration_date) VALUES (?, ?)', (name, expiration_date))
    conn.commit()
    conn.close()

def get_all_foods():
    """Retrieve all food items from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name, expiration_date FROM foods')
    foods = cursor.fetchall()
    conn.close()
    return foods

def delete_food_by_name(name):
    """Delete a food item from the database by its name."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM foods WHERE name = ?', (name,))
    conn.commit()
    conn.close()
