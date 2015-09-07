import gevent.monkey; gevent.monkey.patch_all()

import json
from collections import defaultdict

import gevent
import redis


message_handler_registry = defaultdict(list)


def message_handler(kinds):
    if isinstance(kinds, basestring):
        kinds = [kinds]
    def wrapper(f):
        for kind in kinds:
            message_handler_registry[kind].append(f)
        return f
    return wrapper


def run_dispatcher_with_config(handler_config):
    r = redis.StrictRedis(host='redis')
    p = r.pubsub()
    p.subscribe('incoming')
    print 'running handlers'
    for message in p.listen():
        try:
            kind, body = json.loads(message['data'])
        except:
            print('Malformed message: {}'.format(message))
        else:
            handlers = handler_config.get(kind)
            if handlers:
                for handler in handlers:
                    gevent.spawn(handler, r, kind, body)


def run_dispatcher():
    run_dispatcher_with_config(message_handler_registry)


if __name__ == '__main__':
    run_dispatcher()
