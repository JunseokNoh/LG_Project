import serial
import socketio

sio = socketio.Client()

sio.connect('http://localhost:8080')
print('my sid is',sio.sid)
@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

ser = serial.Serial(
    port='COM4',
    baudrate=9600,
)

while True:
    if ser.readable():
        res = ser.readline()
        data = res.decode()[:len(res)-1]
        print(data)
        sio.emit('my event',{'data':data})