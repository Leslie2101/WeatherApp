from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
DB_NAME = os.environ.get("DB_NAME")
PASSWORD = os.environ.get("PASSWORD")

def create_database(app):
    #if not os.path.exists('todolist/' + DB_NAME):
    with app.app_context():
        db.create_all()
        print("create DB!")


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://root:{PASSWORD}@localhost/weathers'
    db.init_app(app)
    
    from .models import Note

    create_database(app)
    from weather.user import user    
    app.register_blueprint(user)
    return app
    