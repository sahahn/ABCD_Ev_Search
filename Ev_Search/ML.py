from sklearn.model_selection import RepeatedStratifiedKFold, RepeatedKFold, RandomizedSearchCV, train_test_split
from sklearn.model_selection import KFold, ParameterSampler
from sklearn.metrics import roc_auc_score, mean_squared_error, r2_score
from scipy.stats import randint as sp_randint
from scipy.stats import uniform as sp_uniform
from sklearn.linear_model import LogisticRegressionCV, ElasticNetCV, LinearRegression, OrthogonalMatchingPursuitCV, LarsCV, RidgeCV
from sklearn.svm import LinearSVR
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

def get_regression_score(model, X, y, metric_func, target_transform):
    
    preds = model.predict(X)

    if target_transform == 'log':
        preds = np.exp(preds)

    score = metric_func(y, preds)
    return score

def get_binary_score(model, X, y):

    preds = model.predict_proba(X)
    preds = [p[1] for p in preds]

    score = roc_auc_score(y, preds)

    return score

def train_light_gbm_regressor(X, y, cv, n_params, test_size=.2, n_jobs=-1):

    LGBM_params ={'num_leaves': sp_randint(6, 50), 
             'min_child_samples': sp_randint(100, 500), 
             'min_child_weight': [1e-5, 1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e4],
             'subsample': sp_uniform(loc=0.2, scale=0.8), 
             'colsample_bytree': sp_uniform(loc=0.4, scale=0.6),
             'reg_alpha': [0, 1e-1, 1, 2, 5, 7, 10, 50, 100],
             'reg_lambda': [0, 1e-1, 1, 5, 10, 20, 50, 100]}

    Xt, Xv, yt, yv = train_test_split(X, y, test_size=test_size)
    
    param_list = list(ParameterSampler(LGBM_params, n_iter=n_params))
    param_scores = []
    
    for p in range(n_params):
        
        int_skf = KFold(n_splits=cv)
        best_scs = []
       
        for train_i, test_i in int_skf.split(Xt, yt):
            
            Xt_train, yt_train = Xt[train_i], yt[train_i]
            Xt_test, yt_test = Xt[test_i], yt[test_i]
            
            model = LGBMRegressor(n_jobs=n_jobs, silent=True, n_estimators=5000, **param_list[p])
            model.fit(Xt_train, yt_train, eval_set=(Xt_test, yt_test), verbose=False, early_stopping_rounds=300)
            
            best_sc = model.best_score_['valid_0']['l2']
            best_scs.append(best_sc)
        
        param_scores.append(np.mean(best_scs))
    
    bp_ind = np.argmin(param_scores)
    model = LGBMRegressor(n_jobs=n_jobs, silent=True, n_estimators=5000, **param_list[bp_ind])
    model.fit(Xt, yt, eval_set=(Xv, yv), verbose=False, early_stopping_rounds=500)

    return model
    
def train_regression_model(X, y, model_type='elastic', cv=3):


    if model_type == 'linear':
        model = LinearRegression(fit_intercept=True)
    elif model_type == 'elastic cv':
        model = ElasticNetCV(cv=cv)
    elif model_type == 'omp cv':
        model = OrthogonalMatchingPursuitCV(cv=cv)
    elif model_type == 'lars cv':
        model = LarsCV(cv=cv)
    elif model_type == 'ridge cv':
        model = RidgeCV(cv=cv)
    elif model_type == 'simple xgboost':
        model = XGBRegressor()
    elif model_type == 'simple lightgbm':
        model = LGBMRegressor()
    elif model_type == 'full lightgbm':
        model = train_light_gbm_regressor(X, y, cv, n_params=10, test_size=.2)
        return model

    model.fit(X, y)
    return model

def train_binary_model(X, y, int_cv=3, class_weight='balanced'):

    model = LogisticRegressionCV(cv=int_cv, class_weight=class_weight)
    model.fit(X, y)

    return model

def evaluate_regression_model(X, y, model_type='linear', n_splits=3, n_repeats=2, int_cv=3, metric='r2', target_transform=None):

    scores = []
    skf = RepeatedKFold(n_splits=n_splits, n_repeats=n_repeats)

    metric_func = r2_score
    if metric == 'mse':
        metric_func = mean_squared_error

    if target_transform == 'log':
        y_trans = np.log1p(y)

    for train_ind, test_ind in skf.split(X,y):
       
        if target_transform != None:
            X_train, y_train = X[train_ind], y_trans[train_ind]
            
        else:
            X_train, y_train = X[train_ind], y[train_ind]
        
        X_test, y_test = X[test_ind], y[test_ind]
        
        model = train_regression_model(X_train, y_train, model_type, int_cv)
        score = get_regression_score(model, X_test, y_test, metric_func, target_transform)
        scores.append(score)

    scores = np.array(scores)
    macro_scores = np.mean(np.reshape(scores, (n_repeats, n_splits)), axis=1)

    return np.mean(macro_scores), np.std(macro_scores)


def test_regression_model(X, y, X_test, y_test, model_type='linear', int_cv=3, metric='r2', target_transform=None):

    metric_func = r2_score
    if metric == 'mse':
        metric_func = mean_squared_error

    if target_transform == 'log':
        y_trans = np.log1p(y)

    if target_transform != None:
        model = train_regression_model(X, y_trans, model_type, int_cv)
    else:
        model = train_regression_model(X, y, model_type, int_cv)

    score = get_regression_score(model, X_test, y_test, metric_func, target_transform)
    return score


def evaluate_binary_model(X, y, n_splits=3, n_repeats=2, int_cv=3, class_weight='balanced'):

    scores = []
    skf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats)

    for train_ind, test_ind in skf.split(X,y):

        X_train, y_train = X[train_ind], y[train_ind]
        X_test, y_test = X[test_ind], y[test_ind]
        
        model = train_binary_model(X_train, y_train, int_cv, class_weight)
        score = get_binary_score(model, X_test, y_test)
        scores.append(score)

    scores = np.array(scores)
    macro_scores = np.mean(np.reshape(scores, (n_repeats, n_splits)), axis=1)

    return np.mean(macro_scores), np.std(macro_scores)










