from flask import Flask
from flask_cors import CORS #type: ignore

application = Flask(__name__)
application.config.from_object('config')
CORS(application, origins="*")

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()

from routes.movies import * #type: ignore
from routes.users import * #type: ignore