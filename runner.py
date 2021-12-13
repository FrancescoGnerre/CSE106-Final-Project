from flask import Flask, request, render_template, redirect
from flask.helpers import url_for
from flask_admin import Admin
from flask_login import login_required, logout_user, login_user, current_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'keep it secret, keep it safe'
db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return 0;
    # return Users.query.filter_by(user_id = user_id).first()


# users database.
class Users(UserMixin, db.Model):
    __tablename__ = "Users"
    user_name = db.Column(db.String, primary_key=True)
    pasword = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String, nullable=False)
    user_key = db.Column(db.Integer, nullable=False)
    # is_admin is for admin view. Only our accouts will be admin
    # nullable = True is default
    is_admin = db.Column(db.Integer)

    def __init__(self, user_name, display_name, password, is_admin):
        self.user_name = user_name
        self.display_name = display_name
        self.password = password
        self.is_admin = is_admin

    def salt_hash_check_password(self, password):
        # does stuff
        return self.password == password

    def get_key(self):
        return self.user_key


# Login
@app.route("/", methods=["GET", "POST"])
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
