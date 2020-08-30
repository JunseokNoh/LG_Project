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
#!!!!!!해야할것
# 현재인원 들어올시 처리 해야함 api 주기적으로 불러서 처리해야함 
#비오면 창문 안열리게 하기

#필요한 변수들 선언
current_number=0#현재인원
total_number=0 #실내공간 허용가능한 최대인원 
cycle="1" #환기주기
open_time="5" #환기시간
tp=0
out_aqi=0
place="home"
weather_ic=""
room_area=0
space_range=0
int_cycle=0
int_open_time=0
window_state = 0 #창문이 열려있는지 닫혀있는지 
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
	sio.emit('init_confirm',{'place':place,'room_area':room_area,'space_range':space_range,'cycle':cycle,'open_time':open_time,'total_number':total_number})
	

@sio.on('main_connect') # main html 연결성공 메시지 및 메인화면 값전달 
def connect_print(sid,json):
	print(json['main'])
	sio.emit('main_default_value',{'open_time':int_open_time,'current_number':current_number,'total_number':total_number,'tp':tp,'out_aqi':out_aqi,'weather_ic':weather_ic,'place':place,'window_state':window_state})

@sio.on('calculator-person')#최대인원 계산 처리 함수 
def calculator_person(sid,json):
	max_person = round((json['area']*(1-(json['space_value']/100))/144))
	#print(max_person)
	global room_area
	room_area=json['area']
	global space_range
	space_range=json['space_value']
	sio.emit('calculator-person',{'max_person':max_person})
	
@sio.on('confirm-button') #confirm 화면에서 main으로 넘어갈때 값처리 
def confirm_button(sid,json):
	global total_number
	total_number = json['total_number']
	global cycle
	cycle = json['cycle']
	global open_time
	open_time = json['open_time']
	global int_cycle
	int_cycle = int(cycle)
	global int_open_time
	int_open_time = int(open_time)
	print(type(int_cycle),type(int_open_time),int_cycle,int_open_time)
	global place
	place=json['place']
	print('현재인원 ',total_number,cycle,open_time,'현재장소',place)
@sio.on('return_to_confirm')#main에서 confirm으로 돌아가는 설정 처리 
def return_confirm(sid,json):
	sio.emit('init_confirm',{'place':place,'room_area':room_area,'space_range':space_range,'cycle':cycle,'open_time':open_time,'total_number':total_number})
if __name__== '__main__':
	eventlet.wsgi.server(eventlet.listen(('10.178.0.2',8080)),app)
