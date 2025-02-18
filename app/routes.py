from flask import Blueprint, render_template, session, url_for, redirect, flash, request
from .authorization.login_register import Authorization
from .entities.volunteer import Volunteer
from .databasehelper.dbhelper import Databasehelper
from datetime import datetime

# Define your blueprint
main = Blueprint('main', __name__, template_folder='templates/user')

db = Databasehelper()

volunteer = None

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
    global volunteer
    posts = db.getall_records_with_user('Post')
    print(posts)
    return render_template('Dashboard.html', posts=posts)


@main.route('/viewpost/<id>')
def viewpost(id):
    global volunteer
    post = db.find_record_with_user('Post', id=id)
    volunteers = db.getall_records('Post_Participation')
    
    if not post:
        return "Post not found", 404

    # Check if it's a list and get the first record
    if isinstance(post, list) and len(post) > 0:
        post = post[0]  

    return render_template('viewpost.html', post=post, volunteers=volunteers)


@main.route('/join/<id>/<user_id>')
def join(id,user_id):
    global volunteer
    
    if not session.get('user'):
        flash("You must be logged in to join an event.", "error")
        return redirect(url_for('main.loginvolunteer'))  # Redirect to login if not logged in
    
    if volunteer == None:
        volunteer = Volunteer(**{k:v for k,v in session.get('user').items() if k !='success'})

    # Check if user already joined
    existing_record = db.find_record_by_user_post("Post_Participation", user_id=user_id, post_id=id)
    if existing_record:
        flash("You have already joined this event.", "warning")
        return redirect(url_for('main.viewpost', id=id))

    # Insert new participation record
    db.add_record("Post_Participation", user_id=user_id, post_id=id, joined_at=datetime.now())

    flash("Successfully joined the event!", "success")
    return redirect(url_for('main.viewpost', id=id))



# Login handling route
@main.route('/login', methods=['POST'])
def login():
    global volunteer
    email = request.form['email']
    password = request.form['password']

    response = auth.login(email=email, password=password)

    if response['success']:
        session['user'] = response
        volunteer = Volunteer(**{k:v for k,v in response.items() if k !='success'})
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

