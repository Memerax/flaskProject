from flask import Flask, redirect, url_for, request, render_template, flash
from forms import RecipeAddForm, SearchRecipe
import pandas as pd
from werkzeug.utils import secure_filename
import os


def update_recipe_list():
    list_of_recipes = os.listdir('./static/data_dir')
    list_of_recipes = [x.replace(".csv", "") for x in list_of_recipes]
    return list_of_recipes


app = Flask(__name__)
app.config['SECRET_KEY'] = '5b1d36b483c040bed12ec570d12b6a47'
app.config['SUBMITTED_DATA'] = os.path.join('static', 'data_dir', '')
app.config['SUBMITTED_IMG'] = os.path.join('static', 'image_dir', '')
list_of_recipes = update_recipe_list()


@app.route('/')
def home():
    list_of_recipes = os.listdir('./static/data_dir')
    list_of_recipes = [x.replace(".csv", "") for x in list_of_recipes]
    return render_template('home.html', list_of_recipes=update_recipe_list())


@app.route('/about')
def about():
    return render_template('about.html', title="About", list_of_recipes=update_recipe_list())


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
        return redirect(url_for('home'))

    return render_template('add_recipe.html', title="Add a recipe", form=form, list_of_recipes=update_recipe_list())


@app.route('/remove_recipe')
def remove_recipe():
    return render_template('remove_recipe.html', title="Remove a recipe", list_of_recipes=update_recipe_list())


@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact page", list_of_recipes=update_recipe_list())


@app.route('/search', methods=["GET", "POST"])
def search():
    dir = os.listdir(app.config['SUBMITTED_DATA'])
    form = SearchRecipe()
    if form.validate_on_submit():
        query = form.query.data
        choice = form.select.data
        results = []
        for csv in dir:
            df = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] + csv), index_col=False)
            if query.lower() in df.iloc[0][choice].lower():
                results.append(df.iloc[0]['Recipe name'])

        if results:
            flash(f"{len(results)} matches for {query}.",'info')
        else:
            flash(f"{len(results)} matches for {query}.", "warning")
        return render_template('search.html', title="Search page", list_of_recipes=update_recipe_list(), form=form,
                               results=results)
    return render_template('search.html', title="Search page", list_of_recipes=update_recipe_list(), form=form)


@app.route('/display_recipe/<name>')
def display_recipe(name):
    df = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] + name.lower().replace(" ", "_") + '.csv'),
                     index_col=False)
    print(df.iloc[0]['Recipe name'])
    return render_template('display_recipe.html', recipe=df.loc[0], list_of_recipes=update_recipe_list())


@app.route('/remove_recipe/<name>')
def delete_recipe(name):
    os.remove(os.path.join(app.config['SUBMITTED_DATA'] + name.lower().replace(" ", "_") + '.csv'))
    return redirect(url_for('remove_recipe'))


@app.route('/search_results/<results>')
def search_results(results):
    return render_template('search_results.html', list_of_recipes=update_recipe_list())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
