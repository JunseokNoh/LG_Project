import socketio
import eventlet
#create a Socket.IO server
sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
	print('connect ', sid)

@sio.event
def disconnect(sid):
	print('disconnect ', sid)

# @sio.on('my message',namespace='/chat')
# def another_event(sid,data):
# print(str(data))
# sio.emit('my message',{'data':'foobar'})

@sio.on('my message')
def test(sid,json):
	print('sid정보',sid)
	print('현재 들어오는 인원 : ',str(json))

eventlet.wsgi.server(eventlet.listen(('localhost',5050)),app)