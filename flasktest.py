from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit,Namespace
import socket
import websockets;
app = Flask(__name__,template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/")
def main():
    return render_template("clienttest.html")

@socketio.on('my message')
def test(json):
    print('현재 들어오는 인원 : ',int(json))
    
    

@socketio.on('my message', namespace='/chat')
def on_message(sid,data):
    print('hello')
    socketio.emit('my message',data,namespace='/chat')

if __name__== '__main__':
    socketio.run(app,host='localhost',port=5050)



