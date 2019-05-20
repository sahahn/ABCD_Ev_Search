"""
Created on Wed Jan  9 11:39:34 2019

@author: sage
"""

import pandas as pd
from config import config
import numpy as np
import ML

def Run_Evaluation(keys):

    keys.sort()
    
    data = pd.read_csv(config['loc'])
    X = np.array(data.drop(['score'], axis=1))[:,keys]
    y = np.array(data['score'])

    if config['binary']:
        score = ML.evaluate_binary_model(
                                    X, y,
                                    n_splits=config['n_splits'],
                                    n_repeats=config['n_repeats'],
                                    int_cv=config['n_splits'],
                                    class_weight=config['class_weight']
                                    )

    else:
        score = ML.evaluate_regression_model(
                                    X, y,
                                    n_splits=config['n_splits'],
                                    n_repeats=config['n_repeats'],
                                    model_type=config['model_type'],
                                    int_cv=config['n_splits'],
                                    metric=config['metric'],
                                    target_transform=config['target_transform']
                                    )

    return score






