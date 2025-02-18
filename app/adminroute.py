from flask import Blueprint, request, redirect, url_for, session,render_template,flash
from .authorization.login_register import Authorization


# Initialize the Authorization object
auth = Authorization()

# Define your blueprint
admin = Blueprint('admin', __name__, template_folder='templates/admin',url_prefix='/admin')

@admin.route('/login')
def login():
    return render_template('adminlogin.html')

@admin.route('/loginadmin', methods=['POST'])
def loginadmin():
    email = request.form['email']
    password = request.form['password']

    response = auth.login(email=email, password=password)

    if response['success']:
        flash('Login Successful!', 'success')
        return redirect(url_for('main.dashboard'))  # Correctly referring to the main.index route
    else:
        flash(response['error'], 'error')
        return redirect(url_for('main.loginvolunteer'))  # Correctly referring to the main.login route