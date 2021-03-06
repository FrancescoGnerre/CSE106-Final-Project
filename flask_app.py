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
import matplotlib.pyplot as matPlot

UPLOAD_FOLDER = '/home/alexholt54/mysite/static/files'  # for uploading files
ALLOWED_EXTENSIONS = {'csv', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)


SQL_ALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="alexholt54",
    password="mytopsecretpassword",
    hostname="alexholt54.mysql.pythonanywhere-services.com",
    databasename="alexholt54$graphs")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = SQL_ALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
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
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    acct_type = db.Column(db.Integer)  # 0 - User  1 - Admin

    def __init__(self, username, name, password, acct_type):
        self.username = username
        self.name = name
        self.password = password
        self.acct_type = acct_type

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode('utf8'))

    def get_id(self):
        return self.id


class Files(db.Model):
    __tablename__ = "Files"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    public = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, name, public):
        self.user_id = user_id
        self.name = name
        self.public = public

class Posts(db.Model):
    __tablename__ = "Posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    picture = db.Column(db.String(500), nullable=False, unique=True)

    def __init__(self, user_id, picture):
        self.user_id = user_id
        self.picture = picture

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

# User page
@app.route("/user", methods=["GET", "POST"])
@login_required
def user():
    uploadedPosts = []
    files = Posts.query.filter_by(user_id = current_user.id)
    for file in files:
        if file.picture not in uploadedPosts:
            uploadedPosts.append(file.picture)
    if request.method == "GET":
        # Loads the page
        return render_template("user.html", uploadedPosts = uploadedPosts, name ="You")

@app.route("/user/<name>", methods=["GET", "POST"])
def view_user(name):
    uploadedPosts = []
    uid = Users.query.filter_by(username = name).first()
    files = Posts.query.filter_by(user_id = uid.id)
    for file in files:
        if file.picture not in uploadedPosts:
            uploadedPosts.append(file.picture)
    if request.method == "GET":
            return render_template("user.html", name=uid.name, uploadedPosts = uploadedPosts)


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
    uploadedPosts = []
    postUsers = []
    idlist = []
    files = Posts.query.filter(Posts.user_id != current_user.id).all()
    for file in files:
        if file.picture not in uploadedPosts:
            uploadedPosts.append(file.picture)
            idlist.append(file.user_id)
    for uid in idlist:
        user = Users.query.filter_by(id = uid)
        for name in user:
            postUsers.append(name.name)

    if request.method == "GET":
        # Loads the page
        return render_template("home.html", uploadedPosts = uploadedPosts, length = len(uploadedPosts), postUsers = postUsers)

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
                    file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
                    return "success"

@app.route("/files/<filename>", methods=["GET", "POST", "DELETE"])
@login_required
def viewFiles(filename):
    file = Files.query.filter_by(name = filename).first()
    if file is not None:
        df = pd.read_csv("/home/alexholt54/mysite/static/files/" + filename)
        rows = df.shape[0]
        columns = df.columns
        data = df.values
        if request.method == "GET":
            return render_template("viewFile.html", name=filename, columns=columns, data=data, length=len(columns), rows=rows)
        if request.method == "POST":
            data = request.get_json()
            if data["type"] == "pie":
                row = df.iloc[data["row"]]
                labels = df.columns
                matPlot.pie(row, labels=labels)
                matPlot.title(data["title"])
                matPlot.savefig("/home/alexholt54/mysite/static/files/" + data["title"] + ".png")
                matPlot.close('all')
                post = Posts(current_user.id, data["title"] + ".png")
                db.session.add(post)
                db.session.commit()
                return "success"
            elif data["type"] == "bar":
                columns = df.columns
                row = df.iloc[data["row"]]
                matPlot.bar(columns, row)
                matPlot.title(data["title"])
                matPlot.xlabel(data["xlabel"])
                matPlot.ylabel(data["ylabel"])
                matPlot.savefig("/home/alexholt54/mysite/static/files/" + data["title"] + ".png")
                matPlot.close('all')
                post = Posts(current_user.id,data["title"] + ".png")
                db.session.add(post)
                db.session.commit()
                return "success"
            elif data["type"] == "line":
                num_cols = data["numcols"]
                matPlot.plot(df.iloc[:, 1:num_cols+1])
                matPlot.title(data["title"])
                matPlot.xlabel(data["xlabel"])
                matPlot.ylabel(data["ylabel"])
                matPlot.legend(df.iloc[:, 1:num_cols+1], title=data["legend"])
                matPlot.savefig("/home/alexholt54/mysite/static/files/" + data["title"] + ".png")
                matPlot.close('all')
                post = Posts(current_user.id,data["title"] + ".png")
                db.session.add(post)
                db.session.commit()
                return "success"


if __name__ == "__main__":
    db.create_all()  # Only need this line if db not created
    app.run(debug=True)