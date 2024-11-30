from flask import Flask, request, render_template, jsonify
from scanner import scan_image
from db_handler import init_db, add_food, get_all_foods, delete_food_by_name
import base64
from io import BytesIO

app = Flask(__name__)

# Initialize the database
init_db()

@app.route('/')
def index():
    """Render the table with all food data."""
    foods = get_all_foods()
    return render_template('index.html', foods=foods)

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
    add_food(food_name, expiration_date)  # Add to the database

    return jsonify({'message': 'Food item added successfully!', 'name': food_name, 'expiration_date': expiration_date})

@app.route('/delete', methods=['DELETE'])
def delete():
    """Endpoint to delete a food item by its name."""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'No name provided'}), 400

    food_name = data['name']
    delete_food_by_name(food_name)  # Assuming delete_food_by_name is defined in db_handler

    return jsonify({'message': f'Food item "{food_name}" deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
