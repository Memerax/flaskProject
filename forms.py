from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms.fields import StringField, TextAreaField, SubmitField, SelectField
from wtforms.fields import DateField, EmailField, TelField
from wtforms.validators import DataRequired, Length


class RecipeAddForm(FlaskForm):
    recipe_name = StringField("Name of Recipe: ", validators=[DataRequired(), Length(max=100)])
    ingredients = StringField("Enter ingredients: ", validators=[DataRequired()])
    instructions = TextAreaField("Recipe Instructions: ", validators=[DataRequired()])
    serving = TextAreaField("Serving Instructions: ", validators=[DataRequired()])
    food_picture = FileField('Recipe Picture:', validators=[FileRequired()])


class SearchRecipe(FlaskForm):
    choices = [('Recipe name', 'Recipe name'),
               ('Ingredients', 'Ingredients')]
    select = SelectField('Search fields:', choices=choices)
    query = StringField("Query: ",validators=[DataRequired()])
