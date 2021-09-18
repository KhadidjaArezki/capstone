from flask_script import Manager
from flask_migrate import MigrateCommand

from app import app
from models import db

manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

# https://pricelee.herokuapp.com/ | https://git.heroku.com/pricelee.git
# DATABASE_URL: postgres://fcxbxawnnsvauw:44c5b88cda334ae537fb1713883480f3b46fdae73817f0dbfcf8f18580de0605@ec2-54-81-126-150.compute-1.amazonaws.com:5432/d6gjvlbk3cg3gi