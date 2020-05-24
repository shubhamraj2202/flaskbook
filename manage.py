import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
# Above we are appending project path to Python Path

from flask.ext.script import Manager, Server
from application import create_app

app = create_app()
manager = Manager(app)  # Manger will be able to control app
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,  # Application reload when any code is changed
    host=os.getenv('IP', '0.0.0.0'),  # For Cloud9 env else directly use 0.0.0.0 
    port=int(os.getenv('PORT', 7000)) # Same
))

if __name__ == "__main__":
    manager.run()
