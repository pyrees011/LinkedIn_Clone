from flask import Flask, render_template, request
from flask_login import LoginManager, current_user
import os

from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("secret_key")
    app.config['secret_key'] = os.getenv("Secret_key")
    app.config['UPLOAD_FOLDER'] = "LinkedIn/static/uploads"
    app.config['PROFILE'] = "LinkedIn/static/profile"

    from .auth import auth
    from .views import views
    from .mongo import mongo

    app.register_blueprint(auth, url_prefix = "/")
    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(mongo, url_prefix = "/")

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .model import User
    from .sqlite import getUserById

    @login_manager.user_loader
    def load_user(id):
        data = getUserById(id)
        if data:
            cur_user = User(id=data[0][0], username=data[0][1], password=data[0][2], email=data[0][3], type=data[0][4])
            return cur_user
        
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500
        
    @app.before_request
    def log_before_request():
        app.logger.info('Global Middleware - Response header: %s', request.headers)

    @app.after_request
    def log_after_request(response):
        app.logger.info('Global Middleware - Response Status: %s', response.status)
        return response        

    return app