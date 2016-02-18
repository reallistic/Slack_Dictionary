# -*- coding: utf-8 -*-

"""Helper functions."""

import time
import pytz
from datetime import datetime
from flask import json, make_response


def make_json_response(*args, **kwargs):
    """Adds status_code argument to jsonify."""
    status_code = kwargs.pop('status_code', None)
    response_body = json.dumps(dict(*args, **kwargs))
    response = make_response(response_body, status_code)
    response.content_type = 'application/json'
    return response


def get_usec_timestamp(delta=None):
    offset = 0
    if delta:
        offset = delta.total_seconds()
    return int((time.time() + offset) * 1e6)


def iso8601_from_usec(usec):
    """Return a microsecond timestamp as an ISO8601 string

    Note that we prefer the UTC format using 'Z' defined by W3 over the
    equally valid +00:00 used by default in Python.
    """
    return datetime.fromtimestamp(usec / 1e6, pytz.utc).isoformat()[:-6] + 'Z'
