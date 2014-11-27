#! /usr/bin/python
from __future__ import division
import sys
import math

def print_instructions(innp,innv,bw,gend,target):
    p = innp/100 #alcohol content in % ABV
    v = innv/100 #drink volume in cl
    m = p*v*0.789 #drink alcohol mass
    if not gend in ['m', 'f']:
        raise ValueError("Gender must be either m or f")
    if gend == 'm':
        gend_const = 0.58
        rate = 0.15
    elif gend == 'f':
        gend_const = 0.49
        rate = 0.17
    
    #ideal = target*gend_const*bw/(806*0.789*p) #ideal frontload volume
    eff_drink = 806*m/(gend_const*bw) #additional BAC from one drink
    steady_rate = eff_drink/rate
    
    #frontloading schedule
    if steady_rate < 1:
        front_time = 15
    else:
        front_time = 30
    front_num = int(math.ceil(target/(eff_drink-rate*front_time/60))) #no of drinks
    alc_level_after = eff_drink*front_num - rate*front_num*front_time/60

    if alc_level_after - target < 0.05:
        front_num += 1
        alc_level_after += eff_drink - rate*front_time/60
    
    new_target = target - eff_drink/2
    dwell_time = (alc_level_after - new_target)/rate
    steady_time = eff_drink/rate
    
    #Strings for output
    eff_drink_string = str(round(eff_drink,2))
    dwell_hours = str(int(dwell_time))
    dwell_minutes = str(int(dwell_time % 1 * 60))
    steady_hours = str(int(steady_time))
    steady_minutes = str(int(steady_time % 1 * 60))
    BAC_after = str(round(alc_level_after,2))
    BAC_new = str(round(new_target,2))
    BAC_peak = str(round(new_target + eff_drink,2))
    
    print "Effect of single drink: " + eff_drink_string
    print "BAC decreases by " + str(rate) + " every hour."
    print "Recommended drinking procedure:\n"\
        + "Start one drink every "\
        + str(front_time) + " minutes for the first "\
        + str(front_num) + " drinks, to achieve BAC of "\
        + BAC_after + ".\nWait for "\
        + dwell_hours + " hours and "\
        + dwell_minutes\
        + " minutes before next drink to reach BAC "\
        + BAC_new + ". \nThen start a new drink every "\
        + steady_hours + " hours and "\
        + steady_minutes + " minutes, peaking at "\
        + BAC_peak\
        + "\n\nWARNING: High values of target may result in user error."


helpMess = """Usage: alko.py p v bw gend target
\t       p: alcohol content of desired drink in % ABV
\t       v: volume of desired drink in cl
\t       bw: bodyweight of drinker in kg
\t       gend: biological gender of drinker: m or f
\t       target: desired blood alcohol level in parts per thousand"""

if len(sys.argv) != 6:
    print helpMess
    sys.exit()

try:
    (p, v, bw, gend, target) = sys.argv[1:]
    p = float(p)
    v = float(v)
    bw = float(bw)
    target = float(target)
except ValueError:
    print helpMess
    sys.exit()

print_instructions(p,v,bw,gend,target)
