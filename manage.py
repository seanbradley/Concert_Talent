'''

manage.py

This is the file you use to launch the app.

Execute the commands in this file from an interactive shell, like so...

    python manage.py [command]


To get started:

First, reset the database (this drops tables)...

    python manage.py reset_db

Then, populate the database with users listed in populate.py...

    python manage.py populate_db

Finally, run the development server...

    python manage.py runserver

'''
import sys, os
sys.path.pop(0)
sys.path.insert(0, os.getcwd())

from concert1 import app
from flask.ext.script import Manager, Server

manager = Manager(app)
manager.add_command("runserver", Server())

if __name__ == "__main__":
    manager.run()
