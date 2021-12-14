import os
import bcrypt
from flask import Flask, request, render_template, redirect
from flask.helpers import url_for
from flask_admin import Admin
from flask_login import login_required, logout_user, login_user, current_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import sqlite3
import pandas as pd
import mysql.connector
import grapher

UPLOAD_FOLDER = 'static/files'  # for uploading files
UPLOAD_FOLDER2 = "static/graphs"  # for uploading images
ALLOWED_EXTENSIONS = {'csv', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'keep it secret, keep it safe'
db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()

# Makes sure uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Users(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    acct_type = db.Column(db.Integer)  # 0 - User  1 - Admin

    def __init__(self, username, name, password, acct_type):
        self.username = username
        self.name = name
        self.password = password
        self.acct_type = acct_type

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    def get_id(self):
        return self.id


class Files(db.Model):
    __tablename__ = "Files"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    public = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, name, public):
        self.user_id = user_id
        self.name = name
        self.public = public


# Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        data = request.get_json()
        user = Users.query.filter_by(username=data['username']).first()
        if user is None or not user.check_password(data['password']):
            return (url_for("login"))[1:]
        login_user(user)
        if user.acct_type == 0:
            return url_for("home")[1:]
        elif user.acct_type == 1:
            return url_for("admin")[1:]


# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "success"


# Registration page
@app.route("/registration", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("registration.html")
    elif request.method == "POST":
        data = request.get_json()
        user = Users.query.filter_by(username=data["username"]).first()
        if user is None:
            password = data["password"]
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            user = Users(data["username"], data["name"], hashed, 0)
            db.session.add(user)
            db.session.commit()
            return "success"


# Home page
@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "GET":
        return render_template("home.html")


# Admin page
@app.route("/admin", methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def admin():
    return "admin"


# Upload files page
@app.route("/files", methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def files():
    uploadedFiles = []
    files = Files.query.filter_by(user_id = current_user.id)
    for file in files:
        if file.name not in uploadedFiles:
            uploadedFiles.append(file.name)

    if request.method == "GET":
        # Loads the page
        return render_template("editFile.html", uploadedFiles = uploadedFiles)
    elif request.method == "POST":
        # Uploads file to server and in the database
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != "" and not Files.query.filter_by(name = file.filename).first():
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    newFile = Files(current_user.id, filename, 0)
                    db.session.add(newFile)
                    db.session.commit()
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return render_template("editFile.html", uploadedFiles = uploadedFiles)
    return render_template("editFile.html", uploadedFiles = uploadedFiles)

if __name__ == "__main__":
    db.create_all()  # Only need this line if db not created
    app.run(debug=True)