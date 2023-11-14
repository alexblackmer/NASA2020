#! /usr/bin/python
import numpy as np
from datetime import datetime

"""
Filename: readkmqtnws.py
Purpose: This program reads filekmqtnws, reads the event files,
	  filters for reflectivity CZ , and computes estimated precip
	  from the 4 Z-S relationships. 
Author: Alex Blackmer
Updated: 06/17/2020
"""


#Function computes linear value for lograrithmic input
#It is used on CZ data
def log2lin(log):
	lin = 10.**(log/10.)
	return lin

#Function defines Z-S algorithm used
#Inputs: reflectivity(z) and Z-S coefficient(rel)
#Outputs: snow water equivalent(s)
def z2s(z,c,e):
	s = c*(z**e)
	return s

#opens input file, reads in lines, and then closes it
with open ('filekmqtnws', 'r') as file:
	con = file.readlines()
file.close()

with open ('filerel032', 'r') as file:
	zsF = file.readlines()
file.close()


#parameters
niv = 200	        #num of 10 min intervals greater than 144 in day
npix = 9	        #num of pixels
nzs = len(zsF)		#num of Z-S relationships
nev = len(con)		#num of events

coef = []
exp = []
i=0
while i < nzs:
    zs = zsF[i].split()
    coef.append(float(zs[1])) #z-s rel coefficient
    exp.append(float(zs[2])) #z-s rel exponent
    i=i+1

