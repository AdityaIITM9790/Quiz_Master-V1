from flask import Flask
from applications.database import db#3 database

app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
    db.init_app(app)

    # Push app context at runtime
    app.app_context().push()

    return app

# Create the app instance
app = create_app()
from applications.controllers import *
from applications.models import *
# from applications.resources import *

if __name__ == '__main__':
    app.run(debug=True)
