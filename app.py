import os
from flask import Flask, render_template, request
from flask import request
from functools import wraps

def main():
    app = Flask(__name__, static_folder='build/static', template_folder='build')

    def check_auth(username, password):
        if os.environ.get("USERNAME") == username and os.environ.get("PASSWORD") == password:
            return True

    def needs_auth(next):
        @wraps(next)
        def wrapped_view(**kwargs):
            auth = request.authorization
            if not (auth and check_auth(auth.username, auth.password)):
                return ('Unauthorized', 401, {
                    'WWW-Authenticate': 'Basic realm="Login Required"'
                })

            return next(**kwargs)

        return wrapped_view

    @app.route('/')
    @needs_auth
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = main()
    app.run()