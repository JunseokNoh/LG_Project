from websocket import create_connection

#소켓생성
ws = create_connection("ws://localhost:9996")
print('Hello, World')
while True:
	#입력받기
	msg = input()
	#q입력하면 종료
	if msg=="q":
		break
	#메세지 전송
	ws.send(msg)
	print("Sent")
	print("Reeiving...")
	#메세지 받기
	result =  ws.recv()
	#메세지 프린트하기
	print("Received '%s'" % result)
ws.close()