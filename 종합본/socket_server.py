import socketio
import eventlet
import json
import urllib.request
#create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
air_condition_url="http://api.airvisual.com/v2/nearest_city?key=d459ec55-5797-44d9-a8ef-136efc7d1d7c"


air_page = urllib.request.urlopen(air_condition_url) #url을 여는 함수 
air_condition_dic = json.loads(air_page.read()) #url을 열어서 json을 읽어와 Dic 형태로 저장 

#필요한 변수들 선언
current_number=0#현재인원
total_number=0 #실내공간 허용가능한 최대인원 
cycle=0 #환기주기
open_time=0 #환기시간
tp=0
out_aqi=0
weather_ic=""

tp = int(air_condition_dic['data']['current']['weather']['tp'])
out_aqi = int(air_condition_dic['data']['current']['pollution']['aqius'])
weather_ic=air_condition_dic['data']['current']['weather']['ic']


print(type(tp),type(out_aqi),type(weather_ic))
print(tp,out_aqi,weather_ic)



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

@sio.on('my message') #출입구에 설치된 카메라를 통해 실내인원 계산 
def test(sid,json):
	#print('sid정보',sid)
	#print('현재 들어오는 인원 : ',json['key'])
	current_number=json['key']
	if json['key'] == -5:
		value=1
		sio.emit('open_window',{'key':value})
		print('success send to open window')
	elif json['key'] ==-10:
		value = 2
		sio.emit('open_window',{'key':value})
		print('success send to close window')
	

@sio.on('index_connect') #index.html연결 성공 메시지
def connect_print(sid,json):
	print(json['index'])


@sio.on('confirm_connect')#confirm_html 연결성공 메시지
def connct_print(sid,json):
	print(json['confirm'])

@sio.on('main_connect') # main html 연결성공 메시지 및 메인화면 값전달 
def connect_print(sid,json):
	print(json['main'])
	sio.emit('main_default_value',{'current_number':current_number,'total_number':total_number,'tp':tp,'out_aqi':out_aqi,'weather_ic':weather_ic})

@sio.on('calculator-person')#최대인원 계산 처리 함수 
def calculator_person(sid,json):
	max_person = round((json['area']*(1-(json['space_value']/100))/144))
	#print(max_person)
	sio.emit('calculator-person',{'max_person':max_person})
	
@sio.on('confirm-button') #confirm 화면에서 main으로 넘어갈때 값처리 
def confirm_button(sid,json):
	global total_number
	total_number = json['total_number']
	cycle = json['cycle']
	open_time = json['open_time']
	print('현재인원 ',total_number,cycle,open_time)
	
if __name__== '__main__':
	eventlet.wsgi.server(eventlet.listen(('localhost',8080)),app)
