#!/usr/bin/python
#
# Copyright (C), Attila Sukosd, BIT BLUEPRINT ApS (as@bitblueprint.com)
#
# The following is a wrapper around airodump-ng to collect information about wireless APs/clients
# http://www.aircrack-ng.org/doku.php?id=airodump-ng
#

import os, time

class AirodumpProcessor:
	# Command to laucnh airodump-ng with: 
	CMD="airodump-ng --update 1 --berlin 10 mon0 2>&1"
	# String that resets the terminal
	REFRESH_STR='\x1b[J\x1b[1;1H\n'
	# String used to identify the list of clients
	CLIENT_LIST_STR=' BSSID              STATION'
	AP_LIST_STR=' BSSID              PWR'
	###############################################
	fd = None
	ap_list_on = 0
	client_list_on = 0
	ap_list = {}
	client_list = {}	

	def __init__(self):
		pass

	def start(self):
		self.fd = os.popen(self.CMD, "r")

	def process(self):	
		line = self.fd.readline()
		if line == self.REFRESH_STR:
			self.client_list_on = 0
			self.ap_list_on = 0
			cl = self.client_list
			self.client_list = {}
			aps = self.ap_list
			self.ap_list = {}
			return [aps, cl]

		elif line.startswith(self.AP_LIST_STR):
			self.ap_list_on = 1
			return [None,None]

		elif line.startswith(self.CLIENT_LIST_STR):
			self.client_list_on = 1
			self.ap_list_on = 0
			return [None,None]	

		line = line.strip()
		if self.client_list_on == 1 and len(line) > 1:
			v = line.replace("(not associated)", "(not_associated)").split()
			CLIENT = v[1]
			if not self.client_list.has_key(CLIENT):
				self.client_list[CLIENT] = {}

			self.client_list[CLIENT]["ap"] = CLIENT
			self.client_list[CLIENT]["client"] = v[1]
			self.client_list[CLIENT]["pwr"] = v[2]
			self.client_list[CLIENT]["rate"] = v[3]
			self.client_list[CLIENT]["lost"] = v[4]
			self.client_list[CLIENT]["packets"] = v[5]

		if self.ap_list_on == 1 and len(line) > 1:
			v = line.split()
			AP = v[0]
			if not self.ap_list.has_key(AP):
				self.ap_list[AP] = {}
			
			self.ap_list[AP]["ap"] = AP
			self.ap_list[AP]["pwr"] = v[1]
			self.ap_list[AP]["rxq"] = v[2]
			self.ap_list[AP]["beacons"] = v[3]
			self.ap_list[AP]["data"] = v[4]
			self.ap_list[AP]["pps"] = v[5]
			self.ap_list[AP]["ch"] = v[6]
			self.ap_list[AP]["mb"] = v[7]
			self.ap_list[AP]["enc"] = v[8]
			if len(v) == 8:
				self.ap_list[AP]["essid"] = v[9]
			elif len(v) == 9:
				self.ap_list[AP]["cipher"] = v[9]
				self.ap_list[AP]["essid"] = v[10]
			elif len(v) == 10:
				self.ap_list[AP]["cipher"] = v[9]
				self.ap_list[AP]["auth"] = v[10]
				self.ap_list[AP]["essid"] = v[11]

		return [None, None]
	def stop(self):
		self.fd.close()


