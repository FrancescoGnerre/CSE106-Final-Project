from flask import Flask, request, render_template, redirect
from flask.helpers import url_for
from flask_admin import Admin
from flask_login import login_required, logout_user, login_user, current_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Login
@app.route("/", methods = ["GET", "POST"])
def login():
    return render_template('login.html')

if __name__ == "__main__":
    # db.create_all() # Only need this line if db not created
    app.run(debug=True)