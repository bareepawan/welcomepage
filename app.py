from flask import Flask, request, jsonify, render_template
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


# Function to get MySQL connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None


@app.route("/")
def index():
    return render_template("welcom.html")


# 🟢 Register Route
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")

    # Name and Gender are required
    if not name or not gender:
        return jsonify({"error": "Please provide both Name and Gender!"}), 400

    # Age is optional, but if provided, it should be valid
    if age:
        try:
            age = int(age)
            if age < 1 or age > 100:
                return jsonify({"error": "Age must be between 1 and 100!"}), 400
        except ValueError:
            return jsonify({"error": "Age must be a valid number!"}), 400
    else:
        age = None  # Store NULL in the database if age is not given

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed!"}), 500

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
        user = cursor.fetchone()

        if user:
            return jsonify({"error": f"User '{name}' already exists!"}), 400

        cursor.execute(
            "INSERT INTO users (name, age, gender) VALUES (%s, %s, %s)",
            (name, age, gender),
        )
        conn.commit()
        return jsonify({"message": f"Registration successful for {name}!"}), 200

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return jsonify({"error": "Database operation failed!"}), 500

    finally:
        cursor.close()
        conn.close()


# 🔵 Login Route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    gender = data.get("gender")

    if not name or not gender:
        return jsonify({"error": "Please enter both Name and Gender!"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed!"}), 500

    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT * FROM users WHERE name = %s AND gender = %s", (name, gender)
        )
        user = cursor.fetchone()

        if user:
            return jsonify({"message": f"Login successful for {name}!"}), 200
        else:
            return (
                jsonify(
                    {"error": "User not found! Please check your details or register."}
                ),
                404,
            )

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return jsonify({"error": "Database operation failed!"}), 500

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
