from sched import scheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_apscheduler import APScheduler

scheduler = APScheduler()
db = SQLAlchemy()
# DB_NAME = "calendarapp.db"
UPLOAD_FOLDER = 'website/static/uploads/'
ENV = 'prod'
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjhjhjhjhdhjhdhjhgsjkhdshds'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    if ENV == 'dev':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/demodata'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://troologserver:@Getout12@troolog-chima-server.postgres.database.azure.com/demodata?sslmode=require'

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.init_app(app)



    from .views import views
    from .auth import  auth

    app.register_blueprint(views, url_prfix='/')
    app.register_blueprint(auth, url_prfix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    send_email_job(app)

    return app

def send_email():
    print("email sent!!!!")

def send_reminder():
    print("Reminder sent!!!!")

def create_database(app):
    # if not path.exists('website/' + DB_NAME):
    #     db.create_all(app=app)
    db.create_all(app=app)
    print('Created Database!')

def send_email_job(app):
    scheduler.add_job(id = 'send email', func= send_email, trigger = 'interval', seconds = 5)
    scheduler.add_job(id = 'send reminder', func= send_reminder, trigger = 'interval', seconds = 8)
    scheduler.start()
    print('Job Started')


