# -*- coding: utf-8 -*-
"""Tests the basic route"""

from . import BaseTestCase



class RouteTestCase(BaseTestCase):
    def test_base_route(self):
        data = {'token': 'abc',
                'team_id': 'abc',
                'channel_id': 'abc',
                'channel_name': 'abc',
                'user_id': 'abc',
                'user_name': 'abc',
                'command': 'abc',
                'text': 'abc',
                'response_url': 'abc'}
        res = self.post('/', data=data)
        self.assertEquals(res.status_code, 200)