#loops for each event
i = 0
while i < nev:
    #reads each line and then splits into strings by w-space
    line = con[i]
    split_line = line.split()
    dt = int(split_line[0])
    inf0 = split_line[1]
    out0 = split_line[2]
    with open(inf0,'r') as file:
        con1 = file.read()
        file.close()
    split_con1 = con1.split()

    outF = open(out0,"w+")
    
    t = 0
    while t < dt:
        
        elev0fil = []	#filtered elev0 for CZ lines
        elev1fil = []	#filtered elev1 for CZ lines
        elev2fil = []	#filtered elev2 for CZ lines
        dtArr = []	#datetime array
        elev0filp = []	#parsed elev0 CZ lines
        elev1filp = []	
        elev2filp = []
        elevFlagArr = []
        #reads in each elevation file
        inc = 3 * t
        with open(split_con1[0+inc],'r') as file:
            elev0 = file.readlines()
        file.close()
    
        with open(split_con1[1+inc], 'r') as file:
            elev1 = file.readlines()
        file.close()
    
        with open(split_con1[2+inc], 'r') as file:
            elev2 = file.readlines()
        file.close
        
        j=12	#skips the first 12 lines of non-data
        while  j < len(elev0):
            if elev0[j].find("CZ") > 0:
                    #appends filtered string witghout \n
                    elev0fil.append(elev0[j].rstrip("\n"))
                    elev1fil.append(elev1[j].rstrip("\n"))
                    elev2fil.append(elev2[j].rstrip("\n"))
            j = j+1
    
    	#Initializes 2D array to hold CZ for each pixel at each time interval
        elev0cz = np.empty((len(elev0fil),9), dtype=float)
        elev1cz = np.empty((len(elev1fil),9), dtype=float)
        elev2cz = np.empty((len(elev2fil),9), dtype=float)
        compS = np.empty((len(elev0fil), nzs*3), dtype=float)
        compS.fill(-99.99)
    	
        #Parses each line in filtered elevation file
        #Creates datetime array 
        k = 0
        while k < len(elev0fil):
            elevFlag = 0
            #Parses each CZ line
            elev0filp = elev0fil[k].split()
            elev1filp = elev1fil[k].split()
            elev2filp = elev2fil[k].split()
            #Adds new datetime items to dtArr
            dtArr.append(datetime.strptime("20"+elev0filp[0]+elev0filp[1],"%Y%m%d%H%M%S"))
            #Accesses each parsed CZ pixel value and saves it to new float array
            ii =7
            while ii <= 15:
                elev0cz[k,ii-8] = float(elev0filp[ii])
                elev1cz[k,ii-8] = float(elev1filp[ii])
                elev2cz[k,ii-8] = float(elev2filp[ii])
                ii = ii+1
            #Converts each valid pixel from log to lin
            jj=0
            while jj < 9:
                if elev0cz[k,jj] > -90.00:
                    elev0cz[k,jj] = log2lin(elev0cz[k,jj])
                if elev1cz[k,jj] > -90.00:
                    elev1cz[k,jj] = log2lin(elev1cz[k,jj])
                if elev2cz[k,jj] > -90.00:
                    elev2cz[k,jj] = log2lin(elev2cz[k,jj])
                jj=jj+1
            #Initalizes counters
            count1 = 0
            count2 = 0
            zsum1 = 0
            zsum2 = 0
            #Looks at each middle pixel of first elev scan,
            # if invalid it finds the average of each valid adjacent pixel
            if elev0cz[k,4] < -90.00:
                if elev0cz[k,1] > -90.00:
                    count1 = count1+1
                    zsum1 = zsum1 + elev0cz[k,1]
                if elev0cz[k,3] > -90.00:
                    count1 = count1+1
                    zsum1 = zsum1 + elev0cz[k,3]
                if elev0cz[k,5] > -90.00:
                    count1 = count1+1
                    zsum1 = zsum1 + elev0cz[k,5]
                if elev0cz[k,7] > -90.00:
                    count1 = count1+1
                    zsum1 = zsum1 + elev0cz[k,7]
                if count1 > 0:
                    zave = zsum1/float(count1)
                    elev0cz[k,4] = zave
                    elevFlag = 1

                #If adjacent pixels are invalid, then checks mid pix
                #of 2nd elevation scan
                elif elev1cz[k,4] > -90.00:
                    elevFlag = 2
                    elev0cz[k,4] = elev1cz[k,4]
                #If that is invalid, the valid adjacent pixels are averaged
                else:
                    if elev1cz[k,1] > -90.00:
                        count2 = count2+1
                        zsum2 = zsum2 + elev1cz[k,1]
                    if elev1cz[k,3] > -90.00:
                        count2 = count2+1
                        zsum2 = zsum2 + elev1cz[k,3]
                    if elev1cz[k,5] > -90.00:
                        count2 = count2+1
                        zsum2 = zsum2 + elev1cz[k,5]
                    if elev1cz[k,7] > -90.00:
                        count2 = count2+1
                        zsum2 = zsum2 + elev1cz[k,7]
                    if count2 > 0:
                        zave2 = zsum2/float(count2)
                        elev0cz[k,4] = zave2
                        elevFlag = 3
                    if count2 == 0:
                        elevFlag = -1
    			 #If no pixels were valid, middle pixel val stays -99.99
            elevFlagArr.append(elevFlag)
    		#If the middle pixels of each elevation are valid, each Z-S
    		#relationship is applied.
            b = 0
            while b < nzs:
                if elev0cz[k,4] > -90.00 and elev0cz[k,4] < 1800: 
                    compS[k,b] = z2s(elev0cz[k,4], coef[b], exp[b])
                if elev1cz[k,4] > -90.00 and elev1cz[k,4] < 1800:
                    compS[k,b+4] = z2s(elev1cz[k,4],coef[b], exp[b])
                if elev2cz[k,4] > -90.00 and elev2cz[k,4] < 1800:
                    compS[k,b+8] = z2s(elev2cz[k,4],coef[b], exp[b])
                b = b+1
            k = k+1

        #Writes out to .kmqt file
        year = dtArr[0].strftime('%Y')
        day = dtArr[0].strftime('%j')
        n = 0
        while n <len(elev0cz):
            #Date Formatting
            outF.write(dtArr[n].strftime("%Y"+"  "))
            outF.write(dtArr[n].strftime("%j"+"  "))
            outF.write(dtArr[n].strftime("%H"+"   "))
            outF.write(dtArr[n].strftime("%M"+"   "))
            outF.write(dtArr[n].strftime("%S"))
            m = 0
            #Rounds each value to 2 dec and converts to string
            while m < nzs*3:
                item = round(compS[n,m],2)
                itemS = str(item)
                outF.write("    " + itemS)
                m = m+1
            outF.write('\n')
            n = n+1
        t = t+1
    i = i+1
