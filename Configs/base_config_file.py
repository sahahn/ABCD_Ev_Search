# -*- coding: utf-8 -*-
import os, pickle

config = {}

#Unique name of config file / setup **should be unique** so it doesn't conflict with other runs / file names
config['name'] = 'ADHD'

#Job name for each individual run/key set
config['key_name'] = config['name'] + '_set'

#Location/name to store the pickle config file
config['config_loc'] = config['name'] + '.pkl'

#Optional flag to run everything locally vs. on the VACC
config['run_local'] = True

#If set to true, then each over-arching search gen will start a new population,
#and the best indv will be saved automatically at the end of each run (preloaded should be False)
config['one_run_mode'] = True


#GENERAL EV. SEARCH CONFIGS
#-------------------------

#Number of Key_Set individuals to have in the population
config['num_indv'] = 100

#Number of generations to evaluate over, in each VACC job
config['num_gens'] = 300


config['early_stop_rounds'] = 50

#Number of new random Key_Sets to add in each Fill
config['new_rand'] = 3

#Number of keys to start with on a new random Key Set 
#Plus up to 2 (hard coded param for now), so if = 3, then a new set will have either 3, 4 or 5 starting keys
config['start_num'] = 3

# Prob. for a key to mutate (P) = config['change_chance']
# Prob. to remove a key = ((1-P)*(1-P))
# Prob. to add a key = (1-P) - [Prob. to remove a key / ((1-P)*(1-P))]
# So, Prob. that either a key is added or removed = 1-P
config['change_chance'] = .6


# SETTINGS SPECIFIC TO THE TASK MANAGER
# -------------------------------

# Number of overarching generations to run each search for
config['num_search_gens'] = 10

# Number of seperate populations / jobs to run at once
config['num_jobs'] = 30

# Two options exist for starting jobs,
# Either you are,
# 1. starting fresh jobs with new populations 
# 2. Want to load from existing saved populations
# In the first case set preloaded = False
# In the second, set preloaded = True

# If false then fresh jobs are created if true then jobs are loaded from saved files
config['preloaded'] = False

#Path to main directory, with task manager ect..
config['main_dr'] = '/users/s/a/sahahn/ABCD_Ev_Search/'

#Directory path on VACC to Ev_Search Folder
config['ev_search_dr'] = os.path.join(config['main_dr'] + 'Ev_Search')

#Directory to store keys in
config['key_dr'] = 'Keys'

#How often to check for new jobs
config['check_every'] = 600

#Maximum run time for each job in hours (int)
config['max_run_time'] = 20

#How long before a job should be restarted if not finished in num hours
config['restart_lim'] = config['max_run_time'] + 1

#Name of the template file
config['template_name'] = 'Templates/template.script'

#Name of the temp file
config['temp_name'] = config['key_name'] + '.script'

#If using batched jobs:
#Name of the master template file
config['master_template'] = 'Templates/master_template.script'

#Name of the temp master file
config['master_name'] = config['key_name'] + '_master.script'

#Name of the subjob template file
config['subjob_template'] = 'Templates/subjob_template.sh'

#Name of the temp subjob file
config['subjob_name'] = config['key_name'] + '_subjob.sh'

#Name of the file with progress
config['progress_name'] = config['key_name'] + '_progress' 

#If a file with this name is placed in the job directory then the task manager will terminate
config['kill_tasks_command'] =  'KILL_' + config['name'] + '_TASKS'

#If a file with this name is place in the job directory then the main data file will be deleted ending all jobs
config['kill_jobs_command'] = 'KILL_' + config['name'] + '_JOBS'

#If a file with this name is placed in the directory, all active task managers will run Kill Jobs
config['kill_all_command'] = 'KILL_ALL'

#Starting number to append to each job (only change from 1 if adding more populations on after queued)
config['start_key_num'] = 1

#Number of generations to force a save
config['save_every'] = 50

#SETTINGS FOR LOADING THE INITIAL DATA FILE
#-------------------------------

config['datasets'] = {'nBack_Destr_NDA'     : True,
                      'nBack_Destr_Minio'   : False,
                      'sMRI_Destr_NDA'      : True,
                      'sMRI_Destr_Minio'    : False,
                      'MID_Destr_Minio'     : False,
                      'rsfMRI_Gordon_NDA'   : True,
                      'rsfMRI_Destr_NDA'    : False,
                      'SST_Destr_NDA'       : False,
                      'SST_Destr_Minio'     : False
                      }

config['covariates'] = {'include_any'       : True,
                        'sex'               : True,
                        'race'              : True,
                        'parent_education'  : True,
                        'parent_comb_income': True,
                        'normalize'         : True 
                        }

#Boolean to override existing proccessed data
#Note: If not ever created for this unique config['key_name'], then then new data will be created regardless
config['create_new_data'] = True

