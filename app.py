import os
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
# // Database configuration
app = Flask(__name__)

# Database configuration via environment variables
db = mysql.connector.connect(
    host=os.environ.get("DATABASE_HOST", "mysql"),
    user=os.environ.get("DATABASE_USER", "root"),
    password=os.environ.get("DATABASE_PASSWORD", ""),
    database=os.environ.get("DATABASE_NAME", "StudentDB")
)
cursor = db.cursor()

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
    cursor.execute("INSERT INTO Students (name, age, grade) VALUES (%s, %s, %s)", (name, age, grade))
    db.commit()
    return redirect(url_for('index'))

@app.route('/edit', methods=['POST'])
def edit_student():
    """
    Receives form fields: id, name, age, grade
    Updates the student record in the database and redirects to index.
    """
    sid = request.form.get('id')
    name = request.form.get('name')
    age = request.form.get('age')
    grade = request.form.get('grade')

    # Validate id presence
    if not sid:
        return redirect(url_for('index'))

    try:
        cursor.execute(
            "UPDATE Students SET name = %s, age = %s, grade = %s WHERE id = %s",
            (name, age, grade, sid)
        )
        db.commit()
    except Exception as e:
        # For debugging: print(e)
        db.rollback()
        # In production, log the error and surface a friendly message
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_student(id):
    cursor.execute("DELETE FROM Students WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
