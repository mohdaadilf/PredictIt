from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, RadioField, SubmitField, FormField, FieldList, Form
from wtforms.validators import DataRequired

class InfoForm(FlaskForm):
    name =  StringField('Name:', validators=[DataRequired('Kindly Enter Your Name!')])
    submit = SubmitField('Get Started')

class SymptomForm(FlaskForm):
    symptom1 = StringField('Enter Your Symptom:', validators=[DataRequired('Kindly Enter Your Symptom!')])
    num_days = IntegerField('Enter The Number Of Days You Are Experiencing This Symptom For:', validators=[DataRequired('Kindly Input!')])
    submit = SubmitField('Proceed')

class OtherSymptomForm(Form):
    symptom = RadioField('', choices=[('yes','Yes'),('no','No')])



if __name__ == "__main__":
    a = 2