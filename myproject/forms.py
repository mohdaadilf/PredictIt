# NECESSARY IMPORTS FOR FORMS
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField, Form, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
import datetime


from wtforms.fields.html5 import DateTimeField, DateField, TimeField

# LOGIN FORM
class LoginForm(FlaskForm):
    email = StringField('Enter Email:', validators=[DataRequired('Kindly Enter Your Email!'), Email()])
    password = PasswordField('Enter Password:', validators=[DataRequired('Enter Your Password!')])
    submit = SubmitField('Log In')

# REGISTRATION FORM
class RegistrationForm(FlaskForm):
    name = StringField('Enter Your Name:', validators=[DataRequired('Enter Your Name Please!')])
    email = StringField('Enter Your Email:', validators=[DataRequired('Enter A Valid Email Please!'), Email()])
    password = PasswordField('Create A Password:', validators=[DataRequired('Enter Password Please!'),
                                                               EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm Password:', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        # Check if not None for that user email!
        '''
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')
        '''
        if field.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

# BASIC INDEX FORM
class InfoForm(FlaskForm):
    name = StringField('Enter your name to get started:', validators=[DataRequired('Kindly Enter Your Name!')])
    submit = SubmitField('Get Started')

# FIRST SYMPTOM FORM
class SymptomForm(FlaskForm):
    symptom1 = StringField('Enter Your Initial Symptom:', validators=[DataRequired('Kindly Enter Your Symptom!')])
    num_days = IntegerField('Number Of Days Experiencing This Symptom From:', validators=[DataRequired('Kindly Input!')])
    submit = SubmitField('Proceed')

# OTHER SYMPTOMS FORM
class OtherSymptomForm(Form):
    symptom = RadioField('', choices=[('yes', 'Yes'), ('no', 'No')], validators=[DataRequired('Please Select Yes or No!')])

class Consul(FlaskForm):
    date = DateField('Select Date:', format='%Y-%m-%d', default=datetime.date.today(), validators=(DataRequired(),))
    time = TimeField('Select Time:', format='%H:%M',default= datetime.datetime.now(),validators=(DataRequired(),))
    Specialization = SelectField('Specialization',  choices=[('Orthopedic', 'Orthopedic'), ('Pediatrician', 'Pediatrician'),
                                                  ('Oncologist', 'Oncologist')])
    submit = SubmitField('Confirm Appointment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.date.data:
            self.date.data = datetime.date.today()

    def validate_date(form, field):
        if form.date.data < datetime.date.today():
            print("inside the if block")
            raise ValidationError("Appointment date must not be earlier than today.")

    def validate_time(form, field):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        form_time = form.time.data.strftime("%H:%M:%S")
        if form.date.data <= datetime.date.today() and form_time <= current_time:
            raise ValidationError("Appointment time must not be earlier than current time.")
