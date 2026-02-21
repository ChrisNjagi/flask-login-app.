from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
      CREATE TABLE IF NOT EXISTs users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email   TEXT UNIQUE,
        password TEXT
      )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/register",methods=["POST"])
def register():
    data = request.json
    email = data["email"]
    password = generate_password_hash(data["password"])

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(email,password)VALUES(?,?)",(email,
password))
        conn.commit()
        conn.close()
        return jsonify({"message":"User registered successfully"})
    except:
        return jsonify({"message":"User already exist"})


@app.route("/login",methods = ["POST"])
def login():
    data = request.json
    email = data["email"]
    password=data["password"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email=?",(email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[0],password):
        return jsonify({"message","Login Succesful"})
    else:
        return jsonify({"message":"Invalid email or password"})

if __name__=="__main__":
    app.run(debug=True)