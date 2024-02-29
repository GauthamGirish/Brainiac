from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'can be anything for now'
    
    # import and register blueprints
    from .views.auth import auth
    from .views.patient import patient

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(patient, url_prefix='/patient/')


    return app