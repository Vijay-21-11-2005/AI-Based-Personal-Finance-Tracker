from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import MySQLdb.cursors
import os
from datetime import datetime
from model.predictor import ExpensePredictor
from model.categorizer import ExpenseCategorizer

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL Configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' # User needs to configure this
app.config['MYSQL_DB'] = 'finance_tracker'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

predictor = ExpensePredictor()
categorizer = ExpenseCategorizer()

class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    if user:
        return User(user['id'], user['email'])
    return None

@app.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, hashed_password))
            mysql.connection.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Email already exists!', 'danger')
        finally:
            cursor.close()
    return render_template('login.html', action='signup')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and bcrypt.check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['email'])
            login_user(user_obj)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', action='login')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Expense API
@app.route('/api/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
        amount = data.get('amount')
        note = data.get('note')
        category = data.get('category') or categorizer.categorize(note)
        date = data.get('date') or datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('INSERT INTO expenses (user_id, amount, category, date, note) VALUES (%s, %s, %s, %s, %s)',
                       (current_user.id, amount, category, date, note))
        mysql.connection.commit()
        return jsonify({'message': 'Expense added successfully', 'category': category})
    
    cursor.execute('SELECT * FROM expenses WHERE user_id = %s ORDER BY date DESC', (current_user.id,))
    expenses = cursor.fetchall()
    cursor.close()
    return jsonify(expenses)

@app.route('/api/predict')
@login_required
def predict():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT SUM(amount) as total, MONTH(date) as month 
        FROM expenses 
        WHERE user_id = %s 
        GROUP BY MONTH(date) 
        ORDER BY month ASC
    ''', (current_user.id,))
    data = cursor.fetchall()
    cursor.close()
    
    monthly_totals = [float(row['total']) for row in data]
    prediction = predictor.predict_next_month(monthly_totals)
    return jsonify({'predicted_spending': prediction})

@app.route('/api/budgets', methods=['GET', 'POST'])
@login_required
def budgets():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        data = request.json
        category = data.get('category')
        amount = data.get('amount')
        now = datetime.now()
        
        cursor.execute('''
            INSERT INTO budgets (user_id, category, amount, month, year) 
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE amount = VALUES(amount)
        ''', (current_user.id, category, amount, now.month, now.year))
        mysql.connection.commit()
        return jsonify({'message': 'Budget updated'})
    
    cursor.execute('SELECT * FROM budgets WHERE user_id = %s', (current_user.id,))
    budgets = cursor.fetchall()
    cursor.close()
    return jsonify(budgets)

@app.route('/api/alerts')
@login_required
def alerts():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    
    # Get current month spending vs budgets
    cursor.execute('''
        SELECT e.category, SUM(e.amount) as spent, b.amount as budget
        FROM expenses e
        JOIN budgets b ON e.category = b.category AND e.user_id = b.user_id
        WHERE e.user_id = %s AND MONTH(e.date) = %s AND YEAR(e.date) = %s
        GROUP BY e.category
    ''', (current_user.id, now.month, now.year))
    
    status = cursor.fetchall()
    alerts = []
    for s in status:
        if s['spent'] > s['budget']:
            alerts.append(f"Budget exceeded for {s['category']}! Spent: ${s['spent']:.2f}, Budget: ${s['budget']:.2f}")
        elif s['spent'] > s['budget'] * 0.8:
            alerts.append(f"80% of budget reached for {s['category']}.")
            
    return jsonify(alerts)

if __name__ == '__main__':

    app.run(debug=True)
