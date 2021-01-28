###########################################################################################
#
# QcatFilter.py
#
# This is sample code for Qualcomm automated parsing 
# Automated extraction 4G/5G physical throughput value from Qualcomm logs (*.isf/*.hdf) using QCAT application
# Plot its values on graph and save as figure
# More features can be added in this manner and it will be updated
#
# How to use it:
# Step.1 copy and paste onto log folder
# Step.2 run this python file (Python installation pre-required)
#
# Created by Jonggil Nam
# https://www.linkedin.com/in/jonggil-nam-6099a162/ | https://github.com/woodstone10 | woodstone10@gmail.com | +82-10-8709-6299 
###########################################################################################

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import re
from win32com.client import Dispatch


LOG_PACKETS = [0xB97F,0xB8DD,0xB193,0x1FE8]
def qcat_filter():
	filter = qcatApp.PacketFilter
	filter.SetAll(False) 
	for i in range(len(LOG_PACKETS)):
		filter.Set(LOG_PACKETS[i], True) 
	filter = qcatApp.DebugMsgFilter
	filter.Commit() 

QSH_TIME, NR_PHY_TPUT, LTE_PHY_TPUT = [],[],[]
def process_log(packet):
	if packet.Type == 0x1FE8:
		if "5gPHY" in packet.Text:
			v = int(''.join(filter(str.isdigit, re.findall('PHY\|\s+\d+', packet.Text)[0])))	
			print(v)
			NR_PHY_TPUT.append(v/1000)
			f.write(packet.Text)
		elif "4gPHY" in packet.Text:
			v = int(''.join(filter(str.isdigit, re.findall('PHY\|\s+\d+', packet.Text)[0])))			
			LTE_PHY_TPUT.append(v/1000)
			f.write(packet.Text)
	#elif packet.Type in LOG_PACKETS:
		#f.write(packet.Text)

qcatApp = Dispatch('QCAT6.Application')
qcatApp.Visible = 0

f = open("QcatFilter.txt", "w")
for files in ("*.isf","*.hdf"): #parsing all QXDM logs in folder
	for fin in glob.glob(files):
		path = os.path.dirname(os.path.realpath(__file__))+"/"+fin
		print(path)
		qcatApp.OpenLog(path)
		qcat_filter()
		packet = qcatApp.FirstPacket
		process_log(packet)
		while packet.Next():	
			process_log(packet)
			
f.close()

if len(LTE_PHY_TPUT)>0 or len(NR_PHY_TPUT)>0:
	fig=plt.figure(figsize=(13,9))
	plt.subplot(3,1,1)
	if len(LTE_PHY_TPUT)>0: plt.plot(LTE_PHY_TPUT[::1], label='4gPHY Tput', color='blue', linestyle='-', alpha=0.6)
	if len(NR_PHY_TPUT)>0: plt.plot(NR_PHY_TPUT[::1], label='5gPHY Tput', color='red', linestyle='-', alpha=0.6)
	plt.grid()
	plt.ylabel('Tput [Mbps]')
	plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize="x-small", edgecolor="white")
	plt.tight_layout()	
	fig.savefig('Tput.png')

#plt.show()
	
