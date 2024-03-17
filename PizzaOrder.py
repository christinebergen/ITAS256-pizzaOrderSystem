from flask_wtf import Form
from wtforms import IntegerField, SubmitField, SelectField, FloatField, DateField
from wtforms import validators
import json

def load_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        crust_choices = data['crust']
        type_choices = data['type']
        size_choices = data['size']
        return crust_choices, type_choices, size_choices

crust, pizza_type, size = load_from_json('./data/init.json')

class PizzaOrder(Form):
    crust = SelectField('Type of Crust: ', choices = [(choice, choice) for choice in crust])
    type = SelectField('Type of Pizza: ', choices=[(choice, choice) for choice in pizza_type])
    size = SelectField('Size: ', choices=[(choice, choice) for choice in size])
    quantity = IntegerField('Quantity: ', [validators.NumberRange(min=1, max=10, message="Minimum Quantity is 1, Maximum Quantity is 10")])
    price_per = FloatField('Price Per Pizza: $')
    order_date = DateField('Order Date: ')
    submit = SubmitField("Place Order")