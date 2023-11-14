#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt


"""
Filename: plotRayPluv.py
Purpose: This program plots the precipitation accumulation for 16 Rayleigh
         approximation Z-S relationships and pluvio data, for event 003 
         and each station. The outputs are 4 4x4 subplots of each relationship
@author: Alex Blackmer
Updated: 07/19/2020
"""

#Function converts julian time data to partial julian day
#Inputs: d(day), hr(hour), min(minute), sec(seconds)
#Outputs: partial(partial julian day) integer
def toPartial(d,hr,min,sec):
        partial = float(d + hr/24. + min/1440. + sec/86400.)
        return partial

#Opens critical files
with open ('filestation', 'r') as file:
	station = file.readlines()
file.close()
with open('filepratenws','r') as file:
	eventList = file.readlines()
file.close()
with open('fileevent_dbz','r') as file:
	eventDates = file.readlines()
file.close()
with open('filepluvio','r') as file:
	pluvio = file.readlines()
file.close()
with open ('filerel034', 'r') as file:
	zsF = file.readlines()
file.close()

nev = len(eventList)        #num of events
nzs = len(zsF)		        #num of Z-S relationships
nplu = 3                    #Num of pluvio corrections
rel = []    
i=0

while i < nzs:
    zs = zsF[i].split()
    rel.append(zs[0]) #z-s rel coefficient
    i=i+1

#Parses data and creates graphs for 003 event.
ev = 9
yAxis = 20
event = eventList[ev].split()
dates = eventDates[ev].split()
eventPluv = pluvio[ev].split()
day = int(event[0])
nMin =int(event[1]) * 1440
time = np.empty([nMin,1])
data = np.empty([nMin,nzs])
plu = np.empty([nMin,nplu])
#Opens *_ptotal.kmqt file
with open(event[4],'r') as file:
    prateT = file.readlines()
file.close()

with open(eventPluv[2],'r') as file:
    pluvioD = file.readlines()
file.close()
with open(eventPluv[3],'r') as file:
    pluvioCD = file.readlines()
file.close()
        
#Puts snow accumulation data into array for plotting
t = 0
while t < nMin:
    prate = prateT[t].split()
    pluvioDAcc = pluvioD[t].split()
    pluvioCDAcc = pluvioCD[t].split()
    time[t] = toPartial(int(prate[1]),int(prate[2]),int(prate[3]),0)
    i = 0
    while i < nzs:
        data[t,i] = prate[4+i]
        i=i+1
    j = 0
    while j < nplu:
        plu[t,0] = pluvioDAcc[5]   
        plu[t,1] = pluvioDAcc[4]   
        plu[t,2] = pluvioCDAcc[4] 
        j=j+1
    t=t+1
    
#Creates event plot with each Z-S relationship
i = 0
while i < 4:
    if i == 0:
        ax1=plt.subplot(2, 2, 1)
        j=0
        while j < 4:
            ax1.plot(time, data[:,j],label = rel[j])
            j=j+1
        ax1.plot(time, plu[:,0],color = "#FF00FF", label = "Pluvio")
        ax1.plot(time, plu[:,1], color = "#7F00FF", label = "NWS Corr.")
        ax1.plot(time, plu[:,2], color = "#0000FF", label = "Cit. Corr.")
        plt.xticks(fontsize=9)
        plt.ylim(0,yAxis)
        plt.yticks(fontsize=9)
        plt.legend(loc = 2,prop={'size': 6})
        plt.title("BM")
        plt.ylabel('Snow Acc. (mm)')

    if i == 1:
        ax2=plt.subplot(2, 2, 2, sharex = ax1, sharey = ax1)
        j=4
        while j < 8:
            ax2.plot(time, data[:,j],label = rel[j])
            j=j+1
        ax2.plot(time, plu[:,0],color = "#FF00FF", label = "Pluvio")
        ax2.plot(time, plu[:,1], color = "#7F00FF", label = "NWS Corr.")
        ax2.plot(time, plu[:,2], color = "#0000FF", label = "Cit. Corr.")
        plt.xticks(fontsize=9)
        plt.ylim(0,yAxis)
        plt.yticks(fontsize=9)
        plt.legend(loc = 2,prop={'size': 6})
        plt.title("HW")

    if i == 2:
        ax3=plt.subplot(2, 2, 3, sharex = ax1, sharey = ax1)
        j=8
        while j < 12:
            ax3.plot(time, data[:,j],label = rel[j])
            j=j+1
        ax3.plot(time, plu[:,0],color = "#FF00FF", label = "Pluvio")
        ax3.plot(time, plu[:,1], color = "#7F00FF", label = "NWS Corr.")
        ax3.plot(time, plu[:,2], color = "#0000FF", label = "Cit. Corr.")
        plt.xticks(fontsize=9)
        plt.ylim(0,yAxis)
        plt.yticks(fontsize=9)
        plt.legend(loc = 2,prop={'size': 6})
        plt.title("KC")
        plt.ylabel('Snow Acc. (mm)')
        plt.xlabel('Day of Year ({0})'.format(int(dates[0])))

    if i == 3:
        ax4=plt.subplot(2, 2, 4, sharex = ax1, sharey = ax1)
        j=12
        while j < 16:
            ax4.plot(time, data[:,j],label = rel[j])
            j=j+1
        ax4.plot(time, plu[:,0],color = "#FF00FF", label = "Pluvio")
        ax4.plot(time, plu[:,1], color = "#7F00FF", label = "NWS Corr.")
        ax4.plot(time, plu[:,2], color = "#0000FF", label = "Cit. Corr.")
        plt.ylim(0,yAxis)
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)
        plt.legend(loc = 2,prop={'size': 6})
        plt.title("MH")
        plt.xlabel('Day of Year ({0})'.format(int(dates[0])))

    i=i+1  

plt.suptitle('Station ' + station[0].rstrip(), fontsize = 16)
plt.savefig("fig"+station[0].rstrip()+"PAccAll0{0}.png".format(day))