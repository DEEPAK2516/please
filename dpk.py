from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create or connect to a SQLite database
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Create a table to store the data (assuming a table with 'temperature' and 'humidity' columns)
cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  temperature REAL,
                  humidity REAL
                )''')
conn.commit()

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    data = request.get_json()
    
    # Extract data from the GitHub webhook payload
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    
    # Store the data in the database
    cursor.execute("INSERT INTO sensor_data (temperature, humidity) VALUES (?, ?)", (temperature, humidity))
    conn.commit()
    
    return jsonify({"message": "Data received and stored."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
