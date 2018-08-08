#coding:utf-8
import shantenCalculator
ShantenCalculator = shantenCalculator.ShantenCalculator()

import imageProccessing
ImageProccessing = imageProccessing.ImageProccessing()

from time import sleep

from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld

import haifuReader
HaifuReader = haifuReader.HaifuReader()

import stringUtils as su

import logging
import numpy as np
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)
np.set_printoptions(linewidth=200)

###########################
# 手牌ファイルを読み込む
###########################
def readTehaiFile(fileName):
    # 配列の初期化
    tehaiList = []
    shantenList = []

    # ファイルを１行ずつ読み込み
    f = open(fileName, "r")
    text = f.readline()

    while text:
        # 末尾の改行コードを削除し、カンマで分割して配列に格納
        line = text.replace("\n","")
        list = line.split(",")

        # 最後の項目はシャン点数とする
        shantenList.append(int(list[len(list) - 1]))
        list.pop(len(list) - 1)

        # 残りを手牌として取り込む
        tehaiList.append([int(x) for x in list])

        text = f.readline()

    f.close()

    return tehaiList, shantenList


###########################
# メインスクリプト
###########################

# tehaiList, shantenList = readTehaiFile("C:\\Users\\okumura.tomoki\\Desktop\\test.txt")


# for tehai in tehaiList:
#   shantenNomal = ShantenCalculator.calcShantenNormal(tehai)
#    print("標準手のシャンテン数：{0}".format(shantenNomal))

# while True:
#    flag, tehaiList = ImageProccessing.readTenhoWindow()
#    if flag:
#        print(tehaiList)
#    else:
#        print("ウインドウが検出できませんでした。")
#    sleep(5)



###################################
# あがり役と点数を出力する
###################################

# def print_result(result):
#     print('{0}翻 {1}符'.format(result.han, result.fu))
#     if result.cost['additional'] > 0:
#         print('支払い（親）:{0}'.format(result.cost['main']))
#         print('支払い（子）:{0}'.format(result.cost['additional']))
#     else:
#         print('支払い:{0}'.format(result.cost['main']))
#     print('あがり役:{0}'.format(result.yaku))
#     if result.fu_details is not None:
#         print('符の内訳')
#         for fu_item in result.fu_details:
#             print(fu_item)
#
# shiai_list = HaifuReader.read("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\haifu\\test.txt")
# tehai_list, ho_list, richi_list, agari_list, agarihai, junme_list = shiai_list[0].kyoku_list[0].get_tehai(-1)
# print(tehai_list[0])
# print(ho_list[0])
# print(richi_list[0])
# print(agari_list[0])
#
# calculator = HandCalculator()
# tehai_man = tehai_list[0]['man']
# tehai_pin = tehai_list[0]['pin']
# tehai_sou = tehai_list[0]['sou']
# tehai_honors = tehai_list[0]['honors']
# tiles = TilesConverter.string_to_136_array(man=tehai_man, pin=tehai_pin, sou=tehai_sou, honors=tehai_honors)
#
# agari_man = agarihai['man']
# agari_pin = agarihai['pin']
# agari_sou = agarihai['sou']
# agari_honors = agarihai['honors']
# win_tile = TilesConverter.string_to_136_array(man=agari_man, pin=agari_pin, sou=agari_sou, honors=agari_honors)[0]
#
# dora = TilesConverter.string_to_136_array(pin='24')
# hand_config = HandConfig(
#     is_tsumo=True,
#     is_riichi=True,
# )
#
# hand_value = calculator.estimate_hand_value(tiles, win_tile, dora_indicators=dora, config=hand_config)
# print_result(hand_value)


cv_sets = 5  # クロスバリデーションのセット数



#     logging.info('start cross validation #{0}'.format(i))
#
#     training_data_indexes = [j for j in range(1, n + 1) if j % cv_sets != i]
#     test_data_indexes = [j for j in range(1, n + 1) if j % cv_sets == i]
#     train(training_data_indexes)
#     data_num_, corr_count_, acc_ = predict(test_data_indexes)
#     data_num += data_num_
#     corr_count += corr_count_


# acc = corr_count / data_num
# logging.info('平均正解率:{0}'.format(acc))