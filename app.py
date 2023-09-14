from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///justdoit.db'
db = SQLAlchemy(app)


class JustDoIt(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(300), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=["GET", "POST"])
def just_do_it():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        doit = JustDoIt(title=title, desc=desc)
        db.session.add(doit)
        db.session.commit()
    allDoIt = JustDoIt.query.all()
    return render_template('index.html', allDoIt=allDoIt)


def create_database():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    create_database()
    app.run(debug=True, port=6969)
