import gevent.monkey; gevent.monkey.patch_all()

import json
import random

import gevent
import redis

from message_handler import message_handler, run_dispatcher


class ThingZone(object):
    def __init__(self):
        self.next_id = 1
        self.things = {}
        self.is_running = True

    def add_thing(self, thing):
        this_id = self.next_id
        self.next_id += 1
        thing['id'] = this_id
        self.things[this_id] = thing

    def update_thing(self, id, data):
        self.things[id].update(data)

    def remove_thing(self, id):
        del self.things[id]


def broadcast_zone(r, zone, delay=1.0):
    print('Beginning zone broadcast')
    while zone.is_running:
        r.publish('broadcast', json.dumps(['zthings', zone.things]))
        gevent.sleep(delay)
    print('Ending zone broadcast')


def handle_zone_messages(r, zone):
    pass


@message_handler('chat')
def chat_echo_handler(r, kind, body):
    r.publish('broadcast', json.dumps(['chat', body]))


def prop_update_factory(zone):
    def thing_prop_update_handler(r, kind, body):
        try:
            id, props = body
        except:
            print('bad tup {}'.format(body))
        else:
            if id in zone.things:
                thing = zone.things[id]
                thing.update(props)
            else:
                thing = zone.add_thing(props)
    return message_handler('tup')(thing_prop_update_handler)


if __name__ == '__main__':
    # TODO: use commandline params for multiprocess?
    r = redis.StrictRedis(host='redis')
    zone = ThingZone()
    # add some crap
    for i in range(1):
        zone.add_thing(dict(
            sprite='avatar0',
            x=random.randint(0,300),
            y=random.randint(0,300)
        ))
    prop_update_factory(zone)
    # start listeners
    gevent.spawn(broadcast_zone, r, zone)
    gevent.spawn(run_dispatcher)
    gevent.wait()
