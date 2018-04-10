import re
import json
import logging
from channels import Group, Channel
from channels.sessions import channel_session
from .models import Room

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    message.reply_channel.send({"accept": True})

    try:
        print(message['path'])
        prefix, label = message['path'].strip('/').split('/')
        if prefix != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return
        room = Room.objects.get(label=label)
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return
    except Room.DoesNotExist:
        log.debug('ws room does not exist label=%s', label)
        return

    log.debug('chat connect room=%s client=%s:%s', 
        room.label, message['client'][0], message['client'][1])
    Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)
    message.channel_session['room'] = room.label


@channel_session
def ws_receive(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        print(label)
        print(room)
    except KeyError:
        log.debug('no room in channel_session')
        return
    except Room.DoesNotExist:
        log.debug('recieved message, buy room does not exist label=%s', label)
        return
    
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return
    print(data)
    if set(data.keys()) != set(('handle', 'message')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room=%s handle=%s message=%s', 
            room.label, data['handle'], data['message'])
        m = room.messages.create(**data)
        print(m)
        Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})

# def ws_receive(message):
#     payload = json.loads(message['text'])
#     payload['reply_channel'] = message.content['reply_channel']
#     Channel("chat.receive").send(payload)


@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass



@channel_session
# @catch_client_error
def chat_join(message):
    # room = get_room_or_error(message["room"], message.user)
    
    # if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
    #     room.send_message(None, message.user, MSG_TYPE_ENTER)
    room, status = Room.objects.get_or_create(id=1)
    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "title": room.title,
        }),
    })
    

@channel_session
# @catch_client_error
def chat_leave(message):
    # room = get_room_or_error(message["room"], message.user)
    # if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
    #     room.send_message(None, message.user, MSG_TYPE_LEAVE)
    
    room.websocket_group.discard(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))

    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(room.id),
        }),
    })


@channel_session
# @catch_client_error
def chat_send(message):
    # if int(message['room']) not in message.channel_session['rooms']:
    #     raise ClientError("ROOM_ACCESS_DENIED")
    # room = get_room_or_error(message["room"], message.user)
    print(message['message'])
    print(message['user'])
    room, status = Room.objects.get_or_create(id=1)
    # user="123"
    # user, status = User.objects.get_or_create(id=1,username="raju")
    msg = Message.objects.create(content=message['message'], room=room, creator=message['user'])
    room.send_message(message["message"], message['user'])
