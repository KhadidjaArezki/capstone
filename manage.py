from flask_script import Manager
from flask_migrate import MigrateCommand

from app import app
from models import db

manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

# https://pricelee.herokuapp.com/ | https://git.heroku.com/pricelee.git
# DATABASE_URL: postgres://lhuslnebcducvl:30080033264aab1a671c418276bd46d55a041557aa222e134c680409390ffcb6@ec2-44-198-151-32.compute-1.amazonaws.com:5432/d6olfm5pj49u4p