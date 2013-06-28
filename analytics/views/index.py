from flask import current_app, render_template

@current_app.route('/')
def index():
    """Return the landing page.
    """
    return render_template('index.html')
