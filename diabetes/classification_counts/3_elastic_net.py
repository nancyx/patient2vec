import datetime
import logging
import os

import dill
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import log_loss, roc_auc_score

DATA_FILE = '../data/final/counts/diabetes_counts.dill'
LOG_FILE = '../log/diabetes_counts_optimized_elasticnet.log'
RESULTS_FILE = '../log/diabetes_counts_elasticnet_results.dill'

optimized_params = {
    'alpha': 0.01,
    'l1_ratio': 0.014952629369956116,
    # other params:
    'loss': 'log',
    'penalty': 'elasticnet',
    'max_iter': 1000,
    'random_state': 1
}

results = {}

# Logging setup
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(message)s')

# Loading data
data = dill.load(open(DATA_FILE, 'rb'))

for months_before in sorted(list(data.keys())):
    train_x = data[months_before]["TRAIN"]["X"]
    train_y = data[months_before]["TRAIN"]["y"]
    test_x = data[months_before]["TEST"]["X"]
    test_y = data[months_before]["TEST"]["y"]

    # Creating and training model
    clf = SGDClassifier(**optimized_params)
    clf.fit(train_x, train_y)

    # Scoring
    pred_y = clf.predict_proba(test_x)

    auc_score = roc_auc_score(test_y, pred_y[:,1])
    log_score = log_loss(test_y, pred_y)

    results[months_before] = {}
    results[months_before]['true_y'] = test_y
    results[months_before]['pred_y'] = pred_y

    logging.info('{}, {}, {}'.format(months_before, auc_score, log_score))

dill.dump(results, open(RESULTS_FILE, 'wb'))
