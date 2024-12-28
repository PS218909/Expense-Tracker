from flask import Blueprint, render_template, request, redirect, url_for, send_file
from .models import Expense, Category, db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime as dt
import pytz

bp = Blueprint('routes', __name__)


def populate_database():
    category_all = [category.name for category in Category.query.all()]
    if not category_all:
        categories = ['Entertainment', 'Food', 'Gas', 'Rent', 'Savings', 'Transportation', 'Utilities']
        for category in categories:
            if category not in category_all:
                db.session.add(Category(name=category))
                db.session.commit()
populate_database()

@bp.route('/')
@bp.route("/home")
def home():
    category = Category.query.all()
    expense = Expense.query.all()
    total = sum([e.amount for e in expense])
    return render_template('home.html', categories = category, total = total)

@bp.route('/category', methods = ['GET'])
def category():
    categories = Category.query.all()
    expense = Expense.query.all()
    if expense:
        df = pd.DataFrame([{'title': e.title, 'amount': e.amount, 'category': e.category, 'date': e.date} for e in expense])
        for category in categories:
            total = df[df['category'] == category.name]['amount'].sum()
            category.total = total
        category_name = [category.name for category in categories]
        category_total = [category.total for category in categories]
        overall = np.sum(category_total)
        patches, texts = plt.pie(np.array(category_total), radius=1)
        legend_text = []
        plt.subplots_adjust(left=0.5)
        plt.legend(patches, [category_name[idx] + f" : {(category_total[idx]/overall)*100:.2f} %" for idx in range(len(category_total))], title="Category", bbox_to_anchor=(-0.1, 0.85))
        plt.savefig("app\\static\\pie.png", transparent=True)
        plt.close('all')
    return render_template('category.html', categories = categories)

@bp.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        amount = request.form['amount']
        category = request.form['category']
        expense = Expense(title=title, amount=float(amount), category=category, date=dt.now(pytz.timezone('Asia/Kolkata')))
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('routes.view_expenses'))
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template('add_expense.html', categories = categories)

@bp.route('/category/add', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('routes.home'))
    return render_template('add_category.html')

@bp.route('/view', methods = ["GET", "POST"])
def view_expenses():
    date = request.args.get('search_by_date', default='all', type=str)
    expenses = Expense.query.all()
    if date == 'all':
        total = sum([expense.amount for expense in expenses])
        message = f"Total Expense: {total}"
    else:
        expenses = [expense for expense in expenses if str(expense.date).split(" ")[0] == date]
        total = sum([expense.amount for expense in expenses])
        message = f"Expense on {date}: {total}"
    for expense in expenses:
        expense.date = str(expense.date).split(" ")[0]
    return render_template('view_expense.html', expenses = expenses, message = message)

@bp.route("/category/view/<string:name>", methods = ["GET"])
def view_category(name):
    expenses = list(Expense.query.filter(Expense.category == name))
    for expense in expenses:
        expense.date = str(expense.date).split(" ")[0]
    return render_template("view_expense.html", expenses = expenses)

@bp.route('/delete/<int:id>', methods = ["GET"])
def delete_expense(id):
    expense = Expense.query.get(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('routes.view_expenses'))

@bp.route('/category/delete/<string:name>', methods = ["GET"])
def delete_category(name):
    category = Category.query.get(name)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('routes.category'))

@bp.route('/edit/<int:id>', methods = ["GET", "POST"])
def edit_expense(id):
    expense = Expense.query.get(id)
    category = Category.query.all()
    if request.method == 'POST':
        expense.title = request.form['title']
        expense.amount = request.form['amount']
        expense.category = request.form['category']
        db.session.commit()
        return redirect(url_for('routes.view_expenses'))
    return render_template('edit_expense.html', expense = expense, categories = category)

@bp.route("/export", methods = ["GET"])
def export_expense():
    expense = Expense.query.all()
    df = pd.DataFrame([{'title': e.title, 'amount': e.amount, 'category': e.category, 'date': e.date} for e in expense])
    df.to_csv("app\\export.csv")
    return send_file("export.csv", as_attachment=True)