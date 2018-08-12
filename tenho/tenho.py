from feature.bag_of_visual_words import BagOfVisualWords
from logging import getLogger
import cv2
import pickle
import window_handler


class Tenho:
    MODEL_FILE = 'resource\\model\\svm.dat'
    SCALER_FILE = 'resource\\model\\scaler.dat'
    VISUAL_WORDS = 'resource\\visual_words\\visual_words.txt'

    def _get_hai_id(self, pred_class):
        if pred_class == 0:
            hai_id = '1m'
        elif pred_class == 1:
            hai_id = '1p'
        elif pred_class == 2:
            hai_id = '1s'
        elif pred_class == 3:
            hai_id = '2m'
        elif pred_class == 4:
            hai_id = '2p'
        elif pred_class == 5:
            hai_id = '2s'
        elif pred_class == 6:
            hai_id = '3m'
        elif pred_class == 7:
            hai_id = '3p'
        elif pred_class == 8:
            hai_id = '3s'
        elif pred_class == 9:
            hai_id = '4m'
        elif pred_class == 10:
            hai_id = '4p'
        elif pred_class == 11:
            hai_id = '4s'
        elif pred_class == 12:
            hai_id = '5m'
        elif pred_class == 13:
            hai_id = '5mr'
        elif pred_class == 14:
            hai_id = '5p'
        elif pred_class == 15:
            hai_id = '5pr'
        elif pred_class == 16:
            hai_id = '5s'
        elif pred_class == 17:
            hai_id = '5sr'
        elif pred_class == 18:
            hai_id = '6m'
        elif pred_class == 19:
            hai_id = '6p'
        elif pred_class == 20:
            hai_id = '6s'
        elif pred_class == 21:
            hai_id = '7m'
        elif pred_class == 22:
            hai_id = '7p'
        elif pred_class == 23:
            hai_id = '7s'
        elif pred_class == 24:
            hai_id = '8m'
        elif pred_class == 25:
            hai_id = '8p'
        elif pred_class == 26:
            hai_id = '8s'
        elif pred_class == 27:
            hai_id = '9m'
        elif pred_class == 28:
            hai_id = '9p'
        elif pred_class == 29:
            hai_id = '9s'
        elif pred_class == 30:
            hai_id = 'chun'
        elif pred_class == 31:
            hai_id = 'haku'
        elif pred_class == 32:
            hai_id = 'hatsu'
        elif pred_class == 33:
            hai_id = 'nan'
        elif pred_class == 34:
            hai_id = 'pe'
        elif pred_class == 35:
            hai_id = 'sha'
        elif pred_class == 36:
            hai_id = 'ton'

        return hai_id

    def __init__(self):
        self._logger = getLogger('main')

        self._logger.info('--- enter[Tenfo.__init__] ---')

        # SVMモデルのロード
        self._logger.info('load SVM model')
        self._clf = pickle.load(open(Tenho.MODEL_FILE, 'rb'))

        # VisualWordsのロード
        self._logger.info('load Visual Words')
        self._bovw = BagOfVisualWords()
        self._bovw.load_visual_words(Tenho.VISUAL_WORDS)

        # MiniMaxScalerのロード
        self._logger.info('load MiniMaxScaler')
        self._scaler = pickle.load(open(Tenho.SCALER_FILE, 'rb'))

        self._window = None
        self._predicts = []

        self._logger.info('--- exit[Tenfo.__init__] ---')

    def read_window(self):
        """
        スクリーンキャプチャを取得し、天鳳のウインドウを検出する
        :return:
        """

        self._logger.info('--- enter[Tenfo.read_window] ---')
        self._window = window_handler.screenshot()
        self._logger.info('--- exit[Tenfo.read_window] ---')

    def read_image(self, file_name):
        """
        天鳳の画面画像を読み込む
        :param file_name:
        :return: None
        """
        self._logger.info('--- enter[Tenfo.read_image] ---')
        self._window = cv2.imread(file_name)
        self._logger.info('image read: ' + file_name)
        self._logger.info('--- exit[Tenfo.read_image] ---')

    def predict(self, x, y, width, height):
        """
        牌を認識する
        :param x: 座標x
        :param y: 座標y
        :param width: 幅
        :param height: 高さ
        :return: 認識結果
        """

        self._logger.info('--- enter[Tenfo.predict] ---')

        hai_img = self._window[y: y + height, x: x + width]
        hist = [self._bovw.get_histogram(hai_img)]
        self._logger.info('histogram: {}'.format(len(hist[0])))

        hist = self._scaler.transform(hist)
        self._logger.info('normalized: {}'.format(len(hist[0])))

        pred = self._clf.predict(hist)
        hai_str = self._get_hai_id(pred)


        self._predicts.append([x, y, width, height, hai_str])

        self._logger.info('--- exit[Tenfo.predict] ---')

        return hai_str

    def dislpay(self, size):
        self._logger.info('--- enter[Tenfo.dislpay] ---')
        for predict in self._predicts:
            # 矩形の書き込み
            cv2.rectangle(
                self._window,
                (predict[0], predict[1]),
                (predict[0] + predict[2], predict[1] + predict[3]),
                (0, 0, 255),
                thickness=2
            )
            # 文字の書き込み
            fontFace = cv2.FONT_HERSHEY_PLAIN
            fontScale = 1.5
            color = (0, 0, 255)
            cv2.putText(self._window, predict[4], (predict[0] - 2, predict[1] - 2), fontFace, fontScale, color, thickness=2)

        resize_img = cv2.resize(self._window, None, fx=size, fy=size)
        cv2.imshow('window', resize_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        self._logger.info('--- exit[Tenfo.dislpay] ---')







