from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, NumberRange, EqualTo, ValidationError, Length, Email
import bcrypt   
from flask_login import login_manager, UserMixin, login_required, login_user, logout_user, current_user, LoginManager
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = "DOUUFP98Y98VOUDGV8O78ODIJFGIU"
db = SQLAlchemy(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "danger"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Manhwa(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    cover_image = db.Column()
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
    username = StringField("Username", validators=[DataRequired(),Length(min=0, max=20)])
    password = PasswordField("Password",validators= [DataRequired(),Length(min=0)])
    submit = SubmitField("Log In")

class SearchForm(FlaskForm):
    search_name = StringField("Search", validators=[DataRequired()])


def discover_manhwa(manhwa_name):
    url = "https://graphql.anilist.co"
    
    query = """" 
    query ($name: String){
        page(page:1, perpage:10){
        media (search: $name, type: MANGA, countryOfOrigin:"KR", sort: TRENDING_DESC){
            id
            title{
                english
                romaji
            }
            coverImage{
                large
            }
            description(asHTML: false)
            chapters
            status
            avarageScore
            genre
            }
        }
    }
    """

    variables = {
        "name":manhwa_name
    }

    response = requests.post(url, json={'query':query, 'variables':variables})
    if response.status_code == 200:
        data = response.json
        return data["data"]
    return []


def get_manhwa(manhwa_name):
    url = "https://graphql.anilist.co"
    
    query = """
    query ($name: String){
        Page(page:1, perPage:10){
        media (search: $name, type: MANGA, countryOfOrigin:"KR"){
            id
            title{
                english
            }
            coverImage{ large }
            description(asHTML: false)
            chapters
            status
            averageScore
            genre
            }
        }
    }
    """

    variables = {
        "name":manhwa_name
    }

    response = requests.post(url, json={'query':query, 'variables':variables})
    print("STATUS:", response.status_code)
    print("BODY:", response.text[:1000])
    if response.status_code == 200:
        data = (response.json)
        return data["api_ok":True,"data"]

    return {"api_ok": False, "data": {}}

@app.route("/spage")
def startpage():
    return render_template("startpage.html")

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
    return render_template("register.html", form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user:
            db_password = user.password if isinstance(user.password, bytes) else user.password.encode('utf-8')
            form_pw = form.password.data.encode('utf-8') 
            if bcrypt.checkpw(form_pw, db_password):
                login_user(user)
                flash("Login Successful", "success")
                return redirect(url_for('home'))

    return render_template('login.html', form=form)


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/search")
def search():

    form = SearchForm()
    manhwa_name = request.args.get("q", "") 
    if manhwa_name:
        data = get_manhwa(manhwa_name)
        all_data = data.get("Page",{}).get("media", [])
        api_ok = data["api_ok"]
    else:
        api_ok = True
        all_data = []
    print("RESULTS:", all_data)


    return render_template("search.html", form = form, manhwas = all_data, api_ok= api_ok, searched = bool(manhwa_name  ))





if __name__ == "__main__":
    app.run(debug=True)