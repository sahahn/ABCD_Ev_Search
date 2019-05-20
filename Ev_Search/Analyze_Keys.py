#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May something 20 something

@author: sage
"""

import pickle, os, argparse
import numpy as np
from Population import Population
from Key_Set import Key_Set
from config import config
import matplotlib.pyplot as plt

class Analysis():

    def __init__(self):
        
        self.pops = []
        self.key_sets = []

        self.load_all_populations()
        self.load_all_key_sets()

    def load_all_populations(self):

        for i in range(config['start_key_num'], config['start_key_num']+config['num_jobs']):
            pop_name = config['key_name'] + str(i) + '.pkl'

            with open(pop_name, 'rb') as output:
                pop = pickle.load(output)
                self.pops.append(pop)

    def get_best_score(self):
        return max([pop.Get_Best_Score() for pop in self.pops])

    def get_average_eval_time(self):
        return np.mean([pop.Get_Mean_Eval_Time() for pop in self.pops])

    def load_all_key_sets(self):

        for pop in self.pops:
            for indv in pop.individuals:
                if indv.score != None:
                    self.key_sets.append(indv)

    def Save_Keys_To_File(self):

        with open(config['output_key_loc'], 'w') as f:
            for indv in self.key_sets:
                
                f.write(str(indv.score) + ': ')
                feat_names = indv.get_key_names()
                for feat in feat_names:
                    f.write(feat + ',')
                f.write('\n')

    def Print_Best(self):

        best = self.get_best_score()
        print('Best score: ', str(best))

    def Print_Average_Eval_Time(self):

        avg = self.get_average_eval_time()
        print('Average eval time: ', str(avg))


    def Print_Pop_Level_Info(self):

        print('Population Level Statistics')

        cnt = 0
        for i in range(config['start_key_num'], config['start_key_num']+config['num_jobs']):

            pop = self.pops[cnt]
            cnt += 1
            
            n_gens, score = pop.Get_Num_Gens(), pop.Get_Best_Score()
            print('Pop', i, ': num gens -', n_gens, 'score -', score)

    def Plot_Best_By_Generation(self):

        scores_over_time = [pop.best_over_time for pop in self.pops]

        for scores in scores_over_time:
            plt.plot(list(range(1, len(scores)+1)), scores)

        plt.xlabel('Generation')
        plt.ylabel('Score')
        plt.title('Population Performance')
        plt.savefig(config['output_performance_graph_loc'])

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Give quick analysis commands')

    parser.add_argument('command', type=str, help='save - to save, best - to print the best score over all populations, time - to print the average evaluation time, summary - to print a summary')
    args = parser.parse_args()

    a = Analysis()

    if args.command == 'save':
        a.Save_Keys_To_File()

    elif args.command == 'best':
        a.Print_Best()

    elif args.command == 'time':
        a.Print_Average_Eval_Time()

    elif args.command == 'pop_info':
        a.Print_Pop_Level_Info()

    elif args.command == 'plot':
        a.Plot_Best_By_Generation()
    
    elif args.command == 'summary':
        a.Print_Best()
        a.Print_Average_Eval_Time()
        a.Print_Pop_Level_Info()
        a.Plot_Best_By_Generation()






    






        





