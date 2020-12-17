#import os
import time
from hashlib import sha256
from flask import Flask, render_template, request, redirect, url_for, flash, json, jsonify
#from flask_login import LoginManager, login_user, current_user, logout_user
from flask_socketio import SocketIO, join_room, leave_room, send , emit 
from models import *
from job import mainfunc
token='a157d50fa699b5a08ce9a95e185a227dc385741f8209ae92e50ab1040ec089cff2e5aafc64a04ac704c644ce38c34d1d7f7493561687c66e43eeda8186744134'
salt='sds9eMx83l1!@@))[}(+{9[a*Q~`":\'><?<>JKSd8@#$$^%(408aaDAML>.ًًًٌٍََُُُِِّْٓٔ‌ٰ  '

app = Flask(__name__)

app.secret_key = 'ali 1234'
#app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./data.db?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

socketio = SocketIO(app, manage_session=False)

@socketio.on('connect')
def connect():
    return True

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


@app.route('/chat/<Room>',methods=['POST'])
def give_history(Room):
    #print(encrypt(request.values.get('token')))
    if not encrypt(request.values.get('token')) == token:
        return {} ,401
    messages = History.query.filter_by(room=Room)
    list_message = []
    for i in messages:
        b = i.__dict__
        del b['_sa_instance_state']
        b['msg'] = b['message']
        del b['message']
        list_message.append(b)
    data = list_message
    return json.dumps({"res": data})

@socketio.on('msg')
def on_message(data):
    if not encrypt(data['token']) == token:
        emit('msg1',{'mes':'token kharabe'})
        return 0 ,401
    msg = data["msg"]

    mainfunc(msg)

    print(msg.encode('latin-1').decode('utf-8'))
    emit('msg1',{'mes':'recive'})
    room = data["room"]
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    if msg:
        message = History(message=msg.encode(
            'latin-1').decode('utf-8'), time_stamp=time_stamp, room=room)
        db.session.add(message)
        db.session.commit()
    return True

if __name__ == "__main__":
    socketio.run(app,debug=True)
    #app.run(host='0.0.0.0', port=5000, debug=True)  # 9055 ssl_context='adhoc'
