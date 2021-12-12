from flask import Flask, request, render_template, redirect
from flask.helpers import url_for
from flask_admin import Admin
from flask_login import login_required, logout_user, login_user, current_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///class-enrollment.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'keep it secret, keep it safe'
db = SQLAlchemy(app)

# Login
@app.route("/", methods = ["GET", "POST"])
def login():
    return render_template('login.html')

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return url_for('login')[1:]

if __name__ == "__main__":
    # db.create_all() # Only need this line if db not created
    app.run(debug=True)