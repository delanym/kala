#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from collections import namedtuple
import getopt
from operator import *
from re import search

from data import *
from sweph import *
import utils as utl



# Returns the Nakshatra
def get_nakshatra(time, planet):
    longitude = swe_calc_ut(time, planet, SEFLG_SWIEPH)[1][0]
    return NAKSHATRAS[int(longitude/NAKSHATRADEGREE)].name

# Return date object for julian day
def rev_julian(julian_day_ut):
    return swe_revjul(julian_day_ut, SE_GREG_CAL)

# Returns the SWEPH planet data
def get_planet(time, planet):
    return swe_calc_ut(time, planet, SEFLG_SWIEPH)[1]

# BROKEN: Doesn't handle retrograde motion.
# Calculates transit time of two planets. Direction is true/false if searching forward/backward in time.
def get_transit(julian_day_ut, body1, body2, direction):
    #print 'Julian Day', julian_day_ut
    # Later on we'll get in trouble when testing for an overshoot if one of our planets passes 0d,
    # so we just add 1024 to both rectascensions. We need to add this after each swe_calc_ut call.
    sun = swe_calc_ut(julian_day_ut, body1, SEFLG_SWIEPH | SEFLG_SPEED)[1]
    moon = swe_calc_ut(julian_day_ut, body2, SEFLG_SWIEPH | SEFLG_SPEED)[1]
    sun_degree = sun[0] + 1024
    moon_degree = moon[0] + 1024
    speed = abs(sun[3] - moon[3])

    #print 'Start, jday:', julian_day_ut, 'date:', swe_revjul(julian_day_ut, 1), ' pl1:', sun[0], ' pl2:', moon[0]#, 'pl1speed:', sun[3], 'pl2speed:', moon[3]


    # Take a first guess at the transit point.
    if moon_degree > sun_degree:
        if moon[3] - sun[3] > 0:
            distance = (360 + (sun_degree - moon_degree))
        else:
            distance = (moon_degree - sun_degree)
    else:
        if moon[3] - sun[3] > 0:
            distance = (sun_degree - moon_degree)
        else:
            distance = (360 - (sun_degree - moon_degree))
    #print 'distance {0}'.format(distance)

    if not direction:
        time = (distance - 360) / speed
    else:
        time = distance / speed
    #print 'time {0}'.format(time)

    #print 'time', time
    julian_day_ut = julian_day_ut + time

    sun = swe_calc_ut(julian_day_ut, body1, SEFLG_SWIEPH | SEFLG_SPEED)[1]
    moon = swe_calc_ut(julian_day_ut, body2, SEFLG_SWIEPH | SEFLG_SPEED)[1]
    sun_degree = sun[0] + 1024
    moon_degree = moon[0] + 1024
    speed = abs(sun[3] - moon[3])

    #print '1st pass, jday:', julian_day_ut, 'date:', swe_revjul(julian_day_ut, 1), ' pl1:', sun[0], ' pl2:', moon[0], 'pl1speed:', sun[3], 'pl2speed:', moon[3]

    # Loop passes, will exit when accuracy of 0.0001 is achieved, or over 100 cycles calculated without any result
    loop = 0
    patience = 6
    while True:

        # Here we can ignore the direction. We relied on the first pass to place us within 60d of the transit.
        # Now we just find the smaller arc and determine the time needed to close it.
        # The hierarchy of conditions is: largest degree > short arc > direction

        if moon_degree > sun_degree:
            if moon_degree - sun_degree < 60:
                if sun[3] - moon[3] > 0:
                    time = (moon_degree - sun_degree) / speed
                else:
                    time = (sun_degree - moon_degree) / speed
            else:
                if sun[3] - moon[3] > 0:
                    time = -(moon_degree - sun_degree) / speed
                else:
                    time = ((sun_degree + 360) - moon_degree) / speed

        else:
            if sun_degree - moon_degree < 60:
                if moon[3] - sun[3] > 0:
                    time = (sun_degree - moon_degree) / speed
                else:
                    time = (moon_degree - sun_degree) / speed
            else:
                if moon[3] - sun[3] > 0:
                    time = (sun_degree - (moon_degree + 360)) / speed
                else:
                    time = ((moon_degree + 360) - sun_degree) / speed

        julian_day_ut = julian_day_ut + time

        sun = swe_calc_ut(julian_day_ut, body1, SEFLG_SWIEPH | SEFLG_SPEED)[1]
        moon = swe_calc_ut(julian_day_ut, body2, SEFLG_SWIEPH | SEFLG_SPEED)[1]

        if abs(time) < 0.0000001:
            break
        loop = loop + 1
        if loop == patience:
            print 'A transit point was not found after', patience, 'iterations!'
            sys.exit()
            break

        sun_degree = sun[0] + 1024
        moon_degree = moon[0] + 1024
        speed = abs(sun[3] - moon[3])

    print 'Result jday:', julian_day_ut, 'date:', swe_revjul(julian_day_ut, 1), ' pl1:', sun[0], ' pl2:', moon[0] #, 'pl1speed:', sun[3], 'pl2speed:', moon[3]
    #print '{4:6} jday: {0:14} date: {1:38} sun: {2:14} moon: {3:14}'.format(julian_day_ut, swe_revjul(julian_day_ut, 1), sun[0], moon[0], str(direction))

    return julian_day_ut + time, sun[0], moon[0]

