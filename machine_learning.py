import numpy as np
import logging
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

class MachineLearning:
    """
    クラス定数
    """
    X = 'x'
    Y = 'y'
    TRAIN_X = 'train_x'
    TRAIN_Y = 'train_y'
    TEST_X = 'test_x'
    TEST_Y = 'test_y'

    """
    プライベートメソッド
    """
    def _read_file(self, file_name):
        f = open(file_name, 'r')
        lines = f.readlines()
        f.close()

        row = []
        for line in lines:
            # 末尾の改行を除去してカンマで分割
            cols = line.strip('\r\n').split(',')

            row.append(cols)

        return np.array(row).astype('int64')


    """
    コンストラクタ
    """
    def __init__(self, file_name_X, file_name_Y):
        """
        init
        :param file_name_X: データXのファイル名
        :param file_name_Y: データYのファイル名
        """
        logging.info('--- Start [MachineLearning.__init__] ---')

        # データファイルの読み込み
        self._X = self._read_file(file_name_X)
        self._Y = self._read_file(file_name_Y)[0]

        # 訓練データとテストデータの初期化
        self._train_X = None
        self._train_Y = None
        self._test_X = None
        self._test_Y = None

        # 識別器の初期化
        self._svm = None

        logging.info('--- End [MachineLearning.__init__] ---')

    """
    パブリックメソッド
    """
    def train_test_split(self, test_size=None, random_state=None):
        """
        データセットを訓練データとテストデータに分割する
        :param random_state: シャッフル用乱数のシード
        :return: None
        """

        logging.info('--- Start [MachineLearning.train_test_split] ---')

        self._train_X, self._test_X, self._train_Y, self._test_Y = train_test_split(
            self._X, self._Y, test_size=test_size, random_state=random_state
        )

        logging.info('--- End [MachineLearning.train_test_split] ---')

    def normalize(self):
        """
        データを0～1のレンジに正規化する
        :return:
        """

        logging.info('--- Start [MachineLearning.normalize] ---')

        scaler = MinMaxScaler()
        scaler.fit(self._train_X)
        self._train_X = scaler.transform(self._train_X)
        self._test_X = scaler.transform(self._test_X)

        logging.info('--- End [MachineLearning.normalize] ---')

    def init_svm(self, C=None, gamma=None):
        """
        SVMを初期化する
        :param C: C
        :param gamma: gamma
        :return: None
        """

        logging.info('--- Start [MachineLearning.init_svm] ---')

        self._svm = SVC(kernel='rbf', C=C, gamma=gamma)

        logging.info('--- End [MachineLearning.init_svm] ---')

    def train_svm(self):
        """
        SVMを訓練する
        :return: 訓練データの正解率
        """
        logging.info('--- Start [MachineLearning.train_svm] ---')

        self._svm.fit(self._train_X, self._train_Y)
        pred = self._svm.predict(self._train_X)
        pred_details = []
        for i in range(len(self._test_X)):
            pred_details.append([self._train_Y[i], pred[i], self._train_Y[i] == pred[i]])

        acc = self._svm.score(self._train_X, self._train_Y)

        logging.info('--- End [MachineLearning.train_svm] ---')

        return acc, pred_details

    def save_svm(self, file_name):
        """
        学習済みのSVMモデルをファイルに保存する
        :param file_name: ファイル名
        :return: None
        """
        logging.info('--- Start [MachineLearning.save_svm] ---')

        self._svm.save(file_name)

        logging.info('--- End [MachineLearning.save_svm] ---')

    def load_svm(self, file_name):
        """
        学習済みのSVMモデルをファイルから読み込む
        :param file_name: ファイル名
        :return: None
        """
        logging.info('--- Start [MachineLearning.load_svm] ---')

        self._svm.load(file_name)

        logging.info('--- End [MachineLearning.load_svm] ---')

    def predict_svm(self):
        """
        SVMを用いてテストデータの予測を行う
        :return:
        """

        logging.info('--- Start [MachineLearning.predict_svm] ---')
        pred = self._svm.predict(self._test_X)

        pred_details = []
        for i in range(len(self._test_X)):
            pred_details.append([self._test_Y[i], pred[i], self._test_Y[i] == pred[i]])

        acc = self._svm.score(self._test_X, self._test_Y)

        logging.info('--- End [MachineLearning.predict_svm] ---')

        return acc, pred_details

    def cross_val_svm(self, set_num):
        """
        SVMを用いてクロスバリデーションを行う
        :param set_num: セット数
        :return:
        """
        logging.info('--- Start [MachineLearning.cross_val_svm] ---')

        # データをシャッフル
        self._X, self._Y = shuffle(self._X, self._Y)

        # クロスバリデーションのセットを繰り返す
        details = []
        train_true_num = 0
        train_data_num = 0
        test_true_num = 0
        test_data_num = 0
        for i in range(set_num):
            logging.debug('Cross Validation #{0}'.format(i))

            # データをテストデータと訓練データに分割
            self._train_X = np.array(([self._X[k] for k in range(len(self._X)) if k % set_num != i]))
            self._train_Y = np.array([self._Y[k] for k in range(len(self._Y)) if k % set_num != i])
            self._test_X = np.array([self._X[k] for k in range(len(self._X)) if k % set_num == i])
            self._test_Y = np.array([self._Y[k] for k in range(len(self._Y)) if k % set_num == i])

            # データの標準化
            self.normalize()

            # 訓練
            train_acc, train_pred_details = self.train_svm()
            for detail in train_pred_details:
                train_data_num += 1
                if detail[2]:
                    train_true_num += 1

            # テストデータによる検証
            test_acc, test_pred_details = self.predict_svm()
            for detail in test_pred_details:
                test_data_num += 1
                if detail[2]:
                    test_true_num += 1

            details.append([train_acc, test_acc, train_pred_details, test_pred_details])

        ave_train_acc = train_true_num / train_data_num
        ave_test_acc = test_true_num / test_data_num

        logging.info('--- End [MachineLearning.cross_val_svm] ---')

        return ave_train_acc, ave_test_acc, details

    def display_min_max(self, data_type='x'):
        """
        データの最小値と最大値を表示する
        :param data_type: 表示対象データ
        :return: None
        """
        data = None

        if data_type == MachineLearning.X:
            data = self._X
        elif data_type == MachineLearning.Y:
            data = self._Y
        elif data_type == MachineLearning.TRAIN_X:
            data = self._train_X
        elif data_type == MachineLearning.TRAIN_Y:
            data = self._train_Y
        elif data_type == MachineLearning.TEST_X:
            data = self._test_X
        elif data_type == MachineLearning.TEST_Y:
            data = self._test_Y

        plt.plot(data.min(axis=0), marker='o', label='min')
        plt.plot(data.max(axis=0), marker='^', label='max')
        plt.plot(data.mean(axis=0), marker='1', label='mean')
        plt.legend()
        plt.title("Data min-max")
        plt.xlabel("feature#")
        plt.ylabel("val")
        plt.show()


