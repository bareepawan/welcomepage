import mysql.connector # type: ignore

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_root_password",
        database="mydatabase"
    )

# Insert new user
def insert_user(name, gender, age=None):
    db = connect_db()
    cursor = db.cursor()
    try:
        sql = "INSERT INTO users (name, gender, age) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, gender, age))
        db.commit()
        return True
    except mysql.connector.IntegrityError as e:
        print("Error:", e)  # This will help you debug the error
        return False
    finally:
        cursor.close()
        db.close()

        db = connect_db()
        cursor = db.cursor()
try:
        sql = "INSERT INTO users (name, age, gender) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, age, gender))
db.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        cursor.close()
        db.close()

# Check if user exists (for login)
def check_user(name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user
