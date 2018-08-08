#coding:utf-8
import cv2
import numpy as np
from PIL import ImageGrab

import win32gui
import win32ui
import win32con
from PIL import Image

class ImageProccessing():

    ##############################
    # 画像を読み込む
    ##############################
    @classmethod
    def readImage(self, filename):
        return cv2.imread(filename)

    ##############################
    # 画像をトリミングする
    ##############################
    def trimImage(self, src, x, y, width, height):
        return src[y:y + height, x:x + width]

    ##############################
    # 手牌のテンプレート画像を読み込む
    ##############################
    def readTehaiTemplate(self):

        # リサイズ
        width = 54
        height = 81

        tehaiTemplateList = []
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\m1.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\m2.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\m3.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\m4.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\m5.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\m5r.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\m6.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\m7.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\m8.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\m9.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\p1.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\p2.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\p3.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\p4.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\p5.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\p5r.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\p6.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\p7.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\p8.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\p9.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\s1.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\s2.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\s3.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\s4.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\s5.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\s5r.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\s6.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\s7.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\s8.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\s9.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\ton.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\nan.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\sha.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\pe.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\haku.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\hatsu.bmp"),
                (width, height)))
        tehaiTemplateList.append(
            cv2.resize(
                cv2.imread("C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\chun.bmp"),
                (width, height)))

        return tehaiTemplateList

    ##############################
    # テンプレート番号を牌番号に変換する（赤牌なし）
    ##############################
    def convertTemplate2haiNum(self, index):
        if index == 0:
            return 1
        elif index == 1:
            return 2
        elif index == 2:
            return 3
        elif index == 3:
            return 4
        elif index == 4:
            return 5
        elif index == 5:
            return 5
        elif index == 6:
            return 6
        elif index == 7:
            return 7
        elif index == 8:
            return 8
        elif index == 9:
            return 9
        elif index == 10:
            return 11
        elif index == 11:
            return 12
        elif index == 12:
            return 13
        elif index == 13:
            return 14
        elif index == 14:
            return 15
        elif index == 15:
            return 15
        elif index == 16:
            return 16
        elif index == 17:
            return 17
        elif index == 18:
            return 18
        elif index == 19:
            return 19
        elif index == 20:
            return 21
        elif index == 21:
            return 22
        elif index == 22:
            return 23
        elif index == 23:
            return 24
        elif index == 24:
            return 25
        elif index == 25:
            return 25
        elif index == 26:
            return 26
        elif index == 27:
            return 27
        elif index == 28:
            return 28
        elif index == 29:
            return 29
        elif index == 30:
            return 31
        elif index == 31:
            return 32
        elif index == 32:
            return 33
        elif index == 33:
            return 34
        elif index == 34:
            return 35
        elif index == 35:
            return 36
        elif index == 36:
            return 37
        else:
            return -1

    ##############################
    # windowの左上座標を調べる
    ##############################
    def detectWindowPos(self, window):
        # 一致フラグ
        flag = True

        # テンプレートマッチングの閾値
        threshold = 0.01

        # テンプレート画像の読み込み
        filename = "C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\template\\title.bmp"
        template = cv2.imread(filename)

        # テンプレートマッチング
        res = cv2.matchTemplate(window, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # min_valが閾値より大きい場合は一致なしとする
        if min_val > threshold:
            flag = False

        return flag, min_loc

    ###############################
    # スクリーンキャプチャを取る
    ##############################
    def screenshot(self, filename):
        SCREEN_WIDTH = 1920
        SCREEN_HEIGHT = 1080
        SCREEN_SCALING_FACTOR = 1.5
        window = win32gui.GetDesktopWindow()
        window_dc = win32ui.CreateDCFromHandle(win32gui.GetWindowDC(window))
        compatible_dc = window_dc.CreateCompatibleDC()
        width = SCREEN_WIDTH
        height = SCREEN_HEIGHT
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(window_dc, width, height)
        compatible_dc.SelectObject(bmp)
        compatible_dc.BitBlt((0, 0), (width, height), window_dc, (0, 0), win32con.SRCCOPY)
        img = Image.frombuffer('RGB', (width, height), bmp.GetBitmapBits(True), 'raw', 'BGRX', 0, 1)
        img.save(filename)

    ##############################
    # 天鳳画面から手牌情報を読み込む
    ##############################
    def readTenhoWindow(self):
        # 手牌の読み込み結果
        tehaiList = []

        # スクリーンキャプチャ画像のファイル名
        filename = "C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\image\\window\\window.png"

        # スクリーンキャプチャ
        self.screenshot(filename)

        # キャプチャ画像の読み込み
        window = cv2.imread(filename)

        # ウインドウ位置を調べる
        flag, left_top = self.detectWindowPos(window)
        if not flag:
            return False, tehaiList

        # 手牌テンプレート画像の読み込み
        tehaiTemplateList = self.readTehaiTemplate()

        # 手牌左上の座標
        pointList = [
            [left_top[0] + 59, left_top[1] + 727],
            [left_top[0] + 113, left_top[1] + 727],
            [left_top[0] + 167, left_top[1] + 727],
            [left_top[0] + 221, left_top[1] + 727],
            [left_top[0] + 275, left_top[1] + 727],
            [left_top[0] + 329, left_top[1] + 727],
            [left_top[0] + 383, left_top[1] + 727],
            [left_top[0] + 437, left_top[1] + 727],
            [left_top[0] + 491, left_top[1] + 727],
            [left_top[0] + 545, left_top[1] + 727],
            [left_top[0] + 599, left_top[1] + 727],
            [left_top[0] + 653, left_top[1] + 727],
            [left_top[0] + 707, left_top[1] + 727],
            [left_top[0] + 764, left_top[1] + 727]]

        # 手牌画像のサイズ
        width = 54
        height = 81

        for point in pointList:
            # 手牌をトリミング
            tehai = window[point[1] : point[1] + height, point[0] : point[0] + width]

            # テンプレートとマッチング
            min_index = 99
            min_value = 1.0
            threshold = 0.01
            for index, tehaiTemplate in enumerate(tehaiTemplateList):
                res = cv2.matchTemplate(tehai, tehaiTemplate, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if min_value > min_val and threshold > min_val:
                    min_value = min_val
                    min_index = index
            tehaiList.append(self.convertTemplate2haiNum(min_index))

        return True, tehaiList

