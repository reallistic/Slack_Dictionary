# -*- coding: utf-8 -*-

"""A custom logger for the MessageAPI.

TODO: This should be moved into its own repository so it can beresued across
different flask apps.
"""

import sys
import logging

from flask import json, request


def setup_logger(app):

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = JSONFormatter(fmt)
    handler = logging.StreamHandler()
    handler.setLevel(app.config.get('LOG_LEVEL') or logging.INFO)
    handler.setFormatter(formatter)

    logger = logging.getLogger(app.logger_name)
    logger.addHandler(handler)
    logger.setLevel(app.config.get('LOG_LEVEL') or logging.INFO)

    @app.after_request
    def log_details(response):
        if response.direct_passthrough:
            return response

        data = {'request': request.get_loggable_dict(),
                'response': response.get_loggable_dict()}
        text = json.dumps(data)
        print text
        logger.warn(data)
        return response

    return logger


class JSONFormatter(logging.Formatter):
    def format(self, record):
        if isinstance(record.msg, dict):
            record.msg = json.dumps(record.msg)
        return super(JSONFormatter, self).format(record)
