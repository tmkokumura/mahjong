# coding:utf-8

import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from sklearn.utils import shuffle
from fileUtils import FileUtils as fu


# private method
# 各順位の確率から平均順位を計算する
def calc_ave_rank(prob):
    return 1.0 * prob[0] + 2.0 * prob[1] + 3.0 * prob[2] + 4.0 * prob[3]


# private method
# モデルを評価する
def evaluate_model(model, x, y):
    loss_and_metrics = model.evaluate(x, y)
    print('モデルの評価 [誤差, 正解率]')
    print(loss_and_metrics)


# private method
# モデルを使用して平均順位を予測する
def predict_ave_rank(model, data):
    predict = model.predict_proba(data, batch_size=1)
    print('入力データ: {0}'.format(data[0]))
    print('出力確率: {0}'.format(predict[0]))
    print('予想平均順位: {0}'.format(calc_ave_rank(predict[0])))


# private method
# グラフを描画する
def plot_graph(hist, elem, epochs):
    data = hist.history[elem]
    plt.rc('font', family='serif')
    plt.plot(range(epochs), data, label=elem, color='black')
    plt.xlabel('epochs')
    plt.show()


# private method
# ベースラインの一致率を計算する
def get_acc_baseline(x, y):
    data_num = len(x)
    pos_num = 0
    neg_num = 0

    for i in range(data_num):
        scores = x[i][1:4]
        rank = 1

        for score in scores:
            if score <= 0:
                break
            else:
                rank += 1

        if y[i][rank - 1] == 1:
            pos_num += 1
        else:
            neg_num += 1

    print('ベースラインの正解率')
    print(pos_num / data_num)


########################################
# 0.訓練データ・テストデータの読込
########################################

# ファイル読み込み
file_name = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\data\\data.txt'
lines = fu.read_file(file_name)

data_x = []
data_y = []
for i, line in enumerate(lines):
    # 末尾の改行を除去してカンマで分割
    data_str = line.strip('\r\n').split(',')

    # 数値型に変換
    data = [int(i) for i in data_str]

    # 特徴とラベルに分割
    data_x.append(data[1:5])
    data_y.append(data[5:])

# numpy配列に変換
X_ = np.array(data_x)
Y_ = np.array(data_y)

# データをシャッフル
X__, Y__ = shuffle(X_, Y_)

# テストデータと訓練データに分割
test_data_ratio = 0.1                            # 全データに占めるテストデータの割合
test_data_num = int(len(X__) * test_data_ratio)  # テストデータの数
x = X__[:test_data_num]
y = Y__[:test_data_num]
X = X__[test_data_num:]
Y = Y__[test_data_num:]


#######################################
# 1.モデルの定義
#######################################

M = 4        # 入力データの次元
N = 5        # 隠れ層の数
U = 20       # 隠れ層の次元数
K = 4        # 出力クラス数

kernel_initializer = 'truncated_normal'     # 重みの初期化方法
ih_activation = 'relu'                      # 入力層・隠れ層の活性化関数
o_activation = 'softmax'                    # 出力層の活性化関数
dropout = 0.5                               # 隠れ層のドロップアウト率

model = Sequential()                        # モデルの初期化

# 入力層 - 隠れ層を生成
model.add(Dense(input_dim=M, units=U, kernel_initializer=kernel_initializer))
model.add(BatchNormalization())
model.add(Activation(ih_activation))

# 隠れ層 - 隠れ層を生成
for i in range(N - 1):
    model.add(Dense(input_dim=U, units=U, kernel_initializer=kernel_initializer))
    model.add(BatchNormalization())
    model.add(Activation(ih_activation))
    model.add(Dropout(dropout))

# 隠れ層 - 出力層を生成
model.add(Dense(input_dim=U, units=K, kernel_initializer=kernel_initializer))
model.add(Activation(o_activation))


#######################################
# 2. 誤差関数と最適化手法の定義
#######################################

loss = 'categorical_crossentropy'   # 誤差関数
lr = 0.001                          # Adamパラメータ lr
beta_1 = 0.9                        # Adamパラメータ beta_1
beta_2 = 0.999                      # Adamパラメータ beta_2
metrics = 'accuracy'                # 計測するメトリクス

model.compile(loss=loss, optimizer=Adam(lr=lr, beta_1=beta_1, beta_2=beta_2), metrics=[metrics])


#######################################
# 3. モデルの学習
#######################################

batch_size = 1000                   # バッチサイズ
epochs = 2                         # エポック数

hist = model.fit(X, Y, epochs=epochs, batch_size=batch_size)


#######################################
# 4. 正解率の推移を描画
#######################################

plot_graph(hist, 'acc', epochs)


#######################################
# 5. テストデータを用いたモデルの評価
#######################################

evaluate_model(model, x, y)
get_acc_baseline(X__, Y__)

#######################################
# 6. モデルを使って平均順位を予想してみる
#######################################

print()
print('東1局 試合開始時')
sample_data = np.array([[0, 0, 0, 0]])
predict_ave_rank(model, sample_data)

print()
print('東4局 他家全員に対して8000点リード')
sample_data = np.array([[3, 8000, 8000, 8000]])
predict_ave_rank(model, sample_data)

print()
print('東3局 複雑な局面')
sample_data = np.array([[3, -8000, -1000, 8000]])
predict_ave_rank(model, sample_data)