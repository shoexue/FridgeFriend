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
    """Drop and recreate the PostgreSQL database table."""
    print("Dropping and recreating the table...")
    conn = connect_db()
    cursor = conn.cursor()
    
    # # Drop the table if it exists
    # cursor.execute('DROP TABLE IF EXISTS foods;')
    
    # Create the table with the correct schema
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS foods (
        id SERIAL PRIMARY KEY,
        name TEXT,
        when_added DATE DEFAULT CURRENT_DATE,
        expiration_date TEXT
    );
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
        query = 'SELECT name, when_added, expiration_date FROM foods ORDER BY expiration_date ASC'
    else:  # Default to sorting by date added
        query = 'SELECT name, when_added, expiration_date FROM foods ORDER BY when_added ASC'  # Sort by when_added column
    
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
    query = 'SELECT name FROM foods ORDER BY expiration_date ASC LIMIT 3'
    cursor.execute(query)
    foods = cursor.fetchall()
    conn.close()
    
    return foods

def edit_food_expiration(name, new_expiration_date):
    """Update the expiration date of a food item in the database."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Update the expiration_date for the given food name
    cursor.execute(
        'UPDATE foods SET expiration_date = %s WHERE name = %s',
        (new_expiration_date, name)
    )
    
    # Check if any rows were affected
    if cursor.rowcount == 0:
        print(f"No food item found with name: {name}")
    else:
        print(f"Expiration date for '{name}' updated to {new_expiration_date}")
    
    conn.commit()
    conn.close()
