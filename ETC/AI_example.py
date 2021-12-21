# https://data-marketing-bk.tistory.com/28 에근거
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as mp
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score

PATH = os.path.join("datasets","redwine")


