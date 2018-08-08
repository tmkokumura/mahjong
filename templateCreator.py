#coding:utf-8
import cv2
import numpy as np
import os
import sys

from imageProccessing import ImageProccessing


def resize(src, x_scale, y_scale):
    """
    リサイズする
    :param src: 入力画像
    :param x_scale: x方向の倍率
    :param y_scale: y方向の倍率
    :return: リサイズ画像
    """
    hight = src.shape[0]
    width = src.shape[1]

    return cv2.resize(src, (int(width * x_scale), int(hight * y_scale)))

def rotate(src, angle):
    """
    画像を回転する。回転に合わせてサイズも自動調整される。
    :param src: 入力画像
    :param angle: 回転角度
    :return: 回転後の画像
    """
    hight = src.shape[0]
    width = src.shape[1]
    angle_rad = angle/180.0*np.pi

    # 回転後の画像サイズを計算
    w_rot = int(np.round(hight * np.absolute(np.sin(angle_rad)) + width * np.absolute(np.cos(angle_rad))))
    h_rot = int(np.round(hight * np.absolute(np.cos(angle_rad)) + width * np.absolute(np.sin(angle_rad))))
    size_rot = (w_rot, h_rot)

    # 元画像の中心を軸に回転する
    center = (width/2, hight/2)
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)

    # 平行移動を加える (rotation + translation)
    affine_matrix = rotation_matrix.copy()
    affine_matrix[0][2] = affine_matrix[0][2] -width/2 + w_rot/2
    affine_matrix[1][2] = affine_matrix[1][2] -hight/2 + h_rot/2

    return cv2.warpAffine(resized_img, affine_matrix, size_rot, flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))


def correct_gamma(src, gamma):
    """
    ガンマ補正を行う
    :param src: 入力画像
    :param gamma: ガンマ（1より小さいと暗く、1より大きいと明るくなる）
    :return: ガンマ補正後の画像
    """
    gamma_cvt = np.zeros((256, 1), dtype='uint8')
    for i in range(256):
        gamma_cvt[i][0] = 255 * (float(i) / 255) ** (1.0 / gamma)

    return cv2.LUT(src, gamma_cvt)

def paste(src, background):
    """
    背景画像の上に入力画像を張り付ける
    :param src: 入力画像
    :param background: 背景画像
    :return: 貼付後の画像
    """

    # 背景画像を加える
    bg_height, bg_width = background.shape[:2]
    height, width = src.shape[:2]

    # 貼り付け位置を計算
    paste_y = int((bg_height - height) / 2)
    paste_x = int((bg_width - width) / 2)

    transparent = np.full(3, 255)

    # 背景画像を入力画像で上書きする
    dst = background.copy()
    for i in range(paste_y, paste_y + height):
        for j in range(paste_x, paste_x + width):
            # 入力画像が黒色の場合は透過扱い
            color = src[i - paste_y][j - paste_x]
            if not np.allclose(transparent, color):
                dst[i][j] = color

    return dst

###############################################
# テンプレート画像を量産するスクリプト
# リサイズ・回転・ガンマ補正を行う
###############################################
if __name__ == '__main__':

    src_dir = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\original\\'
    dst_dir = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\template\\'

    # オリジナルファイルの一覧を取得
    file_list = os.listdir(src_dir)
    print(file_list)

    # 背景画像の読み込み
    bg_file_name = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\windowsapp\\background\\background.bmp'
    bg_img = cv2.imread(bg_file_name)


    for src_file_name in file_list:

        print('処理対象: ' + src_file_name)

        index = 0

        # 入力画像の読み込み
        src_img = ImageProccessing.readImage(src_dir + src_file_name)

        # リサイズ
        scales = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.05]
        for scale in scales:
            resized_img = resize(src_img, scale, scale)

            # 回転
            angles = [0, 2, 88, 90, 92, 178, 180, 182, 268, 270, 272, 358]
            for angle in angles:
                rotated_img = rotate(resized_img, angle)

                # ガンマ補正
                gammas = [0.4, 0.7, 1.0, 1.3]
                for gamma in gammas:
                    gamma_corrected_img = correct_gamma(rotated_img, gamma)

                    # 背景画像の上に張り付け
                    dst_img = paste(gamma_corrected_img, bg_img)

                    # 画像を保存
                    index += 1
                    tmp_list = src_file_name.split('.')
                    dst_file_name = tmp_list[0] + '_' + str(index).zfill(4) + '.' + tmp_list[1]
                    cv2.imwrite(dst_dir + dst_file_name, dst_img)
