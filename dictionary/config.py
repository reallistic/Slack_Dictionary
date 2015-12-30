# -*- coding: utf-8 -*-

"""Server configuration."""

import os
import logging

from . import meta
from .env import env



class Prod(object):

    """Prod configuration object."""

    __metaclass__ = meta.Config

    AWS_ACCESS_KEY_ID = env('USEFUL_AWS_ACCESS_KEY_ID')

