# -*- coding: utf-8 -*- 

from pyowm import OWM
API_key = '1700bd63d72dea48992a77354c2e38e5'
owm = OWM(API_key)
mgr = owm.weather_manager()
obs = mgr.weather_at_place('Seoul')
w = obs.weather

print('Seoul :', w.status, w.temperature(unit='celsius')['temp'])