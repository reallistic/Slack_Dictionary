# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import logging
import mock
import requests
import time
import unittest

from flask import json

from dictionary.core import cache
from dictionary.app import create_app
from werkzeug.datastructures import Headers


class BaseTestCase(unittest.TestCase):

    """Base for common functions across all tests.

    TODO: We need a dedicated test account.
    """

    app = None
    worker_app = None

    @classmethod
    def setup_class(cls):

        # Prepare the app and push the app context.
        cls.app = cls._create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client(use_cookies=False)

        # Make sure we are not working against the production database.
        assert 'localhost' in cls.app.config['CACHE_REDIS_URL']

        cls.get_request_patcher = mock.patch.object(requests, 'Request')

    def setUp(self):
        """Runs before each job"""
        # Clear the flask-cache redis cache.
        cache.clear()

        self.get_request_mock = self.get_request_patcher.start()
        self.addCleanup(self.tearDown)


    def tearDown(self):
        """Runs after each job"""
        # Stop mocking functions, objects and libraries.
        patchers = [self.get_request_patcher]
        for patcher in patchers:
            try:
                patcher.stop()
            except:
                # Patcher already stopped.
                pass

    def shortDescription(self):
        """Turns off docstrings in verbose output"""
        return None

    @classmethod
    def _create_app(cls):
        """Creates a Flask application instance

        We need to create the app in this base class even though the super class
        determines what app we are creating. Not following this patterns would mean
        we need duplication of the code to push the context.

        For testing non-endpoint related functionality we create an app straight
        from the factory.
        """
        return create_app('automated_tests', config='tests.config.TestConfig')

    def get(self, *args, **kwargs):
        return self.jsonpost(*args, method='GET', **kwargs)

    def delete(self, *args, **kwargs):
        return self.jsonpost(*args, method='DELETE', **kwargs)

    def patch(self, *args, **kwargs):
        return self.jsonpost(*args, method='PATCH', **kwargs)

    def post(self, *args, **kwargs):
        return self.jsonpost(*args, method='POST', **kwargs)

    def jsonpost(self, *args, **kwargs):
        """Convenience method for making JSON POST requests."""
        kwargs.setdefault('content_type', 'application/json')
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])

        headers = Headers()
        override_headers = kwargs.pop('headers', {})
        if override_headers:
            for k, v in override_headers.items():
                headers.add(k, v)

        if 'useragent' in kwargs:
            useragent = kwargs.pop('useragent')
            headers.add('User-Agent', useragent)

        # Set a quick JSON lookup attribute.
        if 'method' in kwargs:
            method = getattr(self.client, kwargs.get('method').lower())
        else:
            method = self.client.post

        response = method(headers=headers, *args, **kwargs)

        try:
            response.json = json.loads(response.data)
        except:
            response.json = None

        return response
