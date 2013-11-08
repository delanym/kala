#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import sys
import math
import datetime
from collections import namedtuple
import getopt
from operator import *
from re import search
import pickle
import os.path
from astro import *
import data
from sweph import *
import utils as utl
#from kala import *



# as it says
def show_all_birth_phase_ordered():

    print 'Viewing all phase values for births ordered:'
    ordered = []
    for rec in data.births:
        phase = get_phase(float(rec.julian_day_ut), PHASE_METHOD_CRITICAL)
        ordered.append([rec.name, phase[0], phase[1], phase[2]]) #tithi_detail = tithi[phase[1]-1]

    ordered.sort(key = itemgetter(2,3))

    for f in ordered:
        for tithi_detail in TITHIS:
            if getattr(tithi_detail, 'num') == f[2]:
                print '{0:50}:{1:3}% of {2:2}, {3:15} {4}, {5}'.format(f[0], f[3], f[2], tithi_detail.name, tithi_detail.omen, tithi_detail.deity)
                break

    print '_' * 25
    return


# as it says
def show_all_birth_nakshatra_ordered():
    print 'Viewing all nakshatra values for births ordered:'
    ordered = []

    for rec in data.births:
        longitude = swe_calc_ut(rec.julian_day_ut, SE_MOON, SEFLG_SWIEPH)[1][0]
        person = rec.name
        degree_string = utl.dec2deg(longitude - (int(longitude/NAKSHATRADEGREE)*NAKSHATRADEGREE))
        nakshatra_name = NAKSHATRAS[int(longitude/NAKSHATRADEGREE)].name
        nakshatra_num = longitude/NAKSHATRADEGREE
        sign_name = SIGNS[int(longitude/30)].name
        ordered.append([person, degree_string, nakshatra_name, nakshatra_num, sign_name])

    ordered.sort(key = itemgetter(3))

    for f in ordered:
        print '{0:50} {1:10} {2:16} {3}'.format(f[0], f[1], f[2], f[4])

    print '_' * 25
    return


# as it says
def show_all_birth_sun_ordered():
    print 'Viewing all sun-sign values for births ordered:'
    ordered = []

    for rec in data.births:
        longitude = swe_calc_ut(rec.julian_day_ut, SE_SUN, SEFLG_SWIEPH)[1][0]
        person = rec.name
        degree_string = utl.dec2deg(longitude - (int(longitude/30)*30))
        sign_name = SIGNS[int(longitude/30)].name
        sign_num = longitude/30
        ordered.append([person, degree_string, sign_name, sign_num])

    ordered.sort(key = itemgetter(3))

    for f in ordered:
        print '{0:50} {1:10} {2:16}'.format(f[0], f[1], f[2])

    print '_' * 25
    return


# Show births ordered by the dasa they would be in today
def show_all_birth_dasa_current_ordered():
    print 'Viewing all todays dasas for births ordered:'
    ordered = []

    for rec in data.births:
        person = rec.name
        dasa_cycle = get_dasa_cycle(float(rec.julian_day_ut))
        md, ad = get_dasa(dasa_cycle)
        mdpercent = int(((utl.getJulian() - float(md.rise)) / (float(md.end) - float(md.rise))) * 100)
        adpercent = int(((utl.getJulian() - float(ad.rise)) / (float(ad.end) - float(ad.rise))) * 100)
        ordered.append([person, md.dasa, mdpercent, ad.dasa, adpercent])

    ordered.sort(key = itemgetter(1, 2, 4))

    for f in ordered:
        print '{0:50} {1:7} {3:7} ({2}%-{4}%)'.format(f[0], f[1], f[2], f[3], f[4])

    print '_' * 25
    return


# Show births ordered by the dasa they were born in (effectively groups people by janma nakshatra lord)
def show_all_birth_dasa_birth_ordered():
    print 'Viewing all birth dasas for births ordered:'
    ordered = []

    for rec in data.births:
        person = rec.name

        dasa_cycle = get_dasa_cycle(float(rec.julian_day_ut))
        nakshatra = get_nakshatra(float(rec.julian_day_ut), SE_MOON)

        # The dasa cycle alone won't tell us the antardasa
        md, ad = get_dasa(dasa_cycle, float(rec.julian_day_ut))
        print 'md', md
        mdpercent = int(((float(rec.julian_day_ut) - float(md.rise)) / (float(md.end) - float(md.rise))) * 100)
        adpercent = int(((float(rec.julian_day_ut) - float(ad.rise)) / (float(ad.end) - float(ad.rise))) * 100)
        ordered.append([nakshatra, person, md.dasa, mdpercent, ad.dasa, adpercent])

    ordered.sort(key = itemgetter(2, 3, 5))

    for f in ordered:
        print '{1:50} {2:7} {3}% {4:7} {5}% ({0})'.format(f[0], f[1], f[2], f[3], f[4], f[5])

    print '_' * 25
    return

