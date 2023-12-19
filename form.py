from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerRangeField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length


class AskForm(FlaskForm):
    user_input = StringField('Please enter your question.', validators=[DataRequired(), Length(min=5, max=100)])
    # rating = IntegerField('test Rating (1-10)  ', validators=[DataRequired()])
    rating = IntegerRangeField('Trustworthy Rating (0-10)  ', validators=[DataRequired()], render_kw={'style': 'width: 40ch'},)
    submit = SubmitField('Submit')


class CollectForm(FlaskForm):
    # rating = IntegerRangeField('Rating')
    rating = IntegerField('Trustworthy Rating (1-10)  ', validators=[DataRequired()])
    submit = SubmitField('Submit Rating')

class DemoForm(FlaskForm):

    gender = SelectField('What gender do you identify with?', 
    choices=[
        ('', ''),
        ('Woman', 'Woman'), 
        ('Man', 'Man'), 
        ('Other', 'Other'),
        ('Choose not to Answer', 'Choose not to Answer'),
    ], validators=[DataRequired()])

    age = SelectField('How many years old are you?', 
    choices=[
        ('', ''),
        ('18-30', '18-30'), 
        ('31-40', '31-40'), 
        ('41-50', '41-50'),
        ('51-60', '51-60'),
        ('61-70', '61-70'),
        ('> 70', '> 70'),
        ('Choose not to Answer', 'Choose not to Answer'),
    ], validators=[DataRequired()])

    residence = SelectField('Which of the following best describes the area you live in?', 
    choices=[
        ('', ''),
        ('Urban Area', 'Urban Area'), 
        ('Suburban Area', 'Suburban Area'), 
        ('Rural Area', 'Rural Area'),
        ('Choose not to Answer', 'Choose not to Answer'),
    ], validators=[DataRequired()])

    education = SelectField('What is your highest completed level of education?', 
    choices=[
        ('', ''),
        ('High School', 'High School'), 
        ('Some College', 'Some College'), 
        ('College Degree', 'College Degree'),
        ('Graduate Degree', 'Graduate Degree'),
        ('Choose not to Answer', 'Choose not to Answer'),
    ], validators=[DataRequired()])

    race = SelectField('What race do you identify as?', 
    choices=[
        ('', ''),
        ('Asia', 'Asia'), 
        ('Black', 'Black'), 
        ('Latino', 'Latino'),
        ('White', 'White'),
        ('Other', 'Other'),
        ('Choose not to Answer', 'Choose not to Answer'),
    ], validators=[DataRequired()])

    political_orientation = SelectField('Please indicate your political orientation.', 
    choices=[
        ('', ''),
        ('Very Liberal', 'Very Liberal'), 
        ('Somewhat Liberal', 'Somewhat Liberal'), 
        ('Moderate', 'Moderate'),
        ('Somewhat Conservative', 'Somewhat Conservative'),
        ('Very Conservative', 'Very Conservative'),
        ('Choose not to Answer', 'Choose not to Answer'),
    ], validators=[DataRequired()])

    chatgpt_heard = SelectField('Have you heard of ChatGPT?', 
    choices=[
        ('', ''),
        ('Never', 'Never'), 
        ('Few Times', 'Few Times'), 
        ('Familiar', 'Familiar'),
        ('Choose not to Answer', 'Choose not to Answer'),
    ], validators=[DataRequired()])


    submit = SubmitField('Submit')
