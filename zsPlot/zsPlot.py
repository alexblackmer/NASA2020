#! /usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

"""
Filename: zsPlot.py
Purpose: This program plots the logarithmic radar reflectivity (dBz) against 
         estimated liquid water equivalence of 12 Z-S relationships.
Author: Alex Blackmer
Updated: 07/19/2020
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


with open ('filerel', 'r') as file:
	zsF = file.readlines()
file.close()

zsD = np.zeros([len(zsF),2])
zsDName = []
i = 0
while i < len(zsF):
    data = zsF[i].split()
    zsDName.append(data[0])
    zsD[i,0] = float(data[1])
    zsD[i,1] = float(data[2])
    i = i+1

#Creates stepped Z values from 0-40
zD = np.linspace(0,40,400)
#Converts from log to lin
zLinD = []
for i in zD:
    zLinD.append(log2lin(i))

sD = np.zeros([len(zsF),len(zLinD)])

i = 0
while i < len(zsD):
    j = 0
    while j < len(zLinD):
        sD[i,j] = z2s(zLinD[j],zsD[i,0],zsD[i,1])
        j=j+1
    i=i+1
    
i = 0
while i < 3:
    if i == 0:
        j=0
        while j < 4:
            plt.plot(zD, sD[j,:],label = zsDName[j])
            j=j+1

        plt.ylabel('Estimated SWE (mm/hr)')
        plt.xlabel('Reflectivity (dB)')
        plt.legend(loc = 2)
        plt.savefig("figZSRelBook.png")
        plt.close()
        
    if i == 1:
        j=4
        while j < 9:
            plt.plot(zD, sD[j,:],label = zsDName[j])
            j=j+1

        plt.ylabel('Estimated SWE (mm/hr)')
        plt.xlabel('Reflectivity (dB)')
        plt.legend(loc = 2)
        plt.savefig("figZSRelGeog.png")
        plt.close()
        
    if i == 2:
        j=9
        while j < 12:
            plt.plot(zD, sD[j,:],label = zsDName[j])
            j=j+1

        plt.ylabel('Estimated SWE (mm/hr)')
        plt.xlabel('Reflectivity (dB)')
        plt.legend(loc = 2)
        plt.savefig("figZSRelRad.png")
        plt.close()
    i=i+1    