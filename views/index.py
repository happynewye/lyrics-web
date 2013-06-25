""" GET '/' - Home Page.
"""
from flask import current_app, render_template
print('hello world')

@current_app.route('/')
def index():
    """ Return the home page.
    """
    return render_template('index.html')
