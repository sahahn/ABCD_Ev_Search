#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Jan 11 11:25:00 2019
@author: sage
"""

from Population import Population
import argparse, pickle
import pandas as pd
import numpy as np

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
key_names = list(data)
key_names.remove('score')
X = np.array(data.drop(['score'], axis=1))
y = np.array(data['score'])
data = (X,y)

if args.load == 1:
    
    print('Load Pop from', args.path)
    with open(args.path, 'rb') as output:
        pop = pickle.load(output)
    
    pop.Evaluate(data, type='New')
    
elif args.load == 0:
    
    print('Init Population')
    pop = Population(config, key_names)
    pop.Evaluate(data)
   
elif args.load == 2:
    print('Load Pop from', args.path)
    with open(args.path, 'rb') as output:
        pop = pickle.load(output)
    
    pop.Evaluate(data, type='Old')

#Initial Generation
pop.Tournament()
pop.Fill()

#Run rest of Generations
for i in range(1, config['num_gens']):
    print('Starting Gen ', i)
    
    pop.Evaluate(data, type='New')
    pop.Tournament()
    
    print('Current best: ', pop.Get_Best_Score())
    pop.Fill()

    if i % config['save_every'] == 0:
        save_population(pop, args.path)
     
print('Average New Evaluation Time: ', pop.Get_Mean_Eval_Time())
pop.Print_Scores()
save_population(pop, args.path)

