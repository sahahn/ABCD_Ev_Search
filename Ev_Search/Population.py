#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 11:38:12 2019

@author: sage
"""

import numpy as np
import copy, random, time

from Key_Set import Key_Set

class Population():
    
    def __init__(self, config, key_names):
        
        self.n_indv = config['num_indv']
        self.new_rand = config['new_rand']
        self.individuals = [Key_Set(config, key_names) for i in range(self.n_indv)]
        self.best_over_time = []
        self.best_over_time_val = []
        self.eval_times = []
        self.config = config
        self.key_names = key_names

    def Check_Rounds(self):

        best_val = np.argmax(self.best_over_time_val) + 1
        rounds_since = len(self.best_over_time_val) - best_val

        return rounds_since

    def Get_Best_Score(self):
        return np.max([indv.score for indv in self.individuals if indv.score != None])

    def Get_Mean_Score_Std(self):
        return np.mean([indv.score_std for indv in self.individuals if indv.score_std != None])

    def Get_Mean_Key_Size(self):
        return np.mean([len(indv.keys) for indv in self.individuals if indv.score != None])

    def Get_Mean_Eval_Time(self):
        return np.mean(self.eval_times)

    def Get_Best_Score_And_Val(self):
        
        best_indv = self.get_best_score_indv()
        return best_indv.score, best_indv.val_score

    def Get_Num_Gens(self):
        return len(self.best_over_time)

    def get_best_score_indv(self):

        ind = np.argmax([indv.score if indv.score != None else -1000 for indv in self.individuals])
        best_indv = self.individuals[ind]

        return best_indv

    def add_best(self, data, val_data):
        
        self.best_over_time.append(self.Get_Best_Score())

        best_indv = self.get_best_score_indv()
        best_indv.Get_Val_Score(data, val_data)
        self.best_over_time_val.append(best_indv.val_score)

    def Evaluate(self, data, val_data, type='None'):
        
        if type == 'None':

            for indv in self.individuals:
                indv.Evaluate(data)
       
        elif type == 'New':

            start_time = time.time()
            
            for indv in self.individuals:
                if indv.score == None:
                    indv.Evaluate(data)

            self.eval_times.append(time.time() - start_time)
      
        elif type == 'Old':
           
            for indv in self.individuals:
                if indv.score != None:
                    indv.Evaluate(data)
   
        self.add_best(data, val_data)

    def Tournament(self):
        
        while len(self.individuals) > self.n_indv // 2:
            self.attempt_remove()
            
    def Fill(self):
        
        while len(self.individuals) + self.new_rand < self.n_indv:
            self.add_mutated()
            
        for i in range(self.new_rand):
            self.individuals.append(Key_Set(self.config, self.key_names))

    def Print_Scores(self):
        '''Print out all indiviudals with scores '''

        for indv in self.individuals:
            if indv.score != None:
                print(indv.score, indv.get_key_names())
                      
    def attempt_remove(self):
        
        r1, r2 = random.sample(range(len(self.individuals)), 2)
        indv1, indv2 = self.individuals[r1], self.individuals[r2]
        
        if indv1.Compare(indv2):
            del self.individuals[r2]
        elif indv2.Compare(indv1):
            del self.individuals[r1]
            
    def add_mutated(self):
       
        r = random.randint(0, (self.n_indv // 2)-1)
        new_copy = copy.deepcopy(self.individuals[r])
        new_copy.Mutate()
        self.individuals.append(new_copy)
            
            
        
    
        
    
