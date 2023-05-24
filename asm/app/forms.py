from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import InputRequired

from .auth.forms import LoginForm, RegistrationForm


# Define your forms here.
# You can also define them inside a package and import them here.
# This is only a convenience so that all your forms are available from a single module.
class CreatePoolForm(FlaskForm):
    pool_name = StringField('Nombre del pool', validators=[InputRequired()])
    submit = SubmitField('Crear Pool')


class DeletePoolForm(FlaskForm):
    pool_name = StringField('Nombre del pool', validators=[InputRequired()])
    submit = SubmitField('Borrar Pool')