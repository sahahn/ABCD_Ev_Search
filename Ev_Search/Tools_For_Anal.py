import matplotlib.pyplot as plt
from scipy.integrate import simps
import numpy as np
import pandas as pd
import operator

class Item():
    def __init__(self, score, feats):
        self.score = score
        self.feats = feats

def load_file(name):
    
    items = []
    
    with open(name, 'r') as f:
        lines = f.readlines()
        
        for line in lines:
            line = line.split(':')
            score = float(line[0])
            all_features = line[1].split(',')
            feats = []
            
            for feat in all_features:
                feat = feat.strip()
                
                if len(feat) > 0:
                    feats.append(feat)
            
            items.append(Item(score, feats))
    return items


def get_feature_counts(items, lim=999, score_lim=.65, normalize=False):
    
    feat_counts = {}
    out_of = 0
    
    for item in items:
        if len(item.feats) <= lim and item.score >= score_lim:
            out_of+=1
            
            for feat in item.feats:
                
                try:
                    feat_counts[feat] += 1
                except KeyError:
                    feat_counts[feat] = 1
    
    if normalize:
        feat_counts = {ft : feat_counts[ft] / out_of for ft in feat_counts}
    
    return feat_counts, out_of

def get_weighted_feature_counts(items, lim=999, score_lim=.65, normalize=True):
    
    feat_counts = {}
    out_of = 0
    feat_count = 0
    
    for item in items:
        if len(item.feats) <= lim and item.score >= score_lim:
            out_of += item.score
            feat_count += 1
            
            for feat in item.feats:
                
                try:
                    feat_counts[feat] += item.score
                except KeyError:
                    feat_counts[feat] = item.score
    
    if normalize:
        feat_counts = {ft : feat_counts[ft] / out_of for ft in feat_counts}
    
    return feat_counts, feat_count

def proc_labels(labels):
    
    new_labels = []

    for l in labels:

        try:
            i = l.index('_')
            l = l[:i] + ' ' + l[i+1:]
        except:
            pass

        try:
            i = l.index('_')
            l = l[:i] + '\n' + l[i+1:]
        except:
            pass

        new_labels.append(l)
        
    return new_labels
    
def plot_feat_importance(feats, title, top=10, print_scores=False, save=False):
    
    plt.style.use('seaborn-white')
    plt.figure(figsize=(top*3,10))
    
    #Sort by score
    sorted_feats = sorted(feats.items(), key=operator.itemgetter(1), reverse=True)

    inds = [i for i in range(top)]
    labels = [sorted_feats[i][0] for i in inds]
    #labels = proc_labels(labels)
    
    #Plot just top #
    for i in inds:
        plt.bar(i, sorted_feats[i][1])
        
        if print_scores:
            print(labels[i], '-', sorted_feats[i][1], i+1)
        
    if max(feats.items(), key=operator.itemgetter(1))[1] <= 1:
        ylabel = 'Normalized Feature Importance'
    else:
        ylabel = 'Feature Importance'
        
    plt.xticks(inds, labels, fontsize=10)
    plt.title(title, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.xlabel('Feature Name', fontsize=20)
    if save:
        plt.savefig(title + '.png', dpi=100)
    plt.show()

def get_sorted_labels(fc, top):
    
    sorted_feats = sorted(fc.items(), key=operator.itemgetter(1), reverse=True)
    inds = [i for i in range(top)]
    labels = [sorted_feats[i][0] for i in inds]
    
    return labels
            

def load_saved(train_loc, val_loc, i_keys, return_df=False):

    if type(train_loc) == list:
        dfs = [pd.read_csv(t) for t in train_loc]
        train = pd.concat(dfs)

    else:
        train = pd.read_csv(train_loc)
    
    val = pd.read_csv(val_loc)

    if i_keys != None:
        if 'score' not in i_keys:
            i_keys += ['score']

        train = train[i_keys]
        val = val[i_keys]

    if return_df:
        return train, val

    X,y = np.array(train.drop('score', axis=1)), np.array(train.score)
    X_val,y_val = np.array(val.drop('score', axis=1)), np.array(val.score)

    return X,y,X_val,y_val

