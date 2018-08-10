import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from logging import getLogger, StreamHandler, Formatter, FileHandler, DEBUG, INFO

from machine_learning import MachineLearning

# Log Settings
LOG_DIR = '../result/'
LOG_FILE = 'train_lgbm.py.log'
logger = getLogger(__name__)
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

# 1. データの読み込み
logger.info('--- load data ---')
file_name_x = 'resource\\image\\windowsapp\\data\\x.txt'
file_name_y = 'resource\\image\\windowsapp\\data\\y.txt'
x = pd.read_csv(file_name_x)
logger.info('x.csv: {}'.format(x))
y = pd.read_csv(file_name_y)
logger.info('y.csv: {}'.format(y))

# 2. データ正規化
logger.info('--- data normalization ---')
scaler = MinMaxScaler()
x = scaler.fit_transform(x)

# 3. グリッドサーチ
logger.info('--- grid search ---')
param_grid = {
    'C': [0.1, 1.0, 10.0],
    'kernel': ['rbf'],
    'gamma': [0.1, 1.0, 10.0],
    'random_state': [0]
}
clf = SVC()
grid = GridSearchCV(clf, param_grid=param_grid, cv=5, scoring='accuracy', return_train_score=True, n_jobs=-1)
grid.fit(x, y)
logger.info('max_auc: {}'.format(grid.best_score_))
logger.info('max_params: {}'.format(grid.best_params_))

# 4. モデルの保存
logger.info('--- model save ---')
file_name_model = 'resource\\image\\windowsapp\\model\\svm.dat'
clf.save(file_name_model)
logger.info('model saved: ' + file_name_model)

logger.info('end')
