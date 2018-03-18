from flask import Flask, render_template , redirect ,  url_for, request

from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, PasswordField, validators, validators, ValidationError, TextAreaField, TextField
from wtforms.validators import InputRequired, Email, Length, URL
from flask_wtf import Form
from flask_wtf import FlaskForm

from flask_bootstrap import Bootstrap
from datetime import datetime
import random, string
from sqlalchemy import desc


app = Flask(__name__)
Bootstrap(app)



#SQLALCHEMY_DATABASE_URI='mysql://username:password@server/databasename'
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://database32:Ya29~Z1iY~36@den1.mysql1.gear.host/database32'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "some_string"

#3 creating the mysql table!
class posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80))
    title = db.Column(db.String(80))
    author = db.Column(db.String(30))
    description = db.Column(db.String(200))
    post= db.Column(db.String(5000))
    AuthorDescription= db.Column(db.String(1000))
    email = db.Column(db.String(100))
    date_posted = db.Column(db.String(20))
    random = db.Column(db.String(5))


class Post_Form(Form):
    title = TextField('Title',validators=[InputRequired(), Length(min=5, max=60, message="The field must be between 5 and 60 characters long")],render_kw={"placeholder": "Title of your Post"})
    url= TextField("Website's Link",render_kw={"placeholder": "Your Blog's Link If You Have Any"})
    author = TextField("Author's Name",validators=[InputRequired(), Length(min=3, max=40, message="The field must be between 5 and 40 characters long")],render_kw={"placeholder": "Author's Name"}) # name of the author
    description = TextField('Subtitle', validators=[InputRequired(), Length(min=5, max=400, message="The field must be between 5 and 380 characters long")] ,render_kw={"placeholder": "Subtitle Of Your Post"})
    post = TextAreaField('Post', validators=[InputRequired(), Length(min=5, max=5000, message="The field must be between 5 and 2000 characters long")], render_kw={"rows": 30, "cols": 50})
    AuthorDescription = TextAreaField("Author's Description",validators=[InputRequired(), Length(min=30, max=1000, message="The field must be between 5 and 60 characters long")], render_kw={"rows": 5, "cols": 50})
    email = TextField("Email Address",validators=[InputRequired(),Email(message='Enter a valid email'), Length(min=10, max=100)],render_kw={"placeholder": "Your Email Address"}) 
    

    
#To give the random endpoint to the url
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


@app.route('/form', methods = ['GET','POST'])
def form():
    form = Post_Form(request.form)   
    if request.method == "GET":
        
        return render_template('post.html', form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            url_genrator = randomword(5)
            postedDate = datetime.utcnow().strftime("%d-%m-%y")
            Data = posts(title= form.title.data, url= form.url.data, author=form.author.data, description=form.description.data,post=form.post.data,AuthorDescription=form.AuthorDescription.data,email=form.email.data, date_posted = postedDate, random=url_genrator)
            db.session.add(Data)
            db.session.commit()

            return redirect(url_for('submitted_posts'))
        else : 
            return render_template("post.html",form=form)

##just to clarify few thing, in this code- 
## On line 69, 'title' in the left is reffered to the 'title' in the class 'posts', i.e the one resposnible for SQLdb. 
## And the 'form.title.data' refers to the info that we passout in the form. 
## And 'title' in 'form.title.data' refers to variable in the class 'Post_Form'. 



##This endpoint will show the list of all the guest posts
@app.route('/posts', methods= ['GET'])
def submitted_posts():
    dbData = posts.query.order_by(posts.id.desc()).all()  
    return render_template('post_submitted.html', dbData= dbData  )



#this endpoint will the specific post and the post will have a randon endpoint
@app.route('/guest-post/<random_id>')
def guest_post(random_id):
    article = posts.query.filter_by(random=random_id ).one()
    return render_template ('guest_post.html', post = article)
    
@app.route('/')
def index():
    return render_template ('index.html')
    
#Sample post    
@app.route('/end-to-end-encryption')
def encryption():
    return render_template ('end_to_end_encryption.html')
    

@app.errorhandler(404)
def page_not_found(e) :
    return render_template("404.html")

# using the same image as 404 error so that if someone tries something mischief, it will still give a 404 error. 
@app.errorhandler(500)
def function(e) :
    return render_template("404.html")


if __name__ == "__main__":
    app.run(port=5559 ,debug=True)
	  
