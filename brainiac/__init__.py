from flask import Flask
from dotenv import load_dotenv, find_dotenv
import os


def create_app():
    app = Flask(__name__)
    # Load environment variables from .env file
    load_dotenv(find_dotenv())

    # Get the MongoDB URI from environment variables
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['MONGO_URI'] = os.getenv('SECRET_KEY')

    # Import and register blueprints
    from .views.auth import auth
    from .views.patient import patient

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(patient, url_prefix='/patient/')

    return app
