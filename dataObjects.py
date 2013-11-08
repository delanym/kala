#!/usr/bin/env python
# -*- coding: UTF-8 -*-



class Point:
    """ A point in time."""

    def __init__(self):
        self.year = '' # Signed
        self.month = ''
        self.day = ''
        self.hour = ''
        self.minute = ''
        self.delta = '' # Daylight saving or wartime correction (sign:HH:MM)
        self.margin = '' # The margin of error in minutes (This is useful is you know the day but not the time)
                                         # The hour and minute is left blank, a margin will be added and the minute


class Time:
    """ A time, including one or two (range) point objects.
            If a range is accepted, the interface must fill in the extreme missing values for the points. e.g. for an event without a time, 00h00m00s and 23h59m59s
            A range cannot exceed 365 days since the tropical zodiac shift 1' every year
    """

    def __init__(self):
        self.default = True # Use as the default time for the event
        self.calendar = '' # Under which calendar (JULIAN, GREGORIAN, CHINESE, ISLAMIC)
        self.zone = '' # According to (APPARENT, LOCALMEAN, GREENWICH, ZONE)
        self.points = [('', '')] # Point, Julian Day tuples. # Julday must be signed decimal (-251291.5 <> 3693368.5) 2 Jan 5401 BC (jul. calendar) to 31 Dec 5399 AD (greg. Cal.)
        self.source = '' # A description of where the data came from (certificate, db, url, book, correspondence).
                                         # Useful for distinguishing conflicting reports. Add Rodden ratings here.


class Location:
    """ A location where the event took place. """

    def __init__(self):
        pass


class Event:
    """ An astrological event. """
    
    def __init__(self):
        self.type = '' # ENUM (BIRTH, DEATH, DIARY, HISTORICAL, ASTRONOMICAL)
        self.comments = '' # String
        self.times = [] # Time objects. Conflicting reports and rectifications can be added here.
        self.location = '' # Location object.


class Person:
    """ Person record. """

    def __init__(self):
        self.name = '' # 50 char string
        self.privacy = '' # Y/N Choose whether public or private record
        self.astrodienst_link = '' # 128 char URL
        self.events = [] # List of Event objects

























