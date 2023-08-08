from flask import Flask, redirect, url_for, request, render_template, flash
from forms import RecipeAddForm
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '5b1d36b483c040bed12ec570d12b6a47'
app.config['SUBMITTED_DATA'] = os.path.join('static', 'data_dir', '')
app.config['SUBMITTED_IMG'] = os.path.join('static', 'image_dir', '')
list_of_recipes = os.listdir('./static/data_dir')
list_of_recipes = [x.replace(".csv", "") for x in list_of_recipes]


@app.route('/')
def home():
    return render_template('home.html', list_of_recipes=list_of_recipes)


@app.route('/about')
def about():
    return render_template('about.html', title="About", list_of_recipes=list_of_recipes)


@app.route('/add_recipe', methods=["GET", "POST"])
def add_recipe():
    form = RecipeAddForm()
    if form.validate_on_submit():
        flash(f"{form.recipe_name.data} has been successfully added", "success")
        recipe_name = form.recipe_name.data
        ingredients = form.ingredients.data
        instructions = form.instructions.data
        serving = form.serving.data
        pic_filename = recipe_name.lower().replace(" ", "_") \
                       + '.' + secure_filename(form.food_picture.data.filename).split('.')[-1]
        form.food_picture.data.save(os.path.join(app.config['SUBMITTED_IMG'] + pic_filename))
        df = pd.DataFrame([{'Recipe name': recipe_name, 'Ingredients': ingredients,
                            'Preparation instructions': instructions, 'Serving Instructions': serving,
                            'picture': pic_filename}])
        df.to_csv(os.path.join(app.config['SUBMITTED_DATA'] + recipe_name.lower().replace(" ", "_") + '.csv'))
        list_of_recipes = os.listdir('./static/data_dir')
        list_of_recipes = [x.replace(".csv", "") for x in list_of_recipes]
        return redirect(url_for('home'))

    return render_template('add_recipe.html', title="Add a recipe", form=form)


@app.route('/remove_recipe')
def remove_recipe():
    return render_template('remove_recipe.html', title="Remove a recipe")


@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact page")


@app.route('/search')
def search():
    return render_template('search.html', title="Search page")


@app.route('/display_recipe/<name>')
def render_information(name):
    df = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] + name.lower().replace(" ", "_") + '.csv'),
                     index_col=False)
    print(df.iloc[0]['name'])
    return render_template('view_beneficiary.html', beneficiary=df.iloc[0])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
