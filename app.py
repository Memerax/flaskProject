from flask import Flask, redirect, url_for, request, render_template
from forms import BeneficiaryForm
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html', title="Add a recipe")

@app.route('/remove_recipe')
def remove_recipe():
    return render_template('remove_recipe.html', title="Remove a recipe")

@app.route('/contact')
def contact():
    return render_template('contact.html',title="Contact page")

@app.route('/search')
def search():
    return render_template('search.html',title="Search page")

if __name__ == '__main__':
    app.run()
