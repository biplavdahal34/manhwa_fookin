from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Manhwa(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String, nullable = False)
    genre = db.Column(db.String, nullable = False)
    ratings_number  = db.Column (db.Integer, nullable = False)
    rating_text = db.Column(db.String)

@app.route("/")
def home():
    return 'app running'



if __name__ == "__main__":
    app.run(debug=True)