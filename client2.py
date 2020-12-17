import socketio
import json
from time import sleep
sio = socketio.Client()

address='http://localhost:5000'
token='123456'
my_room='pc2' #pc num
to_room='pc1'
@sio.event
def connect():
    print('connected')

@sio.on('msg')
def my_message(data):
    print(data)

@sio.on('hist')
def my_message(his):
    for l in his['res']:
        print(' >>> '+l['msg'])


@sio.event
def disconnect():
    print('disconnected')

sio.connect(address)


def sender(msg):
    sio.emit('msg', {'msg': msg, 'room': to_room,'token':token})

def load_history():
    sio.emit('histoy', {'msg': 'load_logs', 'room': my_room , 'qroom': my_room,'token':token})

if sio.connected == False:
    print('--- error to connect ----')
    exit()

while True:
    try:
        sio.emit('join',{'room':my_room,'token':token})
        break
    except:
        sleep(1)

load_history()


while True:
    input()
    text=input(' ➜ ')
    if text!='':
        sender(text)