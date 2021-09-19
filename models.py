import os
# from config import environ
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import TIME
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from datetime import datetime 

database_path = os.environ.get('PROD_DATABASE_URL')

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_path variable to have multiple verisons of a database
'''

def db_drop_and_create_all(db):
    db.drop_all()
    db.create_all()
    
    
    # add one demo row for user, 2 alerts, 1 filter, 1 deal
    
    user = User(
        user_id='112442572274179169362',
        user_name='khadidjaarezki999',
        email='khadidjaarezki999@gmail.com' 
    )
    user.insert()

    filter_ = Filter(
        name='category'
    )
    filter_.insert()

    product1 = Product(
        product_id='110538092605',
        name='Laptop battery for DELL Latitude 6MT4T E5470 E5570 7.6V 62Wh',
        link='https://cgi.sandbox.ebay.com/Laptop-battery-DELL-Latitude-6MT4T-E5470-E5570-7-6V-62Wh-/110538092605',
        image='https://thumbs2.sandbox.ebaystatic.com/m/m24uZs-gnzxrtT1_19PUQxw/140.jpg',
        initial_price=28.5,
        current_price=28.0,
        price_difference=0,
        currency='USD',
        last_updated=datetime.now(),
        store='ebay'
    )
    product1.insert()

    product2 = Product(
        product_id='110538066270',
        name='For 2020 MacBook Pro Air 13” A2338 A2337 laptop sleeve bag handbag carry pouch',
        link='https://cgi.sandbox.ebay.com/2020-MacBook-Pro-Air-13-A2338-A2337-laptop-sleeve-bag-handbag-carry-pouch-/110538066270?var=0',
        image='https://thumbs1.sandbox.ebaystatic.com/pict/04040_0.jpg',
        initial_price=15.99,
        current_price=15.99,
        price_difference=0,
        currency='USD',
        last_updated=datetime.now(),
        store='ebay'
    )
    product2.insert()

    alert1 = Alert(
        user_id=1,
        desired_price=25.0,
        product_id=1,
        created=datetime.now()
    )
    alert1.insert()

    alert2 = Alert(
        user_id=1,
        desired_price=25.0,
        product_id=2,
        created=datetime.now()
    )
    alert2.insert()

    deal = Deal(
            name='2021 Newest Dell Inspiron 3000 Laptop, 15.6 HD Display, Intel N4020 Processor, 16GB RAM, 512GB PCIe SSD, Online Meeting Ready, Webcam, WiFi, HDMI, Bluetooth, Win10 Home, Black',
            link='https://www.dell.com/en-us/shop/gaming-laptops/g15-gaming-laptop/spd/g-series-15-5510-laptop/gn5510eyrns',
            image='https://i.dell.com/is/image/DellContent//content/dam/global-site-design/product_images/dell_client_products/notebooks/g_series/15_5510/cn,hk,tw/media_gallery/cs2003g0063_370697_cs_co_media_gallery_g15_5510_dark-shadow-grey_coral-kb_notebook_ff1.psd?fmt=pjpg&pscan=auto&scl=1&hei=402&wid=402&qlt=85,0&resMode=sharp2&op_usm=1.75,0.3,2,0&size=402,402',
            price=1099.99,
            currency='USD',
            store='dell'
    )
    deal.insert()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# Association table between users and products
#----------------------------------------------------------------------------#
user_products = db.Table('user_products',
    db.Column('user_id', db.INTEGER, db.ForeignKey('User.id'), primary_key=True),
    db.Column('product_id', db.INTEGER, db.ForeignKey('Product.id'), primary_key=True)
)

#----------------------------------------------------------------------------#
# Main Models

class Deal(db.Model):
    __tablename__ = 'Deal'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    link =  db.Column(db.String(500),nullable=False, unique=True)
    image =  db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String, nullable=False)
    store = db.Column(db.String, nullable=False)

    '''
    form representation of the Deal model
    '''

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'link': self.link,
            'image': self.image,
            'price': self.price,
            'currency': self.currency,
            'store': self.store
        }

    '''
    insert()
        inserts a new model into a database

        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.format()}'


class Product(db.Model):
    '''A product is added when a user creates an alert 
    for it. A product is updated periodically 
    '''
    __tablename__ = 'Product'

    id = db.Column(db.INTEGER, primary_key=True)
    product_id = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String(500), nullable=False)
    link =  db.Column(db.String(500),nullable=False, unique=True)
    image =  db.Column(db.String(500), nullable=True)
    initial_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    price_difference = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String, nullable=False)
    store = db.Column(db.String, nullable=False)
    last_updated = db.Column(db.DateTime(), nullable=False)
    alerts = db.relationship('Alert', back_populates='product')
    # users = db.relationship('User', secondary=user_products, backref=db.backref('products', lazy=True))
    '''
    form representation of the Deal model
    '''
    def format(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.name,
            'product_link': self.link,
            'product_image': self.image,
            'product_initial_price': self.initial_price,
            'product_current_price': self.current_price,
            'product_price_difference': self.price_difference,
            'product_currency': self.currency,
            'product_store': self.store,
            'last_updated': self.last_updated
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''
    def update(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.format()}'


class Alert(db.Model):
    '''
    An alert is created by an authenticated 
    user for a particular product
    '''
    __tablename__= 'Alert'
    id = db.Column(db.INTEGER, primary_key=True)
    desired_price = db.Column(db.Float, nullable=False)
    product_id = db.Column(Integer, db.ForeignKey('Product.id'), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(Integer, db.ForeignKey('User.id'), nullable=False)
    product = db.relationship('Product', back_populates='alerts')
    user = db.relationship('User', back_populates='alerts')

    def format(self):
        return {
            'alert_id': self.id,
            'alert_product': self.product.format(),
            'desired_price': self.desired_price,
            'created_at': self.created
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return f'{self.format()}'


class User(db.Model):
    '''A user is added at sign up '''
    __tablename__ = 'User'
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.String(), nullable=False, unique=True)
    user_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    alerts = db.relationship('Alert', back_populates='user')
    products = db.relationship('Product', secondary=user_products, backref=db.backref('users', lazy=True))

    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'email': self.email
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return f'{self.format()}'


class Filter(db.Model):
    ''' 
    Search filters are added by the manager
    and admin to enhance search results precision
    '''
    __tablename__ = 'Filter'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(500), nullable=False, unique=True)

    def format(self):
        return {
            'id': self.id,
            'filter_name': self.name,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f'{self.format()}'
