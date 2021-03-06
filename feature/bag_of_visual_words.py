# coding:utf-8

###########################################
# 麻雀牌をBag of Visual Wordsで分類する
###########################################

import cv2
import os
import numpy as np
from tqdm import tqdm
from sklearn.cluster import MiniBatchKMeans
from logging import getLogger


class BagOfVisualWords:
    """
    クラス定数
    """
    SIFT = 'sift'
    SURF = 'surf'
    AKAZE = 'akaze'

    """
    プライベートメソッド
    """
    def _write_file_1d(self, data, file_name):
        file = open(file_name, 'w')
        for col, word in enumerate(data):
            file.write(str(word))
            if col < len(data) - 1:
                file.write(',')

        file.close()

    def _write_file_2d(self, data, file_name):
        file = open(file_name, 'w')
        for row, line in enumerate(data):
            for col, word in enumerate(line):
                file.write(str(word))
                if col < len(line) - 1:
                    file.write(',')
            if row < len(data) - 1:
                file.write('\n')
        file.close()

    def read_file(self, file_name):
        f = open(file_name, 'r')
        lines = f.readlines()
        f.close()

        row = []
        for line in lines:
            # 末尾の改行を除去してカンマで分割
            data_str = line.strip('\r\n').split(',')

            # 数値型に変換
            cols = [float(i) for i in data_str]
            row.append(cols)

        return np.array(row)

    """
    コンストラクタ
    """
    def __init__(self, detector='sift'):
        """
        init
        :param detector: 特徴検出器
        """
        self._logger = getLogger('main')

        self._logger.info('--- enter [BagOfVisualWords.__init__] ---')

        # 特徴検出器の初期化
        if detector == BagOfVisualWords.SIFT:
            self._detector = cv2.xfeatures2d.SIFT_create()
            self._dim = 128
        elif detector == BagOfVisualWords.SURF:
            self._detector = cv2.xfeatures2d.SURF_create()
            self._dim = 128
        elif detector == BagOfVisualWords.AKAZE:
            self._detector = cv2.AKAZE_create()
            self._dim = 61

        # Visual Wordsの初期化
        self._visual_words = None

        # データセットの初期化
        self._X = None
        self._Y = None
        self._num = 0

        self._logger.info('--- exit [BagOfVisualWords.__init__] ---')

    """
    パブリックメソッド
    """
    def create_visual_words(self, src_dir):
        """
        全テンプレートを使ってVisual Wordsを生成する
        :param src_dir: テンプレートファイルのルードディレクトリ
        :return: None
        """

        self._logger.info('--- enter [BagOfVisualWords.create_visual_words] ---')

        features = []

        # 子ディレクトリ（クラスごと）の取得
        child_dir_list = os.listdir(src_dir)

        # クラスごとのループ
        for dir_name in tqdm(child_dir_list):

            # 画像ファイル名の取得
            file_list = os.listdir(os.path.join(src_dir, dir_name))

            # 画像ごとのループ
            for file_name in file_list:

                # 画像を読み込み
                img = cv2.imread(os.path.join(src_dir, dir_name, file_name))

                # 特徴検出と特徴量の記述
                self._logger.debug('Detecting and computing of ' + file_name)
                kp, des = self._detector.detectAndCompute(img, None)

                # キーポイントが検出されなかった場合は、0ベクトルを仮置き
                if des is None:
                    self._logger.warning('No keypoints are detected on ' + file_name)
                    des = np.zeros((1, self._dim))

                features.extend(des)

        # 特徴量のクラスタリングとセントロイド（＝Visural Word）を計算の計算
        self._logger.debug('Calculating visual words')

        # https://blanktar.jp/blog/2016/03/python-visual-words.html
        self._visual_words = MiniBatchKMeans(n_clusters=self._dim).fit(features).cluster_centers_

        self._logger.info('--- exit [BagOfVisualWords.create_visual_words] ---')

    def save_visual_words(self, file_name):
        """
        Visual Wordsをファイルに保存する
        :param file_name: ファイル名
        :return: None
        """

        self._logger.info('--- enter [BagOfVisualWords.save_visual_words] ---')

        self._write_file_2d(self._visual_words, file_name)

        self._logger.info('--- exit [BagOfVisualWords.save_visual_words] ---')

    def load_visual_words(self, file_name):
        """
        Visual Wordsをファイルから読み込む
        :param file_name: ファイル名
        :return: None
        """

        self._logger.info('--- enter [BagOfVisualWords.load_visual_words] ---')

        self._visual_words = self.read_file(file_name)

        self._logger.info('--- exit [BagOfVisualWords.load_visual_words] ---')

    def get_histogram(self, img):
        """
        入力画像に対応するヒストグラムを取得する
        :param img: 入力画像
        :return: ヒストグラム
        """

        self._logger.debug('--- enter [BagOfVisualWords.get_histogram] ---')

        # 特徴検出と特徴量の記述
        kp, des = self._detector.detectAndCompute(img, None)

        # キーポイントが検出されなかった場合は、0ベクトルを仮置き
        if des is None:
            self._logger.warning('No keypoints are detected')
            des = np.zeros((1, self._dim))

        hist = [0] * 128

        # 特徴ベクトルごとのループ
        for feature in des:

            # 各Visual Wordとの距離を計算し、距離が最小となるVisual Wordを見つける
            min_dist = None
            min_index = 0
            for vw_index, visual_word in enumerate(self._visual_words):
                dist = np.power(feature - visual_word, 2).sum()

                if min_dist is None or min_dist > dist:
                    min_dist = dist
                    min_index = vw_index

            # もっとも距離が近かったVisual Wordに投票する
            hist[min_index] += 1

        self._logger.debug('--- exit [BagOfVisualWords.get_histogram] ---')

        return hist

    def create_data_set(self, src_dir):
        """
        すべてのテンプレート画像を読み込み、ヒストグラムを作成する。
        作成したヒストグラムはデータセットとして保持する
        :param src_dir:
        :return: None
        """

        self._logger.info('--- enter [BagOfVisualWords.create_data_set] ---')

        hists = []
        classes = []

        # 子ディレクトリ（クラスごと）の取得
        child_dir_list = os.listdir(src_dir)

        # クラスごとのループ
        image_index = 0
        for class_index, dir_name in enumerate(tqdm(child_dir_list)):

            # 画像ファイル名の取得
            file_list = os.listdir(os.path.join(src_dir, dir_name))

            # 画像ごとのループ
            for file_name in file_list:

                image_index += 1

                # 画像ごとのヒストグラムを生成
                self._logger.debug('Calculating histogram of image #{0}'.format(image_index))
                img = cv2.imread(os.path.join(src_dir, dir_name, file_name))
                hists.append(self.get_histogram(img))
                classes.append(class_index)

        self._X = np.array(hists)
        self._Y = np.array(classes)
        self._num = image_index

        self._logger.info('--- exit [BagOfVisualWords.create_data_set] ---')

    def save_data_set(self, file_name_X, file_name_Y):
        """
        データセットをファイルに保存する
        :param file_name_X: データXのファイル名
        :param file_name_Y: データYのファイル名
        :return: None
        """
        self._logger.info('--- enter [BagOfVisualWords.save_data_set] ---')

        self._write_file_2d(self._X, file_name_X)
        self._write_file_1d(self._Y, file_name_Y)

        self._logger.info('--- exit [BagOfVisualWords.save_data_set] ---')
