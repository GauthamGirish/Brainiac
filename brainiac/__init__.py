from flask import Flask


def create_app():
    app = Flask(__name__)

    # Import and register blueprints
    from .views.auth import auth
    from .views.patient import patient

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(patient, url_prefix='/patient/')

    return app
