from flask import Flask, url_for, flash, redirect, request, render_template , g
from flask import session as login_session
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context

from databaseSetup import Base, Users, Newsletter ,Forums ,Games ,ContactUs

app = Flask(__name__)
app.secret_key = "lorenzo plz dont tell anyone my secret key:)"

engine = create_engine('sqlite:///DatabaseLES.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()


def hash_password(password):
	password = pwd_context.encrypt(password)

def verify_password(userName,pass1):
	user = session.query(Users).filter_by(userName=userName).first()
	if(user is not None and user.password == hash_password(pass1)):
		return True
	return False

@app.route('/', methods= ['GET','POST'])
def home():
	if request.method =='POST':
		subscription = Newsletter(email=request.form['email'])
		if subscription.email =="":
			flash("Your form is missing arguments")
			return redirect(url_for('home'))
		else:
			session.add(subscription)
			session.commit()
			return redirect(url_for('home'))
	else:
		if 'id' in login_session:
			if(session.query(Users).filter_by(id=login_session['id']).first() is not None):
				user=session.query(Users).filter_by(id=login_session['id']).first()
				return render_template('homePage.html', user = user)
			else:
				return render_template('homePage.html')
		else:
			return render_template('homePage.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		userName = request.form['userName']
		password = request.form['password']
		if userName=="" or password=="":
			flash("Missing Arguments")
			return redirect(url_for('login'))
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
			password = hash_password(request.form['password']),
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
	if 'id' in login_session:
		if login_session['id'] is not None:
			return render_template('profile.html' , user=user , current_id = login_session['id'])
		else:
			return render_template('profile.html' , user=user)
	else:
		return render_template('profile.html' , user=user)

@app.route('/editProfile', methods = ['GET','POST'])
def editProfile():
	if request.method == 'POST':
		userInfo = Users(firstName = request.form['firstName'],
			lastName=request.form['lastName'],
			password = hash_password(request.form['password']),
			email = request.form['email'],
			photo = request.form['photo'],
		#	dob = request.form['dob'],
			description = request.form['description'])

		password = request.form['password']

		if userInfo.firstName =="" or userInfo.lastName == "" or userInfo.userName == "" or userInfo.email=="" or password=="":
			flash("Your form is missing arguments")
			return redirect(url_for('editProfile'))
		
		user = session.query(Users).filter_by(id=login_session['id']).one()

		if session.query(Users).filter_by(email = userInfo.email).first() is not None and user.email != userInfo.email:
			flash("A user with this email address already exists.")
			return redirect(url_for('editProfile'))
		
		if session.query(Users).filter_by(userName = userInfo.userName).first() is not None and user.userName != userInfo.userName:
			flash("This username is already taken.")
			return redirect(url_for('editProfile'))
		user.firstName = userInfo.firstName
		user.lastName = userInfo.lastName
		user.password = userInfo.password
		user.email = userInfo.email
		user.photo = userInfo.photo
		user.description = userInfo.description
		session.commit()
		flash("Applied Changes Successfuly!")
		return redirect(url_for('profile' ,user_id = user.id))
	else:
		user = session.query(Users).filter_by(id=login_session['id']).one()
		return render_template('editProfile.html',user=user)

@app.route("/games")
def games():
	games = session.query(Games).all()
	if 'id' in login_session:
			if(session.query(Users).filter_by(id=login_session['id']).first() is not None):
				user=session.query(Users).filter_by(id=login_session['id']).first()
				return render_template('games.html', user = user , games = games)
			else:
				return render_template('games.html', games=games)
	else:
		return render_template('games.html', games=games)


@app.route("/games/<int:game_id>")
def viewGame(game_id):
	game = session.query(Games).filter_by(id=game_id).one()
	if 'id' in login_session:
			if(session.query(Users).filter_by(id=login_session['id']).first() is not None):
				user=session.query(Users).filter_by(id=login_session['id']).first()
				return render_template('viewGame.html', user = user , game = game)
			else:
				return render_template('viewGame.html', game=game)
	else:
		return render_template('viewGame.html', game=game)

@app.route("/forums")
def forums():
	if 'id' in login_session:
			if(session.query(Users).filter_by(id=login_session['id']).first() is not None):
				user=session.query(Users).filter_by(id=login_session['id']).first()
				posts = session.query(Forums).all()
				return render_template('forums.html', posts=posts , user = user)
			else:
				posts = session.query(Forums).all()
				return render_template('forums.html' , posts = posts)
	else:
		posts = session.query(Forums).all()
		return render_template('forums.html' , posts = posts)

@app.route("/forums/<int:post_id>")
def viewPost(post_id):
	if 'id' in login_session:
			if(session.query(Users).filter_by(id=login_session['id']).first() is not None):
				user=session.query(Users).filter_by(id=login_session['id']).first()
				post = session.query(Forums).filter_by(id=post_id).one()
				return render_template('viewPost.html', post=post , user = user)
			else:
				post = session.query(Forums).filter_by(id=post_id).one()
				return render_template('viewPost.html' , post=post)
	else:
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


@app.route("/aboutUs")
def aboutUs():
	if 'id' in login_session:
		if(session.query(Users).filter_by(id=login_session['id']).first() is not None):
			user=session.query(Users).filter_by(id=login_session['id']).first()
			return render_template('aboutUs.html', user = user)
		else:
			return render_template('aboutUs.html')
	else:
		return render_template('aboutUs.html')


@app.route("/contactUs", methods = ['GET', 'POST'])
def contactUs():
	if request.method =='POST':
		messageRequest = ContactUs(name=request.form['name'],
			email=request.form['email'],
			message=request.form['message'])
			#press=request.form['press'],
			#customer=request.form['cutsomer'])
		if messageRequest.email =="" or messageRequest.name=="" or messageRequest.message=="":
			flash("Your form is missing arguments")
			return redirect(url_for('contactUs'))
		else:
			flash("Your message has been sent.")
			session.add(messageRequest)
			session.commit()
			return redirect(url_for('contactUs'))
	else:
		if 'id' in login_session:
			if(session.query(Users).filter_by(id=login_session['id']).first() is not None):
				user=session.query(Users).filter_by(id=login_session['id']).first()
				return render_template('contactUs.html', user = user)
			else:
				return render_template('contactUs.html')
		else:
			return render_template('contactUs.html')

@app.route('/logout')
def logout():
	login_session.pop('id', None)
	return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
