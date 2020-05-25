from flask import Flask
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py') #update app setiings in app.config
    db.init_app(app) # Initialize database within the flask application
    from user.views import user_app # Importing here to avoid circular imports
    app.register_blueprint(user_app)
    # Above code->Flask to know new module/blueprint is created & make it available across other blueprints.
    return app
