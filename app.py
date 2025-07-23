from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__)


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Maneesh@2005",  
        database="expense_db"
    )

@app.route('/')
def home():
    con = get_connection()
    cur = con.cursor(dictionary=True)


    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()

    
    cur.execute("SELECT SUM(amount) AS total FROM expenses")
    total_expense = cur.fetchone()['total'] or 0

    
    cur.execute("""
        SELECT category, SUM(amount) AS total 
        FROM expenses 
        GROUP BY category 
        ORDER BY total DESC 
        LIMIT 1
    """)
    highest_category = cur.fetchone()
    highest_category_name = highest_category['category'] if highest_category else "None"

    con.close()

    return render_template(
        'home.html',
        expenses=expenses,
        total_expense=total_expense,
        highest_category=highest_category_name
    )


@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("DELETE FROM expenses WHERE expense_id = %s", (expense_id,))
    con.commit()
    cursor.close()
    con.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
