#!/usr/bin/python
#
# Copyright (C), Attila Sukosd, BIT BLUEPRINT ApS (as@bitblueprint.com)
#
# The following is a wrapper around airodump-ng to collect information about wireless APs/clients
# http://www.aircrack-ng.org/doku.php?id=airodump-ng
#

import os, time, traceback, subprocess

DEBUG=False

class AirodumpProcessor:
	# Command to laucnh airodump-ng with: 
	CMD="airodump-ng --update 1 --berlin 20 mon0 2>&1"
	# String that resets the terminal
	#REFRESH_STR='\x1b[J\x1b[1;1H\n'
	# String used to identify the list of clients
	#CLIENT_LIST_STR=' BSSID              STATION'
	#AP_LIST_STR=' BSSID              PWR'
	###############################################
	fd = None
	ap_list_on = 0
	client_list_on = 0
	ap_list = {}
	client_list = {}	

	def __init__(self):
		pass

	def start(self):
		#self.fd = os.popen(self.CMD, "r")
		self.fd = subprocess.Popen(['airodump-ng', '--update', '1', '--berlin', '20', 'mon0'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		print "FD:",self.fd
		if DEBUG: self.logger = open("/logs/dump.log", "a")

	def process(self):	
		#if not self.fd:
		#	self.start()
		line = self.fd.stdout.readline()
		print "Line:",line.encode('ascii', errors='ignore'),
		if not line:
			return [None,None]

		line = line.replace("\r", "").replace("\n", "").strip()

		if line.startswith("CH "):
			if DEBUG: self.logger.write("Got start!\n")
			self.client_list_on = 0
			self.ap_list_on = 0
			cl = self.client_list
			self.client_list = {}
			aps = self.ap_list
			self.ap_list = {}
			return [aps, cl]

		if len(line) < 1:
			return [None,None]

		try:
			v = line.replace("(not associated)", "(not_associated)").split()

			if len(v) < 6:
				return [None, None]
 
			if v[1].find(":") < 0:
				return [None, None]

			CLIENT = v[1]
			if not self.client_list.has_key(CLIENT):
				self.client_list[CLIENT] = {}

			self.client_list[CLIENT]["ap"] = CLIENT
			self.client_list[CLIENT]["client"] = v[1]
			self.client_list[CLIENT]["pwr"] = v[2]
			self.client_list[CLIENT]["rate"] = v[3]
			self.client_list[CLIENT]["lost"] = v[4]
			self.client_list[CLIENT]["packets"] = v[5]

		except:
			print "Failed,",line
			traceback.print_exc()

		return [None, None]
	def stop(self):
		self.fd.close()


