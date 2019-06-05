#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Jan 11 11:25:00 2019
@author: sage
"""

from Population import Population
import Tools_For_Anal as A
import argparse, pickle, os, sys
import pandas as pd
import numpy as np


def check_dr(spot):

    if os.path.isfile(spot):
        sys.exit()

def save_population(pop, location):
    
    with open(location, 'wb') as output:
        pickle.dump(pop, output, pickle.HIGHEST_PROTOCOL)

def add_best(pop, loc):

    best = pop.get_best_score_indv()

    with open(loc, 'a') as f:
  
        f.write(str(best.score) + ': ')
        feat_names = best.get_key_names()
        for feat in feat_names:
            f.write(feat + ',')
        f.write('\n')

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

#If set to in the config, keep only a subset of all avaliable features for the search
if config['limit_features_from'] != None:
    if os.path.isfile(config['limit_features_from']):
        
        items = A.load_file(config['limit_features_from'])
        fc, feat_count = A.get_weighted_feature_counts(items, score_lim=config['feature_score_lim'])
        
        if config['keep_top_x'] < 1:
            n = int(len(data) * config['keep_top_x'])
        else:
            n = int(config['keep_top_x'])
        
        top_feats = A.get_sorted_labels(fc, n) + ['score']
        data, val_data = data[top_feats], val_data[top_feats]

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
    
    if config['early_stop_rounds'] != None:
        if pop.Check_Rounds() < config['early_stop_rounds']:
            pop.Evaluate(data, val_data, type='New')
        else:
            sys.exit()
    else:
        pop.Evaluate(data, val_data, type='New')
    
elif args.load == 0:
    
    print('Init Population', args.path)
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

    if config['early_stop_rounds'] != None:
        rounds_since = pop.Check_Rounds()
        
        if rounds_since == 0:
            save_population(pop, args.path)
        if rounds_since < config['early_stop_rounds']:
            pop.Evaluate(data, val_data, type='New')
        else:
            if config['one_run_mode']:
                add_best(pop, config['output_best_loc'])
            sys.exit()
    else:
        pop.Evaluate(data, val_data, type='New')

    pop.Tournament()
    
    print('Current best: ', pop.Get_Best_Score_And_Val())
    pop.Fill()

    if i % config['save_every'] == 0 and config['early_stop_rounds'] == None:
        save_population(pop, args.path)

    end_spot1 = os.path.join(config['main_dr'], config['kill_all_command'])
    end_spot2 = os.path.join(config['main_dr'], config['kill_jobs_command'])
    check_dr(end_spot1)
    check_dr(end_spot2)
     
print('Average New Evaluation Time: ', pop.Get_Mean_Eval_Time())
pop.Print_Scores()
save_population(pop, args.path)

if config['one_run_mode']:
    add_best(pop, config['output_best_loc'])




