from message_handler import message_handler


@message_handler('chat')
def chat_echo_handler(r, kind, body):
    r.publish('broadcast', json.dumps(['chat', body]))
