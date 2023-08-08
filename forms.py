from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.fields import DateField, EmailField, TelField
from wtforms.validators import DataRequired, Length


class RecipeAddForm(FlaskForm):
    recipe_name = StringField("Name of Recipe: ", validators=[DataRequired(), Length(max=100)])
    ingredients = StringField("Enter ingredients: ", validators=[DataRequired()])
    instructions = TextAreaField("Recipe Instructions: ", validators=[DataRequired()])
    preparation = TextAreaField("Preparation Instructions: ", validators=[DataRequired()])
    food_picture = FileField('Recipe Picture:', validators=[FileRequired()])
