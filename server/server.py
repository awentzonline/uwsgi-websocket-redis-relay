import time

import gevent
import gevent.select
import redis
import uwsgi


def application(env, start_response):
    uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'], env.get('HTTP_ORIGIN', ''))
    print "websockets..."
    r = redis.StrictRedis(host='redis', port=6379, db=0)
    channel = r.pubsub()
    channel.subscribe('broadcast')

    websocket_fd = uwsgi.connection_fd()
    redis_fd = channel.connection._sock.fileno()

    while True:
        # wait max 4 seconds to allow ping to be sent
        ready = gevent.select.select([websocket_fd, redis_fd], [], [], 4.0)
        # send ping on timeout
        if not ready[0]:
            uwsgi.websocket_recv_nb()
        for fd in ready[0]:
            if fd == websocket_fd:
                msg = uwsgi.websocket_recv_nb()
                if msg:
                    r.publish('incoming', msg)
            elif fd == redis_fd:
                msg = channel.parse_response()
                # only interested in user messages
                if msg[0] == 'message':
                    uwsgi.websocket_send("[%s] %s" % (time.time(), msg))
