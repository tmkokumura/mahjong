#coding:utf-8

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD

from sklearn.utils import shuffle

M = 2        # 入力データの次元
U = 3        # 隠れ層の次元数
K = 2        # 出力クラス数
n = 100        # クラスごとのデータ数
N = n * K    # 全データ数

# 教師データ
X1_1 = np.random.randn(int(n/2), M) + np.array([0, 0])
X1_2 = np.random.randn(int(n/2), M) + np.array([10, 10])
X2_1 = np.random.randn(int(n/2), M) + np.array([0, 10])
X2_2 = np.random.randn(int(n/2), M) + np.array([10, 0])

Y1 = np.array([[1, 0] for i in range(n)])
Y2 = np.array([[0, 1] for i in range(n)])

X = np.concatenate((X1_1, X1_2, X2_1, X2_2), axis=0)
Y = np.concatenate((Y1, Y2), axis=0)


#######################################
# 1.モデルの定義
#######################################
model = Sequential()

# 入力 - 中間層
model.add(Dense(input_dim=M, units=U))
model.add(Activation('sigmoid'))

# 中間 - 出力層
model.add(Dense(units=K))
model.add(Activation('softmax'))

#######################################
# 2. 誤差関数の定義, 3. 最適化手法の定義
#######################################
model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.1), metrics=['accuracy'])

#######################################
# 4. モデルの学習
#######################################
minibatch_size = 50
model.fit(X, Y, epochs=2000, batch_size=minibatch_size)

#######################################
# 9. 学習結果の確認
#######################################
X_, Y_ = shuffle(X, Y)
classes = model.predict_classes(X_[0:10], batch_size=minibatch_size)
prob = model.predict_proba(X_[0:10], batch_size=1)

loss_and_metrics = model.evaluate(X, Y)
print('loss_and_metrics')
print(loss_and_metrics)
print('')
print('classified:')
print(np.argmax(model.predict(X_[0:10]), axis=1) == classes)
print()
print('output probability:')
print(prob)


