# -*- coding: utf-8 -*-

"""Server configuration."""

import os
import logging

# Helper to distinctly identify undefined values
ENV_NOT_FOUND = '__NONE__'


def env(key, default=ENV_NOT_FOUND, cast=None, optional=False):
    """Convenience function load environment variables"""

    rv = os.getenv(key, ENV_NOT_FOUND)
    if cast and rv != ENV_NOT_FOUND:
        try:
            if cast == list:
                rv = rv.split(',')
                rv = [v.strip() for v in rv]
            else:
                rv = cast(rv)
        except Exception:
            message = 'WARNING: Environment variable "%s" could not be cast ' + \
                      'by %s'
            print message % (key, cast)

    if rv != ENV_NOT_FOUND:
        return rv

    if default != ENV_NOT_FOUND:
        return default

    if not optional:
        message = 'WARNING: Environment variable "%s" not set and has ' + \
                  'no default value.'
        print message % key
        return ENV_NOT_FOUND


class Config(type):

    """Metaclass to issue warning when loading empty config variables"""

    def __new__(mcs, name, bases, attrs):
        """Wrapper to create a iterator over the config variables"""

        config_values = {}
        for attr_name, attr_value in attrs.iteritems():
            if not callable(attr_value):
                config_values[attr_name] = attr_value

        attrs['_config_values'] = config_values

        return super(Config, mcs).__new__(mcs, name, bases, attrs)

    def __getattribute__(cls, key):
        try:
            value = super(Config, cls).__getattribute__(key)
            if value != ENV_NOT_FOUND:
                return value
            else:
                print "WARNING: Config value not defined: %s" % key
        except AttributeError:
            raise


class Prod(object):

    """Prod configuration object."""

    __metaclass__ = Config

    # Flask app config
    CACHE_DEFAULT_TIMEOUT = 30 * 24 * 3600
    CACHE_ENABLED = False
    CACHE_KEY_PREFIX = 'dictionary-cache:'
    CACHE_REDIS_URL = env('CACHE_REDIS_URL')
    CACHE_TYPE = env('CACHE_TYPE', default='simple')

    CORS_AUTOMATIC_OPTIONS = True
    CORS_HEADERS = 'Content-Type'
    CORS_MAX_AGE = 31 * 86400
    CORS_SEND_WILDCARD = False
    CORS_SUPPORTS_CREDENTIALS = False

    DEBUG = env('DEBUG', cast=bool, default=False)
    LOG_LEVEL = logging.INFO
    PRETTY_PRINT_LOGS = False
    PROPAGATE_EXCEPTIONS = False
    SSLIFY_ENABLED = env('SSLIFY_ENABLED', cast=bool, default=False)
    WTF_CSRF_ENABLED = False

    # Custom config
    API_URL = env('API_URL',
                  default='http://api.urbandictionary.com/v0/define?term=%s')


class Dev(Prod):
    """Development overrides"""
    SSLIFY_ENABLED = False
    PRETTY_PRINT_LOGS = True
    DEBUG = True
    TESTING = True
    LOG_LEVEL = logging.DEBUG
