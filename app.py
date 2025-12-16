import os
import time
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration via environment variables
db_config = {
    "host": os.environ.get("DATABASE_HOST", "mysql"),
    "user": os.environ.get("DATABASE_USER", "root"),
    "password": os.environ.get("DATABASE_PASSWORD", "rootpassword"),
    "database": os.environ.get("DATABASE_NAME", "StudentDB")
}

# Wait for MySQL to be ready and connect
while True:
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        print("Connected to MySQL successfully!")
        break
    except Error as e:
        print(f"Waiting for MySQL... {e}")
        time.sleep(3)

# Auto-create the Students table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS Students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    grade VARCHAR(50) NOT NULL
)
"""
cursor.execute(create_table_query)
db.commit()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']
    cursor.execute(
        "INSERT INTO Students (name, age, grade) VALUES (%s, %s, %s)",
        (name, age, grade)
    )
    db.commit()
    return redirect(url_for('index'))

@app.route('/edit', methods=['POST'])
def edit_student():
    sid = request.form.get('id')
    name = request.form.get('name')
    age = request.form.get('age')
    grade = request.form.get('grade')
    if not sid:
        return redirect(url_for('index'))
    try:
        cursor.execute(
            "UPDATE Students SET name=%s, age=%s, grade=%s WHERE id=%s",
            (name, age, grade, sid)
        )
        db.commit()
    except Error:
        db.rollback()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_student(id):
    cursor.execute("DELETE FROM Students WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
