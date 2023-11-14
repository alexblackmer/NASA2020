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
    
with open ('filestation032', 'r') as file:
	station = file.readlines()
file.close()
with open('fileevent_dbz','r') as file:
	eventDates = file.readlines()
file.close()
with open('filepratenws','r') as file:
	eventList = file.readlines()
file.close()
with open('fileptotaldata032','r') as file:
	ptotal = file.readlines()
file.close()
with open('filepluviodata032','r') as file:
	pluvio = file.readlines()
file.close()
with open('filerel','r') as file:
	rel = file.readlines()
file.close()


nrel = len(rel)
nstat = len(station)
ev = 8
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
outF = open("biasZS032.txt","w+")

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
        rel_path_plu = name[s]+'/'+statPluv[0]
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
        b = (data[i,1]-data[i,0])/nstat
        ab = abs((data[i,1]-data[i,0]))/nstat
        bias = bias + b
        absBias = absBias + ab
        sumObs = sumObs + data[i,0]
        i = i+1
    sumObs = sumObs/nstat
    pBias = (bias/sumObs)*100
    pAbsBias = (absBias/sumObs)*100
    
    relName = rel[r].rstrip().split()
    outF.write(str(relName[0]) +',   ')
    outF.write(str(round(bias,2))+ ',   ')
    outF.write(str(round(absBias,2))+ ',   ')
    outF.write(str(round(pBias,4))+ ',   ')
    outF.write(str(round(pAbsBias,4))+ '\n')
    
    #Plots 4x4 scatter plots
    if r == 0:
        ax1.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.ylabel("Estimated SWE (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        ax1.plot([0, 1], [0, 1], 'k', transform=ax1.transAxes)
        plt.ylim(10**-1,10)

    if r == 1:
        ax2=plt.subplot(4, 4, 2, sharex = ax1, sharey = ax1)
        ax2.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        ax2.plot([0, 1], [0, 1], 'k', transform=ax2.transAxes)
        plt.ylim(10**-1,10)

    if r == 2:
        ax3=plt.subplot(4, 4, 3, sharex = ax1, sharey = ax1)
        ax3.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        ax3.plot([0, 1], [0, 1], 'k', transform=ax3.transAxes)
        plt.ylim(10**-1,10)

    if r == 3:
        ax4=plt.subplot(4, 4, 4, sharex = ax1, sharey = ax1)
        ax4.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        ax4.plot([0, 1], [0, 1], 'k', transform=ax4.transAxes)
        plt.ylim(10**-1,10)

    if r == 4:
        ax5=plt.subplot(4, 4, 5, sharex = ax1, sharey = ax1)
        ax5.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.ylabel("Estimated SWE (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        ax5.plot([0, 1], [0, 1], 'k', transform=ax5.transAxes)
        plt.ylim(10**-1,10)

    if r == 5:
        ax6=plt.subplot(4, 4, 6, sharex = ax1, sharey = ax1)
        ax6.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        ax6.plot([0, 1], [0, 1], 'k', transform=ax6.transAxes)
        plt.ylim(10**-1,10)



    if r == 6:
        ax7=plt.subplot(4, 4, 7, sharex = ax1, sharey = ax1)
        ax7.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        ax7.plot([0, 1], [0, 1], 'k', transform=ax7.transAxes)
        plt.ylim(10**-1,10)

    if r == 7:
        ax8=plt.subplot(4, 4, 8, sharex = ax1, sharey = ax1)
        ax8.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        ax8.plot([0, 1], [0, 1], 'k', transform=ax8.transAxes)
        plt.ylim(10**-1,10)

    if r == 8:
        ax9=plt.subplot(4, 4, 9, sharex = ax1, sharey = ax1)
        ax9.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.ylabel("Estimated SWE (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        ax9.plot([0, 1], [0, 1], 'k', transform=ax9.transAxes)
        plt.ylim(10**-1,10)

    if r == 9:
        ax10=plt.subplot(4, 4, 10, sharex = ax1, sharey = ax1)
        ax10.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        ax10.plot([0, 1], [0, 1], 'k', transform=ax10.transAxes)
        plt.ylim(10**-1,10)

    if r == 10:
        ax11=plt.subplot(4, 4, 11, sharex = ax1, sharey = ax1)
        ax11.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        ax11.plot([0, 1], [0, 1], 'k', transform=ax11.transAxes)
        plt.ylim(10**-1,10)

    if r == 11:
        ax12=plt.subplot(4, 4, 12, sharex = ax1, sharey = ax1)
        ax12.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.title(relName[0], fontsize = 6)
        ax12.plot([0, 1], [0, 1], 'k', transform=ax12.transAxes)
        plt.ylim(10**-1,10)

    if r == 12:
        ax13=plt.subplot(4, 4, 13, sharex = ax1, sharey = ax1)
        ax13.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.ylabel("Estimated SWE (mm)", fontsize = 6)
        plt.xlabel("Pluvio (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        ax13.plot([0, 1], [0, 1], 'k', transform=ax13.transAxes)
        plt.ylim(10**-1,10)

    if r == 13:
        ax14=plt.subplot(4, 4, 14, sharex = ax1, sharey = ax1)
        ax14.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.xlabel("Pluvio (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        ax14.plot([0, 1], [0, 1], 'k', transform=ax14.transAxes)
        plt.ylim(10**-1,10)

    if r == 14:
        ax15=plt.subplot(4, 4, 15, sharex = ax1, sharey = ax1)
        ax15.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.xlabel("Pluvio (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        ax15.plot([0, 1], [0, 1], 'k', transform=ax15.transAxes)
        plt.ylim(10**-1,10)

    if r == 15:
        ax16=plt.subplot(4, 4, 16, sharex = ax1, sharey = ax1)
        ax16.scatter(data[:,0], data[:,1],label = relName)
        plt.yscale('log')
        plt.xscale('log')
        plt.xticks( fontsize=5)
        plt.yticks( fontsize=5)
        plt.xlabel("Pluvio (mm)", fontsize = 6)
        plt.title(relName[0], fontsize = 6)
        ax16.plot([0, 1], [0, 1], 'k', transform=ax16.transAxes)
        plt.ylim(10**-1,10)


    r=r+1
plt.show()
plt.savefig("figZSScat0{0}.png".format(day))
    
