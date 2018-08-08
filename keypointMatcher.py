# coding:utf-8

import cv2
import numpy as np
from imageProccessing import ImageProccessing

file_name1 = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\window.bmp'
file_name2 = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\template\\haku\\haku_0081.bmp'
img1 = ImageProccessing.readImage(file_name1)
img2 = ImageProccessing.readImage(file_name2)

# SIFT(https://qiita.com/hitomatagi/items/62989573a30ec1d8180b)

detector = cv2.xfeatures2d.SIFT_create()

# 特徴検出と特徴量の記述
kp1, des1 = detector.detectAndCompute(img1, None)
kp2, des2 = detector.detectAndCompute(img2, None)

# 画像への特徴点の書き込み
kp_img1 = cv2.drawKeypoints(img1, kp1, None)
kp_img2 = cv2.drawKeypoints(img2, kp2, None)
cv2.imshow('kp_img1', kp_img1)
cv2.imshow('kp_img2', kp_img2)
cv2.waitKey()

# マッチング
matcher = cv2.BFMatcher()
matches = matcher.match(des1, des2)

# Sort them in the order of their distance.
matches = sorted(matches, key=lambda x: x.distance)

# 画像への一致点の書き込み
match_img = cv2.drawMatches(img1, kp1, img2, kp2, matches[:20], None, flags=2)

# 少し大きすぎるのでリサイズ
hight = match_img.shape[0]
width = match_img.shape[1]
scale = 0.8
result = cv2.resize(match_img, (int(width * scale), int(hight * scale)))

# 画像への特徴点の書き込み
keypoint_img = cv2.drawKeypoints(img2, kp2, None)
cv2.imshow('keypoints', keypoint_img)
cv2.waitKey()

#cv2.imwrite('C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\app_window\\keypoints.jpg', out)
# 表示
cv2.imshow('match', result)
cv2.waitKey()
