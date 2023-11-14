#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt


"""
Filename: plotAllPluv.py
Purpose: Plots the total raw pluvio accumulation at all 7 stations for 
         event 003.
@author: Alex Blackmer
Updated: 07/19/2020
"""

#Function converts julian time data to partial julian day
#Inputs: d(day), hr(hour), min(minute), sec(seconds)
#Outputs: partial(partial julian day) integer
def toPartial(d,hr,min,sec):
        partial = float(d + hr/24. + min/1440. + sec/86400.)
        return partial
    
with open ('filestation', 'r') as file:
	station = file.readlines()
file.close()
with open('fileevent_dbz','r') as file:
	eventDates = file.readlines()
file.close()
with open('filepluviodata','r') as file:
	pluvio = file.readlines()
file.close()
with open('filepratenws','r') as file:
	eventList = file.readlines()
file.close()
with open('fileptotaldata','r') as file:
	ptotal = file.readlines()
file.close()


nplu = 1     #Num of pluvio lines
nsta = len(station)
ev = 3
name = np.empty([nsta,1], dtype=str)

#Loops over each event to parse data and create graphs
event = eventList[ev].split()
dates = eventDates[ev].split()
day = int(event[0])
nMin =int(event[1]) * 1440
time = np.empty([nMin,1])
plu = np.empty([nMin,nsta])
names = []
        
#Puts snow accumulation data into array for plotting
i = 0
while i < nsta:
    statPluv = pluvio[i].split()
    statPAcc = ptotal[i].split()
    name = station[i].rstrip()
    names.append(name)
    precipPath = "./" + name + "/" + statPAcc[0]
    pluPath = "./" + name + "/" + statPluv[0]
    with open(precipPath,'r') as file:
        ptotalD = file.readlines()
    file.close()
    with open(pluPath,'r') as file:
        pluvioD = file.readlines()
    file.close()
    
    t = 0
    while t < nMin:
        ptotalDAcc = ptotalD[t].split()
        pluvioDAcc = pluvioD[t].split()
        time[t] = toPartial(int(ptotalDAcc[1]),int(ptotalDAcc[2]),int(ptotalDAcc[3]),0)
        plu[t,i] = pluvioDAcc[5]   
        t=t+1
    i = i+1
#Time formatting
#Creates event plot with each Z-S relationship
    
i = 0
while i < nsta:
    plt.plot(time, plu[:,i],label = names[i])
    i = i+1

plt.ylabel('Snow Acc. (mm)')
plt.xlabel('Day of Year ({0})'.format(int(dates[0])))
plt.legend(loc = 2)
plt.savefig("figTotalPluv.png")
plt.close()