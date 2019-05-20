# -*- coding: utf-8 -*-
config = {}

#Job name / unique name of run (No numbers at end and **should be unique**!!)
config['key_name'] = 'adhd_set'

#GENERAL EV. SEARCH CONFIGS
#-------------------------

#Number of Key_Set individuals to have in the population
config['num_indv'] = 100

#Number of generations to evaluate over, in each job
config['num_gens'] = 30

#Number of new random Key_Sets to add in each Fill
config['new_rand'] = 3

#Number of keys to start with on a new random Key Set
config['start_num'] = 3

# Prob for a key to mutate, 1-Prob - (1-Prob*1-Prob) to add a key, (1-Prob*1-Prob) to delete a key
config['change_chance'] = .6


#SETTINGS SPECIFIC TO THE TASK MANAGER
#-------------------------------

#Number of overarching generations to run each search for
config['num_search_gens'] = 10

#Number of seperate populations / jobs to run at once
config['num_jobs'] = 50

#Three options exist for starting jobs,
#Either you are 1. starting fresh jobs, 2. continuing an ongoing job where key_set outputs exist,
#3. Want to load existing jobs where key sets do not exist. 
#In the first case set continue to false and preloaded also to false
#In the second, set continue to true and preloaded to true
#In the third, set continue to false and preloaded to true

#If continue is set to true, then no new jobs will be initiated, if set to false then all jobs will start
#If continue is true then preloaded will not be checked
config['continue'] = False

#If false then fresh jobs are created if true then jobs are loaded from saved files
config['preloaded'] = False

#Directory path on VACC to Ev_Search Folder
config['ev_search_dr'] = '/users/s/a/sahahn/ABCD_Ev_Search/Ev_Search'

#How often to check for new jobs
config['check_every'] = 120

#Maximum run time for each job in hours (int)
config['max_run_time'] = 20

#How long before a job should be restarted if not finished in num hours
config['restart_lim'] = config['max_run_time'] + 1

#Name of the template file
config['template_name'] = 'template.script'

#If a file with this name is placed in the job directory then the task manager will terminate
config['kill_command'] = 'KILL_TASKS'

#Starting number to append to each job (only change from 1 if adding more populations on after queued)
config['start_key_num'] = 1

#SETTINGS FOR LOADING THE INITIAL DATA FILE
#-------------------------------

#Boolean to override existing proccessed data
config['create_new_data'] = True

#Basic setting that if set to not be None selects only columns with provided names
config['i_keys'] = None

#Basic setting that will drop any columns when reading the dataset if any of the keys show up in that features name
config['d_keys'] = ['norm-mean', '-std', 'fold-ind', 'gaus-curv', 'curv-ind']

#Location of the directory where data files are stored
data_dr = config['ev_search_dr'] + '/Data/'

#Location of the csv with column names subject and score
config['scores_loc'] = data_dr + 'All_ADHD_IDs.csv'

#Location of the csv with subject and raw measurement data (no demographics as of right now)
config['raw_data_loc'] = data_dr + 'Raw_ABCD_Struc_Data.csv'

#Location containing a list of test subject ID's
config['test_id_loc'] = data_dr + 'ABCD_testsetIDs.csv'

#Optionally split the training set further by witholding a validation set- set size to % of train, 0 for none
config['validation_sz'] = .15

#Full path where the proccessed data is stored, passed as output_loc
# e.g. config['proc_data_path'] + _data.cvs or + test_data.csv
config['proc_data_path'] = data_dr + config['key_name']

#Type of scaling to preform on data, standard or robust right now
config['scale_type'] = 'robust'

#Extra parameters if robust scaling is chosen
config['robust_extra_params'] = {'with_centering': True, 'with_scaling': True, 'quantile_range': (5, 95)}


#ANALYSIS PARAMS
#-------------------------------

#Location to output all of the key sets and score in text
config['output_key_loc'] = config['ev_search_dr'] + '/' + config['key_name'] + '.keys'

#Location to save a plot of performance over time
config['output_performance_graph_loc'] = config['ev_search_dr'] + '/' + config['key_name'] + '_gen_performance.jpg'

#SETTINGS FOR EACH RANDOM SEARCH
#-------------------------------

#Location of the pre-processed data csv within the search used in Evaluate.py
config['loc'] = config['proc_data_path'] + '_data.csv'

#If true then binary settings, otherwise regression
config['binary'] = False

#For regression (binary=False) model type option are 'linear' for LinearRegression and 'elastic' for elasticnetCV
config['model_type'] = 'linear'

#Number of times to repeat CV search
config['n_repeats'] = 2

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
