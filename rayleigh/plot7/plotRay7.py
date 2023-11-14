#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt


"""
Filename: plotRay7.py
Purpose: Plots each estimated Rayleigh SWE rate at the 7 sites for event 003
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
with open('filepratenws','r') as file:
	eventList = file.readlines()
file.close()
with open('fileptotaldata','r') as file:
	ptotal = file.readlines()
file.close()
with open('filerel','r') as file:
	rel = file.readlines()
file.close()


nrel = len(rel)
ev = 3
name = []

i = 0
while i < nrel:
    relD = rel[i].split()
    name.append(relD[0])

    i = i+1

#Loops over each event to parse data and create graphs
event = eventList[ev].split()
dates = eventDates[ev].split()
day = int(event[0])
nMin =int(event[1]) * 1440
time = np.empty([nMin,1])
ray = np.empty([nMin,nrel])
        
#Puts snow accumulation data into array for plotting
statPAcc = ptotal[0].split()
with open(statPAcc[0],'r') as file:
    ptotalD = file.readlines()
file.close()


t = 0
while t < nMin:
    ptotalDAcc = ptotalD[t].split()
    time[t] = toPartial(int(ptotalDAcc[1]),int(ptotalDAcc[2]),int(ptotalDAcc[3]),0)
    i = 0
    while i < nrel:
        ray[t,i] = ptotalDAcc[4+i] 
        i = i+1
    t=t+1
#Time formatting
#Creates event plot with each Z-S relationship
    
i = 0
while i < nrel:
    plt.plot(time, ray[:,i],label = name[i])
    i = i+1

plt.title("Station  " + station[0].rstrip())
plt.ylabel('Snow Acc. (mm)')
plt.ylim(0,80)
plt.xlabel('Day of Year ({0})'.format(int(dates[0])))
plt.legend(loc = 2,prop={'size': 8})
plt.savefig("fig" + station[0].rstrip() + "Ray7.png")
plt.close()