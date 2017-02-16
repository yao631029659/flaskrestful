from flask_script import Manager,Server
from flaskrestful import app
from models import db,User
manager=Manager(app)
manager.add_command('server',Server())

@manager.shell
def make_shell_context():
    return dict(app=app,User=User,db=db)

if __name__=="__main__":
    manager.run()
