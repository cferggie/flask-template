from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import path, makedirs

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    # Create databases directory if it doesn't exist
    db_dir = path.join(path.dirname(path.abspath(__file__)), 'databases')
    makedirs(db_dir, exist_ok=True)

    # define where the database is located (in the databases folder)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(db_dir, DB_NAME)}'

    # initialize the database
    db.init_app(app)
    
    CORS(app)

    # register blueprints
    from .routes import routes
    app.register_blueprint(routes, url_prefix='/')

    # create the database (import is necessary to run the models file to define the database before creating it)
    from . import models

    create_database(app)

    # configure CORS with more specific settings
    CORS(app, resources={
        r"/*": {  # Only apply CORS to routes starting with /
            "origins": ["http://localhost:5173", "http://localhost:3000"],  # Allow both Vite and React default ports
            "methods": ["GET", "POST", "PUT", "DELETE"],  # List allowed methods
            "allow_headers": ["Content-Type", "Description", "Context"]  # List allowed headers
        }
    })

    return app

def create_database(app):
    db_path = path.join(path.dirname(path.abspath(__file__)), 'databases', DB_NAME)
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
            print('Created Database!')
