from flask import Flask, request, render_template, redirect, url_for, session, abort, flash
from functools import wraps
import json 
from datetime import date
from CreateUser import CreateUser
from PizzaOrder import PizzaOrder
from email_validator import validate_email, EmailNotValidError


app = Flask(__name__)
app.secret_key = 'pizza'

# login required so function can be called to check user login
def login_required(f):
    @wraps(f)
    def check_user_login(*args, **kwargs):
        if 'email' not in session:
            flash("You need to be logged in to view this page", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return check_user_login

users_file = "./data/users.json"

# read users from users.json
def load_users():
    try:
        with open(users_file, 'r') as fd:
            return json.load(fd)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Returns an empty list if the file is not found or if it's empty/incorrectly formatted
    
# write users to users.json
def save_users(users):
    with open(users_file, 'w') as fd:
        json.dump(users, fd)

current_info = load_users()
print(current_info)

pizza_orders = "./data/pizzaorders.json"

# read pizza orders from pizzaorders.json
def load_pizzas():
    try:
        with open(pizza_orders, 'r') as fd:
            return json.load(fd)
    except (FileNotFoundError, json.JSONDecodeError):
        return[]

# write pizza orders to pizzaorders.json    
def save_pizzas(pizzas):
    with open(pizza_orders, 'w') as fd:
        json.dump(pizzas, fd)

current_pizza_orders = load_pizzas()
print(current_pizza_orders)            

# check if users are logged in
def check_login(email, password):
    current_info = load_users()
    for user in current_info:
        if user['email'] == email and user['password'] == password:
            return True
    return False

# route for home page that will display pizza orders
@app.route('/')
@login_required
def home():
    orders = load_pizzas()
    return render_template('home.html', orders=orders)

# route for login and will set session variables upon login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        role = request.form.get('role')
        password = request.form.get('password')
        if check_login(email, password):
            session['email']= email
            session['role']= role
            return render_template('home.html')
        else:
            flash("Sorry. that user is not registered in our system. Please try again or Click the button below to create an account.", "error")
            return render_template('login.html')
        
# create new user route validates data entered and that passwords match and writes user to users.json
@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateUser(request.form)
    if request.method == 'POST':
        if form.email.validate(form) and form.password.validate(form) and form.verifyPassword.validate(form):
            email = form.email.data
            password = form.password.data
            verify_password = form.verifyPassword.data
            role = form.role.data

            # check if passwords match
            if password != verify_password:
                return "Passwords do not match!", 400

            # check if email already exists
            if any(user['email'] == email for user in current_info):
                return "Email already exists!", 400

            # create new user dictionary
            new_user = {"email": email, "password": password, "role": role}

            # add new user to the list and save it to the file
            current_info.append(new_user)
            save_users(current_info)

            session['email'] = email
            return redirect(url_for('home'))
        else:
            return render_template('create.html', form=form)
    else:
        return render_template('create.html', form=form)
    
# pizza route to display pizza ordering options
@app.route('/pizza', methods=['GET', 'POST'])
@login_required
def pizza():
    form = PizzaOrder(request.form)
    if request.method == 'POST':
        if form.validate():
            crust = form.crust.data
            type = form.type.data
            size = form.size.data
            quantity = form.quantity.data
            price_per = form.price_per.data
             # convert the date to a string format
            order_date = form.order_date.data
            if isinstance(order_date, date):
                order_date = order_date.isoformat()

            # calculations
            subtotal = quantity * price_per
            delivery_fee = subtotal * 0.1
            total = subtotal + delivery_fee

            # load pizza orders to see what the highest id numeber is and increment it by 1
            current_pizza_orders = load_pizzas()
            highest_id = max([order['id'] for order in current_pizza_orders], default=0)
            # set new id as highest id + 1
            new_order_id = highest_id +1 

            new_order = {
                "id": new_order_id,
                "type": type,
                "crust": crust, 
                "size": size,
                "quantity": quantity,
                "price_per": price_per,
                "order_date": order_date,
                "subtotal": subtotal,
                "delivery_fee": delivery_fee,
                "total": total,
            }
            # append new order to pizzaorders.json
            current_pizza_orders.append(new_order)
            save_pizzas(current_pizza_orders)

            return redirect(url_for('home'))

        else:
            # if the form is not valid, re-render the page with the form
            return render_template('pizza.html', form=form)

    # handle GET request
    return render_template('pizza.html', form=form)

# logout and remove session variables
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out! Login again to order more pizza!")
    return redirect(url_for('login'))    

if __name__ == '__main__':
    app.run(debug=True, port=8888)