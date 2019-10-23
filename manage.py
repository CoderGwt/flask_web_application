import os

from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, Migrate

app = create_app(os.environ.get("FLASK_CONFIG") or 'default')
manage = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Role=Role, User=User)


manage.add_command('shell', Shell(make_context=make_shell_context))
manage.add_command('db', MigrateCommand)


@manage.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manage.run()