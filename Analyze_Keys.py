#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May something 20 something

@author: sage
"""

import pickle, os, argparse, sys
sys.path.append(os.getcwd() + '/Ev_Search/')

import numpy as np
import matplotlib.pyplot as plt
from Population import Population

class Analysis():

    def __init__(self, config):

        self.config = config
        
        self.pops = []
        self.key_sets = []

        self.load_all_populations()
        self.load_all_key_sets()

    def load_all_populations(self):
        config = self.config

        for i in range(config['start_key_num'], config['start_key_num']+config['num_jobs']):
            pop_name = os.path.join(config['ev_search_dr'], config['key_dr'], config['key_name'] + str(i) + '.pkl')
 
            with open(pop_name, 'rb') as output:
                pop = pickle.load(output)
                self.pops.append(pop)

    def load_all_key_sets(self):

        for pop in self.pops:
            for indv in pop.individuals:
                if indv.score != None:
                    self.key_sets.append(indv)

    def Save_Keys_To_File(self):

        with open(self.config['output_key_loc'], 'w') as f:
            for indv in self.key_sets:
                
                f.write(str(indv.score) + ': ')
                feat_names = indv.get_key_names()
                for feat in feat_names:
                    f.write(feat + ',')
                f.write('\n')

    
    def Print_Mean_Eval_Time(self):

        mean = np.mean([pop.Get_Mean_Eval_Time() for pop in self.pops])
        print('Mean Eval Time: ', str(mean))

    def Print_Best(self):

        best = np.max([pop.Get_Best_Score() for pop in self.pops])
        print('Best Score: ', str(best))

    def Print_Mean_Key_Size(self):

        mean = np.mean([pop.Get_Mean_Key_Size() for pop in self.pops])
        print('Mean Key Size: ', str(mean))

    def Print_Mean_Score_Std(self):
        
        mean = np.mean([pop.Get_Mean_Score_Std() for pop in self.pops])
        print('Mean Score Std: ', str(mean))

    def Print_Pop_Level_Info(self):
        config = self.config

        print('Population Level Statistics')

        cnt = 0
        for i in range(config['start_key_num'], config['start_key_num']+config['num_jobs']):

            pop = self.pops[cnt]
            cnt += 1

            score, val_score = Get_Best_Score_And_Val()
            n_gens, size, score_std = pop.Get_Num_Gens(),  pop.Get_Mean_Key_Size(), pop.Get_Mean_Score_Std()
            print('Pop -', i, 'Num Gens: ', n_gens, 'Score:', score, 'Mean Size:', size, 'Mean Score Std: ', score_std)

    def Plot_Best_By_Generation(self):

        scores_over_time = [pop.best_over_time for pop in self.pops]

        for scores in scores_over_time:
            plt.plot(list(range(1, len(scores)+1)), scores)

        plt.xlabel('Generation')
        plt.ylabel('Score')
        plt.title('Population Performance')
        plt.savefig(self.config['output_performance_graph_loc'], dpi=100)

    def Plot_Best_Val_Test(self):

        ind = np.argmax([pop.Get_Best_Score() for pop in self.pops])
        best_pop = self.pops[ind]
        scores, val_scores = best_pop.best_over_time, best_pop.best_over_time_val
        
        plt.plot(list(range(1, len(scores)+1)), scores, label='Scores')
        plt.plot(list(range(1, len(val_scores)+1)), val_scores, label='Val Scores')

        plt.xlabel('Generation')
        plt.ylabel('Score')
        plt.title('Performance vs. Val')
        plt.legend()
        plt.savefig(self.config['output_val_graph_loc'], dpi=100)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Provides quick analysis tools')
    parser.add_argument('config', type=str, help='Location/name of the pickled config file to use (can add .pkl automatically) + assumes to be in Configs folder')
    parser.add_argument('command', type=str, help='save - to save, best - to print the best score over all populations, time - to print the average evaluation time, summary - to print a summary')
    args = parser.parse_args()

    cwd = os.getcwd()
    CONFIG_LOC = os.path.join(cwd, 'Configs', args.config)

    if not os.path.exists(CONFIG_LOC):
        CONFIG_LOC += '.pkl'

    with open(CONFIG_LOC, 'rb') as output:
        config = pickle.load(output)

    os.makedirs(config['stats_loc'], exist_ok=True)

    a = Analysis(config)

    if args.command == 'save':
        a.Save_Keys_To_File()

    elif args.command == 'best':
        a.Print_Best()

    elif args.command == 'time':
        a.Print_Mean_Eval_Time()

    elif args.command == 'key_size':
        a.Print_Mean_Key_Size()

    elif args.command == 'score_std':
        a.Print_Mean_Score_Std()

    elif args.command == 'pop_info':
        a.Print_Pop_Level_Info()

    elif args.command == 'plot':
        a.Plot_Best_By_Generation()
    
    elif args.command == 'summary':
        a.Print_Mean_Eval_Time()
        a.Print_Best()
        a.Print_Mean_Key_Size()
        a.Print_Mean_Score_Std()
        a.Print_Pop_Level_Info()
        a.Plot_Best_By_Generation()
        a.Plot_Best_Val_Test()






    






        





