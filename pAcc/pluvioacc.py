#! /usr/bin/python
import numpy as np
"""
Filename: pluvioacc.py
Purpose: This program computes the raw pluvio accumulation as well as the 
         single altar-shielded estimations from the WX and civilian stations.
Author: Alex Blackmer
Updated: 07/19/2020
"""

#Function converts julian time data to partial julian day
#Inputs: d(day), hr(hour), min(minute), sec(seconds)
#Outputs: partial(partial julian day) integer
def toPartial(d,hr,min,sec):
        partial = float(d + hr/24. + min/1440. + sec/86400.)
        return partial
    
#Opens necessary files
with open('filepluvio','r') as file:
	eventList = file.readlines()
file.close()
with open('fileevent_dbz','r') as file:
	eventTimes = file.readlines()
file.close()
with open('filepluviodata','r') as file:
	pluvioFilesD = file.readlines()
file.close()

pluvioFiles = pluvioFilesD[0].split() 
#Imports pluvio data
with open(pluvioFiles[0],'r') as file:
	pluvio = file.readlines()
file.close()
with open(pluvioFiles[1],'r') as file:
	pluvioC = file.readlines()
file.close()

n10 = 200	#num greater than the 10 min increments in a day
nev = len(eventList)	#num of events
inTime = np.empty([len(pluvio), 1])     #Time arr for input 10 min inc.
pluvD = np.empty([len(pluvio), 2])   #Input snowfall rate data
pluvCD = np.empty([len(pluvioC), 2])   #Input snowfall rate data

#Loops over each line in event file to fill time and data arrays
t = 0
while t < len(pluvioC):
    line = pluvio[t].split()
    lineC = pluvioC[t].split()
    inTime[t,0] = toPartial(int(line[1]),int(line[2]),int(line[3]),0)
    i = 0
    #Saves raw and corrected pluvio data for both stations
    while i < 2:
        if i == 0:
            pluvD[t,i] = line[i+10]
            pluvCD[t,i] = lineC[i+10]
        if i == 1:
            pluvD[t,i] = float(line[i+10])
            pluvCD[t,i] = float(lineC[i+10])
        i=i+1
    t = t+1


#Loop for each event
ev = 0
while ev < nev:
    event = eventList[ev].split()
    eTimes = eventTimes[ev].split()
    #Time info
    year = int(eTimes[0])
    nDays =int(event[1])
    sDay = int(eTimes[1])
    fDay = int(eTimes[3])
    sHr = int(eTimes[2])
    fHr = int(eTimes[4])
    nMin = nDays * 1440

    #Creates partial day of critical times
    sDate = toPartial(sDay,sHr,0,0)
    fDate = toPartial(fDay,fHr,59,59)
    #Filemnames
    outf1 = event[2]
    outf2 = event[3]
    pluvAcc = np.empty([nMin,2])           #Output snow accumulation data
    pluvCAcc = np.empty([nMin,2])           #Output snow accumulation data
    pluvAcc.fill(0.00)
    pluvCAcc.fill(0.00)
    outTime = np.empty([nMin,4])            #Time arr for both output files
    
    timeI = 0           #Time increment for indexing
    d = 0       
    while d < nDays:
        h = 0
        while h < 24:
            m = 0
            while m < 60:
                #Sets time data for each 1 min increment
                outTime[timeI,0] = int(year)
                outTime[timeI,1] = int(sDay + d)
                outTime[timeI,2] = int(h)
                outTime[timeI,3] = int(m)
                #Converts this time to partial
                pDate = toPartial(outTime[timeI,1],h,m,0)
                closest = -1
                bDate = toPartial(sDay,0,0,0)
                #Loops over input array, looking for smallest difference
                #Between the current time an 10 min intervals
                i = 0
                while i < len(inTime):
                    if inTime[i,0] == pDate:
                        closest = i                    
                    i=i+1
                
                k = 0
                while k < 2:
                    #Writes out snowfal total in mm
                    if closest > 0:
                        if k == 0:
                            if pDate >= sDate and pDate <= fDate:
                                pluvAcc[timeI,k] = pluvAcc[timeI-1,k] + pluvD[closest,1]/pluvD[closest,0]
                                pluvCAcc[timeI,k] = pluvCAcc[timeI-1,k] + pluvCD[closest,1]/pluvCD[closest,0]
                            if pDate > fDate:
                                pluvAcc[timeI,k] = pluvAcc[timeI-1,k]
                                pluvCAcc[timeI,k] = pluvCAcc[timeI-1,k]
                        
                        if k == 1:
                            if pDate >= sDate and pDate <= fDate:
                                pluvAcc[timeI,k] = pluvAcc[timeI-1,k] + pluvD[closest,k]
                                pluvCAcc[timeI,k] = pluvCAcc[timeI-1,k] + pluvCD[closest,k]
                            if pDate > fDate:
                                pluvAcc[timeI,k] = pluvAcc[timeI-1,k]
                                pluvCAcc[timeI,k] = pluvCAcc[timeI-1,k]
                        
                    elif closest < 0:
                        pluvAcc[timeI,k] = pluvAcc[timeI-1,k]
                        pluvCAcc[timeI,k] = pluvCAcc[timeI-1,k]

                    k = k+1
                timeI = timeI+1
                m = m+1
            h = h+1
        d = d+1  
    
    #Writes to each output file
    #First output file    
    outF1= open(outf1,"w+")
    outF2= open(outf2,"w+")

    n = 0
    while n < nMin:
        outF1.write(str(int(outTime[n,0]))+"  ")
        outF1.write(str(int(outTime[n,1]))+"    ")
        outF1.write(str(int(outTime[n,2]))+"    ")
        outF1.write(str(int(outTime[n,3]))+"    ")

        outF2.write(str(int(outTime[n,0]))+"  ")
        outF2.write(str(int(outTime[n,1]))+"    ")
        outF2.write(str(int(outTime[n,2]))+"    ")
        outF2.write(str(int(outTime[n,3]))+"    ")
        m = 0
        while m < 2:
            rpluvAcc = round(pluvAcc[n,m],2)
            rpluvCAcc = round(pluvCAcc[n,m],2)
            outF1.write(str(rpluvAcc)+"      ")
            outF2.write(str(rpluvCAcc)+"      ")
            m = m+1
        n=n+1
        outF1.write("\n")
        outF2.write("\n")
    
    ev=ev+1