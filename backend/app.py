# Import necessary modules
from flask import Flask, request, jsonify, render_template_string
import os
import psycopg2

# Initialize Flask app
app = Flask(__name__)

# Get the backend service IP address from environment variable
backend_service_ip = os.getenv("BACKEND_SERVICE_IP")

# Database connection setup
DATABASE_URL = (
    f"dbname='{os.getenv('DB_NAME', 'myappdbs')}' "
    f"user='{os.getenv('DB_USER', 'rajat')}' "
    f"password='{os.getenv('DB_PASSWORD', 'Rajat@123')}' "
    f"host='{os.getenv('DB_HOST', '35.238.207.154')}'"
)

# Function to establish database connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Create a new record in the database
@app.route('/create-record', methods=['POST'])
def create_record():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Get data from request
    data = request.form
    # Insert data into database
    cursor.execute("INSERT INTO users (id, username, email) VALUES (%s, %s, %s)", (data['id'], data['username'], data['email']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Record created successfully'})

# Read records from the database
@app.route('/read-records', methods=['GET'])
def read_records():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    # Format records as JSON
    result = [{'id': record[0], 'username': record[1], 'email': record[2]} for record in records]
    return jsonify(result)

# Update a record in the database
@app.route('/update-record/<int:id>', methods=['PUT'])
def update_record(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Get data from request
    data = request.form
    # Update record in database
    cursor.execute("UPDATE users SET username = %s, email = %s WHERE id = %s", (data['username'], data['email'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Record updated successfully'})

# Delete a record from the database
@app.route('/delete-record/<int:id>', methods=['DELETE'])
def delete_record(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Delete record from database
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Record deleted successfully'})

# Define a route to display the HTML form
@app.route('/')
def index():
    return render_template_string('index.html')


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
