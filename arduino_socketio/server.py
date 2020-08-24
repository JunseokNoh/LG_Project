import socketio
import eventlet
#create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
	print('connect ', sid)

@sio.event
def disconnect(sid):
	print('disconnect ', sid)


@sio.on('my event')
def test(sid,json):
	print('sid정보',sid)
	print('현재 들어오는 인원 : ',str(json))

@sio.on('connect_message') #index.html연결 성공 메시지
def connect_print(sid,json):
	print('connect2 : ',sid)
	print(str(json))

@sio.on('where_connect') # where_html 연결성공 메시지
def connect_print(sid,json):
	print('where.html : ',sid)
	print(str(json))
@sio.on('confirm_connect')#confirm_html 연결성공 메시지
def connct_print(sid,json):
	print('confirm_connect: ',sid)
	print(str(json))

@sio.on('calculator-person')#최대인원 계산 처리 함수 
def calculator_person(sid,json):
	max_person = round((json['area']*(1-(json['space_value']/100))/144))
	#print(max_person)
	sio.emit('calculator-person',{'max_person':max_person})
if __name__== '__main__':
	eventlet.wsgi.server(eventlet.listen(('localhost',8080)),app)