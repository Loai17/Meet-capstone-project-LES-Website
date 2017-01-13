from flask import Flask, url_for, flash, redirect, request, render_template , g
from flask import session as login_session
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func

from databaseSetup import Base, Users, Newspaper

app = Flask(__name__)
app.secret_key = "lorenzo plz dont tell anyone my secret key:)"

engine = create_engine('sqlite:///DatabaseLES.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

def verify_password(email,password):
	user = session.query().filter_by(email=email).first()
	if not customer or not customer.verify_password(password):
		return False
	g.customer = customer
	return True

@app.route('/')
def home():
	return render_template('homePage.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if email=="" or password=="":
			flash("Missing Arguments")
			return redirect(url_for(login))
		if verify_password(email,password):
			customer=session.query(Customer).filter_by(email=email).one()
			flash('Login Successful, welcome, %s' % customer.name)
			login_session['name']=customer.name
			login_session['email']=customer.email
			login_session['id']=customer.id
			return redirect(url_for('inventory'))
		else:
			#incorrect username/password
			flash("Incorrect username/password combination")
			return redirect(url_for('login'))


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
		flash("User Created Successfully!")
		return redirect(url_for('profile' ,user_id = user.id))
	else:
		return render_template('signUp.html')

@app.route("/profile/<int:user_id>")
def profile(user_id):
	user = session.query(Users).filter_by(id=user_id).one()
	return render_template('profile.html' , user=user)

@app.route("/product/<int:product_id>/addToCart", methods = ['POST'])
def addToCart(product_id):
	if 'id' not in login_session:
		flash("You must be logged in to perform this action")
		return redirect(url_for('login'))
	quantity = request.form['quantity']
	product = session.query
	#CONTINUE FROM HERE - ADD TO CART BUTTON (SECTION II)

@app.route("/shoppingCart")
def shoppingCart():
	return "To be implemented"

@app.route("/removeFromCart/<int:product_id>", methods = ['POST'])
def removeFromCart(product_id):
	return "To be implmented"

@app.route("/updateQuantity/<int:product_id>", methods = ['POST'])
def updateQuantity(product_id):
	return "To be implemented"

@app.route("/checkout", methods = ['GET', 'POST'])
def checkout():
	return "To be implmented"

@app.route("/confirmation/<confirmation>")
def confirmation(confirmation):
	return "To be implemented"

@app.route('/logout', methods = ['POST'])
def logout():
	return "To be implmented"

if __name__ == '__main__':
    app.run(debug=True)
