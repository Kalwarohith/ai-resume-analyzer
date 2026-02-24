from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes.upload_routes import upload_bp
    from .routes.analysis_routes import analysis_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(analysis_bp)

    return app