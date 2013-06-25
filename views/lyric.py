""" GET '/lyric/<_id>' - Internal Lyric Page
"""
from flask import current_app, render_template, request, Markup

from backend.backend import Backend
backend = Backend()

@current_app.route('/lyric/<_id>/')
def lyric(_id):
    """ Show a lyric.
    """
    query = request.args.get('query', 'magic')
    song = backend.get(_id)
    return render_template('lyric.html', song=song)
