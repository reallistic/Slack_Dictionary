# -*- coding: utf-8 -*-

"""Server configuration."""

from dictionary.config import Dev


class TestConfig(Dev):
    CACHE_REDIS_URL = 'redis://localhost:6379/0'