# as it says
def show_all_birth_animal_ordered():
    print 'Viewing all Jupiter positions for births ordered:'
    ordered = []

    for rec in data.births:
        person = rec.name

        longitude = swe_calc_ut(float(rec.julian_day_ut), SE_JUPITER, SEFLG_SWIEPH)[1][0]
        ordered.append([person, longitude, utl.dec2deg(longitude - (int(longitude/30)*30)), SIGN_NAMES[int(longitude/30)]])

    ordered.sort(key = itemgetter(1))

    for f in ordered:
        print '{0:50} {1:10} {2:16} {3}'.format(f[0], f[2], f[3], f[4])

    print '_' * 25
    return


# as it says
def show_all_birth_weekdays_ordered():
    print 'Viewing all weekdays for births ordered:'
    ordered = []

    for rec in res:
        person = rec.name
        num = int((float(rec.julian_day_ut)+1.5)%7)
        day = WEEKDAYS[num]
        ordered.append([person, day, num])

    ordered.sort(key = itemgetter(2))

    for f in ordered:
        print '{0:50} {1}'.format(f[0], f[1])

    print '_' * 25
    return




# Show Sun positions
def show_sun(julian_day_ut):
    longitude = swe_calc_ut(julian_day_ut, SE_SUN, SEFLG_SWIEPH)[1][0]
    degree = utl.dec2deg(longitude - (int(longitude/30)*30))
    sign = SIGNS[int(longitude/30)]
    print 'Sun    : {0} {1:10} {2:11}'.format(sign.glyph, degree, sign.name)
    return


# Show Moon positions
def show_moon(julian_day_ut):
    longitude = swe_calc_ut(julian_day_ut, SE_MOON, SEFLG_SWIEPH)[1][0]
    sdegree = utl.dec2deg(longitude - (int(longitude/30)*30))
    sign = SIGNS[int(longitude/30)]
    ndegree = utl.dec2deg(longitude - (int(longitude/NAKSHATRADEGREE)*NAKSHATRADEGREE))
    nakshatra = NAKSHATRAS[int(longitude/NAKSHATRADEGREE)]
    print 'Moon   : {0} {1:10} {2:11} {3:10} {4}, {5}, {6}, {7}'.format(sign.glyph, sdegree, sign.name, ndegree, nakshatra.name, nakshatra.lord, nakshatra.deity, nakshatra.symbol)
    return


# Show Jupiter positions
def show_planets(julian_day_ut):
    longitude = swe_calc_ut(julian_day_ut, SE_JUPITER, SEFLG_SWIEPH)[1][0]
    degree = utl.dec2deg(longitude - (int(longitude/30)*30))
    sign = SIGNS[int(longitude/30)]
    print 'Jupiter: {0} {1:10} {2:11}'.format(sign.glyph, degree, sign.name)

    longitude = swe_calc_ut(julian_day_ut, SE_MERCURY, SEFLG_SWIEPH)[1][0]
    degree = utl.dec2deg(longitude - (int(longitude/30)*30))
    sign = SIGNS[int(longitude/30)]
    print 'Mercury: {0} {1:10} {2:11}'.format(sign.glyph, degree, sign.name)

    longitude = swe_calc_ut(julian_day_ut, SE_VENUS, SEFLG_SWIEPH)[1][0]
    degree = utl.dec2deg(longitude - (int(longitude/30)*30))
    sign = SIGNS[int(longitude/30)]
    print 'Venus  : {0} {1:10} {2:11}'.format(sign.glyph, degree, sign.name)

    longitude = swe_calc_ut(julian_day_ut, SE_MARS, SEFLG_SWIEPH)[1][0]
    degree = utl.dec2deg(longitude - (int(longitude/30)*30))
    sign = SIGNS[int(longitude/30)]
    print 'Mars   : {0} {1:10} {2:11}'.format(sign.glyph, degree, sign.name)

    longitude = swe_calc_ut(julian_day_ut, SE_SATURN, SEFLG_SWIEPH)[1][0]
    degree = utl.dec2deg(longitude - (int(longitude/30)*30))
    sign = SIGNS[int(longitude/30)]
    print 'Saturn : {0} {1:10} {2:11}'.format(sign.glyph, degree, sign.name)

    longitude = swe_calc_ut(julian_day_ut, SE_MEAN_NODE, SEFLG_SWIEPH)[1][0]
    degree = utl.dec2deg(longitude - (int(longitude/30)*30))
    sign = SIGNS[int(longitude/30)]
    print 'Rahu   : {0} {1:10} {2:11}'.format(sign.glyph, degree, sign.name)
    degree = utl.dec2deg(utl.oppDeg(longitude) - (int(utl.oppDeg(longitude)/30)*30))
    sign = SIGNS[int(utl.oppDeg(longitude)/30)]
    print 'Ketu   : {0} {1:10} {2:11}'.format(sign.glyph, degree, sign.name)
    return



