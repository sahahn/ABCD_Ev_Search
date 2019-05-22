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
parser.add_argument('config', type=str, help='Location/name of the pickled config file to use (can add .pkl automatically) + assumes to be in Configs folder')
args = parser.parse_args()

cwd = os.getcwd()
CONFIG_LOC = os.path.join(cwd, 'Configs', args.config)

if not os.path.exists(CONFIG_LOC):
    CONFIG_LOC += '.pkl'

with open(CONFIG_LOC, 'rb') as output:
    config = pickle.load(output)

print('Using config', config['name'], 'with config file at', CONFIG_LOC)

COUNTER = {}
TIMER = {}

def check_directory():
    
    files = os.listdir()

    if config['kill_tasks_command'] in files:
        os.remove(config['kill_command'])
        sys.exit()

    if config['kill_jobs_command'] in files or config['kill_all_command'] in files:
        os.remove(config['kill_jobs_command'])
        os.remove(config['loc'])
        sys.exit()

    if config['single_jobs']:

        valid_files = []
        files = [file for file in files if config['key_name'] in file]
        valid = [str(i) for i in range(config['start_key_num'], config['start_key_num']+config['num_jobs'])]
    
        for file in files:
            name = file.split('.')[0].replace(config['key_name'], '')
            
            if name in valid:
                valid_files.append(file)        

        return valid_files

    else:
        
        files = [file for file in files if config['key_name'] + '_Output' in file]
        return files

def read_file(loc):

    with open(loc, 'r') as f:
        lines = f.readlines()
    return lines

def write_file(loc, lines):

    with open(loc, 'w') as f:
        for line in lines:
            f.write(line)

def change_lines(lines, replacements):

    for i in range(len(lines)):
        for r in replacements:
            if r in lines[i]:
                lines[i] = lines[i].replace(r, str(replacements[r]))
    
    return lines

def change_temp_script(name, load):
    
    pkl_loc = os.path.join(config['key_dr'], config['key_name'] + name)

    replacements = {'MAX_RUN_TIME': config['max_run_time'],
                    'EV_SEARCH_LOCATION': config['ev_search_dr'],
                    'REPLACE': pkl_loc,
                    'JOBNAME': config['key_name'] + name,
                    'LOAD': load,
                    'CONFIG_LOC': CONFIG_LOC}

    lines = read_file(config['template_name'])
    lines = change_lines(lines, replacements)
    write_file(config['temp_name'], lines)

def change_temp_scripts(load):

    pkl_loc = os.path.join(config['key_dr'], config['key_name'])

    replacements = {'MAX_RUN_TIME': config['max_run_time'],
                    'REPLACE': pkl_loc,
                    'EV_SEARCH_LOCATION': config['ev_search_dr'],
                    'JOBNAME': config['key_name'] + '_Output',
                    'SUBJOB_NAME': config['subjob_name'],
                    'NUM_JOBS': config['num_jobs'],
                    'START_NUM': config['start_key_num'],
                    'LOAD': load,
                    'CONFIG_LOC': CONFIG_LOC}

    #Master
    lines = read_file(config['master_template'])
    lines = change_lines(lines, replacements)
    write_file(config['master_name'], lines)

    #Subjob
    lines = read_file(config['subjob_template'])
    lines = change_lines(lines, replacements)
    write_file(config['subjob_name'], lines)
    
    #Change permissions of subjob
    os.system('chmod u+x ' + config['subjob_name'])

def run_job(temp_name):
    os.system('qsub ' + temp_name)

def init_jobs(arg):

    if config['single_jobs']:
    
        for i in range(config['start_key_num'], config['start_key_num']+config['num_jobs']):
            change_temp_script(str(i), arg)
            run_job(config['temp_name'])
            
            COUNTER[str(i)] = 1
            TIMER[str(i)] = time.time()

    else:

        change_temp_scripts(arg)
        run_job(config['master_name'])

        COUNTER['1'] = 1
        TIMER['1'] = time.time()

def check_counter():
    '''Returns true if jobs need to be run more'''

    if config['single_jobs']:
    
        #Check if any jobs are not done
        for i in range(config['start_key_num'], config['start_key_num']+config['num_jobs']):
            if COUNTER[str(i)] < config['num_search_gens']:
                return True
        return False

    else:

        if COUNTER['1'] < config['num_search_gens']:
            return True
        return False



def proc_new_files(files):

    if config['single_jobs']:
    
        for file in files:
            name = file.split('.')[0].replace(config['key_name'], '')
            
            if COUNTER[name] < config['num_search_gens']:
                change_temp_script(name, '1')
                run_job(config['temp_name'])
            
                COUNTER[name] += 1
                TIMER[name] = time.time()
                
                os.remove(file)

    else:
        
        file = files[0]
        if COUNTER['1'] < config['num_search_gens']:
            change_temp_scripts('1')
            run_job(config['master_name'])

            COUNTER['1'] += 1
            TIMER['1'] = time.time()

        
def save_progress():
    with open(config['progress_name'], 'w') as f:
        for c in COUNTER:
            f.write(str(c) + ' ' + str(COUNTER[c]) + '\n')
            
def restart_job(name):
    
    #If starting from scratch and counter still == 1
    if config['preloaded'] == False and COUNTER[name] == 1:
        print('restart job ', name, 'with new')

        change_temp_script(name, '0')
        COUNTER[name] = 1
    
    #Otherwise, just try again
    else:
        print('restart job w/ load', name)
        
        change_temp_script(name, '1')
        COUNTER[name] += 1
    
    run_job(config['temp_name'])
    TIMER[name] = time.time()

def restart_jobs():

    #If starting from scratch and counter still == 1
    if config['preloaded'] == False and COUNTER['1'] == 1:
        print('restart jobs with new')

        change_temp_scripts('0')
        COUNTER['1'] = 1
        
    #Otherwise, just try again
    else:
        print('restart jobs with load')

        change_temp_scripts('1')
        COUNTER['1'] += 1

    run_job(config['master_name'])
    TIMER['1'] = time.time()
            
def check_progress():
    
    current_time = time.time()

    if config['single_jobs']:
        for i in range(config['start_key_num'], config['start_key_num']+config['num_jobs']):
            i = str(i)
            
            if COUNTER[i] < config['num_search_gens']:
                print('check progress job ', i, current_time - TIMER[i])
                
                #If job hasnt been updated in enough time, restart it-
                if current_time - TIMER[i] > config['restart_lim'] * 3600:
                    restart_job(i)

    else:
        if COUNTER['1'] < config['num_search_gens']:
            print('check progress on batched jobs ', current_time - TIMER['1'])

            if current_time - TIMER['1'] > config['restart_lim'] * 3600:
                restart_jobs()

#Ensure key directory exists
key_dr = os.path.join(config['ev_search_dr'], config['key_dr'])
os.makedirs(key_dr, exist_ok=True)

#If the data file does not exist or if an override is specified, create data file
if not os.path.isfile(config['loc']) or config['create_new_data']:
    
    print('creating data file')    
    process_new_dataset(config)

init_jobs(str(int(config['preloaded'])))

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





