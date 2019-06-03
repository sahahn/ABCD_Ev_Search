import pandas as pd 
import numpy as np
import os
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split
from scipy.stats.mstats import winsorize


def load_data(dr, loc):
    print('Reading data from: ', loc)

    data = pd.read_csv(os.path.join(dr, loc))
    data = data.drop_duplicates(subset = 'subject')
    data = data.dropna()

    return data

def load_data_from_default(config):

    dfs = []

    if config['datasets']['nBack_Destr_NDA']:
        dfs.append(load_data(config['data_dr'], 'nBack_Destrieux_NDA.csv'))
    if config['datasets']['nBack_Destr_Minio']:
        dfs.append(load_data(config['data_dr'], 'nBack_Destrieux_Minio.csv'))
    if config['datasets']['sMRI_Destr_NDA']:
        dfs.append(load_data(config['data_dr'], 'sMRI_Destrieux_NDA.csv'))
    if config['datasets']['sMRI_Destr_Minio']:
        dfs.append(load_data(config['data_dr'], 'sMRI_Destrieux_Minio.csv'))
    if config['datasets']['MID_Destr_Minio']:
        dfs.append(load_data(config['data_dr'], 'MID_Destrieux_Minio.csv'))
    if config['datasets']['rsfMRI_Gordon_NDA']:
        dfs.append(load_data(config['data_dr'], 'rsfMRI_GordonCorr_NDA.csv',))
    if config['datasets']['rsfMRI_Destr_NDA']:
        dfs.append(load_data(config['data_dr'], 'rsfMRI_Destrieux_NDA.csv'))
    if config['datasets']['SST_Destr_NDA']:
        dfs.append(load_data(config['data_dr'], 'SST_Destrieux_NDA.csv'))
    if config['datasets']['SST_Destr_Minio']:
        dfs.append(load_data(config['data_dr'], 'SST_Destrieux_Minio.csv'))

    print('Num datasets to merge = ', len(dfs))

    data = dfs[0]
    for i in range(1, len(dfs)):
        data = pd.merge(data, dfs[i], on='subject')

    return data

def normalize(col):

    mx, mn = np.max(col), np.min(col)
    col = (col - mn) / (mx-mn)

    return col

def load_covars_from_default(config):

    covars = pd.read_csv(os.path.join(config['data_dr'], 'Parent_Demographics_NDA.csv'))

    races = ['demo_race_a_p___10','demo_race_a_p___11','demo_race_a_p___12','demo_race_a_p___13','demo_race_a_p___14',
             'demo_race_a_p___15','demo_race_a_p___16','demo_race_a_p___17','demo_race_a_p___18','demo_race_a_p___19',
             'demo_race_a_p___20','demo_race_a_p___21','demo_race_a_p___22','demo_race_a_p___23','demo_race_a_p___24',
             'demo_race_a_p___25','demo_race_a_p___77','demo_race_a_p___99']

    to_include = ['subject']

    if config['covariates']['sex']:
        to_include.append('demo_sex_v2')
        covars.demo_sex_v2 = [d-1 if d < 3 else np.nan for d in covars.demo_sex_v2]
    
    if config['covariates']['parent_education']:
        to_include.append('demo_prnt_ed_v2')
        covars.demo_prnt_ed_v2 = [d if d != 777 else np.nan for d in covars.demo_prnt_ed_v2]
    
    if config['covariates']['parent_comb_income']:
        to_include.append('demo_comb_income_v2')
        covars.demo_comb_income_v2 = [d if d != 777 and d!= 999 else np.nan for d in covars.demo_comb_income_v2]

    if config['covariates']['race']:
        for race in races:
            to_include.append(race)

    covars = covars[to_include]
    covars = covars.dropna()

    if config['covariates']['normalize']:
        if config['covariates']['parent_education']:
            covars.demo_prnt_ed_v2 = normalize(covars.demo_prnt_ed_v2)
        if config['covariates']['parent_comb_income']:
            covars.demo_comb_income_v2 = normalize(covars.demo_comb_income_v2)

    return covars

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

    invalid_score_inds = in_scores[np.isnan(in_scores.score)].index
    print('Dropping', len(invalid_score_inds), 'scores/subjects for NaN scores')
    in_scores = in_scores.drop(index=invalid_score_inds)

    return in_scores

