""" Flask based web interface.
"""

from analytics.track import Track
track = Track()


from flask import Flask, request
import time

# Create the flask web app with the current module as the import_module.
app = Flask(__name__)

@app.before_request
def set_start_time():
    """ Set the request's start time.
    """
    request.start_time = time.monotonic()

@app.after_request
def track_total_time(req):
    """ Track the total time spent handling the request.
    """
    dt = time.monotonic() - request.start_time
    track.request(request, dt)
    return req

# Import all the files in the 'views' directory.
with app.app_context():
    import views