# Show degree positions of all planets
def show_birth():
    fragment = raw_input('\nEnter full or partial name: ').lower()
    dasas = raw_input('Show all dasas? (y\\n):').lower()
    if dasas == 'y':
        dasas = True
    else :
        dasas = False

    #res = get_db('SELECT * FROM births WHERE name LIKE "%{}%"'.format(name))
    for rec in data.births:
        if search(fragment, rec.name.lower()):
            print 'Positions for', rec.name
            show_all(float(rec.julian_day_ut))
            show_dasa(float(rec.julian_day_ut))
            if dasas: show_dasa_cycle(float(rec.julian_day_ut))
    return

# Show current date
def show_date(julian_day_ut):
    print 'Date: {0} {1}, Julian day: {2}'.format(swe_revjul(float(julian_day_ut), SE_GREG_CAL), WEEKDAYS[int((float(julian_day_ut)+1.5)%7)], julian_day_ut)
    return

# Show all positions
def show_all(julian_day_ut):
    show_date(julian_day_ut)
    show_phase(julian_day_ut, PHASE_METHOD_CRITICAL)
    #show_phase(julian_day_ut, PHASE_METHOD_FULL_BREATH)
    show_moon(julian_day_ut)
    show_sun(julian_day_ut)
    show_planets(julian_day_ut)
    print '****************'
    return

# List all signs
def list_signs():
    print '{0:3} {1:14} {2:8} {3:8} {4:8}'.format(SIGNS_HEADER[0], SIGNS_HEADER[1], SIGNS_HEADER[2], SIGNS_HEADER[3], SIGNS_HEADER[4])
    for rec in SIGNS:
        print '{0:3} {2:2} {1:12} {3:8} {4:8} {5:8}'.format(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5])
    return

# List all nakshatras
def list_nakshatras():
    print '{0:3} {1:16} {2:18} {3:7} {4:7}'.format(NAKSHATRAS_HEADER[0], NAKSHATRAS_HEADER[1], NAKSHATRAS_HEADER[2], NAKSHATRAS_HEADER[3], NAKSHATRAS_HEADER[4])
    for rec in NAKSHATRAS:
        print '{0:3} {1:16} {2:18} {3:7} {4:7}'.format(rec[0], rec[1], rec[2], rec[3], rec[4])
    return

# List all tithis
def list_tithis():
    print '{0:3} {1:19} {2:18} {3:16}'.format(TITHIS_HEADER[0], TITHIS_HEADER[1], TITHIS_HEADER[2], TITHIS_HEADER[3])
    for rec in TITHIS:
        print '{0:3} {1:19} {2:18} {3:16}'.format(rec[0], rec[1], rec[2], rec[3])
    return

# List all animals
def list_animals():
    print '{0:3} {1:7} {2:16} {3:8} {4:7} {5:7} {6:7} {7:7} {8:10} {9:15} {10:15}'.format(ANIMALS_HEADER[0], ANIMALS_HEADER[1], ANIMALS_HEADER[2], ANIMALS_HEADER[3], ANIMALS_HEADER[4], ANIMALS_HEADER[5], ANIMALS_HEADER[6], ANIMALS_HEADER[7], ANIMALS_HEADER[8], ANIMALS_HEADER[9], ANIMALS_HEADER[10])
    for rec in ANIMALS:
        print '{0:3} {1:7} {2:16} {3:8} {4:7} {5:7} {6:7} {7:7} {8:10} {9:15} {10:15}'.format(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8], rec[9], rec[10])
    return

