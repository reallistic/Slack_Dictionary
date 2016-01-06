# -*- coding: utf-8 -*-

"""Urban Dictionary client"""

import requests
from flask import current_app
from requests.exceptions import RequestException
from .errors import APIError

def get_definition(word):
    word = word.strip()
    if not word:
        raise APIError('Word cannot be blank')
    try:
        resp = requests.get(current_app.config.get('API_URL') % word,
                            timeout=10)
        data = resp.json()
    except (RequestException, ValueError):
        raise APIError('Error defining word')

    try:
        definition = data['list'][0]
    except (KeyError, IndexError):
        raise APIError('No definition available')

    try:
        definition['sound'] = data['sounds'][0]
    except (KeyError, IndexError):
        pass

    return definition



