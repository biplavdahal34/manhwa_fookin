from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, NumberRange, EqualTo, ValidationError, Length, Email
import bcrypt   

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = "DOUUFP98Y98VOUDGV8O78ODIJFGIU"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)


class Manhwa(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String, nullable = False)
    genre = db.Column(db.String, nullable = False)
    ratings_number  = db.Column (db.Integer, nullable = False)
    rating_text = db.Column(db.String)

class MYmanhwalist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    manhwa_id = db.Column(db.Integer, db.ForeignKey('manhwa.id'), nullable = False)
    my_review_number = db.Column(db.Integer, nullable = False)
    my_review_text = db.Column(db.String)



#forms
class RegisterForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Length(min=6, max=50),Email()])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = StringField("Confirm Password", validators=[DataRequired(), Length(min=8),EqualTo('password')])
    submit = SubmitField("Create Account")

    def validate_username(self, field):
        existing_username = User.query.filter_by(username= field.data).first()
        if existing_username:
            raise ValidationError("Username Already Exists. Please Try Another One!")

    def validate_email(self, field):
        if not field.data.lower().endswith(("@gmail.com", "@yahoo.com", "@hotmail.com")):
            raise ValidationError("Please Enter A Valid Email!")

        exiting_email = User.query.filter_by(email = field.data).first()
        if exiting_email:
            raise ValidationError("Email Already Exists, Please Enter Another One!")


class LoginForm(FlaskForm):
    username = StringField(DataRequired(), validators=[Length(min=0, max=20)])
    password = PasswordField(DataRequired(),validators= [Length(min=0)])
    submit = SubmitField("Log In")

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(email = form.email.data, username = form.username.data, password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()))
        db.session.add(new_user)
        db.session.commit()
        flash("Account Has Been Created!", 'success')
        print('success')
        return redirect(url_for('login'))
    print(request.form)
    return render_template("register.html", form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    return "register success"




if __name__ == "__main__":
    app.run(debug=True)