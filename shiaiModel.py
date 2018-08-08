# coding:utf-8

import stringUtils as su
from mahjong.meld import Meld
from mahjong.tile import TilesConverter

###################################
# 局のモデルクラス
###################################
class KyokuModel:
    def __init__(self,
                 _kyoku_kbn,            # 局区分(0:東1局 1:東2局 2:東3局 3:東4局 4:南1局・・・15:北1局)
                 _honba_num,            # n本場
                 _richibo_num,          # 供託リーチ棒の数
                 _tokuten_map,          # 得点者の名前と点数のマップ
                 _fusu,                 # あがり役の符数
                 _han,                  # あがり役の翻
                 _tsumo_ron_kbn,        # ツモ／ロン区分(0:ツモ 1:ロン)
                 _ryukyoku_flag,        # 流局フラグ
                 _kyusyukyuhai_flag,    # 九種九牌フラグ
                 _yaku_list,            # あがり役のリスト
                 _dorasu,               # あがり役のドラ数
                 _player_1_kaze,        # プレイヤー1の風
                 _player_1_haipai,      # プレイヤー1の配牌
                 _player_2_kaze,        # プレイヤー2の風
                 _player_2_haipai,      # プレイヤー2の配牌
                 _player_3_kaze,        # プレイヤー3の風
                 _player_3_haipai,      # プレイヤー3の配牌
                 _player_4_kaze,        # プレイヤー4の風
                 _player_4_haipai,      # プレイヤー4の配牌
                 _omotedora,            # 表ドラ
                 _uradora,              # 裏ドラ
                 _haifu):               # 牌譜
        self.kyoku_kbn = _kyoku_kbn
        self.honba_num = _honba_num
        self.richibo_num = _richibo_num
        self.tokuten_map = _tokuten_map
        self.fusu = _fusu
        self.han = _han
        self.tsumo_ron_kbn = _tsumo_ron_kbn
        self.ryukyoku_flag = _ryukyoku_flag
        self.kyusyukyuhai_flag = _kyusyukyuhai_flag
        # 役リスト
        # 門前清模和, リーチ, ダブルリーチ, 一発, 海底撈月, 河底撈魚, 嶺上開花, 槍槓, 断ヤオ, 平和,
        # 三色同順, 三色同刻,　一盃口, 二盃口, 混一色, 清一色, 一気通貫, 三暗刻, 混老頭, 対々和, 全帯, 純全帯, 小三元,
        # 七対子, 自風, 場風, 白, 発, 中, 天和, 地和, 国士無双, 大三元, 四暗刻, 四暗刻単騎待ち, 小四喜和, 大四喜和,
        # 字一色, 緑一色, 清老頭, 四槓子, 九蓮宝灯, 流し満貫
        self.yaku_list = _yaku_list
        self.dorasu = _dorasu
        self.player_1_kaze = _player_1_kaze
        self.player_1_haipai = _player_1_haipai
        self.player_2_kaze = _player_2_kaze
        self.player_2_haipai = _player_2_haipai
        self.player_3_kaze = _player_3_kaze
        self.player_3_haipai = _player_3_haipai
        self.player_4_kaze = _player_4_kaze
        self.player_4_haipai = _player_4_haipai
        self.omotedora = _omotedora
        self.uradora = _uradora
        self.haifu = _haifu

    def print(self):
        """
        局の内容を出力する
        :return: None
        """
        print("  --- 局 --------------------------")
        print("  局区分(kyoku_kbn): {0}".format(self.kyoku_kbn))
        print("  本場(honba_num): {0}".format(self.honba_num))
        print("  リーチ棒(richibo_num): {0}".format(self.richibo_num))
        print("  得点(tokuten_map): {0}".format(self.tokuten_map))
        print("  あがり役の符数(fusu): {0}".format(self.fusu))
        print("  あがり役の翻(han): {0}".format(self.han))
        print("  ツモ・ロン区分(tsumo_ron_kbn): {0}".format(self.tsumo_ron_kbn))
        print("  流局フラグ(ryukyoku_flag): {0}".format(self.ryukyoku_flag))
        print("  九種九牌フラグ(kyusyukyuhai_flag): {0}".format(self.kyusyukyuhai_flag))
        print("  あがり役(yaku_list): {0}".format(self.yaku_list))
        print("  あがり役のドラ数(dorasu): {0}".format(self.dorasu))
        print("  プレイヤー1の風(player_1_kaze): {0}".format(self.player_1_kaze))
        print("  プレイヤー1の配牌(player_1_haipai): {0}".format(self.player_1_haipai))
        print("  プレイヤー2の風(player_2_kaze): {0}".format(self.player_2_kaze))
        print("  プレイヤー2の配牌(player_2_haipai): {0}".format(self.player_2_haipai))
        print("  プレイヤー3の風(player_3_kaze): {0}".format(self.player_3_kaze))
        print("  プレイヤー3の配牌(player_3_haipai): {0}".format(self.player_3_haipai))
        print("  プレイヤー4の風(player_4_kaze): {0}".format(self.player_4_kaze))
        print("  プレイヤー4の配牌(player_4_haipai): {0}".format(self.player_4_haipai))
        print("  表ドラ(omotedora): {0}".format(self.omotedora))
        print("  裏ドラ(uradora): {0}".format(self.uradora))
        print("  牌譜(haifu): {0}".format(self.haifu))

    def add_hainum_to_tehai(self, hais, hainum):
        """
        haisにhainumを追加し、昇順にソートして返却する
        :param hais: str １種類の牌の数列
        :param hainum: str 追加する牌の番号
        :return: str 牌の文字列
        """
        result = hais + hainum
        return su.sort(result)

    def add_haistr_to_tehai(self, tehai, haistr):
        """
        tehaiにhaistrを追加する
        :param tehai: dictionary
        :param haistr:
        :return: haistrを追加したtehai
        """

        if haistr == '東':
            tehai['honors'] = self.add_hainum_to_tehai(tehai['honors'], '1')
        elif haistr == '南':
            tehai['honors'] = self.add_hainum_to_tehai(tehai['honors'], '2')
        elif haistr == '西':
            tehai['honors'] = self.add_hainum_to_tehai(tehai['honors'], '3')
        elif haistr == '北':
            tehai['honors'] = self.add_hainum_to_tehai(tehai['honors'], '4')
        elif haistr == '白':
            tehai['honors'] = self.add_hainum_to_tehai(tehai['honors'], '5')
        elif haistr == '発':
            tehai['honors'] = self.add_hainum_to_tehai(tehai['honors'], '6')
        elif haistr == '中':
            tehai['honors'] = self.add_hainum_to_tehai(tehai['honors'], '7')
        elif haistr[1] == 'm':
            tehai['man'] = self.add_hainum_to_tehai(tehai['man'], haistr[0])
        elif haistr[1] == 'p':
            tehai['pin'] = self.add_hainum_to_tehai(tehai['pin'], haistr[0])
        elif haistr[1] == 's':
            tehai['sou'] = self.add_hainum_to_tehai(tehai['sou'], haistr[0])

        return tehai

    def delete_hainum_from_tehai(self, hais, hainum):
        """
        haisからhainumを削除する
        :param hais: str １種類の牌の数列
        :param hainum: str 追加する牌の番号
        :return: str 牌の文字列
        """
        index = hais.find(hainum)
        if index == -1:
            return hais
        elif index == 0:
            return hais[index + 1:]
        elif index == len(hais) - 1:
            return hais[:index]
        else:
            return hais[:index] + hais[index + 1:]


    def delete_haistr_from_tehai(self, tehai, haistr):
        """
        haistrで指定された牌を手牌から削除する
        :param haistr:
        :return: haistrを削除した手牌
        """
        if haistr == '東':
            tehai['honors'] = self.delete_hainum_from_tehai(tehai['honors'], '1')
        elif haistr == '南':
            tehai['honors'] = self.delete_hainum_from_tehai(tehai['honors'], '2')
        elif haistr == '西':
            tehai['honors'] = self.delete_hainum_from_tehai(tehai['honors'], '3')
        elif haistr == '北':
            tehai['honors'] = self.delete_hainum_from_tehai(tehai['honors'], '4')
        elif haistr == '白':
            tehai['honors'] = self.delete_hainum_from_tehai(tehai['honors'], '5')
        elif haistr == '発':
            tehai['honors'] = self.delete_hainum_from_tehai(tehai['honors'], '6')
        elif haistr == '中':
            tehai['honors'] = self.delete_hainum_from_tehai(tehai['honors'], '7')
        elif haistr[1] == 'm':
            tehai['man'] = self.delete_hainum_from_tehai(tehai['man'], haistr[0])
        elif haistr[1] == 'p':
            tehai['pin'] = self.delete_hainum_from_tehai(tehai['pin'], haistr[0])
        elif haistr[1] == 's':
            tehai['sou'] = self.delete_hainum_from_tehai(tehai['sou'], haistr[0])

        return tehai

    def naku(self, naki_kbn, haistrs):
        """
        なきの場合、対応するMeldオブジェクトを返却する
        :param naki_kbn:
        :param haistrs:
        :return:
        """

        # ポン
        if naki_kbn == 'N':
            meld_type = Meld.PON

        # チー
        elif naki_kbn == 'C':
            meld_type = Meld.CHI

        # カン
        elif naki_kbn == 'K':
            meld_type = Meld.KAN

        man = ""
        pin = ""
        sou = ""
        honors = ""

        for haistr in haistrs:
            buff = buff = haistr
            if buff == '東':
                honors = self.add_hainum_to_tehai(honors, '1')
            elif buff == '南':
                honors = self.add_hainum_to_tehai(honors, '2')
            elif buff == '西':
                honors = self.add_hainum_to_tehai(honors, '3')
            elif buff == '北':
                honors = self.add_hainum_to_tehai(honors, '4')
            elif buff == '白':
                honors = self.add_hainum_to_tehai(honors, '5')
            elif buff == '発':
                honors = self.add_hainum_to_tehai(honors, '6')
            elif buff == '中':
                honors = self.add_hainum_to_tehai(honors, '7')
            elif buff[1] == 'm':
                man = self.add_hainum_to_tehai(man, buff[0])
            elif buff[1] == 'p':
                pin = self.add_hainum_to_tehai(pin, buff[0])
            elif buff[1] == 's':
                sou = self.add_hainum_to_tehai(pin, buff[0])
            else:
                print('[error]不正な文字列が入力されました。')

        tiles = TilesConverter.string_to_136_array(man=man, pin=pin, sou=sou, honors=honors)
        return Meld(meld_type=meld_type, tiles=tiles)




    def convert_haipai_to_tehai(self, str):
        """
        牌譜の文字列を手牌データ型に変換する
        :return: 手牌データ型の牌情報
        """
        man = ''
        pin = ''
        sou = ''
        honors = ''

        buff = ''
        for i, char in enumerate(str):
            buff = buff + char

            if buff == '1m' or buff == '2m' or buff == '3m' or buff == '4m' or buff == '5m' \
                    or buff == '6m' or buff == '7m' or buff == '8m' or buff == '9m':
                man = man + buff[0]
            elif buff == '1p' or buff == '2p' or buff == '3p' or buff == '4p' or buff == '5p' \
                    or buff == '6p' or buff == '7p' or buff == '8p' or buff == '9p':
                pin = pin + buff[0]
            elif buff == '1s' or buff == '2s' or buff == '3s' or buff == '4s' or buff == '5s' \
                    or buff == '6s' or buff == '7s' or buff == '8s' or buff == '9s':
                sou = sou + buff[0]
            elif buff == '東':
                honors = honors + '1'
            elif buff == '南':
                honors = honors + '2'
            elif buff == '西':
                honors = honors + '3'
            elif buff == '北':
                honors = honors + '4'
            elif buff == '白':
                honors = honors + '5'
            elif buff == '発':
                honors = honors + '6'
            elif buff == '中':
                honors = honors + '7'
            else:
                continue

            buff = ''

        return {'man': su.sort(man), 'pin': su.sort(pin), 'sou': su.sort(sou), 'honors': su.sort(honors)}

    def get_tehai(self, t):
        """
        指定された局時間の全プレイヤーの手牌とリーチの状況を返却する
        終局時を指定する場合は t = -1とする
        :param 局時間
        :return: 全プレイヤーの手牌リスト, 全プレイヤーのリーチフラグ, 全プレイヤーのあがりフラグ
        """

        # 配牌から手牌を生成
        tehai_list = [self.convert_haipai_to_tehai(self.player_1_haipai),
                      self.convert_haipai_to_tehai(self.player_2_haipai),
                      self.convert_haipai_to_tehai(self.player_3_haipai),
                      self.convert_haipai_to_tehai(self.player_4_haipai)]

        # 鳴き牌
        meld_list = [[], [], [], []]

        # 捨て牌を初期化
        ho_list = [[], [], [], []]

        # リーチリストを初期化
        richi_list = [False, False, False, False]

        # あがりリストを初期化
        agari_list = [False, False, False, False]

        # あがり牌の辞書オブジェクトを初期化
        agarihai = {'man': '', 'pin': '', 'sou': '', 'honors': ''}

        # 各プレイヤーの巡目（ツモ, ポン, チー, カン,の直前に1増える
        junme_list = [0, 0, 0, 0]

        # 内部処理用
        prev_hai = ""

        # 指定された局時間に達するまで牌譜を読み込み
        for i, word in enumerate(self.haifu):

            if t > -1 and i + 1 > t:
                break

            player_index = int(word[0]) - 1
            action = word[1]

            # ツモ
            if action == 'G':
                junme_list[player_index] += 1
                tehai_list[player_index] = self.add_haistr_to_tehai(tehai_list[player_index], word[2:])
                prev_hai = word[2:]

            # ツモ切り
            elif action == 'D':
                tehai_list[player_index] = self.delete_haistr_from_tehai(tehai_list[player_index], word[2:])
                ho_list[player_index].append(word[2:])
                prev_hai = word[2:]

            # 手出し
            elif action == 'd':
                tehai_list[player_index] = self.delete_haistr_from_tehai(tehai_list[player_index], word[2:])
                ho_list[player_index].append(word[2:])
                prev_hai = word[2:]

            # リーチ
            elif action == 'R':
                richi_list[player_index] = True

            # あがり
            elif action == 'A':
                agari_list[player_index] = True
                agarihai = self.add_haistr_to_tehai(agarihai, prev_hai)

            # ポン
            elif action == 'N':
                junme_list[player_index] += 1
                tehai_list[player_index] = self.add_haistr_to_tehai(tehai_list[player_index], prev_hai)
                haistrs = [prev_hai, prev_hai, prev_hai]
                meld_list[player_index].append(self.naku(action, haistrs))

            # チー
            elif action == 'C':
                junme_list[player_index] += 1
                tehai_list[player_index] = self.add_haistr_to_tehai(tehai_list[player_index], prev_hai)
                haistrs = [prev_hai, word[2:4], word[4:]]
                meld_list[player_index].append(self.naku(action, haistrs))

            # カン
            elif action == 'K':
                junme_list[player_index] += 1
                haistrs = [word[2:], word[2:], word[2:]]
                meld_list[player_index].append(self.naku(action, haistrs))

            else:
                print('[error]不正な文字列が存在します。')

        return tehai_list, ho_list, richi_list, agari_list, agarihai, junme_list





