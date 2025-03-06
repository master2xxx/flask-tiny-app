from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Import blueprints
    from .views import views
    from .auth import auth
    from .admin import admin
    from .posts import posts

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(posts, url_prefix='/')

    # Create database
    with app.app_context():
        # Import models here (inside app context)
        from .models import User, Note, Post
        db.create_all()
        print('Database tables checked/created!')

    # Setup login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Add nl2br filter for post content
    @app.template_filter('nl2br')
    def nl2br_filter(s):
        if not s:
            return s
        return s.replace('\n', '<br>')

    return app