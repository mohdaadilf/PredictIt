from myproject import app, db
from flask import render_template, session, redirect, url_for, session, flash,  request
from flask_wtf import FlaskForm
from wtforms import SubmitField, FormField, FieldList
from flask_login import login_required, login_user, logout_user, current_user
from myproject.models import User, Disease
from myproject.forms import LoginForm, RegistrationForm, InfoForm, SymptomForm, OtherSymptomForm
import myproject.ml as ml

symptom_list, symptoms_spaced, symptoms_dict = ml.get_symptoms_list()

@app.route('/predicted')
@login_required
def predicted():
    disease_dict = current_user.diseases_dict()
    return render_template('predicted.html', disease_dict = disease_dict)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        try:
            if user.check_password(form.password.data) and user is not None:

                login_user(user)
                flash('Logged in successfully')

                next = request.args.get('next')

                if next == None or not next[0] == '/':
                    next = url_for('index')

                return redirect(next)
            else:
                flash("Incorrect Password!")
                return redirect(url_for('login'))
        except AttributeError:
            flash("Email doesn't exist. Kindly register.")
            return redirect(url_for('login'))
        
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    try:
        if form.validate_on_submit():
            user = User(name=form.name.data, email=form.email.data,
                        password=form.password.data)

            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering! Now you can login!')
            return redirect(url_for('login'))
    except:
        flash("Already Registered!")
        return redirect(url_for('register'))

    return render_template('register.html', form=form)


# ~~~~~~~~~~~~~


@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('symptom1'))
    return render_template('index.html', form=form)

# first symptom page


@app.route('/symptom1', methods=['GET', 'POST'])
def symptom1():
    symp_form = SymptomForm()
    if symp_form.validate_on_submit():
        session['num_days'] = symp_form.num_days.data
        session['symptom1_spaced'] = symp_form.symptom1.data.lower()
        if session['symptom1_spaced'] in symptoms_spaced:
            session['symptom1'] = symptoms_dict[symp_form.symptom1.data.lower()]
            return redirect(url_for('ml_symptom'))
        else:
            flash('Enter A Valid Symptom!')
            return redirect(url_for('symptom1'))

    return render_template('symptom1.html', form=symp_form, symptoms_spaced=symptoms_spaced)



# additional symptoms page


@app.route('/symptoms', methods=['GET', 'POST'])
def ml_symptom():
    clf, cols = ml.train()
    symptom1 = session['symptom1']
    symptoms_given = ml.tree_to_code(clf, cols, symptom1)
    symptoms_label = []
    for symptom in list(symptoms_given):
        symptoms_label.append(symptom.replace('_',' '))
    
    class SymptomsForm(FlaskForm):
        symptoms = FieldList(FormField(OtherSymptomForm),
                             min_entries=len(symptoms_given))
        submit = SubmitField('Continue')
    form = SymptomsForm()
    if form.validate_on_submit():
        ml.yes_or_no = []
        ml.symptoms_exp = []
        for field in form.symptoms:
            ml.yes_or_no.append(field.symptom.data)
        return redirect('result')

    return render_template('symptoms.html', symptoms=list(symptoms_given), form=form, symptoms_label = symptoms_label)


@app.route('/result')
def result():
    ml.getDicts()
    ml.recurse2(session['num_days'])
    predicted_disease = ml.predicted_disease
    symptom_string = ml.list_to_string(ml.symptoms_exp)
    if current_user.is_authenticated:
        if ml.yes_or_no == []:
            flash('Prediction Already Saved!')
        else:
            disease = Disease(predicted_disease, symptom_string, current_user.id)
            db.session.add(disease)
            db.session.commit()
            ml.yes_or_no = []
            flash('Prediction saved!')
    return render_template("result.html", condition=ml.condition,color = ml.color, precaution_list=ml.precaution_list, predicted_disease=predicted_disease, predicted_disease_description=ml.predicted_disease_description, predicted_disease_description2 = ml.predicted_disease_description2, precaution_list2= ml.precaution_list2)



if __name__ == "__main__":
    app.run(debug=True)
