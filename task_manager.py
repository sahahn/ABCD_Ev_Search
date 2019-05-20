#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 13:30:35 2019

@author: sage
"""

import os, time, sys, argparse, pickle
from Ev_Search.loaders import process_new_dataset

#Load in the config file with args as a global variable
parser = argparse.ArgumentParser(description='Main task manager for the ABCD Evolutionary search')
parser.add_argument('config', type=str, help='Location/name of the pickled config file to use (can add .pkl automatically)')
args = parser.parse_args()

cwd = os.getcwd()
CONFIG_LOC = os.path.join(cwd, args.config)

if not os.path.exists(CONFIG_LOC):
    CONFIG_LOC += '.pkl'

with open(CONFIG_LOC, 'rb') as output:
    config = pickle.load(output)

print('Using config', config['name'], 'with config file at', CONFIG_LOC)

COUNTER = {}
TIMER = {}

def check_directory():
    
    files = os.listdir()

    if config['kill_command'] in files:
        os.remove(config['kill_command'])
        sys.exit()

    files = [file for file in files if config['key_name'] in file]
    
    valid = [str(i) for i in range(config['start_key_num'], config['start_key_num']+config['num_jobs'])]
    valid_files = []
    
    for file in files:
        name = file.split('.')[0].replace(config['key_name'], '')
        
        if name in valid:
            valid_files.append(file)        

    return valid_files

def change_temp_script(name, load):
    
    with open(config['template_name'], 'r') as f:
        lines = f.readlines()
        
    for i in range(len(lines)):
        
        if 'MAX_RUN_TIME' in lines[i]:
            lines[i] = lines[i].replace('MAX_RUN_TIME', str(config['max_run_time']))
        if 'EV_SEARCH_LOCATION' in lines[i]:
            lines[i] = lines[i].replace('EV_SEARCH_LOCATION', config['ev_search_dr'])
        if 'REPLACE' in lines[i]:
            pkl_loc = os.path.join(config['key_dr'], config['key_name'] + name)
            lines[i] = lines[i].replace('REPLACE', pkl_loc)
        if 'LOAD' in lines[i]:
            lines[i] = lines[i].replace('LOAD', load)
        if 'CONFIG_LOC' in lines[i]:
            lines[i] = lines[i].replace('CONFIG_LOC', load)
            
            
    with open('temp.script', 'w') as f:
        for line in lines:
            f.write(line)
            
def run_job():
    os.system('qsub temp.script')

def init_jobs(arg):
    
    for i in range(config['start_key_num'], config['start_key_num']+config['num_jobs']):
        change_temp_script(str(i), arg)
        run_job()
        
        COUNTER[str(i)] = 1
        TIMER[str(i)] = time.time()
        
def check_counter():
    '''Returns true if jobs need to be run more'''
    
    #Check if any jobs are not done
    for i in range(config['start_key_num'], config['start_key_num']+config['num_jobs']):
        if COUNTER[str(i)] < config['num_search_gens']:
            return True
        
    return False

def proc_new_files(files):
    
    for file in files:
        name = file.split('.')[0].replace(config['key_name'], '')
        
        if COUNTER[name] < config['num_search_gens']:
            change_temp_script(name, '1')
            run_job()
        
            COUNTER[name] += 1
            TIMER[name] = time.time()
            
            os.remove(file)
        
def save_progress():
    with open('progress', 'w') as f:
        for c in COUNTER:
            f.write(str(c) + ' ' + str(COUNTER[c]) + '\n')
            
def restart_job(name):
    
    #If starting from scratch and counter still == 1
    if config['preloaded'] == False and COUNTER[name] == 1 and config['continue'] == False:
        print('restart job ', name, 'with new')

        change_temp_script(name, '0')
        run_job()
        
        COUNTER[name] = 1
        TIMER[name] = time.time()
    
    #Otherwise, just try again
    else:
        print('restart job w/ load', name)
        change_temp_script(name, '1')
        run_job()
    
        COUNTER[name] += 1
        TIMER[name] = time.time()
            
def check_progress():
    
    current_time = time.time()
    
    for i in range(config['start_key_num'], config['start_key_num']+config['num_jobs']):
        i = str(i)
        
        if COUNTER[i] < config['num_search_gens']:
            print('check progress job ', i, current_time - TIMER[i])
            
            #If job hasnt been updated in enough time, restart it-
            if current_time - TIMER[i] > config['restart_lim'] * 3600:
                restart_job(i)

#Ensure key directory exists
key_dr = os.path.join(config['ev_search_dr'], config['key_dr'])
os.makedirs(key_dr, exist_ok=True)

#If the data file does not exist or if an override is specified, create data file
if not os.path.isfile(config['loc']) or config['create_new_data']:
    
    print('creating data file')    
    process_new_dataset(config)

if config['continue']:
    for i in range(config['start_key_num'], config['start_key_num']+config['num_jobs']):
        COUNTER[str(i)] = 0
        TIMER[str(i)] = time.time()

elif config['preloaded']:
    init_jobs('1')

else:
    init_jobs('0')

sys.stdout.flush()
save_progress()
  
#MAIN LOOP
while check_counter():
    
    files = check_directory()
    if len(files) > 0:
        
        proc_new_files(files)
        save_progress()

    print('check progress')        
    check_progress()
        
    time.sleep(config['check_every'])
    sys.stdout.flush()        
