#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Jan 11 11:25:00 2019
@author: sage
"""

from Population import Population
import argparse, pickle, os, sys
import pandas as pd
import numpy as np

def check_dr(spot):

    if os.path.isfile(spot):
        sys.exit()

def save_population(pop, location):
    
    with open(location, 'wb') as output:
        pickle.dump(pop, output, pickle.HIGHEST_PROTOCOL)

parser = argparse.ArgumentParser(description='Give load/save commands')

parser.add_argument('path', type=str, help='File Path')
parser.add_argument('load', type=int, help='Load old or not')
parser.add_argument('config', type=str, help='Location/name of the pickled config file to use')
args = parser.parse_args()

with open(args.config, 'rb') as output:
    config = pickle.load(output)

#Read in data only once at start
data = pd.read_csv(config['loc'])
val_data = pd.read_csv(config['val_loc'])

key_names = list(data)
key_names.remove('score')

X, X_val = np.array(data.drop(['score'], axis=1)), np.array(val_data.drop(['score'], axis=1))
y, y_val = np.array(data['score']), np.array(val_data['score'])

data = (X,y)
val_data = (X_val, y_val)

if args.load == 1:
    
    print('Load Pop from', args.path)
    with open(args.path, 'rb') as output:
        pop = pickle.load(output)
    
    pop.Evaluate(data, val_data, type='New')
    
elif args.load == 0:
    
    print('Init Population')
    pop = Population(config, key_names)
    pop.Evaluate(data, val_data)
   
elif args.load == 2:
    print('Load Pop from', args.path)
    with open(args.path, 'rb') as output:
        pop = pickle.load(output)
    
    pop.Evaluate(data, val_data, type='Old')

#Initial Generation
pop.Tournament()
pop.Fill()

#Run rest of Generations
for i in range(1, config['num_gens']):
    print('Starting Gen ', i)
    
    pop.Evaluate(data, val_data, type='New')
    pop.Tournament()
    
    print('Current best: ', pop.Get_Best_Score())
    pop.Fill()

    if i % config['save_every'] == 0:
        save_population(pop, args.path)

    end_spot1 = os.path.join(config['main_dr'], config['kill_all_command'])
    end_spot2 = os.path.join(config['main_dr'], config['kill_jobs_command'])
    check_dr(end_spot1)
    check_dr(end_spot2)
     
print('Average New Evaluation Time: ', pop.Get_Mean_Eval_Time())
pop.Print_Scores()
save_population(pop, args.path)




