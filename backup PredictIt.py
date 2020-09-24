#flask imports here
from flask import Flask, render_template, session, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, RadioField, SubmitField, FormField, FieldList, Form
from wtforms.validators import DataRequired
import pandas as pd
#app config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

#forms start here
class InfoForm(FlaskForm):
    name =  StringField('Name:', validators=[DataRequired('Kindly Enter Your Name!')])
    submit = SubmitField('Get Started')

class SymptomForm(FlaskForm):
    symptom1 = StringField('Enter Your Symptom:', validators=[DataRequired('Kindly Enter Your Symptom!')])
    num_days = IntegerField('Enter The Number Of Days You Are Experiencing This Symptom For:', validators=[DataRequired('Kindly Input!')])
    submit = SubmitField('Proceed')


#home page
@app.route('/', methods=['GET', 'POST'])
def index():

    form = InfoForm()
    if form.validate_on_submit():
            session['name'] = form.name.data
            return redirect(url_for('symptom1'))
    return render_template('index.html',form=form)

#first symptom page
@app.route('/symptom1', methods=['GET', 'POST'])
def symptom1():
    df = pd.read_csv('symptom_severity.csv')
    symptoms_list = df['itching'].tolist()
    symptoms_list.append('itching')
    symp_form = SymptomForm()
    if symp_form.validate_on_submit():
            session['symptom1'] = symp_form.symptom1.data
            session['num_days'] = symp_form.num_days.data
            if session['symptom1'] in symptoms_list:
                return redirect(url_for('ml_symptom'))
            else:
                flash('Enter A Valid Symptom!')
                return redirect(url_for('symptom1'))

    return render_template('symptom1.html', form = symp_form)

#additional symptoms page
@app.route('/symptoms', methods=['GET', 'POST'])
def ml_symptom():
    import ml
    clf,cols = ml.train()
    symptom1 = session['symptom1']
    symptoms_given = ml.tree_to_code(clf,cols,symptom1)
    class OtherSymptomForm(Form):
        symptom = RadioField('', choices=[('yes','Yes'),('no','No')])

    class SymptomsForm(FlaskForm):
        symptoms = FieldList(FormField(OtherSymptomForm), min_entries=len(symptoms_given))
        submit = SubmitField('Continue')
    form = SymptomsForm()
    if form.validate_on_submit():
        for field in form.symptoms:
            ml.yes_or_no.append(field.symptom.data)
            return redirect('result')

    return render_template('symptoms.html',symptoms= list(symptoms_given), form=form)

@app.route('/result')
def result():
    import ml
    ml.getDescription()
    ml.getSeverityDict()
    ml.getprecautionDict()
    ml.recurse2(session['num_days'])
    return render_template("result.html", condition = ml.condition, precaution_list = ml.precaution_list, predicted_disease=ml.predicted_disease, predicted_disease_description=ml.predicted_disease_description)


if __name__ == "__main__":
    app.run()