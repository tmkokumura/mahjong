import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, train_test_split
from mglearn.tools import heatmap

# 0. 変数の初期化
file_name_x = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\data\\x.txt'
file_name_y = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\data\\y2.txt'

# 1.データの読み込み
x = pd.read_csv(file_name_x, header=None)
y = pd.read_csv(file_name_y, header=None)

print(x.head())
print(y.head())

# 2.訓練データとテストデータに分割
train_x, test_x, train_y, test_y = train_test_split(
            x, y, test_size=0.2, random_state=0
        )


# 3. グリッドサーチ
pipe = Pipeline([('scaler', MinMaxScaler()), ('svm', SVC())])
param_grid = {'svm__C': [0.1, 1.0, 2.0],
              'svm__gamma': [0.1, 1.0, 2.0]}
grid = GridSearchCV(pipe, param_grid=param_grid, cv=3)
grid.fit(train_x, train_y)

print('Best cross-validation accuracy: {:.2f}'.format(grid.best_score_))
print('Test set score: {:.2f}'.format(grid.score(test_x, test_y)))
print('Best params: {}'.format(grid.best_params_))

result = pd.DataFrame(grid.cv_results_)
score = np.array(result.mean_test_score).reshape(3, 3)
heatmap(score, xlabel='gamma', xticklabels=param_grid['svm__gamma'],
        ylabel='C', yticklabels=param_grid['svm__C'], cmap='viridis')


# score_image = heatmap(
#     confusion_matrix(y_test, pred)
# )


