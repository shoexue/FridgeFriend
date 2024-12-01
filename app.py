from flask import Flask, request, render_template, jsonify
from scanner import scan_image
from db_handler import *
import base64
from io import BytesIO

app = Flask(__name__)

# Initialize the database
init_db()

from datetime import datetime

@app.route('/')
def index():
    """Render the table with all food data."""
    
    sort_by = request.args.get('sort_by', 'date_added')  # Default to sorting by 'date_added' if no parameter is provided
    foods = get_all_foods(sort_by)
    
    # Calculate the days left until expiration for each food item
    current_date = datetime.now()
    
    # Assuming each 'food' in 'foods' is a tuple with (food_name, date_added, expiration_date)
    # Modify each item in 'foods' to include days_left
    updated_foods = []
    for food in foods:
        food_name, date_added, expiration_date = food
        
        # Parse the expiration date (assuming it's in 'YYYY-MM-DD' format)
        expiration_date_obj = datetime.strptime(expiration_date, '%Y-%m-%d')
        
        # Calculate days left until expiration
        days_left = (expiration_date_obj - current_date).days
        
        # Add the days_left to the food tuple
        updated_foods.append((food_name, date_added, expiration_date, days_left))
    
    # Render the updated list to the template
    return render_template('home.html', foods=updated_foods, sort_by=sort_by)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    food_name = data.get('name', 'Unknown Food')
    image_data = data.get('image')
    
    if not image_data:
        return jsonify({'error': 'No image provided'}), 400

    base64_str = image_data.split(",")[1]
    image_bytes = base64.b64decode(base64_str)

        # Save the image to a file
    image_path = f"{food_name.replace(' ', '_').lower()}.png"
    with open(image_path, "wb") as image_file:
        image_file.write(image_bytes)


    # Call your scan_image function (if required) and add to the database
    expiration_date = scan_image(image_path)  # Process image to get expiration date

    if not expiration_date:
        expiration_date = "Unknown"  # Default fallback value
        # Optionally log or notify the user about the failure
        print(f"Failed to process expiration date for {food_name}")

        return jsonify({
            'message': 'expiration date could not be determined.',
            'name': food_name,
            'expiration_date': expiration_date
        }), 202  # HTTP 202 Accepted

    add_food(food_name, expiration_date)  # Add to the database

    return jsonify({
        'message': 'Food item added successfully!', 
        'name': food_name, 
        'expiration_date': expiration_date})

@app.route('/delete', methods=['DELETE'])
def delete():
    """Endpoint to delete a food item by its name."""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'No name provided'}), 400

    food_name = data['name']
    delete_food_by_name(food_name)  # Assuming delete_food_by_name is defined in db_handler

    return jsonify({'message': f'Food item "{food_name}" deleted successfully!'})

@app.route('/edit', methods=['PUT'])
def edit():
    """Endpoint to edit the expiration date of a food item by its name."""
    data = request.get_json()
    if not data or 'name' not in data or 'expiration_date' not in data:
        return jsonify({'error': 'Name or expiration date not provided'}), 400

    food_name = data['name']
    new_expiration_date = data['expiration_date']
    try:
        edit_food_expiration(food_name, new_expiration_date)
        return jsonify({'message': f'Expiration date for "{food_name}" updated to "{new_expiration_date}" successfully!'})
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    


@app.route('/recipe')
def top_expiring():
    """Display the top 3 expiring foods."""
    foods = get_top_3_expiring_foods()
    print(foods)

    if not foods:
        return jsonify({'ERROR': 'no foods found'})
    
    food_names = [food[0] for food in foods]
    prompt = "Give me 3 recipes with "+ ','.join(food_names)+" with their names, prep time and which kind of cuisines they are from."
    

    response = jsonify({
        'prompt': prompt,
        'foods' : food_names
    })
    response.headers['Content-Type'] = 'application/json'

    return response



@app.route('/reset', methods=['POST'])
def reset_table():
    """Drop and recreate the table through a POST request."""
    print("Resetting the table...")
    conn = connect_db()
    cursor = conn.cursor()
    
    # Drop the table if it exists
    cursor.execute('DROP TABLE IF EXISTS foods;')
    
    # Recreate the table
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
    
    return jsonify({"message": "Table reset successfully!"}), 200


if __name__ == '__main__':
    app.run(debug=True)

