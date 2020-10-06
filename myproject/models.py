from myproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# loads the user according to their unique id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# user class for making new users, checking if passwords match


class User(db.Model, UserMixin):

    # this is the tablename inside the database
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # id, remains unique
    name = db.Column(db.String(20))
    email = db.Column(db.String(64), unique=True,
                      index=True)  # email should be unique
    password_hash = db.Column(db.String(128))  # password hash
    diseases = db.relationship('Disease', backref='users', lazy='dynamic')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        # saving a sha sum hash instead of actual pass
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # checking if hashes match
        return check_password_hash(self.password_hash, password)

    def diseases_dict(self):
        disease_list = []
        symptoms_list = []
        for disease in self.diseases:
            disease_list.append(disease.disease_name)
            symptoms_list.append(disease.symptoms)
        disease_dict = dict(zip(symptoms_list, disease_list))    
        return disease_dict


# diseases class


class Disease(db.Model):
    __tablename__ = 'diseases'
    id = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.Text)
    symptoms = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, disease_name, symptoms, user_id):
        self.disease_name = disease_name
        self.user_id = user_id
        self.symptoms = symptoms
