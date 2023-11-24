from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AskForm(FlaskForm):
    user_input = StringField('User_input', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Submit User Input')
