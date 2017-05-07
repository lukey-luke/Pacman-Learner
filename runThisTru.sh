#!/usr/bin/env bash

#you may need to 'chmod +x runThisTru.sh' to run this file


for i in `seq 1 100`; do
    python pacman.py -p ANNAgent -q
done
