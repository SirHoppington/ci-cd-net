from flask import Flask, redirect, request
from config import config
#import asyncio
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from werkzeug.security import generate_password_hash
import uuid
from flask_login import LoginManager
from nornir import InitNornir

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
nr = InitNornir(config_file="./app/config.yaml")

def create_app(config_name=None):
    if config_name is None:
        app = Flask(__name__, instance_path="/usr/src/app")
        app.config.from_object(config.get("development"))
    else:
        app = Flask(__name__, instance_path="/usr/src/app")
        app.config.from_object(config.get(config_name))
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    '''
    login_manager.login_view='auth.sign_in'
    login_manager.init_app(app)
    '''
    from app.routes.get_configs import get

    app.register_blueprint(get)

    from app.routes.add_hosts import post

    app.register_blueprint(post)

    
    with app.app_context():
        db.create_all()

    '''
        if not Users.query.filter_by(email=admin_email).first():
            # Generate default admin user account:
            new_user = Users(
                public_id = str(uuid.uuid4()),
                name = default_admin,
                email = admin_email,
                password = generate_password_hash(admin_password),
                role="admin")
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
    
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return redirect('/signin?next=' + request.path)
    '''
    return app
