from __future__ import print_function, division
from sklearn import linear_model

try:
    import cPickle as pickle
except:
    import pickle
import sys
sys.path.append("../../classifiers")
import numpy as np
from collections import Counter
import operator
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import warnings
import sklearn
from classifiers.Baseline import BaselineModel
from classifiers.knn_classifiers.KNN import KNNModel
from classifiers.lr_classifiers.LogisticRegression import LRModel
from classifiers.svm_classifiers.SVM_C import SVMCModel
from classifiers.svm_classifiers.SVM_Nu import SVMNuModel
from classifiers.svm_classifiers.SVM_Linear import SVMLinearModel
from classifiers.decision_tree_classifiers.DecisionTree import DecisionTreeModel
from classifiers.emsemble_classifiers.AdaBoost import AdaBoostModel
from classifiers.emsemble_classifiers.Bagging import BaggingModel
from classifiers.emsemble_classifiers.RandomForest import RandomForestModel
from classifiers.bayes_classifiers.GaussianNB import GaussianNBModel
from classifiers.bayes_classifiers.BernoulliNB import BernoulliNBModel
from classifiers.bayes_classifiers.MultinomialNB import MultinomialNBModel
from classifiers.bayes_classifiers.ComplementNB import ComplementNBModel
from classifiers.neural_network_classifiers.MLPModel import MLPModel
# from trainers.Trainer import *
warnings.filterwarnings("ignore", category=sklearn.exceptions.ConvergenceWarning)

baseline = BaselineModel()
knn = KNNModel()
lr = LRModel()
svm_c = SVMCModel()
svm_nu = SVMNuModel()
svm_linear = SVMLinearModel()
dt = DecisionTreeModel()
adaboost = AdaBoostModel()
bagging = BaggingModel()
rf = RandomForestModel()
gaussian_nb = GaussianNBModel()
bernoulli_nb = BernoulliNBModel()
multi_nb = MultinomialNBModel()
complement_nb = ComplementNBModel()
mlp = MLPModel()

# Removed baseline from models in case baseline result changes
# model_list = [baseline, knn, lr, svm_c, svm_nu, svm_linear, dt, adaboost, bagging, rf, gaussian_nb,
#                     bernoulli_nb, multi_nb, complement_nb, mlp]

model_list = [bernoulli_nb, multi_nb, complement_nb, gaussian_nb, adaboost, svm_linear, lr]
from trainers.Trainer import *


def get_model_list_f1_dict(X, y, model_list):

    f1_dict = {}

    for mod in model_list:
        return_dict = mod.model_cross_val_predict(X, y, cv = 5)
        f1_dict[mod] = return_dict['f1']

    return f1_dict


def print_model(model_dict):
    for model in model_dict:
        print(model.name, ": ", model_dict[model], "; ", end = "")


def get_best_model(X, y):
    model_f1 = get_model_list_f1_dict(X, y, model_list)
    print_model(model_f1)
    itemMaxValue = max(model_f1.items(), key=lambda x: x[1])
    listOfKeys = list()
    # Iterate over all the items in dictionary to find keys with max value
    for key, value in model_f1.items():
        if value == itemMaxValue[1]:
            listOfKeys.append(key)
    best_model = np.random.choice(listOfKeys[:4], 1)[0]
    print("best model for this session is: ", best_model.name)
    return best_model


class ModelSelectionTrainer(Trainer):
    def __init__(self, X, y):
        super().__init__(X, y)

    def get_best_model(self):
        best_model = get_best_model(self.X, self.y)
        print(best_model.model_cross_val_predict(self.X, self.y))
