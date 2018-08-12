import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from logging import getLogger, StreamHandler, Formatter, FileHandler, DEBUG, INFO
import pickle

# Log Settings
LOG_DIR = 'log\\'
LOG_FILE = 'main_03_gridsearch.py.log'
logger = getLogger('main')
log_fmt = Formatter('%(asctime)s %(name)s %(lineno)d [%(levelname)s][%(funcName)s] %(message)s')
log_handler = StreamHandler()
log_handler.setLevel(INFO)
log_handler.setFormatter(log_fmt)
logger.addHandler(log_handler)
log_handler = FileHandler(LOG_DIR + LOG_FILE, 'a')
log_handler.setFormatter(log_fmt)
logger.setLevel(DEBUG)
logger.addHandler(log_handler)

# numpy Settings
np.set_printoptions(linewidth=200)

logger.info('--- start ---')

file_name_scaler = 'resource\\model\\scaler.dat'
file_name_model = 'resource\\model\\svm.dat'

# 1. データの読み込み
logger.info('--- load data ---')
file_name_x = 'resource\\data\\x.txt'
file_name_y = 'resource\\data\\y.txt'
x = pd.read_csv(file_name_x, header=None)
logger.info('x.csv: {}'.format(x.shape))
y = pd.read_csv(file_name_y, header=None).T
logger.info('y.csv: {}'.format(y.shape))

# 2. データ正規化
logger.info('--- data normalization ---')
scaler = MinMaxScaler()
x = scaler.fit_transform(x)
pickle.dump(scaler, open(file_name_scaler, 'wb'))
logger.info('model dumped: ' + file_name_scaler)

# 3. グリッドサーチ
logger.info('--- grid search ---')
param_grid = {
    'C': [5.0],
    'kernel': ['rbf'],
    'gamma': [0.2],
    'random_state': [0],
    'probability': [True]
}
clf = SVC()
grid = GridSearchCV(clf, param_grid=param_grid, cv=5, scoring='accuracy', return_train_score=True)
grid.fit(x, y)
logger.info('max_auc: {}'.format(grid.best_score_))
logger.info('max_params: {}'.format(grid.best_params_))

# 4. モデルの書き出し
logger.info('--- model dump ---')
pickle.dump(grid, open(file_name_model, 'wb'))
logger.info('model dumped: ' + file_name_model)

logger.info('end')
