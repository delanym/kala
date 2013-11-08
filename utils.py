# -*- coding: UTF-8 -*-

import time
from data import *

def isSign(sign):
    for _ in SIGN_NAMES :
        if sign == _.lower() :
            return True
    return False

def isPlanet(planet):
    for _ in PLANET_NAMES_LUNAR :
        if planet == _.lower() :
            return True
    return False

def isNakshatra(nakshatra):
    for _ in NAKSHATRA_NAMES :
        if nakshatra == _.lower() :
            return True
    return False

def isDay(day):
    for _ in WEEKDAYS :
        if day == _.lower() :
            return True
    return False

def normalize(deg):
	"""Adjusts deg between 0-360"""
	while deg < 0.0:
		deg += 360.0
	while deg >= 360.0:
		deg -= 360.0
	return deg

# Make sure input is a number and not null
def inputNull():
    input = raw_input()
    if input.__len__() == 0:
        input = 0
    return input

# Return the opposite degree
def oppDeg(deg):
    if deg < 180 :
        deg += 180
    else :
        deg -= 180
    return deg

# Return the julian day for the current system time. Unix Epoch begins on 1st Jan 1970, 00:00:00
def getJulian():
    return 2440587.5 + (time.time() / 86400)

# Convert decimal float (deg.mmss) to degree string
def dec2deg(decimal):
    deg = int(decimal)
    min = int((decimal-deg) * 60)
    sec = int((((decimal-deg) * 60) - min) * 60)
    return str(deg) + '°' + str(min).zfill(2) + '\'' + str(sec).zfill(2) + '"'

# Convert seconds(int) to a time string (hh:mm:ss)
def sec2time(seconds):
    sec = int(seconds % 60)
    min = int((seconds - sec) % (60 * 60)) / 60
    hrs = int((seconds - sec) - min) / (60 * 60)
    return str(hrs).zfill(2) + 'h' + str(min).zfill(2) + 'm' + str(sec).zfill(2) + 's'