# List all planets
def list_planets():
    print '{0:3} {1:7} {2:5} {3:8} {4:9} {5:7}'.format(PLANETS_SOLAR_HEADER[0], PLANETS_SOLAR_HEADER[1], PLANETS_SOLAR_HEADER[2], PLANETS_SOLAR_HEADER[3], PLANETS_SOLAR_HEADER[4], PLANETS_SOLAR_HEADER[5])
    for rec in PLANETS_SOLAR:
        print '{0:3} {1:7} {2:7} {3:10} {4:9} {5:7}'.format(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5])
    return


# Prints a list, such as SIGNS, NAKSHATRAS or ANIMALS
def list(choice) :
    if choice == 'nakshatras':
        list_nakshatras()
    elif choice == 'signs':
        list_signs()
    elif choice == 'animals':
        list_animals()
    elif choice == 'tithis':
        list_tithis()
    elif choice == 'planets':
        list_planets()
    return

# Shows positions for a given time
def show(choice) :
    if choice == 'date':
        show_date(utl.getJulian())
    elif choice == 'all':
        show_all(utl.getJulian())
    elif choice == 'sun':
        show_sun(utl.getJulian())
    elif choice == 'moon':
        show_moon(utl.getJulian())
    elif choice == 'planets':
        show_planets(utl.getJulian())
    return

# Search the database for births matching the query
def find(args) :
    if utl.isPlanet(args[0]) : # Check planet lexical
        sweph_planet = PLANETS_DICT.get(args[0].capitalize()) # Get sweph planet number from planet dictionary
        if utl.isSign(args[1]) : # Check sign lexical
            # Find everyone born with planet(int) in sign
            print 'All births with', args[0].capitalize(), 'in', args[1].capitalize(), ':'
            for rec in data.births:
                longitude = get_planet(rec.julian_day_ut, sweph_planet)
                if SIGNS[int(longitude[0]/30)].name == args[1].capitalize() :
                    print rec.name, 'has', args[0].capitalize(), 'at', utl.dec2deg(longitude[0] % 30), args[1].capitalize()

        elif utl.isNakshatra(args[1]) : # Check nakshatra lexical
            # Find everyone born with planet(int) in nakshatra
            print 'All births with', args[0].capitalize(), 'in', args[1].capitalize(), ':'
            for rec in data.births:
                longitude = get_planet(rec.julian_day_ut, sweph_planet)
                if NAKSHATRAS[int(longitude[0]/13.3334)].name == args[1].capitalize():
                    print rec.name, 'has', args[0].capitalize(), 'at', utl.dec2deg(longitude[0] % 13.3334), args[1].capitalize()

    elif args[0] == 'day':
        if utl.isDay(args[1]):
            print 'All born on a', args[1].capitalize(), ':'
            for rec in data.births:
                if WEEKDAYS[int((float(rec.julian_day_ut)+1.5)%7)] == args[1].capitalize():
                    print rec.name
    elif args[0] == 'tithi':
        if args[1].isdigit():
            #res1 = get_db('SELECT name, julian_day_ut FROM births')
            #res2 = get_db('SELECT name FROM tithi WHERE id = "%s"' %(args[1]))
            print 'All births on', res2[0][0], ':'
            for rec in res1:
                if get_tithi(rec[1]) == res2[0][0]:
                    print rec[0]

    return

# Give interpretation on astrological omens
def describe(args) :
    if args[0] == 'tithi' :
        if args[1].isdigit() :
            #res1 = get_db('SELECT name FROM tithi WHERE id = "%s"' %(args[1]))
            #res2 = get_db('SELECT description FROM analysis where category = "Tithi" AND key_one = "%s"' %(res1[0][0]))
            print 'Tithi', args[1], res1[0][0], ':', res2[0][0]
    elif utl.isPlanet(args[0]) : # Check planet lexical
        sweph_planet = PLANETS_DICT.get(args[0].capitalize()) # Get sweph planet number from planet dictionary
        if utl.isSign(args[1]) : # Check sign lexical
            #res = get_db('SELECT description FROM analysis where category = "Planets in Signs" AND key_one = "%s" AND key_two = "%s"' %(args[0].capitalize(), args[1].capitalize()))
            print args[0].capitalize(), 'in', args[1].capitalize(), ':', res[0][0]
    return