def filter_data(data, i_keys=None, d_keys=None):
    
    if d_keys != None:

        to_remove = set()
        col_names = list(data)

        for name in col_names:
            for key in d_keys:
                if key in name:
                    to_remove.add(name)

        data = data.drop(list(to_remove), axis=1)
        
    if i_keys != None:

        i_keys += ['subject', 'score']
        
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
    
    if config['raw_data_loc'] != None:

        print('Reading underlying dataset from: ', config['raw_data_loc'])
        data = pd.read_csv(config['raw_data_loc'])

    else: 
        data = load_data_from_default(config)

    if config['covariates']['include_any']:

        print('Reading covariates')
        
        covars = load_covars_from_default(config)
        covar_keys = list(covars)
        covar_keys.remove('subject')
        
        print('Shape of data before merge with co-variates: ', np.shape(data))
        data = pd.merge(data, covars, on='subject')
        print('Shape of data after merge with co-variates: ', np.shape(data))

    print('Filtering dataset with -')
    print('Inclusion Keys: ', config['i_keys'])
    print('Drop Keys: ', config['d_keys'])
    data = filter_data(data, config['i_keys'], config['d_keys'])

    relevant_data = pd.merge(data,scores)

    keys = list(relevant_data)
    keys.remove('score')
    keys.remove('subject')

    if config['covariates']['include_any']:
        for k in covar_keys:
            keys.remove(k)

    if config['winsorize'] != None:
        print('Winzorizing data with', config['winsorize'])
        relevant_data[keys] = winsorize(relevant_data[keys], (config['winsorize']), axis=0)

    print('--Splitting Test Set--')
    train_data, test_data = preform_split(relevant_data, config['test_id_loc'], config['test_sz'], config['random_split_state'])

    print('--Splitting Outer Validation Set--')
    train_data, outer_val_data = preform_split(train_data, config['outer_val_id_loc'], config['outer_val_sz'], config['random_split_state'])

    print('--Splitting Validation Set--')
    train_data, val_data = preform_split(train_data, config['val_id_loc'], config['val_sz'], config['random_split_state'])

    if config['save_ids']:

        save_subject_ids(train_data, config['proc_data_path'] + '_train_ids.txt')
        save_subject_ids(test_data, config['proc_data_path'] + '_test_ids.txt')
        save_subject_ids(outer_val_data, config['proc_data_path'] + '_outer_val_ids.txt')
        save_subject_ids(val_data, config['proc_data_path'] + '_val_ids.txt')

    train_data = train_data.drop(['subject'], axis=1)
    test_data = test_data.drop(['subject'], axis=1)
    outer_val_data = outer_val_data.drop(['subject'], axis=1)
    val_data = val_data.drop(['subject'], axis=1)

    scaler = None
    
    if config['scale_type'] == 'standard':
        scaler = StandardScaler()
    elif config['scale_type'] == 'robust':
        scaler = RobustScaler(**config['robust_extra_params'])

    if scaler != None:
        print('Scaling data with', config['scale_type'], 'scaling')
        
        train_data[keys] = scaler.fit_transform(train_data[keys])

        if len(test_data) > 0:
            test_data[keys] = scaler.transform(test_data[keys])
        if len(val_data) > 0:
            outer_val_data[keys] = scaler.transform(outer_val_data[keys])
        if len(val_data) > 0:
            val_data[keys] = scaler.transform(val_data[keys])

    print('Saving data to: ', config['proc_data_path'])
    train_data.to_csv(config['proc_data_path'] + '_data.csv', index=False)
    test_data.to_csv(config['proc_data_path'] + '_test_data.csv', index=False)
    outer_val_data.to_csv(config['proc_data_path'] + 'outer_val_data.csv', index=False)
    val_data.to_csv(config['proc_data_path'] + '_val_data.csv', index=False)

    print('Loaded training data with size: ', np.shape(train_data))
    print('Loaded test data with size: ', np.shape(test_data))
    print('Loaded outer-validation data with size: ', np.shape(outer_val_data))
    print('Loaded validation data with size: ', np.shape(val_data))

def load_key_names(data_loc):

    key_names = list(pd.read_csv(data_loc, index_col=0, nrows=0))
    key_names.remove('score')
    
    return key_names


