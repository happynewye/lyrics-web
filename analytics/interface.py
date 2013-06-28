#!/usr/bin/python
from flask import Flask

app = Flask('analytics')

with app.app_context():
    import views
    import api

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=5001)
