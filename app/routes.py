from flask import Blueprint, render_template, request, redirect, url_for
from .models import Expense, Category, db

bp = Blueprint('routes', __name__)

@bp.route('/')
@bp.route("/home")
def home():
    category = Category.query.all()
    return render_template('home.html', categories = category)

@bp.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        amount = request.form['amount']
        category = request.form['category'].lower()
        expense = Expense(title=title, amount=float(amount), category=category)
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('routes.home'))
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template('add_expense.html', categories = categories)

@bp.route('/view', methods = ["GET"])
def view_expenses():
    expenses = Expense.query.all()
    return render_template('view_expense.html', expenses = expenses)

@bp.route('/delete/<int:id>', methods = ["GET"])
def delete_expense(id):
    expense = Expense.query.get(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('routes.view_expenses'))

@bp.route('/edit/<int:id>', methods = ["GET", "POST"])
def edit_expense(id):
    expense = Expense.query.get(id)
    if request.method == 'POST':
        expense.title = request.form['title']
        expense.amount = request.form['amount']
        expense.category = request.form['category']
        db.session.commit()
        return redirect(url_for('routes.view_expenses'))
    return render_template('edit_expense.html', expense = expense)