""" files.py """

# Write data files (only birth data)
def write_data_files():
    with open("./public.edb", 'wb') as fpublic:
        pickle.dump(data.births, fpublic)
        print 'Birth data written to disk.'
    fpublic.close()
    return

# Get data from files and populate lists
def load_data_files():
    os.chdir(os.path.dirname(sys.argv[0]))

    # Load Birth data
    path = './public.edb'

    if os.path.isfile(path):
        with open(path, 'rb') as f:
            data.births = pickle.load(f)
        f.close()
        if data.births:
            print 'Birth data retrieved.'
        else:
            print 'Invalid path or filename.'
    else:
        print 'Invalid path or filename.'

    return

""" special.py """

# List all commands
def list_commands():
    print '\nadd | birth | recalc'
    print 'list <signs | nakshatras | tithis | animals>'
    print 'find {sign, nakshatra or animal}'
    print 'show <all | {planet}>'
    return


# Add a birth time
def add_birth():
    choice = '2'
    while choice == '2':

        name = raw_input('\nName (max 50): ')
        relation = raw_input('If this is a personal record type \'p\':').lower()
        if relation == 'p':
            relation = 'personal'
        else :
            relation = 'public'

        print 'Timezone (decimal): '
        lst_delta = float(utl.inputNull())

        print 'Daylight saving or war time correction (decimal): '
        dst_delta = float(utl.inputNull())

        print 'Year (Gregorian): '
        year = int(utl.inputNull())
        print 'Month: '
        month = int(utl.inputNull())
        print 'Day: '
        day = int(utl.inputNull())
        print 'Hour: '
        hour = int(utl.inputNull())
        print 'Minute: '
        minute = int(utl.inputNull())
        lst = str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + '00'


        #print 'Enter co-ordinates in de(g)rees, decima(l), or neither:',
        #choice = raw_input().lower()
        #if choice == 'g':
        #    print 'EW longitude (deg):',
        #    long_deg = int(raw_input())
        #    print 'EW longitude (min):',
        #    long_min = int(raw_input())

        #    print 'NS latitude (deg):',
        #    lat_deg = int(raw_input())
        #    print 'NS latitude (min):',
        #    lat_min = int(raw_input())

        #    longitude = long_deg + (int(long_min) / 60.0)
        #    latitude = lat_deg + (int(lat_min) / 60.0)

        #    print '(E)ast or (W)est:',
        #    if raw_input().upper() == 'W':
        #        longitude = -longitude
        #    print '(N)orth or (S)outh:',
        #    if raw_input().upper() == 'S':
        #        latitude = -latitude

        #elif choice == 'l':
        #    print 'EW longitude (deg decimal): ',
        #    longitude = float(raw_input())
        #    print 'NS latitude (deg decimal): ',
        #    latitude = float(raw_input())
        #else :
        #    longitude = 0
        #    latitude = 0

        # Calculate Julian Day UT:
        hrs = hour + (minute / 60.0)
        julian_day_ut = swe_julday(year, month, day, hrs, SE_GREG_CAL) - ((lst_delta + dst_delta) / 24)
        if julian_day_ut < -251291.5 or julian_day_ut > 3693368.5 :    # 2 Jan 5401 BC (jul. calendar) <> 31 Dec 5399 AD (greg. Cal.)
            print 'Sorry, your date exceeds the range of the Swiss Ephemeris.'
            break

        place = raw_input('Place (max 50): ')
        comments = raw_input('Comments (max 65535): ')

        # Display all info
        print '\nName: ',name,'-',relation
        print 'Born: ',place #,' Alt:',altitude,'m', ' Long:',longitude,', Lat:', latitude
        print 'Date: ',day,'/',month,'/',year,' Local time: ',lst,' lst_delta + Correction:',lst_delta + dst_delta
        print 'Julian Day UT: ', julian_day_ut
        print 'Comments: ', comments
        print '<1> Add this information to the database'
        print '<2> Re-enter information'

        choice = raw_input()
        if choice == '1':
            new = Birth(name, place, 1, lst, year, month, day, lst_delta, relation, dst_delta, julian_day_ut, comments)
            data.births.append(new)
            write_data_files()
            print name, 'added to database.'
    return



