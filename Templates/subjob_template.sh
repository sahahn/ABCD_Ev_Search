#!/bin/bash
export PATH="/users/s/a/sahahn/scratch/anaconda3/bin:$PATH"

cd EV_SEARCH_LOCATION
python Search.py REPLACE$(($PBS_TASKNUM-2+START_NUM)).pkl LOAD "CONFIG_LOC"