#! coding: utf-8

import cv2
import numpy as np

def imshow_small(img):
    hight = img.shape[0]
    width = img.shape[1]
    scale = 0.8
    small = cv2.resize(img, (int(width * scale), int(hight * scale)))
    cv2.imshow('image', small)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 手牌領域
tehai_x = 204
tehai_y = 672
tehai_width = 665
tehai_height = 81
tehai_area_min = 2000
tehai_area_max = 4000


# 河領域
ho1_x = 385
ho1_y = 436
ho1_width = 341
ho1_height = 136
ho1_area_min = 1400
ho1_area_max = 2500

# 下家の河領域
ho4_x = 231
ho4_y = 273
ho4_width = 181
ho4_height = 247
ho4_area_min = 500
ho4_area_max = 9999

# 処理対象領域（ここを変更する）
target_x = ho1_x
target_y = ho1_y
target_width = ho1_width
target_height = ho1_height
area_min = ho1_area_min
area_max = ho1_area_max

# 画像を読込
window = cv2.imread('C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\window.bmp', cv2.IMREAD_COLOR)

# 手牌領域を切り出す
target = window[target_y:target_y + target_height, target_x:target_x + target_width]

# グレースケール画像へ変換
gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

# 2値化
bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)
imshow_small(bw)

# 輪郭を抽出
img, contours, hierarchy = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# 矩形検出された数（デフォルトで0を指定）
detect_count = 0

# 各輪郭に対する処理
for i in range(0, len(contours)):

    # 輪郭の領域を計算
    area = cv2.contourArea(contours[i])

    # 外接矩形
    if len(contours[i]) > 0:
        rect = contours[i]
        x, y, w, h = cv2.boundingRect(rect)

        # 面積によるフィルタリング
        area = w * h
        if area < area_min or area_max < area:
            continue

        # 検出した矩形をオリジナル画像に書き込む
        cv2.rectangle(window, (target_x + x, target_y + y), (target_x + x + w, target_y + y + h), (0, 255, 0), 2)

# 外接矩形された画像を表示
imshow_small(window)

