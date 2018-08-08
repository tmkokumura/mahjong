# coding:utf-8

###########################################
# 麻雀牌をBag of Visual Wordsで分類する
###########################################

import cv2
import os
import numpy as np
from sklearn.cluster import MiniBatchKMeans
import fileUtils as fu
import logging


def train(indexes):
    logging.info('--- start training ---')
    ###########################################
    # 1.すべてのテンプレートを読み込み、SIFT特徴量を計算する
    ###########################################
    logging.info('calculating SIFT features')

    src_dir = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\template'
    child_dir_list = os.listdir(src_dir)

    # SIFT(https://qiita.com/hitomatagi/items/62989573a30ec1d8180b)
    detector = cv2.xfeatures2d.SIFT_create()

    all_features = []          # クラスタリング用にすべての特徴を保持する
    class_features = []        # 投票用の特徴を保持する

    # クラスごとのループ
    for dir_name in child_dir_list:
        img_features = []

        # 画像ごとのループ
        for index in indexes:
            file_name = dir_name + '_' + '{0:04d}'.format(index) + '.bmp'
            file_path = os.path.join(src_dir, dir_name, file_name)
            img = cv2.imread(file_path)

            # 特徴検出と特徴量の記述
            logging.debug('calculating SIFT features of ' + file_name)
            kp, des = detector.detectAndCompute(img, None)

            # キーポイントが検出されなかった場合
            if des is None:
                des = np.zeros((1, 128))

            all_features.extend(des)
            img_features.append(des)

        class_features.append(img_features)

    ###########################################
    # 2.特徴量を128個のクラスタにクラスタリングし
    # 各クラスタのセントロイド（＝Visural Word）を計算する
    ###########################################
    logging.info('calculating visual words')

    # https://blanktar.jp/blog/2016/03/python-visual-words.html
    visual_words = MiniBatchKMeans(n_clusters=128).fit(all_features).cluster_centers_
    fu.write_2d_list('C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\model\\visual_words.txt', visual_words)

    ###########################################
    # 3.牌ごとにクラスタへの投票を行い、ヒストグラムを作成する
    ###########################################
    logging.info('calculating histogram')

    hists = []
    classes = []

    # クラスごとのループ
    image_index = 0
    for class_index, img_features in enumerate(class_features):

        # 画像ごとのループ
        for features in img_features:
            image_index += 1
            logging.debug('calculating histogram of image #{}'.format(image_index))

            hist = [0] * 128

            # 特徴ベクトルごとのループ
            for feature in features:

                # 各Visual Wordとの距離を計算し、距離が最小となるVisual Wordを見つける
                min_dist = None
                min_index = 0
                for vw_index, visual_word in enumerate(visual_words):
                    dist = np.power(feature - visual_word, 2).sum()

                    if min_dist is None or min_dist > dist:
                        min_dist = dist
                        min_index = vw_index

                # もっとも距離が近かったVisual Wordに投票する
                hist[min_index] += 1

            # 画像ごとのヒストグラムを保存する
            hists.append(hist)
            classes.append(class_index)

    ###########################################
    # 4.ヒストグラムをSVMに投入し、学習する
    ###########################################
    logging.info('training SVM')
    # https://algorithm.joho.info/programming/python/hog-svm-classifier-py/#Python3OpenCV34

    svm = cv2.ml.SVM_create()
    svm.setType(cv2.ml.SVM_C_SVC)
    svm.setKernel(cv2.ml.SVM_RBF)
    # svm.setDegree(0.0)
    # svm.setGamma(0.0)
    # svm.setCoef0(0.0)
    # svm.setC(0)
    # svm.setNu(0.0)
    # svm.setP(0.0)
    # svm.setClassWeights(None)
    svm.setTermCriteria((cv2.TERM_CRITERIA_COUNT, 100, 1.e-06))
    svm.train(np.array(hists).astype(np.float32), cv2.ml.ROW_SAMPLE, np.array(classes))
    svm.save('C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\model\\svm.dat')

    logging.info('--- end training ---')

