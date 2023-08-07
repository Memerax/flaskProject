from flask import Flask, redirect, url_for, request, render_template
# from forms import BeneficiaryForm
import pandas as pd

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
