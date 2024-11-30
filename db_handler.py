import psycopg2
from psycopg2 import sql

# Database connection parameters (use your own credentials)
DB_HOST = 'aws-0-ca-central-1.pooler.supabase.com'
DB_PORT = '6543'  # Default PostgreSQL port
DB_NAME = 'postgres'
DB_USER = 'postgres.rjwrbpwguwojbcmhsvbc'
DB_PASSWORD = 'FridgeFriend122'

# Function to establish a database connection
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def init_db():
    """Initialize the PostgreSQL database with a table."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS foods (
        id SERIAL PRIMARY KEY,
        name TEXT,
        expiration_date TEXT
    )
    ''')
    conn.commit()
    conn.close()

def add_food(name, expiration_date):
    """Insert a new food item into the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO foods (name, expiration_date) VALUES (%s, %s)', (name, expiration_date))
    conn.commit()
    conn.close()

def get_all_foods(sort_by='date'):
    """Retrieve all food items from the database."""
    conn = connect_db()
    cursor = conn.cursor()

    if sort_by == 'expiration_date':
        query = 'SELECT name, expiration_date FROM foods ORDER BY expiration_date ASC'
    else:  # Default to sorting by date added
        query = 'SELECT name, expiration_date FROM foods ORDER BY id ASC'
    
    cursor.execute(query)
    foods = cursor.fetchall()
    conn.close()
    return foods

def delete_food_by_name(name):
    """Delete a food item from the database by its name."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM foods WHERE name = %s', (name,))
    conn.commit()
    conn.close()

def get_top_3_expiring_foods():
    """Retrieve the top 3 foods with the closest expiration dates."""
    conn = connect_db()
    cursor = conn.cursor()

    # Query to fetch the top 3 foods with the closest expiration dates, ordered by expiration_date
    query = 'SELECT name, expiration_date FROM foods ORDER BY expiration_date ASC LIMIT 3'
    cursor.execute(query)
    foods = cursor.fetchall()
    conn.close()
    
    return foods