from flask import Flask
from user.views import user_app

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    app.register_blueprint(user_app)
    # Above code->Flask to know new module/blueprint is created & make it available across other blueprints.
    return app