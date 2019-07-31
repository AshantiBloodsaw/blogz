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
    body= db.Column(db.Text)
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
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users, header='Blogz Users')

@app.route('/blog') # route 
def blog(): # route handler functions
    blog_id = request.args.get('id')
    user_id = request.args.get('userid')
    blogs = Blog.query.all()

    if user_id:
        Posts = Blog.query.filter_by(owner_id=user_id)
        return render_template('user.html', posts=posts, header='User Posts')
    if blog_id:
        blogs = Blog.query.get(blog_id)
        return render_template('blog.html',blogs=blogs, header='All Blog Posts')
        blog = Blog.query.get(blog_id) # GET request with a blog id query parameter
    return render_template ('entry.html', posts=post, header='All Blog Post')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-entry']
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
if __name__ == '__main__':
    app.run()        