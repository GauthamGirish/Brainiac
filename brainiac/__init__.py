import os
from flask import Flask, render_template
from pymongo import MongoClient
from azure.storage.blob import BlobServiceClient


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A homepage
    @app.route('/')
    def home():
        return render_template('index.html')

    # import and register blueprints
    from .views.auth import auth_bp
    from .views.patient import patient_bp
    from .views.doctor import doctor_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)

    # Database Connection
    # client = MongoClient()
    client = MongoClient(app.config['MONGO_URI'])
    app.db = client.brainiac_db

    # Azure Blob Storage Connection

    connect_str = app.config['AZURE_CONTAINER_KEY']
    container_name = "mriscans"

    # create a blob service client to interact with the storage account
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str)
    app.container_client = blob_service_client.get_container_client(container=container_name)

    return app

