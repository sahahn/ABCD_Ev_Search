import pandas as pd 
import numpy as np
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split

def load_subject_ids(testID_loc):

    with open(testID_loc, 'r') as f:
        lines = f.readlines()
    
    test_set = set()

    for line in lines:
        test_set.add(line.rstrip())

    return test_set


def save_subject_ids(data, loc):

    subjects = list(data.subject)

    with open(loc, 'w') as f:
        for s in subjects:
            f.write(s + '\n')


def common_corrections(in_scores):
    ''' Preform some common corrections on the input scores csv after loading,
        Specifically: column renaming and checking for duplicate subjects'''

    col_names = list(in_scores)

    if 'subject' not in col_names:
        print(col_names[0], 'renamed to: ', 'subject')
        in_scores = in_scores.rename({col_names[0]: 'subject'}, axis=1)

    in_scores = in_scores.drop_duplicates(subset = 'subject')

    if 'score' not in col_names:
        print(col_names[1], 'renamed to: ', 'score')
        in_scores = in_scores.rename({col_names[1]: 'score'}, axis=1)

    return in_scores

def filter_data(data, i_keys, d_keys):
    
    if d_keys != None:

        to_remove = set()
        col_names = list(data)

        for name in col_names:
            for key in d_keys:
                if key in name:
                    to_remove.add(name)

        data = data.drop(list(to_remove), axis=1)
        
    if i_keys != None:
        
        to_remove = set()
        col_names = list(data)
        
        for name in col_names:
            flag = False
            
            for key in i_keys:
                if key in name:
                    flag = True
            
            if not flag:
                to_remove.add(name)
                
        data = data.drop(list(to_remove), axis=1)
            
    return data


def filter_by_subject_set(df, s):
    '''Returns two dataframes, the first with subjects not in the set,
       and second those with subjects in the set'''

    return df[~df.subject.isin(s)], df[df.subject.isin(s)]


def preform_split(data, loc, split_sz, random_state):
    '''Preforms either a train/test split or train/val split based on either a saved file with ids
       or computing a new split.'''

    if loc != None:
        print('Reading ids from saved loc: ', loc)

        test_set = load_subject_ids(loc)
        train_data, test_data = filter_by_subject_set(data, test_set)

    else:
        print('Creating set of size: ', split_sz)
        train_data, test_data = train_test_split(data, test_size=split_sz, random_state=random_state)

    return train_data, test_data

def process_new_dataset(config):
    '''Load and process a new dataset with various corrections and parameters'''
    
    print('Reading ids + scores from: ', config['scores_loc'])
    scores = common_corrections(pd.read_csv(config['scores_loc']))
    
    print('Reading underlying dataset from: ', config['raw_data_loc'])
    data = pd.read_csv(config['raw_data_loc'])

    print('Filtering dataset with -')
    print('Inclusion Keys: ', config['i_keys'])
    print('Drop Keys: ', config['d_keys'])
    data = filter_data(data, config['i_keys'], config['d_keys'])

    relevant_data = pd.merge(data,scores)

    print('--Splitting Test Set--')
    train_data, test_data = preform_split(relevant_data, config['test_id_loc'], config['test_sz'], config['random_split_state'])

    print('--Splitting Validation Set--')
    train_data, val_data = preform_split(train_data, config['val_id_loc'], config['val_sz'], config['random_split_state'])

    if config['save_ids']:

        save_subject_ids(train_data, config['proc_data_path'] + '_train_ids.txt')
        save_subject_ids(test_data, config['proc_data_path'] + '_test_ids.txt')
        save_subject_ids(val_data, config['proc_data_path'] + '_val_ids.txt')

    train_data = train_data.drop(['subject'], axis=1)
    test_data = test_data.drop(['subject'], axis=1)
    val_data = val_data.drop(['subject'], axis=1)

    scaler = None
    
    if config['scale_type'] == 'standard':
        scaler = StandardScaler()
    elif config['scale_type'] == 'robust':
        scaler = RobustScaler(**config['robust_extra_params'])

    if scaler != None:
        print('Scaling data with', config['scale_type'], 'scaling')
        
        keys = list(train_data)
        keys.remove('score')

        train_data[keys] = scaler.fit_transform(train_data[keys])

        if len(test_data) > 0:
            test_data[keys] = scaler.transform(test_data[keys])
        if len(val_data) > 0:
            val_data[keys] = scaler.transform(val_data[keys])

    print('Saving data to: ', config['proc_data_path'])
    train_data.to_csv(config['proc_data_path'] + '_data.csv', index=False)
    test_data.to_csv(config['proc_data_path'] + '_test_data.csv', index=False)
    val_data.to_csv(config['proc_data_path'] + '_val_data.csv', index=False)

    print('Loaded training data with size: ', np.shape(train_data))
    print('Loaded test data with size: ', np.shape(test_data))
    print('Loaded validation data with size: ', np.shape(val_data))

def load_key_names(data_loc):

    key_names = list(pd.read_csv(data_loc, index_col=0, nrows=0))
    key_names.remove('score')
    
    return key_names