#Basic setting that if set to not be None selects only columns with provided names
config['i_keys'] = None

#Basic setting that will drop any columns when reading the dataset if any of the keys show up in that features name
config['d_keys'] = None #['norm-mean', '-std', 'fold-ind', 'gaus-curv', 'curv-ind']

#Location of the directory where data files are stored
config['data_dr'] = os.path.join(config['ev_search_dr'], 'Data')

#Location of the csv with column names subject and score
config['scores_loc'] =  os.path.join(config['data_dr'], 'All_ADHD_IDs.csv')

#Location of the csv with subject and raw measurement data, for a custom dataset, otherwise set to None
config['raw_data_loc'] = None  #os.path.join(config['data_dr'], 'Raw_ABCD_Struc_Data.csv')

#Test and val ids should simply be a test or csv file with no headers and one subject per line!
#Location containing a list of test subject ID's
#Set to None if creating one from provided data
config['test_id_loc'] = os.path.join(config['data_dr'], 'ABCD_testsetIDs.csv')

#Same as for test and validation
config['outer_val_id_loc'] = None

#Optionally provide a location contained a saved list of validation set subject ID's
#Set to None if creating on from test set
config['val_id_loc'] = None

#Note, will check first for saved test / val ids, but if None will check to create
#Optionally split the data by witholding a test set- set size to % of all, 0 for none, see above ^
config['test_sz'] = 0

#Same as for test and validation
config['outer_val_sz'] = .1

#Optionally split the training set further by witholding a validation set- set size to % of train, 0 for none
config['val_sz'] = .1

#Provide a specific random seed when splitting by train test
config['random_split_state'] = 40

#Optionally save the train, val and test ids to a file (for easy use elsewhere)
config['save_ids'] = True

#Full path where the proccessed data is stored, passed as output_loc
# e.g. config['proc_data_path'] + _data.cvs or + test_data.csv, _val_data.csv
config['proc_data_path'] = os.path.join(config['data_dr'], config['name'])

#Type of scaling to preform on data, standard or robust right now
config['scale_type'] = 'robust'

#Extra parameters if robust scaling is chosen
config['robust_extra_params'] = {'with_centering': True, 'with_scaling': True, 'quantile_range': (5, 95)}

#Either None or the the num/% to take of either side
config['winsorize'] = .001


#SETTINGS FOR EACH RANDOM SEARCH
#-------------------------------

#Location of the pre-processed data csv within the search used in Evaluate.py
config['loc'] = config['proc_data_path'] + '_data.csv'

#Location of the pre-processed validation-data csv within the search used in Evaluate.py
config['val_loc'] = config['proc_data_path'] + '_val_data.csv'

#If true then binary settings, otherwise regression
config['binary'] = False

#For regression (binary=False) many model type options
config['model_type'] = 'linear'

#Number of times to repeat CV search
config['n_repeats'] = 3

#Number of CV splits to evaluate at each random split
config['n_splits'] = 3

#Number of internal CV to preform during model training
config['int_cv'] = 3

#If binary, then 'balanced' or None
config['class_weight'] = 'balanced'

#If regression (binary=False), then what metric to use 
config['metric'] = 'r2'

#Type of transform to compute on the target regression variable (only for regression)
#Options are: 'log' to preform a log1p transform, or None
config['target_transform'] = None

#ANALYSIS PARAMS
#-------------------------------

#Location/name of the folder to store analysis output
config['stats_loc'] = os.path.join(config['main_dr'], 'Stats')

#Location to output all of the key sets and score in text
config['output_key_loc'] = os.path.join(config['stats_loc'], config['name'] + '_all_keys.txt')

#Location to store just best sets of keys
config['output_best_loc'] = os.path.join(config['stats_loc'], config['name'] + '_best_keys.txt')

#Location of saved key_sets to limit features from, set to None to not limit features
config['limit_features_from'] = config['output_best_loc']

#Optional threshold in which to filter out key sets from consideration
config['feature_score_lim'] = 0

#Number of top features to keep (if less then 1, treat as keep % of total # of features)
config['keep_top_x'] = .5

#Location to save a plot of performance over time
config['output_performance_graph_loc'] = os.path.join(config['stats_loc'], config['name'] + '_performance_plot.jpg')

#Location to save a plot of performance over time
config['output_val_performance_graph_loc'] = os.path.join(config['stats_loc'], config['name'] + '_val_performance_plot.jpg')

#Location to save a plot of best pop over time with validation
config['output_val_graph_loc'] = os.path.join(config['stats_loc'], config['name'] + '_validation_plot.jpg')

#Keep as True, False is broken right now
config['single_jobs'] = True               

with open(config['config_loc'], 'wb') as output:
    pickle.dump(config, output)

