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
with open('fileptotaldata362','r') as file:
	ptotal = file.readlines()
file.close()
with open('filepluviodata362','r') as file:
	pluvio = file.readlines()
file.close()
with open('filerel362','r') as file:
	rel = file.readlines()
file.close()


nrel = len(rel)
nstat = len(station)
ev = 2
name = []

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
ptot = np.empty([nMin,nstat])
plu = np.empty([nMin,nstat])

        

ax1=plt.subplot(4, 4, 1)
outF = open("biasRay362.txt","w+")

r = 0
while r < nrel:
    s = 0
    data = np.zeros([nstat,2])
    while s < nstat:
        #Puts snow accumulation data into array for plotting
        statPAcc = ptotal[s].split()
        statPluv = pluvio[s].split()
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path_ptot = name[s]+'/'+statPAcc[0]
        abs_file_path_ptot = os.path.join(script_dir, rel_path_ptot)
        #abs_file_path_ptot = statPAcc[0]
        with open(abs_file_path_ptot,'r') as file:
            ptotalD = file.readlines()
        file.close()
        rel_path_plu = name[s]+'/'+statPAcc[0]
        abs_file_path_plu = os.path.join(script_dir, rel_path_plu)
        #abs_file_path_plu = statPluv[0]
        with open(abs_file_path_plu,'r') as file:
            pluvioD = file.readlines()
        file.close()
        
        
        t = 0
        while t < nMin:
            ptotalDAcc = ptotalD[t].split()
            pluvioDAcc = pluvioD[t].split()
            time[t] = toPartial(int(ptotalDAcc[1]),int(ptotalDAcc[2]),int(ptotalDAcc[3]),0)
            ptot[t,s] = ptotalDAcc[4+r] 
            plu[t,s] = pluvioDAcc[5] 

            t=t+1
            
        data[s,1] = ptot[len(ptot)-1,s]
        data[s,0] = plu[len(plu)-1,s]
        s=s+1

    #Computes bias, absolute bias, and percent bias
    i = 0
    bias = 0
    absBias = 0
    sumObs = 0
    while i < nstat:
        b = (data[i,1]-data[i,0])
        ab = abs((data[i,1]-data[i,0]))
        bias = bias + b
        absBias = absBias + ab
        sumObs = sumObs + data[i,0]
        i = i+1
    bias = bias/nstat
    absBias = absBias/nstat
    pBias = bias/sumObs 
    
    relName = rel[r].rstrip().split()
    outF.write(str(relName[0]) +'   ')
    outF.write(str(round(bias,2))+ '   ')
    outF.write(str(round(absBias,2))+ '   ')
    outF.write(str(round(pBias,4))+ '\n')

    if r == 0:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.ylabel("Estimated SWE (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        ax1.plot([0, 1], [0, 1], 'k', transform=ax1.transAxes)
        plt.ylim(10**-1,10)
        plt.show()

    if r == 1:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()


    if r == 2:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()
    if r == 3:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()
    if r == 4:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.ylabel("Estimated SWE (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()
    if r == 5:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()
    if r == 6:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()
    if r == 7:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()
    if r == 8:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.ylabel("Estimated SWE (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()
    if r == 9:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()
    if r == 10:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()
    if r == 11:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()
    if r == 12:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.ylabel("Estimated SWE (mm)", fontsize = 6)
        plt.xlabel("Pluvio Uncorr. (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()
    if r == 13:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.xlabel("Pluvio Uncorr. (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()
    if r == 14:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.xlabel("Pluvio Uncorr. (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()
    if r == 15:
        plt.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.xlabel("Pluvio Uncorr. (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        
        plt.ylim(10**-1,10)
        plt.show()


    r=r+1
plt.savefig("figRayScat{0}.png".format(day))
    
