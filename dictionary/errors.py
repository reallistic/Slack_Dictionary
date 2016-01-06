# -*- coding: utf-8 -*-

"""Error module to standardize the way the API can do a clean exit"""


from werkzeug.exceptions import ClientDisconnected
from .helpers import make_json_response

class ErrorManager(object):
    """Helper class to dispatch and monitor errors."""

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initializes error handles"""

        @app.errorhandler(400)
        def handle_general_error(err):
            """Handler for general error"""
            error_message = 'Uh oh. An error yet to be described has occurred.'
            return make_json_response(text=error_message, status_code=400)

        @app.errorhandler(429)
        def handle_ratelimit_error(err):
            """Handler for too many requests."""
            return make_json_response(text=str(err.description), status_code=429)

        @app.errorhandler(500)
        def handle_error(err):
            message = 'An unhandled exception occurred.'
            return make_json_response(text=message, status_code=500)

        @app.errorhandler(APIError)
        def handle_api_error(err):
            """Generic handler making it easy to do a clean exit from anywhere

            It is good practice to initialize this instance with a status_code
            property as that will be picked up by `make_json_response`.
            """
            return make_json_response(**err.to_dict())

        @app.errorhandler(ClientDisconnected)
        def handle_client_disconnect_error(err):
            return make_json_response(text=err.description, status_code=400)



class APIError(Exception):
    """Error for when a generic error occurs"""

    def __init__(self, message, status_code=400):
        super(APIError, self).__init__()
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return 'API error: %s' % self.message

    def to_dict(self):
        error = {'text': self.message,
                 'response_type': 'ephemral'}
        if self.status_code:
            error['status_code'] = self.status_code
        return error