# Determines future transit of sun and moon if direction is True, past time if False. Returns time, moon degree and moon speed.
def get_sun_moon_transit(julian_day_ut, direction):

    # Later on we'll get in trouble when testing for an overshoot if one of our planets passes 0d,
    # so we just add 1024 to both rectascensions. We need to add this after each swe_calc_ut call.
    sun = swe_calc_ut(julian_day_ut, SE_SUN, SEFLG_SWIEPH | SEFLG_SPEED)[1]
    moon = swe_calc_ut(julian_day_ut, SE_MOON, SEFLG_SWIEPH | SEFLG_SPEED)[1]
    sun_degree = sun[0] + 1024
    moon_degree = moon[0] + 1024
    speed = abs(sun[3] - moon[3])
    transit_date = julian_day_ut

    # Take a first guess at the transit point.
    if moon_degree > sun_degree:
        distance = (360 + (sun_degree - moon_degree))
    else:
        distance = (sun_degree - moon_degree)

    if not direction:
        time = (distance - 360) / speed
    else:
        time = distance / speed

    # Loop passes, will exit when accuracy of 0.0001 is achieved, or over 100 cycles calculated without any result
    loop = 0
    patience = 6
    while True:

        # Here we can ignore the direction. We relied on the first pass to place us within 60d of the transit.
        # Now we just find the smaller arc and determine the time needed to close it.
        # The hierarchy of conditions is: largest degree > short arc > direction
        transit_date += time
        sun = swe_calc_ut(transit_date, SE_SUN, SEFLG_SWIEPH | SEFLG_SPEED)[1]
        moon = swe_calc_ut(transit_date, SE_MOON, SEFLG_SWIEPH | SEFLG_SPEED)[1]

        if abs(time) < 0.0000001:
            break

        sun_degree = sun[0] + 1024
        moon_degree = moon[0] + 1024
        speed = abs(sun[3] - moon[3])

        if moon_degree > sun_degree:
            if moon_degree - sun_degree < 60:
                time = (sun_degree - moon_degree) / speed
            else:
                time = ((sun_degree + 360) - moon_degree) / speed
        else:
            if sun_degree - moon_degree < 60:
                time = (sun_degree - moon_degree) / speed
            else:
                time = (sun_degree - (moon_degree + 360)) / speed

    return transit_date, moon[0], moon[3]

# Returns the exact time and degree of full moon
def get_full_moon(julian_day_ut):
    offset = 1.0
    while True:
        plus = swe_pheno_ut(julian_day_ut+offset, SE_MOON, SEFLG_SWIEPH)[1][0]
        minus = swe_pheno_ut(julian_day_ut-offset, SE_MOON, SEFLG_SWIEPH)[1][0]

        if plus > minus:
            offset_range = (plus + minus) / 2
            offset_degree = offset_range - minus
            offset *= offset_degree / offset_range
            julian_day_ut -= offset
        else:
            offset_range = (plus + minus) / 2
            offset_degree = offset_range - plus
            offset *= offset_degree / offset_range
            julian_day_ut += offset

        # Stop when we're less than a second off. The phase degree often doesn't reach zero, because of the ascension of the moon.
        if offset < 0.00001:
            break

    return julian_day_ut, swe_calc_ut(julian_day_ut, SE_MOON, SEFLG_SWIEPH)[1][0]

