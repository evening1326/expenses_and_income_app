'''
Nicholas DeMaestri
10/31/2024
CS-391

Assignment: Code Generation

Main flask application.
'''

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Data storage (in-memory for simplicity)
income_list = []
expense_list = []
categories = []
initial_balance = 0.0

# Helper function to calculate the budget summary
def calculate_summary():
    total_income = sum([item['amount'] for item in income_list])
    total_expenses = sum([item['amount'] for item in expense_list])
    remaining_balance = initial_balance + total_income - total_expenses
    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'remaining_balance': remaining_balance
    }

@app.route('/')
def index():
    summary = calculate_summary()
    return render_template('index.html', income_list=income_list, expense_list=expense_list, categories=categories, summary=summary, initial_balance=initial_balance)

@app.route('/set_initial_balance', methods=['POST'])
def set_initial_balance():
    global initial_balance
    initial_balance = float(request.form['initial_balance'])
    return redirect(url_for('index'))

@app.route('/add_income', methods=['POST'])
def add_income():
    amount = float(request.form['amount'])
    description = request.form['description']
    income_list.append({'id': len(income_list), 'amount': amount, 'description': description, 'date': datetime.now()})
    return redirect(url_for('index'))

@app.route('/add_expense', methods=['POST'])
def add_expense():
    amount = float(request.form['amount'])
    description = request.form['description']
    category = request.form['category']
    expense_list.append({'id': len(expense_list), 'amount': amount, 'description': description, 'category': category, 'date': datetime.now()})
    return redirect(url_for('index'))

@app.route('/add_category', methods=['POST'])
def add_category():
    category = request.form['category']
    if category not in categories:
        categories.append(category)
    return redirect(url_for('index'))

@app.route('/remove_category/<category>', methods=['POST'])
def remove_category(category):
    global categories, expense_list
    categories = [c for c in categories if c != category]
    expense_list = [expense for expense in expense_list if expense['category'] != category]
    return redirect(url_for('index'))

@app.route('/remove_income/<int:income_id>', methods=['POST'])
def remove_income(income_id):
    global income_list
    income_list = [income for income in income_list if income['id'] != income_id]
    return redirect(url_for('index'))

@app.route('/remove_expense/<int:expense_id>', methods=['POST'])
def remove_expense(expense_id):
    global expense_list
    expense_list = [expense for expense in expense_list if expense['id'] != expense_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
