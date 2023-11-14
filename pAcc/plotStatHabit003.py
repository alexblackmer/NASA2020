#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import os


"""
Filename: plotRay7Rel.py
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
with open('fileptotaldata003','r') as file:
	ptotal = file.readlines()
file.close()
with open('filerel','r') as file:
	rel = file.readlines()
file.close()


nrel = len(rel)
nstat = len(station)
ev = 3
name = []
yAxis = 30

i = 0
while i < nstat:
    statD = station[i].split()
    name.append(statD[0])
    i = i+1

#Loops over each event to parse data and create graphs
event = eventList[ev].split()
dates = eventDates[ev].split()
day = int(event[0])
nMin =int(event[1]) * 1440
time = np.empty([nMin,1])
ray = np.empty([nMin,nstat])
        


r = 0
while r < nrel:
    s = 0
    while s < nstat:
        #Puts snow accumulation data into array for plotting
        statPAcc = ptotal[s].split()
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = name[s]+'/'+statPAcc[0]
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path,'r') as file:
            ptotalD = file.readlines()
        file.close()
        
        t = 0
        while t < nMin:
            ptotalDAcc = ptotalD[t].split()
            time[t] = toPartial(int(ptotalDAcc[1]),int(ptotalDAcc[2]),int(ptotalDAcc[3]),0)
            ray[t,s] = ptotalDAcc[4+r] 
            t=t+1
        
        relName = rel[r].rstrip().split()

        if r == 12:
            ax1=plt.subplot(2, 2, 1)
            ax1.plot(time, ray[:,s],label = name[s])
            plt.xticks(fontsize=9)
            plt.ylim(0,yAxis)
            plt.yticks(fontsize=9)
            plt.legend(loc = 2,prop={'size': 8})
            plt.title(relName[0])
            plt.ylabel('Estimated SWE (mm)')
            
        if r == 13:
            ax2=plt.subplot(2, 2, 2, sharex = ax1, sharey = ax1)
            ax2.plot(time, ray[:,s],label = name[s])
            plt.xticks(fontsize=9)
            plt.ylim(0,yAxis)
            plt.yticks(fontsize=9)
            plt.legend(loc = 2,prop={'size': 8})
            plt.title(relName[0])

        if r == 14:
            ax3=plt.subplot(2, 2, 3, sharex = ax1, sharey = ax1)
            ax3.plot(time, ray[:,s],label = name[s])
            plt.xticks(fontsize=9)
            plt.ylim(0,yAxis)
            plt.yticks(fontsize=9)
            plt.legend(loc = 2,prop={'size': 8})
            plt.title(relName[0])
            plt.xlabel('Day of Year ({0})'.format(int(dates[0])))
            plt.ylabel('Estimated SWE (mm)')

        if r == 15:
            ax4=plt.subplot(2, 2, 4, sharex = ax1, sharey = ax1)
            ax4.plot(time, ray[:,s],label = name[s])
            plt.xticks(fontsize=9)
            plt.ylim(0,yAxis)
            plt.yticks(fontsize=9)
            plt.legend(loc = 2,prop={'size': 8})
            plt.title(relName[0])
            plt.xlabel('Day of Year ({0})'.format(int(dates[0])))

        s=s+1
    r=r+1
plt.suptitle('Habit Z-S Rel.', fontsize = 16)
plt.savefig("figHabit00{0}.png".format(day))    
plt.close()
   

    