# Return phase info [{waxing or waning}, {day integer 1-30}, {progress%}]
def get_phase(julian_day_ut, method = PHASE_METHOD_FULL_BREATH):
    progression, tithi, percent_complete = '', 0, 0
    new_moon_past = get_sun_moon_transit(julian_day_ut, False)
    new_moon_future = get_sun_moon_transit(julian_day_ut, True)

    synodic_duration = new_moon_future[0] - new_moon_past[0]
    if new_moon_future[1] < new_moon_past[1]:
        synodic_distance = new_moon_future[1] + (360 - new_moon_past[1]) + 360
    else:
        synodic_distance = (new_moon_future[1] - new_moon_past[1]) + 360

    # Take a guess at full moon and get an accurate time.
    full_moon = get_full_moon(new_moon_past[0] + (synodic_duration / 2))

    # Just a container to break out of doing extra work
    while True:

        # 1st method
        if method == PHASE_METHOD_FULL_BREATH:
            phase_length = new_moon_future[0] - new_moon_past[0]
            tithi_length = phase_length / 30.0
            position = julian_day_ut - new_moon_past[0]
            tithi = (position // tithi_length) + 1
            percent_complete = (position % tithi_length) * 100
            if julian_day_ut < full_moon[0]:
                progression = 'waxing'
            else:
                progression = 'waning'
            break

        # 2nd method
        if method == PHASE_METHOD_HALF_BREATH:
            if julian_day_ut < full_moon[0]:
                progression = 'waxing'
                waxing_length = full_moon[0] - new_moon_past[0]
                tithi_length = waxing_length / 15.0
                waxing_position = julian_day_ut - new_moon_past[0]
                tithi = (waxing_position // tithi_length) + 1
                percent_complete = (waxing_position % tithi_length) * 100
            else:
                progression = 'waning'
                waning_length = new_moon_future[0] - full_moon[0]
                tithi_length = waning_length / 15.0
                waning_position = julian_day_ut - full_moon[0]
                tithi = (waning_position // tithi_length) + 16
                percent_complete = (waning_position % tithi_length) * 100
            break

        moon = swe_calc_ut(julian_day_ut, SE_MOON, SEFLG_SWIEPH | SEFLG_SPEED)[1]
        moon_ahead = moon[0]

        # 3rd method
        if method == PHASE_METHOD_CRITICAL:
            tithi_degree = 0

            if julian_day_ut < full_moon[0]:
                progression = 'waxing'

                if full_moon[1] < new_moon_past[1]:
                    waxing_range = (full_moon[1] + 360) - new_moon_past[1]
                else:
                    waxing_range = full_moon[1] - new_moon_past[1]

                tithi_length = waxing_range / 15.0

                if moon[0] < new_moon_past[1]:
                    moon_ahead += 360

                k = range(1,16)
                for i in k:
                    if moon_ahead < new_moon_past[1] + (tithi_length * i):
                        tithi = i
                        tithi_degree = (moon_ahead - new_moon_past[1]) % tithi_length
                        break
            else:
                progression = 'waning'

                if new_moon_future[1] < full_moon[1]:
                    waning_range = (new_moon_future[1] + 360) - full_moon[1]
                else:
                    waning_range = new_moon_future[1] - full_moon[1]

                tithi_length = waning_range / 15.0

                if moon[0] < full_moon[1]:
                    moon_ahead += 360

                k = range(1,16)
                for i in k:
                    if moon_ahead < full_moon[1] + (tithi_length * i):
                        tithi = i + 15
                        tithi_degree = (moon_ahead - full_moon[1]) % tithi_length
                        break

            percent_complete = (tithi_degree / tithi_length) * 100
            break

        # 4th method
        elif method == PHASE_METHOD_NOBLE:
            karana = 0
            karana_length = 0
            karana_degree = 0

            if julian_day_ut < full_moon[0]:
                progression = 'waxing'

                if full_moon[1] < new_moon_past[1]:
                    waxing_range = (full_moon[1] + 360) - new_moon_past[1]
                else:
                    waxing_range = full_moon[1] - new_moon_past[1]

                karana_length = waxing_range / 30.0

                if moon[0] < new_moon_past[1]:
                    moon_ahead += 360

                k = range(1,31)
                for i in k:
                    if moon_ahead < new_moon_past[1] + (karana_length * i):
                        karana = i
                        karana_degree = (moon_ahead - new_moon_past[1]) % karana_length
                        break
            else:
                progression = 'waning'

                if new_moon_future[1] < full_moon[1]:
                    waning_range = (new_moon_future[1] + 360) - full_moon[1]
                else:
                    waning_range = new_moon_future[1] - full_moon[1]

                karana_length = waning_range / 30.0

                if moon[0] < full_moon[1]:
                    moon_ahead += 360

                k = range(1,31)
                for i in k:
                    if moon_ahead < full_moon[1] + (karana_length * i):
                        karana = i + 30
                        karana_degree = (moon_ahead - full_moon[1]) % karana_length
                        break

            if karana == 1 or karana == 60:
                tithi = 30
            else:
                tithi = karana / 2

            tithi_length = karana_length * 2

            if karana % 2 == 1:
                percent_complete = ((karana_degree + karana_length) / tithi_length) * 100
            else:
                percent_complete = (karana_degree / tithi_length) * 100
            break

        # Wrong method
        else:
            print 'Phase method not supported. Exiting...'
            sys.exit(0)

    return progression, int(tithi), int(percent_complete), PHASE_METHOD_NAMES[method]

# Return Mahadasa and Antardasa tuples, each with a name, rise time, and end time
# Do this for the given cycle at the current time, if none is specified
def get_dasa(cycle, derivative_time=utl.getJulian()):
    mdName, mdRise, mdEnd, adName, adRise, adEnd = '', '', '', '', '', ''
    while True:
        for md in cycle:
            if md.antardasas[8][1] > derivative_time:
                mdName = md.mahadasa
                mdRise = md.rise
                mdEnd = md.antardasas[8][1]
                adRise = md.rise
                for ad in md.antardasas:
                    if ad[1] > derivative_time:
                        adName = ad[0]
                        adEnd = ad[1]
                        break
                    else:
                        adRise = ad[1]
                break
        # If the person was born more than 120 before derivative_time
        if adEnd == '':
            derivative_time -= 120 * SUN_YEAR
        else:
            break

    return Dasa(mdName, mdRise, mdEnd), Dasa(adName, adRise, adEnd)


# Returns a 120 year dasa cycle as an array of 9 Mahadasa namedtuplets
def get_dasa_cycle(time):
    degree = swe_calc_ut(time, SE_MOON, SEFLG_SWIEPH)[1][0]
    rDASAS = DASAS.__class__(DASAS) # New instance of dasas so when we rotate we don't disorder the original
    dasa_cycle = []
    for nakshatra, _ in enumerate(NAKSHATRAS):
        if nakshatra == int(degree / NAKSHATRADEGREE):
            # Find the 1st Mahadasa and its rising time
            rDASAS.rotate(-nakshatra)
            mahadasa = rDASAS[0]
            period_days = rDASAS[0].dasa * SUN_YEAR
            nakshatra_degree = degree % NAKSHATRADEGREE
            progress = (nakshatra_degree / NAKSHATRADEGREE)
            mahadasa_rise = time - (progress * period_days)

            # Now find Antardasas and create Mahadasa namedtuple
            # Do this for each dasa to complete 120years
            for i in range(9):
                antardasas = []
                dasa_cusp = mahadasa_rise
                for antardasa in rDASAS:
                    antardasa_length = (antardasa.dasa / 120.0) * (mahadasa.dasa * SUN_YEAR)
                    antardasa_end = dasa_cusp + antardasa_length
                    dasa_cusp = antardasa_end
                    antardasas.append((antardasa.name, antardasa_end))

                md = Mahadasa(mahadasa.name, mahadasa_rise, antardasas)
                dasa_cycle.append(md)

                # If we've covered 120yrs, exit, else find next mahadasa
                if i == 8:
                    break
                mahadasa_rise += rDASAS[0].dasa * SUN_YEAR
                rDASAS.rotate(-1)
                mahadasa = rDASAS[0]
            break
    return dasa_cycle


































