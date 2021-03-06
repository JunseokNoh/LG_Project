import socketio
import eventlet
import json
import urllib.request
import time
#create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


#!!!!!!해야할것
# 현재인원 들어올시 처리 해야함 
#비오면 창문 안열리게 하기 (처리완료)
#부저울리게 처리

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
distance_number=0
window_state = 0 #창문이 열려있는지 닫혀있는지 
buzzer_state=0 #부저가 울리고있는지 아닌지
pm=0.0
co=0.0


@sio.event
def connect(sid, environ):
	print('connect ', sid)

@sio.event
def disconnect(sid):
	print('disconnect ', sid)


@sio.on('my message') #출입구에 설치된 카메라를 통해 실내인원 계산 
def test(sid,json):
	#print('sid정보',sid)
	#print('현재 들어오는 인원 : ',json['key'])
	current_number=json['key']
	sio.emit('current_number',{'key':current_number})
	# if json['key'] == -5:
	# 	value=1
	# 	sio.emit('open_window',{'key':value})
	# 	print('success send to open window')
	# elif json['key'] ==-10:
	# 	value = 2
	# 	sio.emit('open_window',{'key':value})
	# 	print('success send to close window')
@sio.on('from_in_camera')
def cal(sid,json):
	distance_number=json['key']
	print(distance_number)
	sio.emit('social_distance',{'key':distance_number})

	
@sio.on('control_the_window_plz') #main으로부터 창문 통제 제어받음 
def control(sid,json):
	print("창문 동작 신호 수신",json['value'])
	global window_state
	if json['value'] ==0: #0이오면 창문을 닫아달라
		if window_state ==1: #창문이 열려있는 상태면
			sio.emit('to_window',{'value':0})
			window_state=0 
	elif json['value']==1:#1이오면 창문을 열어달라 
		if window_state ==0: #창문이 닫혀있는 상태면
			sio.emit('to_window',{'value':1})
			window_state=1
@sio.on('control_the_buzzer_plz')
def buz_control(sid,json):
	global buzzer_state
	if json['value']==1:
		if buzzer_state==0:
			sio.emit('to_buzzer',{'value':1})

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
	sio.emit('main_default_value',{'open_time':int_open_time,'current_number':current_number,'total_number':total_number,'place':place,'window_state':window_state,'open_cycle':int_cycle})

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

@sio.on('in_aqi')
def calculator_aqi(sid,json):
	print(json)
	global pm
	global co
	pm = json['pm'] #미세먼지
	co = json['co'] #일산화탄소
	print("일산화탄소",co)
	print("미세먼지",pm)
	co_hi=0#지수구분
	co_lo=0
	co_bp_hi=0.0#농도구분
	co_bp_lo=0.0

	pm_hi=0# 지수구분
	pm_lo=0
	pm_bp_hi=0 #농도구분
	pm_bp_lo=0

	Ip=0.0
	if co<=2:
		co_hi=50
		co_lo=0
		co_bp_hi=2
		co_bp_lo=0
	elif co>=2.01 and co<=9:
		co_hi=100
		co_lo=51
		co_bp_hi=9
		co_bp_lo=2.01
	elif co>=9.01 and co<=15:
		co_hi=250
		co_lo = 101
		co_bp_hi=15
		co_bp_lo=9.01
	else:
		co_hi = 500
		co_lo = 251
		co_bp_hi=50
		co_bp_lo=15.01
	if int(pm)<=15:
		pm_hi=50
		pm_lo=0
		pm_bp_hi=15
		pm_bp_lo=0
	elif int(pm)>=16 and int(pm)<=35:
		pm_hi = 100
		pm_lo = 51
		pm_bp_hi=35
		pm_bp_lo=16
	elif int(pm)>=36 and int(pm)<=75:
		pm_hi=250
		pm_lo=101
		pm_bp_hi=75
		pm_bp_lo=36
	else:
		pm_hi=500
		pm_lo=251
		pm_bp_hi=500
		pm_bp_lo=76
	if pm_hi>=250 and co_hi>=250:#둘다 나쁨 이상일경우
		if co_hi>pm_hi:#co가 매우나쁨일경우
			Ip=(((co_hi-co_lo)/(co_bp_hi-co_bp_lo))*(co-co_bp_lo)+co_lo)
			Ip+=50
		else: #아닐경우 미세먼지로 계산 
			Ip=((pm_hi-pm_lo)/(pm_bp_hi-pm_bp_lo))*(pm-pm_bp_lo)+pm_lo
			Ip+=50
	elif co_hi > pm_hi: #일산화탄소가 더 오염됐을경우 
		Ip=(((co_hi-co_lo)/(co_bp_hi-co_bp_lo))*(co-co_bp_lo)+co_lo)
	else: #둘다 나쁨이아닐경우는 미세먼지로 계산
		Ip=(((pm_hi-pm_lo)/(pm_bp_hi-pm_bp_lo))*(pm-pm_bp_lo)+pm_lo)
	
	Ip=round(Ip)
	print('실내공기상태 : ',Ip)
	sio.emit('in_aqi_to_main',{'in_aqi':Ip})
	#보내주면끝//완료


		
		 


			


			
@sio.on('return_to_confirm')#main에서 confirm으로 돌아가는 설정 처리 
def return_confirm(sid,json):
	sio.emit('init_confirm',{'place':place,'room_area':room_area,'space_range':space_range,'cycle':cycle,'open_time':open_time,'total_number':total_number})
if __name__== '__main__':
	eventlet.wsgi.server(eventlet.listen(('',8080)),app)

