import gevent
import gevent.monkey; gevent.monkey.patch_all()
import redis


def run_workers():
    r = redis.StrictRedis(host='redis')
    p = r.pubsub()
    p.subscribe('incoming')
    print('echo is listening')
    for message in p.listen():
        print message
        r.publish('broadcast', message)


if __name__ == '__main__':
    run_workers()
