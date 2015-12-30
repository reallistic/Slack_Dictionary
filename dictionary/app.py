# -*- coding: utf-8 -*-

"""Factory function for creating API apps."""



from flask import App
from .core import cache, errors, cors
from .routes import app_bp


def create_app(name=None, config=None, **kwargs):
    """Creates a configured Flask app"""
    app = App(name or __name__, **kwargs)
    if config:
        app.config.from_object(config)

    # Initialize Flask-Cors
    cors.init_app(app)

    # Initialize Flask-Cache.
    cache.init_app(app)

    # Initialize error manager.
    errors.init_app(app)

    app.register_blueprint(app_bp)


    return app
