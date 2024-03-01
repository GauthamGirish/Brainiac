from flask_pymongo import PyMongo

mongo = PyMongo()


def initialize_db(app):
    mongo.init_app(app)

    # Check if the connection is successful
    try:
        # Accessing any attribute to trigger connection
        app.config['MONGO_DBNAME']
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print("Failed to connect to MongoDB. Error:", e)
