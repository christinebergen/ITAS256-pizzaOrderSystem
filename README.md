# ITAS256-pizzaOrderSystem

A class assignment for ITAS 256 to order pizza. written in Python using Flask and WTForms

## Features

The user can:

- Create an account
- Log in with their user information
- View a list of pizza orders
- Submit a new pizza order
- Update or Delete a pizza order
- Log out and end their session

## Tech Stack

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [WTForms](https://wtforms.readthedocs.io/en/3.1.x/)

## Installation

```bash
git clone https://github.com/christinebergen/ITAS256-pizzaOrderSystem
cd ITAS256-pizzaOrderSystem
pip install flask
```

## Virtual Deployment

```bash
python PizzaMain.py
```

Visit: localhost:8888 in a web browser

## Issues encountered

Multiple issues were noted with the Update route, and chatGPT was utilized for assistance with debugging and troubleshooting. The Update route was meant to over write the data when it was saved, but I was never able to get this functionality working.
