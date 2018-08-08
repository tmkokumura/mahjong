#coding:utf-8

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD

from sklearn.utils import shuffle


M = 2       # 入力データの次元
K = 3       # クラス数
n = 100     # クラスごとのデータ数
N = n * K   # 全データ数


# 教師データ
X1 = np.random.randn(n, M) + np.array([0, 10])
X2 = np.random.randn(n, M) + np.array([5, 5])
X3 = np.random.randn(n, M) + np.array([10, 0])

Y1 = np.array([[1, 0, 0] for i in range(n)])
Y2 = np.array([[0, 1, 0] for i in range(n)])
Y3 = np.array([[0, 0, 1] for i in range(n)])

X = np.concatenate((X1, X2, X3), axis=0)
Y = np.concatenate((Y1, Y2, Y3), axis=0)

#######################################
# 1.モデルの定義
#######################################

model = Sequential([
    Dense(input_dim=M, units=K),
    Activation('softmax')
])

#######################################
# 2. 誤差関数の定義, 3. 最適化手法の定義
#######################################

# 誤差関数を用いて確率的勾配効果法を行う
model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.1))

#######################################
# 4. モデルの学習
#######################################
minibatch_size = 50
model.fit(X, Y, epochs=20, batch_size=minibatch_size)

#######################################
# 9. 学習結果の確認
#######################################
X_, Y_ = shuffle(X, Y)
classes = model.predict_classes(X_[0:10], batch_size=minibatch_size)
prob = model.predict_proba(X_[0:10], batch_size=1)


print('classified:')
print(np.argmax(model.predict(X_[0:10]), axis=1) == classes)
print()
print('output probability:')
print(prob)
