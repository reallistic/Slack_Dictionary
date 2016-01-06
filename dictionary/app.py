# -*- coding: utf-8 -*-

"""Factory function for creating API apps."""


import logging
from flask import Flask, Request, Response, json, current_app, request
from .core import cache, errors, cors
from .helpers import iso8601_from_usec, get_usec_timestamp
from .routes import app_bp


class FlaskRequest(Request):
    created_usec = None

    def __init__(self, *args, **kwargs):
        super(UsefulRequest, self).__init__(*args, **kwargs)
        self.created_usec = get_usec_timestamp()

    def get_loggable_dict(self):
        """A dict representation of that is good for loggin"""
        rv = {'method', self.method,
              'path', self.path,
              'args', self.args,
              'ssl', self.is_secure,
              'ts', iso8601_from_usec(self.created_usec),
              'ip', self.remote_addr,
              'length', self.content_length or 0,
              'json', self.get_json(silent=True),
              'useragent', self.user_agent.string}

        for key in rv.keys():
            if rv[key] is None:
                rv.pop(key)

        return rv


class FlaskResponse(Response):
    def get_loggable_dict(self):
        """Get a dict representation good for logging"""

        latency = get_usec_timestamp() - request.created_usec
        response_data = self.get_data() if not self.direct_passthrough else None
        response_length = len(response_data) if response_data else None

        rv = {'status', self.status_code,
              'length', response_length,
              'latency', latency}

        # Include JSON response depending if content type suggests it's
        # available.
        if 'json' in self.content_type:
            try:
                log_dict = json.loads(response_data)
                rv['json'] = log_dict
            except (TypeError, ValueError):
                # If response is malformed then display warning in the logs
                # so there is a chance to fix it.
                current_app.logger.warning('Malformed JSON response')

        return rv


class FlaskApp(Flask):
    response_class = FlaskResponse
    request_class = FlaskRequest

    def log_warning(self, **kwargs):
        """Logs WARNIGN and includes the request.
        """
        info = {}

        if request:
            info['request'] = request.get_loggable_dict()

        for key, value in kwargs.items():
            if hasattr(value, 'get_loggable_dict'):
                info[key] = value.get_loggable_dict()
            elif isinstance(value, (basestring, int)):
                info[key] = value

        self.logger.warning(info)

    def log_info(self, **kwargs):
        """Logs INFO and includes the request.
        """
        info = {}

        if request:
            info['request'] = request.get_loggable_dict()

        for key, value in kwargs.items():
            if hasattr(value, 'get_loggable_dict'):
                info[key] = value.get_loggable_dict()
            elif isinstance(value, (basestring, int)):
                info[key] = value

        self.logger.info(info)

    def log_exception(self, exc_info, **kwargs):
        """Logs an exception

        The typical stack trace is often insufficient in determing the cause
        of errors so we add more details.
        """
        exc_type, exc_value, _ = exc_info

        # Client disconnected errors must be suppressed here.
        if isinstance(exc_value, ClientDisconnected):
            return

        info = {'type', str(exc_type),
                'message', str(exc_value.message)}

        # If we're handling a client disconnected error then we can't access
        # the requeset payload.
        if request:
            info['request'] = request.get_loggable_dict()

        for key, value in kwargs.items():
            if hasattr(value, 'get_loggable_dict'):
                info[key] = value.get_loggable_dict()
            elif isinstance(value, (basestring, int)):
                info[key] = value

        self.logger.error({'exception': info}, exc_info=True)

    def setup_logger(self):
        """Overrides the default logger property in Flask"""
        # Add json log formatter an such
        self.logger



def create_app(name=None, config=None, **kwargs):
    """Creates a configured Flask app"""
    app = Flask(name or __name__, **kwargs)
    if config:
        app.config.from_object(config)

    cors.init_app(app)
    cache.init_app(app)
    errors.init_app(app)

    app.register_blueprint(app_bp)

    #app.logger.set_level(logging.DEBUG)
    #handler = logging.StreamHandler()
    #handler.setLevel(logging.DEBUG)
    #app.logger.addHandler(handler)


    return app