###################################
# 試合のモデルクラス
###################################
class ShiaiModel:
    def __init__(self,
                 _tonpu_nanpu_kbn,            # 東風南風区分(0:東風戦 1:南風戦)
                 _taku_name1,                 # 卓の名前1
                 _taku_name2,                 # 卓の名前2
                 _start_dt,                   # 開始日時
                 _mochiten,                   # 持ち点
                 _player_1_name,              # プレイヤー1の名前
                 _player_1_rate,              # プレイヤー1のR
                 _player_2_name,              # プレイヤー2の名前
                 _player_2_rate,              # プレイヤー2のR
                 _player_3_name,              # プレイヤー3の名前
                 _player_3_rate,              # プレイヤー3のR
                 _player_4_name,              # プレイヤー4の名前
                 _player_4_rate,              # プレイヤー4のR
                 _kyoku_list,                 # 局のリスト
                 _result_1st_player_name,     # 1位プレイヤーの名前
                 _result_1st_player_score,    # 1位プレイヤーのスコア
                 _result_2nd_player_name,     # 2位プレイヤーの名前
                 _result_2nd_player_score,    # 2位プレイヤーのスコア
                 _result_3rd_player_name,     # 3位プレイヤーの名前
                 _result_3rd_player_score,    # 3位プレイヤーのスコア
                 _result_4th_player_name,     # 4位プレイヤーの名前
                 _result_4th_player_score,    # 4位プレイヤーのスコア
                 _end_dt):                    # 終了日時
        self.tonpu_nanpu_kbn = _tonpu_nanpu_kbn
        self.taku_name1 = _taku_name1
        self.taku_name2 = _taku_name2
        self.start_dt = _start_dt
        self.mochiten = _mochiten
        self.player_1_name = _player_1_name
        self.player_1_rate = _player_1_rate
        self.player_2_name = _player_2_name
        self.player_2_rate = _player_2_rate
        self.player_3_name = _player_3_name
        self.player_3_rate = _player_3_rate
        self.player_4_name = _player_4_name
        self.player_4_rate = _player_4_rate
        self.kyoku_list = _kyoku_list[:]
        self.result_1st_player_name = _result_1st_player_name
        self.result_1st_player_score = _result_1st_player_score
        self.result_2nd_player_name = _result_2nd_player_name
        self.result_2nd_player_score = _result_2nd_player_score
        self.result_3rd_player_name = _result_3rd_player_name
        self.result_3rd_player_score = _result_3rd_player_score
        self.result_4th_player_name = _result_4th_player_name
        self.result_4th_player_score = _result_4th_player_score
        self.end_dt = _end_dt

    # private method 試合前半の内容を出力する
    def print_first_half(self):
        print("--- 試合 --------------------------")
        print("東風南風区分(tonpu_nanpu_kbn): {0}".format(self.tonpu_nanpu_kbn))
        print("卓の名前1(taku_name1): {0}".format(self.taku_name1))
        print("卓の名前2(taku_name2): {0}".format(self.taku_name2))
        print("開始日時(start_dt): {0}".format(self.start_dt))
        print("持ち点(mochiten): {0}".format(self.mochiten))
        print("プレイヤー1の名前(player_1_name): {0}".format(self.player_1_name))
        print("プレイヤー1のR(player_1_rate): {0}".format(self.player_1_rate))
        print("プレイヤー2の名前(player_2_name): {0}".format(self.player_2_name))
        print("プレイヤー2のR(player_2_rate): {0}".format(self.player_2_rate))
        print("プレイヤー3の名前(player_3_name): {0}".format(self.player_3_name))
        print("プレイヤー3のR(player_3_rate): {0}".format(self.player_3_rate))
        print("プレイヤー4の名前(player_4_name): {0}".format(self.player_4_name))
        print("プレイヤー4のR(player_4_rate): {0}".format(self.player_4_rate))
        print("局数(len(kyoku_list)): {0}".format(len(self.kyoku_list)))

    # private method 試合後半の内容を出力する
    def print_second_half(self):
        print("1位プレイヤーの名前(result_1st_player_name): {0}".format(self.result_1st_player_name))
        print("1位プレイヤーのスコア(result_1st_player_score): {0}".format(self.result_1st_player_score))
        print("2位プレイヤーの名前(result_2nd_player_name): {0}".format(self.result_2nd_player_name))
        print("2位プレイヤーのスコア(result_2nd_player_score): {0}".format(self.result_2nd_player_score))
        print("3位プレイヤーの名前(result_3rd_player_name): {0}".format(self.result_3rd_player_name))
        print("3位プレイヤーのスコア(result_3rd_player_score): {0}".format(self.result_3rd_player_score))
        print("4位プレイヤーの名前(result_4th_player_name): {0}".format(self.result_4th_player_name))
        print("4位プレイヤーのスコア(result_4th_player_score): {0}".format(self.result_4th_player_score))
        print("終了日時(end_dt): {0}".format(self.end_dt))

    ###############################################
    # 試合の内容を出力する（局の内容は含まない）
    ###############################################
    def print(self):
        self.print_first_half()
        self.print_second_half()

    ###############################################
    # 試合の内容を出力する（局の内容も含む）
    ###############################################
    def print_all(self):
        self.print_first_half()
        for kyoku in self.kyoku_list:
            kyoku.print()
        self.print_second_half()

    ###############################################
    # 指定されたプレイヤー名のインデックスを返却する
    # 該当するプレイヤーが存在しない場合は -1 を返却する
    ###############################################
    def get_player_index(self, player_name):
        if player_name == self.player_1_name:
            return 0
        elif player_name == self.player_2_name:
            return 1
        elif player_name == self.player_3_name:
            return 2
        elif player_name == self.player_4_name:
            return 3
        else:
            return -1

    ###############################################
    # インデックスで指定されたプレイヤー名を返却する
    ###############################################
    def get_player_name(self, player_index):
        if player_index == 0:
            return self.player_1_name
        elif player_index == 1:
            return self.player_2_name
        elif player_index == 2:
            return self.player_3_name
        elif player_index == 3:
            return self.player_4_name
        else:
            return ""

    ###############################################
    # 指定されたプレイヤー名の順位を返却する
    # 該当するプレイヤーが存在しない場合は -1 を返却する
    ###############################################
    def get_rank_by_name(self, player_name):
        if player_name == self.result_1st_player_name:
            return 1
        elif player_name == self.result_2nd_player_name:
            return 2
        elif player_name == self.result_3rd_player_name:
            return 3
        elif player_name == self.result_4th_player_name:
            return 4
        else:
            print('不正な名前が指定されました: {0}'. format(player_name))
            print('result_1st_player_name: {0}'.format(self.result_1st_player_name))
            print('result_2nd_player_name: {0}'.format(self.result_2nd_player_name))
            print('result_3rd_player_name: {0}'.format(self.result_3rd_player_name))
            print('result_4th_player_name: {0}'.format(self.result_4th_player_name))
            return -1

    ###############################################
    # インデックスで指定されたプレイヤーの順位を返却する
    # 該当するプレイヤーが存在しない場合は -1 を返却する
    ###############################################
    def get_rank_by_index(self, player_index):
        return self.get_rank_by_name(self.get_player_name(player_index))

    ###############################################
    # 局開始時・プレイヤーごとの持ち点のリストを返却
    # [プレイヤー1の持ち点, プレイヤー2の持ち点, プレイヤー3の持ち点, プレイヤー4の持ち点]のリストを返却
    ###############################################
    def get_mochiten(self):

        mochiten_list = [self.mochiten, self.mochiten, self.mochiten, self.mochiten]
        kyokukaishiji_mochiten_list = []

        for kyoku in self.kyoku_list:

            kyokukaishiji_mochiten_list.append(mochiten_list[:])
            tokuten_list = [0, 0, 0, 0]

            for player_name, tokuten in kyoku.tokuten_map.items():
                tokuten_list[self.get_player_index(player_name)] += tokuten

            for i in range(4):
                mochiten_list[i] += tokuten_list[i]

        return kyokukaishiji_mochiten_list

    ###################################
    # 残り局数を取得する
    ###################################
    def get_remaining_kyoku_num(self, kyoku_kbn):
        if self.tonpu_nanpu_kbn == 0:
            max_kyoku_num = 4

        else:
            max_kyoku_num = 8

        return max_kyoku_num - kyoku_kbn - 1
