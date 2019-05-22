"""
Created on Wed Jan  9 11:39:34 2019

@author: sage
"""

import ML

def Run_Evaluation(keys, config, data):

    keys.sort()
    X,y = data[0][:,keys], data[1]

    if config['binary']:
        score, score_std = ML.evaluate_binary_model(
                                    X, y,
                                    n_splits=config['n_splits'],
                                    n_repeats=config['n_repeats'],
                                    int_cv=config['n_splits'],
                                    class_weight=config['class_weight']
                                    )

    else:
        score, score_std = ML.evaluate_regression_model(
                                    X, y,
                                    n_splits=config['n_splits'],
                                    n_repeats=config['n_repeats'],
                                    model_type=config['model_type'],
                                    int_cv=config['n_splits'],
                                    metric=config['metric'],
                                    target_transform=config['target_transform']
                                    )

    return score, score_std






