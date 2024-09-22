from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
HOSTNAME = "rindfleisch.mysql.pythonanywhere-services.com"
USERNAME = "rindfleisch"
PASSWORD = "supersecurepassword"
DATABASE = "rindfleisch$dbShop"


def create_database():
    db.create_all()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'this a zamazon'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DATABASE}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))

    # NOTE: For Blueprint lib
    from .views import views
    from .auth import auth
    from .admin import admin
    from .routeSP import routeSP
    from .models import Customer, Cart, Product, Order

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(routeSP, url_prefix='/')

    #with app.app_context():
    #    create_database()

    return app
