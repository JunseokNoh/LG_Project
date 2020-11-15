Automatic Ventilation Smart Window
===================================
출입구와 실내에 설치된 카메라를 통해 실내 공간 대비 적정 인원 초과시 자동 환기를 시켜주는 시스템.      
(본 시스템은 LG Soft India가 주관한 LG WebOS 해커톤 3-rd prize 수상작입니다.)

### 컴포넌트
+ WebOS 설치 RaspberryPi 4
+ Arduino와 Serial 통신을 위한 RaspberryPi 4
+ Arduino CO Sensor,Fine dust Sensor,Step Motor, Buzzer
+ Webcam 
+ Socket io 통신을 위한 Google Cloud Web Server
+ 실내 공간 제어를 위한 Web App

### 사용 라이브러리
+ People counting Open cv
+ Social distance check Open cv

<hr/>

### 시스템 설명
#### 1. 실내 인원 > 적정 인원 시 자동 환기     
- 출입구에 설치된 카메라를 통해 실내 출입 인원 트래킹 및 실내 인원 계산
- Social distancing caculator를 활용한 실내 적정 인원 계산
    - Formula : Square feet*(1-(Percent of floor space/100))/144
- 환기 주기 및 환기 시간 설정 가능

#### 2. 내부 공기 AQI > 외부 공기 AQI시 자동 환기
+ 외부 공기 AQI 사용자 위치 IP 기반 대기 질 API 사용 : <https://www.iqair.com/ko/>
    + 데이터 포맷 : JSON,
    + request : {{urlExternalAPI}}v2/nearest_city?key={{YOUR_API_KEY}}
    + response:
    <pre>
    <code>
    {"status": "success","data": {"city": "Port Harcourt", "state": "Rivers","country": "Nigeria","location": {"type": "Point","coordinates": [7.048623,4.854166]},
    "forecasts": [{"ts": "2019-08-15T12:00:00.000Z","aqius": 137,"aqicn": 69,"tp": 23, "tp_min": 23,"pr": 996,"hu": 100,"ws": 2,"wd": 225,"ic": "10d"},.......}</code>
   </pre>
   
+ 내부 공기 AQI Arduino CO Sensor, Fine dust Sensor를 활용해 계산
    + Formula : ![air_quality](https://user-images.githubusercontent.com/58390757/99180432-9e8ca980-2769-11eb-9043-d5f195a83f3a.PNG)
+ 실내 공기 AQI > 실외 공기 AQI 일 경우 자동 환기 시작 (현재 비가 올 경우 환기 시스템 가동 불가 설정)

#### 3. 사회적 거리두기를 유지하지 않는 사람들이 80% 이상일 경우 부저를 활용한 경고음 발생
+ Arduino 부저를 활용 사회적 거리두기를 유지 하지 않을 시 경고음 발생
    + Formula : (위험 인원/ 실내인원)*(실내인원/적정인원)

#### 4. 스텝 모터를 활용한 창문 제어
<hr/>    

### 흐름도
<img src="https://user-images.githubusercontent.com/58390757/99180657-6be3b080-276b-11eb-812b-68fceb17aa1f.png" width="450px" height="300px" title="" alt="flow chart"></img><br/>

<hr/>

### 데모

