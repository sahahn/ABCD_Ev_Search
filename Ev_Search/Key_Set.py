#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 11:25:41 2019

@author: sage
"""

from Evaluate import Run_Evaluation
from loaders import load_key_names
import random

class Key_Set():
    
    def __init__(self, config):

        self.config = config
        self.key_names = load_key_names(self.config['loc'])
        self.n_options = len(self.key_names)
        self.keys = random.sample(range(self.n_options), self.config['start_num'] + random.randint(0,2))
        self.score = None
        self.score_std = None
        
    def Evaluate(self):

        self.score, self.score_std = Run_Evaluation(self.keys, self.config)
        
    def Compare(self, other):

        if set(self.keys) == set(other.keys):
            return True
        
        if self.score > other.score and len(self.keys) <= len(other.keys):
            return True
        
        return False
        
    def Mutate(self):
        
        r = random.random()
        
        if r < self.config['change_chance']:
            self.change_key()
        else:
            if len(self.keys) > self.config['start_num']:
                r = random.random()
                
                if r < self.config['change_chance']:
                    self.remove_key()
                else:
                    self.add_key()
            else:
                self.add_key()

        self.score = None
            
    def change_key(self):
        
        to_change = random.randint(0, len(self.keys)-1)
        new = random.randint(0, self.n_options-1)
        
        while new in self.keys:
            new = random.randint(0, self.n_options-1)
            
        self.keys[to_change] = new
        
    def add_key(self):
        
        new = random.randint(0, self.n_options-1)
        
        while new in self.keys:
            new = random.randint(0, self.n_options-1)
            
        self.keys.append(new)

    def remove_key(self):
        
        to_del = random.randint(0, len(self.keys)-1) 
        del self.keys[to_del]      
  
    def get_key_names(self):
        
        return sorted([self.key_names[i] for i in self.keys])
        
        
            
        
        
        
        
        
        
        
        
        
        
