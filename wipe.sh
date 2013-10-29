#!/bin/bash

PEERS="192.168.1.10 192.168.1.11 192.168.1.12"

for p in $PEERS; do
	echo "Wiping logs for $p"
	ssh $p rm -rf /logs/*
done;
