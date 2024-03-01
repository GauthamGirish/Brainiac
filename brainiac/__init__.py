from flask import Flask
from dotenv import load_dotenv
import os
from database import initialize_db  # Correct import

load_dotenv()  # Load environment variables from the .env file


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # config and init db
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
    initialize_db(app)

    # Import and register blueprints
    from .views.auth import auth
    from .views.patient import patient

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(patient, url_prefix='/patient/')

    return app
