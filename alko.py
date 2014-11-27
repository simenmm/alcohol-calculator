#! /usr/bin/python
import sys
import math

def promille(innp,innv,bw,gend,target):
    p = innp/100 #alcohol content in % ABV
    v = innv/100 #drink volume in cl
    m = p*v*0.789 #drink alcohol mass
    if gend == 'm':
        gendConst = 0.58
        rate = 0.15
    elif gend == 'f':
        gendConst = 0.49
        rate = 0.17
    else:
        print "please input biological gender"
        return
    
    #ideal = target*gendConst*bw/(806*0.789*p) #ideal frontload volume
    effDrink = 806*m/(gendConst*bw) #additional BAC from one drink
    steadyRate = effDrink/rate
    
    #frontloading schedule
    if steadyRate < 1:
        frontTime = 15
    else:
        frontTime = 30
    frontNum = int(math.ceil(target/(effDrink-rate*frontTime/60))) #no of drinks
    alcLevelAfter = effDrink*frontNum - rate*frontNum*frontTime/60

    if alcLevelAfter - target < 0.05:
        frontNum += 1
        alcLevelAfter += effDrink - rate*frontTime/60
    
    newTarget = target - effDrink/2
    dwellTime = (alcLevelAfter - newTarget)/rate
    steadyRate = effDrink/rate
    
    print "Effect of single drink: " + str(round(effDrink,2))
    
    print "Recommended drinking procedure:\n"\
        + "Start one drink every "\
        + str(frontTime) + " minutes for the first "\
        + str(frontNum) + " drinks, to achieve BAC of "\
        + str(round(alcLevelAfter,2)) + ".\nWait for "\
        + str(int(dwellTime)) + " hours and "\
        + str(int(dwellTime % 1 * 60))\
        + " minutes before next drink to reach BAC "\
        + str(round(newTarget,2)) + ". \nThen start a new drink every "\
        + str(int(steadyRate)) + " hours and "\
        + str(int(steadyRate % 1 * 60)) + " minutes, peaking at "\
        + str(round(newTarget + effDrink,2))
    
    return

helpMess = """Usage: alko.py p v bw gend target
\t       p: alcohol content of desired drink in % ABV
\t       v: volume of desired drink in cl
\t       bw: bodyweight of drinker in kg
\t       gend: biological gender of drinker: m or f
\t       target: desired blood alcohol level in parts per thousand"""

if len(sys.argv) != 5:
    print helpMess
    sys.exit()

try:
    (lol, p, v, bw, gend, target) = sys.argv
    p = float(p)
    v = float(v)
    bw = float(bw)
    target = float(target)
except ValueError:
    print helpMess
    sys.exit()

promille(p,v,bw,gend,target)
