#coding:utf-8

import codecs
import numpy as np


def read_file(file_name, encode='shift_jisx0213'):
    """
    ファイルを読み込む
    :param file_name:
    :param encode:
    :return:
    """
    f = codecs.open(file_name, 'r', encode)
    lines = f.readlines()
    f.close()
    return lines


def write_2d_list(file_name, list):
    """
    2次元配列をファイルに出力する
    :param file_name: 出力ファイル名
    :param list: 二次元配列
    :return: None
    """
    file = open(file_name, 'w')
    for row, line in enumerate(list):
        for col, word in enumerate(line):
            file.write(str(word))
            if col < len(line) - 1:
                file.write(',')
        if row < len(list) - 1:
            file.write('\n')
    file.close()


def read_2d_nparray(file_name, encode='shift_jisx0213'):
    """
    ファイルを読み込み、二次元のnumpy配列として返す
    :param file_name: ファイル名
    :param encode: ファイルエンコード
    :return: numpy配列
    """
    lines = read_file(file_name, encode)
    row = []
    for line in lines:
        # 末尾の改行を除去してカンマで分割
        data_str = line.strip('\r\n').split(',')

        # 数値型に変換
        cols = [float(i) for i in data_str]
        row.append(cols)

    return np.array(row)
