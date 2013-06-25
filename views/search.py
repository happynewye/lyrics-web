""" GET '/search/' - Search results page.
"""
from flask import current_app, render_template, request
from backend.backend import Backend

backend = Backend()

@current_app.route('/search/')
def search():
    """ Return search results.
    """
    # Search query.
    query = request.args.get('query')

    results = backend.search(query)

    return render_template('search.html',
            query=query,
            results = results
            )
