from flask import Blueprint, render_template, session, url_for, redirect

main = Blueprint('main',__name__,template_folder='templates/user')

@main.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache,no-store,must-revalidate'
    return response 

@main.route('/')
def index():
    """Landing page."""
    return render_template('index.html')