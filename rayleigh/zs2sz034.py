#!/usr/bin/env python2
"""
Filename: zs2sz.py
Purpose: Converts Z-S coefficient and exponent to S-Z via basic algebra
@author: Alex Blackmer
Updated: 07/24/2020
"""

def zs2sz(c,e):
    list = []
    ec = 1/e
    list.append(round(ec,3))
    cc = (1/c)**ec
    list.append(round(cc,3))
    return list

with open ('filerelu034', 'r') as file:
	zsF = file.readlines()
file.close()

nzs = len(zsF)
out0 = zsF[0].rstrip()
outF = open(out0,"w+")
names = []

i = 1
while i < nzs:
    ec = zsF[i].split()
    names.append(str(ec[0]))
    c = float(ec[1])
    e = float(ec[2])
    cec = zs2sz(c,e)
    outF.write(ec[0] + "   ")
    outF.write(str(cec[1]) + "   ")
    outF.write(str(cec[0]) + "\n")
    i=i+1

