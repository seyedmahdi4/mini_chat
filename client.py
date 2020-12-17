import socketio
import requests
import json
import time


address='http://localhost:5000'
tok='123456'
sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.on('msg1')
def my_message(data):
    print('>>> '+ data['mes'])

@sio.event
def disconnect():
    print('disconnected from server')

try:
    sio.connect(address)
except:
    print('i dont have connect')
    exit()


def send(msg,room='msg'):
    sio.emit(room, {
                'msg': msg, 'room': 'exe','token':tok })

his=requests.post(address+'/chat/exe',data={'token':tok})
for i in json.loads(his.text)['res']:
    print('>>> '+i['msg'])

while True:
    input()
    send(input(' ➜ '))