# Print a julian day
def get_julian_day():
    print 'Timezone (decimal): '
    lst_delta = float(utl.inputNull())

    print 'Daylight saving or war time correction (decimal): '
    dst_delta = float(utl.inputNull())

    print 'Year (Gregorian): '
    year = int(utl.inputNull())
    print 'Month: '
    month = int(utl.inputNull())
    print 'Day: '
    day = int(utl.inputNull())
    print 'Hour: '
    hour = int(utl.inputNull())
    print 'Minute: '
    minute = int(utl.inputNull())
    lst = str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + '00'

    # Calculate Julian Day UT:
    hrs = hour + (minute / 60.0)
    julian_day_ut = swe_julday(year, month, day, hrs, SE_GREG_CAL) - ((lst_delta + dst_delta) / 24)
    if julian_day_ut < -251291.5 or julian_day_ut > 3693368.5 :    # 2 Jan 5401 BC (jul. calendar) <> 31 Dec 5399 AD (greg. Cal.)
        print 'Sorry, your date exceeds the range of the Swiss Ephemeris.'
    else:
        print 'Julian Day UT: ', julian_day_ut
    return


# Recalculate all Julian Day UT times in the birth table
def recalculate_all_julian_day_ut():
    for rec in data.births:
        # Calculate Julian Day UT:
        time = str(rec.lst).split(':')
        hrs = int(time[0]) + (int(time[1]) / 60.0)
        julian_day_ut = swe_julday(rec.year, rec.month, rec.day, hrs, SE_GREG_CAL) - ((float(rec.lst_delta) + float(rec.dst_delta)) / 24)
        if (abs(float(rec.julian_day_ut) - julian_day_ut)) >= 0.00001 : # Not using sys.float_info.epsilon since rec[8] lost precision from dec string
            set_db(statement = """UPDATE births SET julian_day_ut = %s WHERE name = '%s'""" %(julian_day_ut, rec[0]))
            print rec[0] + ' changed from ' + str(rec.julian_day_ut) + ' to ' + str(julian_day_ut)
        else :
            print '.'
    return


""" phase.py """


# Print phase info
def show_phase(julian_day_ut, method):
    phase = get_phase(julian_day_ut, method)
    for tithi_detail in TITHIS:
        if getattr(tithi_detail, 'num') == phase[1]:
            print '{2:3}% of {0:6} day {1:2}, {3:20} {4:12} ruled by {5:15}'.format(phase[0], phase[1], phase[2], tithi_detail.name, tithi_detail.omen, tithi_detail.deity)
            break
    return


# as it says
def show_all_birth_phase():
    print 'Viewing all phase values for births:'
    for rec in data.births:
        print rec[name]
        show_phase(rec[julian_day_ut])
    print '_' * 25
    return


# as it says
def show_dasa(time):
    dasa_cycle = get_dasa_cycle(time)
    info_born = get_dasa(dasa_cycle, time)
    info_now = get_dasa(dasa_cycle)
    mdper = int(((time - float(info_born[0].rise)) / (float(info_born[0].end) - float(info_born[0].rise))) * 100)
    adper = int(((time - float(info_born[1].rise)) / (float(info_born[1].end) - float(info_born[1].rise))) * 100)
    print 'Dasa born: {0}({1}%)-{2}({3}%)'.format(info_born[0].dasa, mdper, info_born[1].dasa, adper)
    mdper = int(((utl.getJulian() - float(info_now[0].rise)) / (float(info_now[0].end) - float(info_now[0].rise))) * 100)
    adper = int(((utl.getJulian() - float(info_now[1].rise)) / (float(info_now[1].end) - float(info_now[1].rise))) * 100)
    print 'Dasa now:  {0}({1}%)-{2}({3}%)'.format(info_now[0].dasa, mdper, info_now[1].dasa, adper)
    return

# Show dasa cycle for the given time and note the age at each dasa cusp
def show_dasa_cycle(time):
    dasa_cycle = get_dasa_cycle(time)
    print 'Dasa Cycle'
    for i in dasa_cycle:
        raw_date = rev_julian(float(i.rise))
        date = datetime.date(raw_date[0], raw_date[1], raw_date[2])
        age = int((float(i.rise) - time) / SUN_YEAR)
        print 'MD {0:3}yrs {1} {2}'.format(age, i.mahadasa, date.strftime("%Y, %B"))
        for a in i.antardasas:
            raw_date = rev_julian(float(a[1]))
            date = datetime.date(raw_date[0], raw_date[1], raw_date[2])
            age = int((float(a[1]) - time) / SUN_YEAR)
            print '{0:3}yrs {1:8} {2}'.format(age, a[0], date.strftime("%Y, %B"))
        print '***************************'
    return

