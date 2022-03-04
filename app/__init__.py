from flask import Flask

def create_app():
    app = Flask(__name__)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')
    
    from .simulate import simulate as simulate_blueprint
    app.register_blueprint(simulate_blueprint, url_prefix='/simulate')

    return app

