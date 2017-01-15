from flask import Flask, url_for, flash, redirect, request, render_template , g
from flask import session as login_session
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func

from databaseSetup import Base, Users, Newspaper , Forums

app = Flask(__name__)
app.secret_key = "lorenzo plz dont tell anyone my secret key:)"

engine = create_engine('sqlite:///DatabaseLES.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

def verify_password(userName,pass1):
	user = session.query(Users).filter_by(userName=userName).first()
	if(user.password == pass1):
		return True
	return False

@app.route('/')
def home():
	return render_template('homePage.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		userName = request.form['userName']
		password = request.form['password']
		if userName=="" or password=="":
			flash("Missing Arguments")
			return redirect(url_for(login))
		elif (verify_password(userName,password)):
			user =session.query(Users).filter_by(userName=userName).one()
			flash('Login Successful, welcome, %s' % user.firstName)
			login_session['userName']=user.userName
			login_session['email']=user.email
			login_session['id']=user.id
			return redirect(url_for('home'))
		else:
			#incorrect username/password
			flash("Incorrect username/password combination")
			return redirect(url_for('login'))
	else:
		return render_template('login.html')


@app.route('/signup', methods = ['GET','POST'])
def signup():
	if request.method == 'POST':
		user = Users(firstName = request.form['firstName'],
			lastName=request.form['lastName'],
			userName = request.form['userName'],
			email = request.form['email'],
			photo = request.form['photo'],
		#	dob = request.form['dob'],
			description = request.form['description'])
		
		password = request.form['password']

		if user.firstName =="" or user.lastName == "" or user.userName == "" or user.email=="" or password=="":
			flash("Your form is missing arguments")
			return redirect(url_for('signup'))
		
		if session.query(Users).filter_by(email = user.email).first() is not None:
			flash("A user with this email address already exists.")
			return redirect(url_for('signup'))
		
		if session.query(Users).filter_by(userName = user.userName).first() is not None:
			flash("This username is already taken.")
			return redirect(url_for('signup'))

		user.hash_password(password)
		session.add(user)
		session.commit()
		login_session['id'] = user.id
		flash("User Created Successfully!")
		return redirect(url_for('profile' ,user_id = user.id))
	else:
		return render_template('signUp.html')

@app.route("/profile/<int:user_id>")
def profile(user_id):
	user = session.query(Users).filter_by(id=user_id).one()
	if login_session['id'] is not None:
		return render_template('profile.html' , user=user , current_id = login_session['id'])
	else:
		return render_template('profile.html' , user=user)


@app.route("/games")
def games():
	return render_template('games.html')

@app.route("/forums")
def forums():
	posts = session.query(Forums).all()
	return render_template('forums.html' , posts = posts)

@app.route("/forums/<int:post_id>")
def viewPost(post_id):
	post = session.query(Forums).filter_by(id=post_id).one()
	return render_template('viewPost.html' , post=post)

@app.route("/addPost", methods = ['GET', 'POST'])
def addPost():
	if request.method == 'POST':
		post = Forums(title = request.form['title'],
			description = request.form['description'],
			user_id = login_session['id'])
		if post.title =="" or post.description == "":
			flash("Your form is missing arguments")
			return redirect(url_for('addPost'))
		else:
			session.add(post)
			session.commit()
			return redirect(url_for('viewPost' , post_id=post.id))
	else:
		return render_template('addPost.html')


@app.route("/confirmation/<confirmation>")
def confirmation(confirmation):
	return "To be implemented"

@app.route('/logout', methods = ['POST'])
def logout():
	return "To be implmented"

if __name__ == '__main__':
    app.run(debug=True)
