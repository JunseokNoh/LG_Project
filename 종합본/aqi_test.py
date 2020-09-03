import socketio


sio = socketio.Client()

sio.connect('http://34.64.236.227:8080')
json={}
json['pm']=45
json['co']=13
sio.emit('in_aqi',json)