try:
    swe_set_ephe_path(SE_EPHE_PATH)
except:
    print 'Invalid path to Swiss Ephemeris. Exiting...'
    sys.exit()

try:
    load_data_files()
except:
    print 'Could not load data files. Exiting...'
    sys.exit()

# Start
print "\n\n☼ ☾ ☿ ♀ ♂ ♃ ♄ ☊ ☋ ♈ ♉ ♊ ♋ ♌ ♍ ♎ ♏ ♐ ♑ ♒ ♓\nEast - Comparative Astrology Software\n"
show_all(utl.getJulian())

while True:
    args = raw_input('\nEnter operation: ').strip().lower().split()

# 1 arguments
    if len(args) == 0:
        continue
    elif args[0] in ('exit', 'quit', 'q'):
        print 'Bye'
        break
    elif args[0] in ('help', 'h', '?'):
        list_commands()
    elif args[0] == 'add':
        add_birth()
    elif args[0] == 'birth':
        show_birth()
    elif args[0] == 'recalc':
        recalculate_all_julian_day_ut()
    elif args[0] == 'load':
        deserialize_db()
    elif args[0] == 'save':
        serialize_db()
    elif args[0] == 'phase':
        show_all_birth_phase()
    elif args[0] == 'orderphase':
        show_all_birth_phase_ordered()
    elif args[0] == 'ordermoon':
        show_all_birth_nakshatra_ordered()
    elif args[0] == 'orderdasacurrent':
        show_all_birth_dasa_current_ordered()
    elif args[0] == 'orderdasabirth':
        show_all_birth_dasa_birth_ordered()
    elif args[0] == 'orderanimal':
        show_all_birth_animal_ordered()
    elif args[0] == 'ordersun':
        show_all_birth_sun_ordered()
    elif args[0] == 'orderday':
        show_all_birth_weekdays_ordered()
    elif args[0] == 'store':
        db_to_file()
    elif args[0] == 'get':
        pass

    elif args[0] == 'transit':
        # On 2456400.83238 the future and past transits for sun and moon are equal
        #get_transit(2456400.83238, SE_SUN, SE_MOON, True)
        #get_transit(2456400.83238, SE_SUN, SE_MOON, False)

        #get_transit(2756335.74399, SE_SUN, SE_MOON, True)
        #get_transit(2756335.74399, SE_SUN, SE_MOON, False)

        #Saturn Mars retrograde problem:
        #get_transit(2456650.72274, 6, 4, True)

        # Sun and Moon test loop
        interval = 0
        while interval < 4000:
            print 'final:', get_sun_moon_transit(utl.getJulian() + interval, True)
            print 'final:', get_sun_moon_transit(utl.getJulian() + interval, False)
            interval = interval + math.pi

        # Planet test loop
        """interval = 0.01
        while interval < 1:
            pl1 = 0
            while pl1 < 7:
                pl2 = 0
                while pl2 < 7:
                    if pl1 != pl2:
                        print 'Pl1: {} Pl2: {}'.format(pl1, pl2))
                        get_transit(utl.getJulian() + interval, pl1, pl2, True)
                        get_transit(utl.getJulian() + interval, pl1, pl2, False)
                    pl2 = pl2 + 1
                pl1 = pl1 + 1

            interval = interval + 0.11"""
    elif args[0] == 'revjul':
        juldayut = raw_input('\nJulian date to convert: ')
        print swe_revjul(float(juldayut), SE_GREG_CAL)
    elif args[0] == 'getjul':
        get_julian_day()

# 2 arguments
    elif len(args) < 2:
        print 'Not understanding.'
    elif args[0] == 'list':
        list(args[1])
    elif args[0] == 'show':
        show(args[1])

# 3 arguments
    elif len(args) < 3:
        print 'Not understanding.'
    elif args[0] == 'find':
        find(args[1:])
    elif args[0] in ('describe', 'desc'):
        describe(args[1:])

    else:
        print 'say again?'

swe_close()





