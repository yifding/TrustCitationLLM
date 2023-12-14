from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerRangeField, IntegerField
from wtforms.validators import DataRequired, Length


class AskForm(FlaskForm):
    user_input = StringField('Please enter your question.', validators=[DataRequired(), Length(min=5, max=100)])
    # rating = IntegerField('test Rating (1-10)  ', validators=[DataRequired()])
    rating = IntegerRangeField('Trustworthy Rating (0-10)  ', validators=[DataRequired()], render_kw={'style': 'width: 40ch'},)
    submit = SubmitField('Ask ChatGPT')


class CollectForm(FlaskForm):
    # rating = IntegerRangeField('Rating')
    rating = IntegerField('Trustworthy Rating (1-10)  ', validators=[DataRequired()])
    submit = SubmitField('Submit Rating')
