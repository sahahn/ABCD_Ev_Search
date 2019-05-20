#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Jan 11 11:25:00 2019
@author: sage
"""

from Population import Population
from config import config
import argparse
import pickle

def save_population(pop, location):
    
    with open(location, 'wb') as output:
        pickle.dump(pop, output, pickle.HIGHEST_PROTOCOL)

parser = argparse.ArgumentParser(description='Give load/save commands')

parser.add_argument('path', type=str, help='File Path')
parser.add_argument('load', type=int, help='Load old or not')
args = parser.parse_args()

if args.load == 1:
    
    print('Load Pop from', args.path)
    with open(args.path, 'rb') as output:
        pop = pickle.load(output)
    
    pop.Evaluate(type='New')
    
elif args.load == 0:
    
    print('Init Population')
    n_indv = config['num_indv']
    new_rand = config['new_rand']
    
    pop = Population(n_indv, new_rand)
    pop.Evaluate()
   
elif args.load == 2:
    print('Load Pop from', args.path)
    with open(args.path, 'rb') as output:
        pop = pickle.load(output)
    
    pop.Evaluate(type='Old')

num_gens = config['num_gens']

#Initial Generation
pop.Tournament()
pop.Fill()

#Run rest of Generations
for i in range(1, num_gens):
    print('Starting Gen ', i)
    
    pop.Evaluate(type='New')
    pop.Tournament()
    
    print('Current best: ', pop.Get_Best_Score())
    pop.Fill()
    save_population(pop, args.path)
     
print('Average New Evaluation Time: ', pop.Get_Mean_Eval_Time())
pop.Print_Scores()
save_population(pop, args.path)