def predict(indexes):
    logging.info('--- start predicting ---')

    ###########################################
    # 5.テストデータからSIFT特徴量を計算する
    ###########################################
    logging.info('calculating sift features')

    src_dir = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\template'
    child_dir_list = os.listdir(src_dir)

    # SIFT(https://qiita.com/hitomatagi/items/62989573a30ec1d8180b)
    detector = cv2.xfeatures2d.SIFT_create()

    img_features = []          # クラスタリング用にすべての特徴を保持する
    img_classes = []

    # 子ディレクトリにクラスごとのテンプレートが格納されている
    for class_index, dir_name in enumerate(child_dir_list):
        for index in indexes:

            file_name = dir_name + '_' + '{0:04d}'.format(index) + '.bmp'
            file_path = os.path.join(src_dir, dir_name, file_name)
            img = cv2.imread(file_path)

            # 特徴検出と特徴量の記述
            logging.debug('detecting and computing on {0}'.format(file_name))
            kp, des = detector.detectAndCompute(img, None)

            # キーポイントが検出されなかった場合、ゼロベクトルを仮置き
            if des is None:
                des = np.zeros((1, 128))

            img_features.append(des)
            img_classes.append(class_index)

    ###########################################
    # 6. 特徴ベクトルをvisual wordsのヒストグラムに変換する
    ###########################################
    logging.info('calculating visual words histogram')

    hists = []
    visual_words = fu.read_2d_nparray('C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\model\\visual_words.txt')

    # 画像ごとのループ
    for img_index, features in enumerate(img_features):
        logging.debug('calculating histogram of image #{}'.format(img_index))

        hist = [0] * 128

        # 特徴ベクトルごとのループ
        for feature in features:

            # 各Visual Wordとの距離を計算し、距離が最小となるVisual Wordを見つける
            min_dist = None
            min_index = 0
            for vw_index, visual_word in enumerate(visual_words):
                dist = np.power(feature - visual_word, 2).sum()

                if min_dist is None or min_dist > dist:
                    min_dist = dist
                    min_index = vw_index

            # もっとも距離が近かったVisual Wordに投票する
            hist[min_index] += 1

        # 画像ごとのヒストグラムを保存する
        hists.append(hist)

    ###########################################
    # 7. ヒストグラムをSVMに投入し、クラスを予測する
    ###########################################
    logging.info('predicting class by svm')

    svm = cv2.ml.SVM_load('C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\model\\svm.dat')

    # 予測結果の評価
    pred = svm.predict(np.array(hists).astype(np.float32))
    pred_ = pred[1]

    corr_count = 0
    data_num = len(pred_)
    for i in range(data_num):
        class_label = img_classes[i]
        class_predict = int(pred_[i][0])
        result = (class_label == class_predict)
        if result:
            corr_count += 1
        logging.debug('ラベル:{0} 予想クラス:{1} 正誤:{2}'.format(class_label, class_predict, result))

    acc = corr_count / data_num
    logging.info('正解率:{0}'.format(acc))

    logging.info('--- end predicting ---')

    return data_num, corr_count, acc


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.DEBUG)
    np.set_printoptions(linewidth=200)

    #######################################
    # クロスバリデーション
    #######################################
    n = 336            # 各クラスのデータ数
    cv_sets = 5        # クロスバリデーションのセット数

    data_num = 0
    corr_count = 0
    for i in range(cv_sets):
        logging.info('start cross validation #{0}'.format(i))

        training_data_indexes = [j for j in range(1, n + 1) if j % cv_sets != i]
        test_data_indexes = [j for j in range(1, n + 1) if j % cv_sets == i]
        train(training_data_indexes)
        data_num_, corr_count_, acc_ = predict(test_data_indexes)
        data_num += data_num_
        corr_count += corr_count_

    acc = corr_count / data_num
    logging.info('平均正解率:{0}'.format(acc))



