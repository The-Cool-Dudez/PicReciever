from flask import Flask
from app.db import dbinit

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    dbinit(app)
    from app.receiver import bp as reciever_bp
    app.register_blueprint(reciever_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app

app = create_app()
