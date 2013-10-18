#!/usr/bin/python
#
# Copyright (C), Attila Sukosd, BIT BLUEPRINT ApS (as@bitblueprint.com)
# 
# The following is a wrapper around airodump-ng to collect information about wireless APs/clients
# http://www.aircrack-ng.org/doku.php?id=airodump-ng
#


import os, time
import logging
import airodump

def log_client_appeared(k, l):
	if l:
		l.info("%s", "Appeared - "+k["client"])

def log_client_disappeared(k, l):
	if l:
		l.info("%s", "Disappeared - "+k["client"])

def log_update(clients, l):
	if l:
		for k in clients.keys():
			v = clients[k]	
			l.info("%s", v["client"]+" - "+v["pwr"])


# Setup logger(s)
update_logger = logging.getLogger('update')
hdlr = logging.FileHandler('updates.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
hdlr.setFormatter(formatter)
update_logger.addHandler(hdlr)
update_logger.setLevel(logging.INFO)

changes_logger = logging.getLogger('changes')
hdlr2 = logging.FileHandler('changes.log')
hdlr2.setFormatter(formatter)
changes_logger.addHandler(hdlr2)
changes_logger.setLevel(logging.INFO)

# Start the airodump-ng processor
ad = airodump.AirodumpProcessor()
ad.start()

prev_clients = {}

while 1:
	[aps, clients] = ad.process()
	if clients:
		# Trigger logging for disappearing clients
		for k in prev_clients.keys():
			if not clients.has_key(k):
				log_client_disappeared(prev_clients[k], changes_logger)

		# Trigger logging for appearing clients
		for k in clients.keys():
			if not prev_clients.has_key(k):
				log_client_appeared(clients[k], changes_logger)	

		# Trigger logging for updates
		log_update(clients, update_logger)

		# Save the current state
		prev_clients = clients


# Stop the dumping
ad.stop()

