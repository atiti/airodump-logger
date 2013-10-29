#!/bin/bash

PEERS="192.168.5.10 192.168.5.11 192.168.5.12"

for p in $PEERS; do
	echo "Wiping logs for $p"
	ssh $p rm -rf /logs/*
done;
