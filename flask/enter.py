from flask import Flask,render_template,request,url_for,session,redirect,flash
from flask_sqlalchemy import SQLAlchemy
import bpdb
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import Form, BooleanField, StringField, IntegerField, PasswordField, validators
from flask_mail import Mail, Message
from flask_login import LoginManager


app = Flask(__name__)


app.config['DEBUG'] =True
app.config['TESTING'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'baburajaiswarya862@gmail.com'
app.config['MAIL_PASSWORD'] = 'baburajaiswarya321'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False


mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HmS.sqlite3'
db = SQLAlchemy(app)
app.secret_key="43221"

login_manager = LoginManager()
login_manager.login_view = 'signin'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return register.query.get(int(id))

class RegistrationForm(Form):
    id =  IntegerField('id')
    firstname = StringField('firstname', [validators.Length(min=4, max=25)])
    lastname = StringField('lastname', [validators.Length(min=4, max=25)])
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=35)])
    password = PasswordField('password', [validators.DataRequired(),
        validators.EqualTo('confirm', message='passwords must match')])
    confirmpassword = PasswordField('confirmpassword')


class MyForm(Form):
    bid = IntegerField('bid',validators=[DataRequired()])
    id =  IntegerField('id', validators=[DataRequired()]) 
    username = StringField('username', [validators.Length(min=4, max=25)])
    about = StringField('about', [validators.Length(min=4, max=25)]) 
    description = StringField('description', [validators.Length(min=4, max=25)]) 
    

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


@app.route('/signin',methods=["POST", "GET"])
def signin():

    if request.method == "POST":
        user=request.form["email"]
        
        session["user"]=user

        user1=request.form["Password"]
        
        
        user=register.query.filter_by(email=user).first()
    
        
        return redirect(url_for("signup",user=user))

        if not user or not check_password_hash(user.password,user1):
        #if login is not None:
            flash("check login credential")
            return(redirect(url_for("signin")))


        login_user(user)
        flash("you have been logged in")
        return redirect(url_for("index"))

@app.route('/signup',methods=["POST","GET"])
def signup():

    form=RegistrationForm(request.form)
    #bpdb.set_trace()
    if request.method =="POST":
        
        msg = Message("successfully registered",

                sender="baburajaiswarya862@gmail.com",

                recipients=["aiswaryababuraj61@gmail.com"])

        msg.body = "Thank you for registering with us"
        mail.send(msg)
        user= register(id=form.id.data, firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, password=form.password.data, confirmpassword=form.confirmpassword.data)
        db.session.add(user)
        db.session.commit()
        result=register.query.all()
        #bpdb.set_trace()
        return redirect(url_for('signin', result=result))
    else:   
        return render_template('signup.html',form=form) 

@app.route('/about')
def about():
    return render_template('/about.html') 

@app.route('/services',methods=["POST","GET"])
def services():
    form = MyForm(request.form)
    if request.method =="POST":
        obj= blog(bid=form.bid.data,id=form.id.data,username=form.username.data,date_created=date,about=form.about.data,description=form.description.data)
        db.session.add(obj)
        db.session.commit()
        #result=blog.query.all()
        return redirect(url_for('bdes'))
    else:
        return render_template('/services.html',form=form) 

@app.route('/services/<int:bid>/update',methods=["GET","POST"])
def update(bid):
    form = MyForm(request.form)
    emp=blog.query.filter_by(bid=bid).first()
    if request.method=='POST':
        if emp:
            db.session.delete(emp)
            db.session.commit()
            bid=form.bid.data
            id=form.id.data
            username=form.username.data
            date_created=date
            about=form.about.data
            description=form.description.data
            emp=blog(bid=bid,id=id,username=username,date_created=date,about=about,description=description)
            
            db.session.add(emp)
            db.session.commit()
            return redirect(url_for('bdes', bid=bid))
        return f"User with id = {bid} Does not exist"
    user = blog.query.filter_by(bid=bid).first()
    return render_template('update.html', emp=user)

@app.route('/services/<int:bid>/delete', methods=['GET','POST'])
def delete(bid):
    sample = blog.query.filter_by(bid=bid).first()
    if request.method == 'POST':
        if sample:
            db.session.delete(sample)
            db.session.commit()
            return redirect(url_for('bdes'))
        abort(404)
 
    return render_template('delete.html', sample=sample)


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