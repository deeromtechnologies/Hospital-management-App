from flask import Flask,render_template,request,url_for,session,redirect
from flask_sqlalchemy import SQLAlchemy
import bpdb
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import Form, BooleanField, StringField, IntegerField, PasswordField, validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HMS.sqlite3'
db = SQLAlchemy(app)
app.secret_key="43221"

class RegistrationForm(Form):
    id =  IntegerField('id')
    firstname = StringField('firstname', [validators.Length(min=4, max=25)])
    lastname = StringField('lastname', [validators.Length(min=4, max=25)])
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=35)])
    password = PasswordField('password', [validators.DataRequired(),
        validators.EqualTo('confirm', message='passwords must match')])
    confirmpassword = PasswordField('confirmpassword')
    

class register(db.Model):

    id = db.Column(db.String(120), primary_key=True)
    firstname = db.Column(db.String(120), unique=False, nullable=False)
    lastname = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    confirmpassword = db.Column(db.String(120), unique=False, nullable=False)

def __init__(self, id, firstname, lastname, username, email, password, confirmpassword):

    self.id = id
    self.firstname = firstname
    self.lastname = lastname
    self.username = username
    self.email = email
    self.password = password
    self.confirmpassword = confirmpassword

class blog(db.Model):

    bid = db.Column(db.String(120), primary_key=True)
    id = db.Column(db.String(120), db.ForeignKey('register'))
    username = db.Column(db.String(100), unique=False, nullable=False)
    #bpdb.set_trace()
    date_created = db.Column(db.DateTime, nullable=False)
    about = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(800), unique=False, nullable=False)
    
    

def __init__(self, bid, id, username, date_created, about, description):

    self.bid = bid
    self.id = id
    self.username = username
    self.date_created = date_created
    self.about = about
    self.description = description
date=date.today()    

    
@app.route('/users')
def users():
    result1=register.query.all()
    #bpdb.set_trace()
    return render_template('users.html',result=result1 )


@app.route('/details/<id>')
def details(id):
    result1=register.query.filter_by(id=id).first()
    return render_template('details.html',result=result1 )


@app.route('/bdes')
def bdes():
    result1=blog.query.all()
    #bpdb.set_trace()
    return render_template('bdes.html',result=result1 )



@app.route('/')
def index():
    # bpdb.set_trace()
    return render_template('index.html')


@app.route('/signin',methods=["POST","GET"])
def signin():
    if request.method =="POST":
        username=request.form["username"]
        # bpdb.set_trace()
        session["username"]=username
        password=request.form["password"]
        session["password"]=password
        return redirect(url_for("index"))
    else:
        return render_template('signin.html')

@app.route('/signup',methods=["POST","GET"])
def signup():

    form=RegistrationForm(request.form)
    #bpdb.set_trace()
    if request.method =="POST":
        #bpdb.set_trace()
        user= register(id=form.id.data, firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, password=form.password.data, confirmpassword=form.confirmpassword.data)
        db.session.add(user)
        db.session.commit()
        result=register.query.all()
        return redirect(url_for('users', result=result))
    else:   
        return render_template('signup.html',form=form) 

@app.route('/about')
def about():
    return render_template('/about.html') 

@app.route('/services',methods=["POST","GET"])
def services():
    #bpdb.set_trace()
    if request.method =="POST" and form.validate_on_submit() :
        #bpdb.set_trace()
        obj= blog(bid=request.form['bid'],id=request.form['id'],username=request.form['username'],date_created=date,about=request.form['about'],description=request.form['description'])
        db.session.add(obj)
        db.session.commit()
        return redirect(url_for('bdes'))
    else:
        return render_template('/services.html') 

@app.route('/edit',methods=["POST","GET"])
def edit():
    #bpdb.set_trace()
    if request.method =="POST":
        #bpdb.set_trace()
        obj= blog(bid=request.form['bid'],id=request.form['id'],username=request.form['username'],date_created=date,about=request.form['about'],description=request.form['description'])
        db.session.add(obj)
        db.session.commit()
        return redirect(url_for('bdes'))
    else:
        return render_template('/services.html')


@app.route('/images')
def images():
    return render_template('/images.html') 

@app.route('/doctors')
def doctors():
    return render_template('/doctors.html') 

@app.route('/contact')
def contact():
    return render_template('/contact.html') 

@app.route('/logout')
def logout():
    
    # bpdb.set_trace()
    session.pop('username', None)
    return redirect(url_for('signin')) 


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)