# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

import os
if os.getenv('ENV') and os.getenv('ENV') == 'PROD':
    import newrelic.agent
    newrelic.agent.initialize('newrelic.ini', 'api')
import argparse

from collections import namedtuple
from gevent.wsgi import WSGIServer
from dictionary.app import create_app


args = None
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Slack Urban Dictionary API server.')
    parser.add_argument('--config', dest='config',
                        default='dictionary.config.Prod',
                        help='Dotted module path of config class.')
    parser.add_argument('--port', dest='port', type=int, default=3000,
                        help='The port to listen on.')
    args = parser.parse_args()
else:
    args = namedtuple('Args', ['config'])('dictionary.config.Prod')

app = create_app(name='api', config=args.config)

if __name__ == '__main__':
    try:
        http_server = WSGIServer(('', args.port), app, log=None)
        http_server.serve_forever()
    except KeyboardInterrupt:
        print 'goodbye'

