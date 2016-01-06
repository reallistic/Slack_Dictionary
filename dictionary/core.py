# -*- coding: utf-8 -*-

"""Instantiation of core libraries."""

from flask_cache import Cache
from flask_cors import CORS

from .errors import ErrorManager


cache = Cache()
cors = CORS()
errors = ErrorManager()
