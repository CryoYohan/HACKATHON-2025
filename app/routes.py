from flask import Blueprint, render_template, session, url_for, redirect, flash, request
from .authorization.login_register import Authorization
from .entities.volunteer import Volunteer
from .databasehelper.dbhelper import Databasehelper

# Define your blueprint
main = Blueprint('main', __name__, template_folder='templates/user')

db = Databasehelper()

# Initialize the Authorization object
auth = Authorization()

# After request function to control cache
@main.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
    return response

# Landing page route
@main.route('/')
def index():
    """Landing page."""
    return render_template('index.html')

# Login page route
@main.route('/loginvolunteer')
def loginvolunteer():
    """Render Login Page."""
    return render_template('login.html')

# Register page route
@main.route('/registervolunteer')
def registervolunteer():
    return render_template('register.html')


@main.route('/dashboard')
def dashboard():
    posts = db.getall_records_with_user('Post')
    print(posts)
    return render_template('Dashboard.html', posts=posts)

# Login handling route
@main.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    response = auth.login(email=email, password=password)

    if response['success']:
        flash('Login Successful!', 'success')
        return redirect(url_for('main.dashboard'))  # Correctly referring to the main.index route
    else:
        flash(response['error'], 'error')
        return redirect(url_for('main.loginvolunteer'))  # Correctly referring to the main.login route

# Register handling route
@main.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    volunteer = Volunteer(name=name,email=email)

    response = auth.register(**volunteer.__dict__,password=password)

    if response['success']:
        flash('Register Successful!', 'success')
        return redirect(url_for('main.loginvolunteer'))  # Correctly referring to the main.index route
    else:
        flash(response['error'], 'error')
        return redirect(url_for('main.loginvolunteer'))  # Correctly referring to the main.login route

