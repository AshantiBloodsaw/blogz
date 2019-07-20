from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:jimjonestown2435@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body= db.Column(db.String(120))

    
    def __init__(self,title,body):
        self.title = title
        self.body = body

@app.route('/')
def index():
     return redirect('/blog')

@app.route('/blog')
def blog():
    blog_id = request.args.get('id')

    if blog_id == None:
        blogs = Blog.query.all()
        return render_template('blog.html',blogs=blogs, title='Build-a-blog')
    else :
        blog = Blog.query.get(blog_id)
        return render_template ('entry.html', blog=blog, title='Blog Entry')

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