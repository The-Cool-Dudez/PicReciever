from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.receiver import bp as reciever_bp
    app.register_blueprint(reciever_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app

app = create_app()
