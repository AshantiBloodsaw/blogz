from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime # imports for timestamps and password hashing.
from hashutils import make_pw_hash, check_pw_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:phpMyAdminExtra645@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = '\xa7X\xc3\xa8{0\x87)\xb2\xd7;\xedg?\xfd\xb3\xcf!jF6\x88\x13Z'

db = SQLAlchemy(app)

# create User class with ID, username, hashword, and post.

class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(120), unique=True)
     pw_hash = db.Column(db.String(120))
     blogs = db.relationship('Blog', backref='owner')

def __init__(self, password, username):
        self.pw_hash = make_pw_hash(password)
        self.username = username
# pw = password I'm assuming.

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body= db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_date = db.Column(db.DateTime)


    
    def __init__(self,title,body):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date    
        self.owner = owner
@app.before_request # required so that user is allowed to visit specific routes prior to logging in.
# this also redirects to login page once encountering a page without permission.
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index',]
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

#index route redirects to home page.        
@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users, header='Blogz Users')

@app.route('/blog') # route 
def blog(): # route handler functions
    blog_id = request.args.get('id')
    user_id = request.args.get('owner_id')
    blogs = Blog.query.all()

    if user_id:
        posts = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('user.html', posts=posts, header='User Posts')
    if blog_id:
        blogs = Blog.query.all()
        return render_template('blog.html',blogs=blogs, header='All Blog Posts')
    else:
        blog = Blog.query.get(blog_id) # GET request with a blog id query parameter
        return render_template ('entry.html', blog=blog, header='All Blog Post')
    return render_template('blog.html')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error=''
        body_error=''
        

        if not blog_title:
            title_error = "Please enter a blog title"
        if not blog_body:
            body_error = "Now enter a blog Entry"

        if not body_error and not title_error:
            new_entry = Blog(blog_title, blog_body)
            db.session.add(new_entry)
            db.session.commit()
            return redirect("./blog?id={}".format(new_entry.id))

        else:
            return render_template('newpost.html',title = 'Build-a-blog', title_error=title_error, body_error=body_error, blog_title=blog_title, blog_body=blog_body)

    return render_template('newpost.html', title='Build-a-blog')

@pp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login_username = request.form['login-username']
        login_password = request.form['login-password']
        user = User.query.filter_by(username=login_username).first()

        if not user:
            username_error = "Username does not exist."
            return render_template('login.html', username_error, username='', login_active="active")
        
        elif not check_pw_hash(login_password, user.pw_hash):
            password_error = "Incorrect password."
            return render_template('login.html', password_error=password_error, username=login_username, login_active="active")

        else:
            session['username'] = login_username
            return redirect('/newpost')

    return render_template('login.html', login_active="active")

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'GET':
        return render_template('signup.html', title="Sign Up", signup_active="active")

    if request.method == 'POST':
        new_username = request.form['new-username']
        new_password = request.form['new-password']
        new_password_verify = request.form['new-password-verify']

    username_error = ''
    password_error = ''
    verify_error = ''

    if new_username == '':
        username_error = 'Please enter a valid username.'
    elif len(new_username) <=3:
        username_error = 'Please enter a username with 4 or more characters.'
    if new_password != new_password_verify or new_password_verify == '':
        verify_error = "Please verify your password."
        password_error = 'Please reenter your password.'
    if new_password == '':
        password_error = 'Please enter a valid password.'
    elif len(new_password) <= 3:
        password_error = 'Please enter a password with 4 or more characters.'

    user_exists = User.query.filter_by(username=new_username).first()

    if user_exists:
        username_error = 'This username is already taken.'

    if username_error or password_error or verify_error:
        return render_template('/signup.html', title="Sign Up", new_username=new_username,
    username_error=username_error, password_error=password_error, verify_error=verify_error, signup_active"active")

    new_user = User(new_username, new_password)
    db.session.add(new_user)
    db.session.commit()
    session['username'] = new_user.username

    return redirect('/newpost')

@app.route('logout')
def logout():
    del session['email']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()        