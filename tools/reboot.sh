#!/bin/bash

PEERS="192.168.5.12 192.168.5.11 192.168.5.10"

for p in $PEERS; do
	echo "Rebooting $p"
	ssh $p reboot
done;
