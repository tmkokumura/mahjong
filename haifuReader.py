#coding:utf-8

import codecs
import datetime
from shiaiModel import ShiaiModel
from shiaiModel import KyokuModel
import fileUtils as fu

class HaifuReader():

    # private method
    # 飜の取得
    def get_han(self, word):
        return word.strip("ツモ").strip("ロン")

    # private method
    # ツモ／ロン区分の取得
    def get_tsumo_ron_kbn(self, word):
        if word.find("ツモ") >= 0:
            return 0
        elif word.find("ロン") >= 0:
            return 1
        else:
            return 9

    # private method
    # ヘッダ行のパース
    def parse_header(self, words):
        tonpu_nanpu_kbn = 9
        taku_name1 = ""
        taku_name2 = ""
        start_y = 1900
        start_m = 1
        start_d = 1
        start_h = 0
        start_mi = 0
        start_s = 0

        # 単語でループ
        for index, word in enumerate(words):
            if index == 1:
                ton_nan_kbn_str = word[:3]
                taku_name1 = word[3:]

                if ton_nan_kbn_str == "東風戦":
                    tonpu_nanpu_kbn = 0
                elif ton_nan_kbn_str == "東南戦":
                    tonpu_nanpu_kbn = 1

            elif index == 2:
                taku_name2 = word

            elif index == 4:
                start_y = int(word[:4])
                start_m = int(word[5:7])
                start_d = int(word[8:10])

            elif index == 5:
                start_h = int(word[:2])
                start_mi = int(word[3:5])

        start_dt = datetime.datetime(start_y, start_m, start_d, start_h, start_mi, start_s)


        return tonpu_nanpu_kbn, taku_name1, taku_name2, start_dt

    # private method
    # 持ち点・プレイヤー行のパース
    def parse_players(self, words):
        mochiten = 0
        player_1_name = ""
        player_1_rate = 0
        player_2_name = ""
        player_2_rate = 0
        player_3_name = ""
        player_3_rate = 0
        player_4_name = ""
        player_4_rate = 0

        # 単語でループ
        for index, word in enumerate(words):
            if index == 0:
                mochiten = int(word[2:])
            elif index == 1:
                player_1_name = word[3:]
            elif index == 2:
                player_1_rate = int(word[1:])
            elif index == 3:
                player_2_name = word[3:]
            elif index == 4:
                player_2_rate = int(word[1:])
            elif index == 5:
                player_3_name = word[3:]
            elif index == 6:
                player_3_rate = int(word[1:])
            elif index == 7:
                player_4_name = word[3:]
            elif index == 8:
                player_4_rate = int(word[1:])

        return mochiten, player_1_name, player_1_rate, player_2_name, player_2_rate, player_3_name, player_3_rate, player_4_name, player_4_rate

    # private method
    # 局の開始行のパース
    def parse_kyoku_header(self, words):
        kyoku_kbn = -1
        honba_num = -1
        richibo_num = -1
        tokuten_map = {}

        # 内部変数
        player_name = ""
        player_name_flag = True

        # 単語でループ
        for index, word in enumerate(words):
            if index == 0:
                if word[0] == "東":
                    kyoku_kbn = -1
                elif word[0] == "南":
                    kyoku_kbn = 3
                elif word[0] == "西":
                    kyoku_kbn = 7
                elif word[0] == "北":
                    kyoku_kbn = 11

                kyoku_kbn += int(word[1])

            elif index == 1:
                hon_index = word.find("本")
                honba_num = int(word[:hon_index])

                chi_index = word.find("チ")
                richibo_num = int(word[chi_index + 1].strip(")"))

            else:
                # 得点者の名前と点数をマップに保存する
                if player_name_flag:
                    player_name = word
                    player_name_flag = False
                else:
                    tokuten_map.update({player_name: int(word)})
                    player_name_flag = True


        return kyoku_kbn, honba_num, richibo_num, tokuten_map

    #局の結果行のパース
    def parse_kyoku_result(self, words):
        fusu = 0
        han = 0
        tsumo_ron_kbn = 9
        ryukyoku_flag = False
        kyusyukyuhai_flag = False
        yaku_list = []
        dorasu = 0

        # 内部判定用フラグ
        manganmiman_flag = False

        # 単語でループ
        for index, word in enumerate(words):
            if index == 0:
                # 流局の場合
                if word == "流局":
                    ryukyoku_flag = True

                #九種九牌の場合
                if word == "九種公九牌倒牌":
                    kyusyukyuhai_flag = True

                # 満貫未満の場合
                elif word.find("符") >= 0:
                    fusu = int(word.strip("符"))
                    manganmiman_flag = True

                # 満貫以上の場合
                else:
                    han = self.get_han(word)
                    tsumo_ron_kbn = self.get_tsumo_ron_kbn(word)

            else:
                # 満貫未満の場合、２単語目で飜とツモ／ロンを取得する
                if manganmiman_flag:
                    han = self.get_han(word)
                    tsumo_ron_kbn = self.get_tsumo_ron_kbn(word)
                    manganmiman_flag = False
                    continue

                yaku_list.append(word)

                if word[0:2] == "ドラ":
                    dorasu = int(word[2:])

        return fusu, han, tsumo_ron_kbn, ryukyoku_flag, kyusyukyuhai_flag, yaku_list, dorasu

    # 配牌行のパース
    def parse_haipai(self, words):
        kaze = words[0][2]
        haipai = words[0][4:]
        return kaze, haipai

    # ドラ行のパース
    def parse_dora(self, words):
        omotedora = words[0][5:]
        uradora = words[1][5:]
        return omotedora, uradora

    # 牌譜行のパース
    def parse_haifu(self, words):
        haifu_list = []

        # 単語でループ
        for index, word in enumerate(words):
            # 1単語目は"*"のため無視する
            if index > 0:
                haifu_list.append(word)

        return haifu_list

    # 試合結果行のパース
    def parse_result(self, words):
        player_name = words[1]
        player_score = int(words[2])
        return player_name, player_score

    # 試合終了行のパース
    def parse_end(self, words):
        end_y = int(words[3][:4])
        end_m = int(words[3][5:7])
        end_d = int(words[3][8:10])
        end_h = int(words[4][:2])
        end_mi = int(words[4][3:5])
        end_s = 0

        return datetime.datetime(end_y, end_m, end_d, end_h, end_mi, end_s)


    #######################################
    # 牌譜を読み込み、試合モデルのリストを返却する
    #######################################
    def read(self, file_name):
        # 変数の初期化
        shiai_list = []

        tonpu_nanpu_kbn = 9
        taku_name1 = ""
        taku_name2 = ""
        start_dt = datetime.datetime(1900, 1, 1, 0, 0, 0)
        mochiten = 0
        player_1_name = ""
        player_1_rate = 0
        player_2_name = ""
        player_2_rate = 0
        player_3_name = ""
        player_3_rate = 0
        player_4_name = ""
        player_4_rate = 0
        kyoku_list = []
        kyoku_kbn = 0
        honba_num = 0
        richibo_num = 0
        tokuten_map = {}
        fusu = 0
        han = ""
        tsumo_ron_kbn = 9
        ryukyoku_flag = False
        kyusyukyuhai_flag = False
        yaku_list = []
        dorasu = 0
        player_1_kaze = ""
        player_1_haipai = ""
        player_2_kaze = ""
        player_2_haipai = ""
        player_3_kaze = ""
        player_3_haipai = ""
        player_4_kaze = ""
        player_4_haipai = ""
        omotedora = ""
        uradora = ""
        haifu_list = []
        result_1st_player_name = ""
        result_1st_player_score = 0
        result_2nd_player_name = ""
        result_2nd_player_score = 0
        result_3rd_player_name = ""
        result_3rd_player_score = 0
        result_4th_player_name = ""
        result_4th_player_score = 0

        kyoku_start_flag = False

        # ファイル読み込み
        lines = fu.read_file(file_name)

        # 行区分
        line_kbn = 0

        # 行でループ
        for line in lines:
            words = line.split()

            if len(words) == 0:
                continue

            # 試合の開始行の場合、局リストをクリアして行区分をリセット
            if words[0] == "=====":
                line_kbn = 0
                kyoku_list.clear()

            # 局の開始行の場合、行区分をセット
            elif words[0][0] == "東" or words[0][0] == "南" or words[0][0] == "西" or words[0][0] == "北":
                line_kbn = 2

                # 2局目以降の場合、前局のモデルを生成
                if kyoku_start_flag:
                    kyoku = KyokuModel(kyoku_kbn, honba_num, richibo_num, tokuten_map, fusu, han, tsumo_ron_kbn,
                                       ryukyoku_flag, kyusyukyuhai_flag, yaku_list, dorasu, player_1_kaze,
                                       player_1_haipai, player_2_kaze, player_2_haipai, player_3_kaze, player_3_haipai,
                                       player_4_kaze, player_4_haipai, omotedora, uradora, haifu_list[:])
                    kyoku_list.append(kyoku)

                kyoku_start_flag = True
                haifu_list.clear()

            # 牌譜行の場合、行区分をセット
            elif words[0] == "*":
                line_kbn = 10

            # 試合結果行の場合、行区分をセット
            elif words[0] == "----":
                line_kbn = 11

                if kyoku_start_flag:
                    kyoku = KyokuModel(kyoku_kbn, honba_num, richibo_num, tokuten_map, fusu, han, tsumo_ron_kbn,
                                       ryukyoku_flag, kyusyukyuhai_flag, yaku_list, dorasu, player_1_kaze,
                                       player_1_haipai, player_2_kaze, player_2_haipai, player_3_kaze, player_3_haipai,
                                       player_4_kaze, player_4_haipai, omotedora, uradora, haifu_list)
                    kyoku_list.append(kyoku)

                kyoku_start_flag = False

            # 行区分で処理を分岐
            # ヘッダ行
            if line_kbn == 0:
                tonpu_nanpu_kbn, taku_name1, taku_name2, start_dt = self.parse_header(words)

            # 持ち点・プレイヤー行
            elif line_kbn == 1:
                mochiten, player_1_name, player_1_rate, player_2_name, player_2_rate, player_3_name, player_3_rate, player_4_name, player_4_rate = self.parse_players(
                    words)

            # 局の開始行
            elif line_kbn == 2:
                kyoku_kbn, honba_num, richibo_num, tokuten_map = self.parse_kyoku_header(words)

            # 局の結果行
            elif line_kbn == 3:
                fusu, han, tsumo_ron_kbn, ryukyoku_flag, kyusyukyuhai_flag, yaku_list, dorasu = self.parse_kyoku_result(words)

            # プレイヤー1の配牌行
            elif line_kbn == 4:
                player_1_kaze, player_1_haipai = self.parse_haipai(words)

            # プレイヤー2の配牌行
            elif line_kbn == 5:
                player_2_kaze, player_2_haipai = self.parse_haipai(words)

            # プレイヤー3の配牌行
            elif line_kbn == 6:
                player_3_kaze, player_3_haipai = self.parse_haipai(words)

            # プレイヤー4の配牌行
            elif line_kbn == 7:
                player_4_kaze, player_4_haipai = self.parse_haipai(words)

            # ドラ行
            elif line_kbn == 8:
                omotedora, uradora = self.parse_dora(words)

            # 牌譜行
            elif line_kbn == 10:
                haifu_list.extend(self.parse_haifu(words))

            # 試合結果（1位）行
            elif line_kbn == 12:
                result_1st_player_name, result_1st_player_score = self.parse_result(words)

            # 試合結果（2位）行
            elif line_kbn == 13:
                result_2nd_player_name, result_2nd_player_score = self.parse_result(words)

            # 試合結果（3位）行
            elif line_kbn == 14:
                result_3rd_player_name, result_3rd_player_score = self.parse_result(words)

            # 試合結果（4位）行
            elif line_kbn == 15:
                result_4th_player_name, result_4th_player_score = self.parse_result(words)

            # 試合終了行
            elif line_kbn == 16:
                end_dt = self.parse_end(words)

                # 試合モデルを生成
                shiai = ShiaiModel(tonpu_nanpu_kbn, taku_name1, taku_name2, start_dt, mochiten, player_1_name,
                                   player_1_rate, player_2_name, player_2_rate, player_3_name, player_3_rate,
                                   player_4_name, player_4_rate, kyoku_list, result_1st_player_name, result_1st_player_score,
                                   result_2nd_player_name, result_2nd_player_score, result_3rd_player_name,
                                   result_3rd_player_score, result_4th_player_name, result_4th_player_score, end_dt)
                shiai_list.append(shiai)

            line_kbn += 1

        return shiai_list