import logging
import numpy as np
from machine_learning import MachineLearning

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.DEBUG)
np.set_printoptions(linewidth=200)

# 0. 変数の初期化
file_name_X = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\data\\x.txt'
file_name_Y = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\data\\y.txt'

# 1.MachineLearningの初期化とデータの読み込み
ml = MachineLearning(file_name_X, file_name_Y)

# ml.display_min_max(MachineLearning.X)

# 2.SVMの初期化
C = 1.2
gamma = 0.6
ml.init_svm(C, gamma)

# 3.クロスバリデーション
set_num = 5
ave_train_acc, ave_test_acc, details = ml.cross_val_svm(set_num)

for i, vals in enumerate(details):
    print('--- {0}回目 ---'.format(i + 1))
    print('訓練データに対する正解率: {0}'.format(vals[0]))
    print('テストデータに対する正解率: {0}'.format(vals[1]))

print('--- 平均値 ---')
print('訓練データに対する正解率: {0}'.format(ave_train_acc))
print('テストデータに対する正解率: {0}'.format(ave_test_acc))
