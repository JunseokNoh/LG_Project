Automatic Ventilation Smart Window
===================================
출입구와 실내에 설치된 카메라를 통해 실내 공간 대비 적정 인원 초과시 자동 환기를 시켜주는 시스템.

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
1. 실내 인원 > 적정 인원 시 자동 환기 
    - 출입구에 설치된 카메라를 통해 실내 출입 인원 트래킹 및 실내 인원 계산
    - Social distancing caculator를 활용한 실내 적정 인원 계산
        - Formula : Square feet*(1-(Percent of floor space/100))/144
    - 환기 주기 및 환기 시간 설정 가능

2. 내부 공기 AQI > 외부 공기 AQI시 자동 환기
    + 외부 공기 AQI 사용자 위치 IP 기반 대기 질 API 사용 : <https://www.iqair.com/ko/>
        + 데이터 포맷 : JSON,
        + request : {{urlExternalAPI}}v2/nearest_city?key={{YOUR_API_KEY}}
        + response:
        <pre>
        <code>
        {"status": "success","data": {"city": "Port Harcourt", "state": "Rivers","country": "Nigeria","location": {"type": "Point","coordinates": [7.048623,4.854166]},
        "forecasts": [{"ts": "2019-08-15T12:00:00.000Z","aqius": 137,"aqicn": 69,"tp": 23, "tp_min": 23,"pr": 996,"hu": 100,"ws": 2,"wd": 225,"ic": "10d"},.......}
      </code>
      </pre>
    + 내부 공기 AQI Arduino CO Sensor, Fine dust Sensor를 활용해 계산
      + Formula : 
1. 출입구에 설치된 카메라를 통해 실내 출입 인원 트래킹 및 실내 인원 계산
2. Social distancing caculator를 활용한 실내 적정 인원 계산
    - Formula : square feet*(1-(Percent of floor space/100))/144
3. 

  





일반부분

    this is code
    
보통부분
