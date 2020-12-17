from flask_socketio import send, emit,join_room,SocketIO
from flask import Flask
import time
from models import *
from hashlib import sha256
import config

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = config.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = config.database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
token=config.token
salt=config.salt
namespace=config.namespace


@socketio.on('connect')
def connect():
    return True

@socketio.on('join')
def joined(data):
    if not encrypt(data['token']) == token:
        emit('msg',{'msg':'false'},room=data['room'])
        return 0
    join_room(data['room'])
    emit('msg',{'msg':'joind to '+data['room']+' channel'},room=data['room'])


@socketio.on('msg')
def handle_msg(data):
    if not encrypt(data['token']) == token:
        return {} ,401
    emit('msg',{'msg':data['msg']},room=data['room'])
    tohistory(data)


@socketio.on('histoy')
def load_history(data):
    print('hi')
    if not encrypt(data['token']) == token:
        return {}
    if data['msg']!='load_logs':
        return False
    emit('hist',give_history(data['qroom']),room=data['room'])


def tohistory(data):
    msg = data["msg"]
    room = data['room']
    print(msg.encode('latin-1').decode('utf-8'))
    room = data["room"]
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    if msg:
        message = History(message=msg.encode(
            'latin-1').decode('utf-8'), time_stamp=time_stamp, room=room)
        db.session.add(message)
        db.session.commit()



def give_history(Room):
    #print(encrypt(request.values.get('token')))
    messages = History.query.filter_by(room=Room)
    list_message = []
    for i in messages:
        b = i.__dict__
        del b['_sa_instance_state']
        b['msg'] = b['message']
        del b['message']
        list_message.append(b)
    data = list_message
    return {"res": data}

num=45
def encrypt(tok):
    num0 = num
    salt2 = salt
    for i in tok[3::-1]:
        try:
            num1=int(i)
            num0 *= int(i)
        except:
            pass
    for i in range (len(str(num0)),2):
        salt2+=chr(int(str[i])*10+int(str[i+1]))
    return sha256((tok+salt2[num1:]).encode()).hexdigest()+sha256((salt2[:num1]+tok).encode()).hexdigest()

if __name__ == "__main__":
    socketio.run(app,debug=True)
    #app.run(host='0.0.0.0', port=5000, debug=True)  # 9055 ssl_context='adhoc'
