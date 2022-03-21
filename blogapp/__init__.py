from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from flask_login import LoginManager, login_required
import pandas as pd
from flask_uploads import UploadSet, IMAGES, configure_uploads
import dash
import dash_bootstrap_components as dbc
from flask.helpers import get_root_path

db = SQLAlchemy()
csrf = CSRFProtect()
csrf._exempt_views.add('dash.dash.dispatch')
login_manager = LoginManager()


def create_app(config_class_name):
    # print(str(config_class_name) + "1111")
    app = Flask(__name__)
    from blogapp import config
    app.config.from_object(config.DevelopmentConfig)

    dashapp = register_dashapp(app)
    csrf.init_app(app)

    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        from blogapp.models import Blog
        db.create_all()
        init_db(db)

    from blogapp.blog.routes import blog_bp
    app.register_blueprint(blog_bp)

    from blogapp.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app


def register_dashapp(app):
    """ Registers the Dash app in the Flask app and make it accessible on the route /dashboard/ """
    from blogapp.dashapp import layout
    from blogapp.dashapp.callbacks import register_callbacks

    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/dashboard/',
                         assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                         meta_tags=[meta_viewport],
                        )

    with app.app_context():
        dashapp.title = 'Dashboard'
        dashapp.layout = layout.layout
        register_callbacks(dashapp)

    # Protects the views with Flask-Login
    _protect_dash_views(dashapp)


def _protect_dash_views(dash_app):
    """ Protects Dash views with Flask-Login"""
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.routes_pathname_prefix):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])


def init_db(db):
    filename = Path(__file__).parent.joinpath('data', 'blogs.csv')
    df = pd.read_csv(filename)
    df.dropna(axis=0, inplace=True)
    df.to_sql(name='blog', con=db.engine, if_exists='replace', index=False)
