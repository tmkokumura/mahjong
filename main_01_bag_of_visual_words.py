import logging
import numpy as np
from feature.bag_of_visual_words import BagOfVisualWords

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.DEBUG)
np.set_printoptions(linewidth=200)

# 変数の初期化
src_dir = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\template'
vw_file_name = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\visual_words\\visual_words.txt'
file_name_X = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\data\\x.txt'
file_name_Y = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\data\\y.txt'

# 1.BagOfVisualWordsインスタンスの初期化
bvw = BagOfVisualWords(BagOfVisualWords.SIFT)

# 2.Visual Wordsの生成
bvw.create_visual_words(src_dir)
# bvw.save_visual_words(vw_file_name)

# 3. データセットの作成
# bvw.load_visual_words(vw_file_name)
# bvw.create_data_set(src_dir)
# bvw.save_data_set(file_name_X, file_name_Y)
