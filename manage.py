from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os
from subprocess import call

from rova import app, db
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

@manager.command
def runserver():
    app.run()

@manager.command
def cc():
    filelist = ["main", "login"]
    for fname in filelist:
        call(["browserify", "rova/client/%s.js" % fname,
              "-o", "rova/static/js/%s.js" % fname])
    if not app.config["DEBUG"]:
        for fname in filelist:
            call(["uglify", "-s", "rova/static/js/%s.js",
                  "-o", "rova/static/js/%s.js"])

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
