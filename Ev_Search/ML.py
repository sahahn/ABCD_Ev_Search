from sklearn.model_selection import RepeatedStratifiedKFold, RepeatedKFold, RandomizedSearchCV
from sklearn.metrics import roc_auc_score, mean_squared_error, r2_score
from sklearn.linear_model import LogisticRegressionCV, ElasticNetCV, LinearRegression
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
    
def train_regression_model(X, y, model_type='elastic', cv=3):

    if model_type == 'elastic':
        model = ElasticNetCV(cv=cv)
    elif model_type == 'linear':
        model = LinearRegression(fit_intercept=True)

    model.fit(X, y)
    return model

def train_binary_model(X, y, int_cv=3, class_weight='balanced'):

    model = LogisticRegressionCV(cv=int_cv, class_weight=class_weight)
    model.fit(X, y)

    return model

def evaluate_regression_model(X, y, model_type='elastic', n_splits=3, n_repeats=2, int_cv=3, metric='r2', target_transform=None):

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










