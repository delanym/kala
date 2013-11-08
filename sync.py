
# When does the synodic new moon come back to the same nakshatra. How many revolutions?
# By how many degrees does the new moon travel each synodic month? A: 29,105216732 degrees
# So in 12,368916655 months the new moon will have returned to the same sign, but it would
# have overshot or fallen short of the same nakshatra.

"""
How many degrees in a synodic day? 12,970173891
How many degrees in a nakshatra? 13,333333333
It takes around 36 days for the synodic day to be out of sync with the nakshatra days by 1 nakshatra.
By that time however, the synodic month will have already elapsed, and the 1st day of
the next month will conincide with the nakshatra approximately one whole sign ahead, or, just over 2 nakshatras.
"""


SUN_YEAR = 365.2522
MOON_MONTH = 27.3217
SYNODIC_MONTH = 29.5306

Ratio = 1,080847824
SynodicMonth = Ratio * 360 # 389,105216732






a = 3
b = 4
start = 0
i = 1
print 'i={0}, a={1}, b={2}'.format(i, a, b)

while True:
    
    a += 3
    b += 4
    i += 1
    if a > 359:
        a -= 360
    if b > 359:
        b -= 360

    print 'i={0}, a={1}, b={2}'.format(i, a, b)
    if a == b == start:
        break

print 'Finished'



    
