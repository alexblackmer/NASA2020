#! /usr/bin/python
import numpy as np

"""
Filename: radarratenws.py
Purpose: This program stretches the 10 min precipitation rate values to 1 min
        increments. Additionally, it computes the accumulated precipitation in mm for
        each 1 min increment. 
Author: Alex Blackmer
Updated: 06/23/2020
"""

#Function converts julian time data to partial julian day
#Inputs: d(day), hr(hour), min(minute), sec(seconds)
#Outputs: partial(partial julian day) integer
def toPartial(d,hr,min,sec):
        partial = float(d + hr/24. + min/1440. + sec/86400.)
        return partial

with open('filepratenws','r') as file:
	eventList = file.readlines()
file.close()

with open('fileevent_dbz','r') as file:
	eventTimes = file.readlines()
file.close()

with open ('filerel032', 'r') as file:
	zs = file.readlines()
file.close()


n10 = 200	#num greater than the 10 min increments in a day
nzs = len(zs)		#num of Z-S relationships
nev = len(eventList)	#num of events
nel = 3		#num of elevations


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
    inf = event[2]
    outf1 = event[3]
    outf2 = event[4]
 
    #Opens each kmqt event file
    with open(inf,'r') as file:
        inFile = file.readlines()
    file.close()
    
    #Initializes arrays
    pRateD = np.empty([nMin,nzs*3])            #Output snowfall rate data
    pTotalD = np.empty([nMin,nzs*3])           #Output snow accumulation data
    pTotalD.fill(0.00)
    outTime = np.empty([nMin,4])            #Time arr for both output files
    inTime = np.empty([len(inFile), 1])     #Time arr for input 10 min inc.
    refData = np.empty([len(inFile), nzs*3])   #Input snowfall rate data
	
    #Loops over each line in event file to fill time and data arrays
    t = 0
    while t < len(inFile):
        line = inFile[t].split()
        inTime[t,0] = toPartial(int(line[1]),int(line[2]),int(line[3]),int(line[4]))
        i = 0
        while i < nzs*3:
            refData[t,i] = line[i+5]
            i=i+1
        t = t+1
 
    
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
                closest = 0
                bDate = toPartial(sDay,0,0,0)
                diff = abs(bDate - pDate)
                #Loops over input array, looking for smallest difference
                #Between the current time an 10 min intervals
                i = 0
                while i < len(inTime):
                    diffT = abs(inTime[i,0] - pDate)
                    if  diffT < diff:
                        diff = diffT
                        closest = i                    
                    i=i+1
                
                k = 0
                while k < nzs*3:
                    #Writes out the 10-min inc snowfall rate data to corresponding
                    #1 min increment in cm/hr
                    pRateD[timeI,k] = refData[closest,k]
                    #Writes out snowfal total in cm
                    if pDate >= sDate and pDate <= fDate:
                        if refData[closest,k] > 0:
                            acc = refData[closest,k]/60.
                            pTotalD[timeI,k] = pTotalD[timeI-1,k] + acc
                        elif refData[closest,k] < 0:
                            pTotalD[timeI,k] = pTotalD[timeI-1,k]
                            
                    if pDate > fDate:
                            pTotalD[timeI,k] = pTotalD[timeI-1,k]

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
        while m < nzs*3:
            rpTotal = round(pTotalD[n,m],2)
            outF1.write(str(pRateD[n,m])+"      ")
            outF2.write(str(rpTotal)+"      ")
            m = m+1
        n=n+1
        outF1.write("\n")
        outF2.write("\n")

    
    #Second output file
    ev = ev+1
