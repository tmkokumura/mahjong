from shiaiModel import ShiaiModel


class HaifuAnalyzer:

    ##################################
    # コンストラクタ
    ##################################
    def __init__(self, shiai_list):
        self.shiai_list = shiai_list

    # private method
    # 順位の数値を順位クラスのラベルに変換する
    def get_rank_label(self, rank):
        rank_label = [0, 0, 0, 0]
        rank_label[rank - 1] = 1
        return rank_label

    # private method
    # 他プレイヤーとの点差リストを取得する
    def _get_tensa_list(self, shiai_index, kyoku_index, player_index):

        _tensa_list = []

        # 局開始時・プレイヤーごとの持ち点のリストを取得
        all_mochiten_list = self.shiai_list[shiai_index].get_mochiten()

        # この局のプレイヤーの持ち点
        player_mochiten = all_mochiten_list[kyoku_index][player_index]

        # この局の他家の持ち点リスト
        tacha_mochiten_list = []
        for j, mochiten in enumerate(all_mochiten_list[kyoku_index]):
            if not player_index == j:
                tacha_mochiten_list.append(mochiten)

        # 他家持ち点を降順にソート
        tacha_mochiten_list.sort(reverse=True)

        # 他家との点差を計算
        for j in range(3):
            _tensa_list.append(tacha_mochiten_list[j] - player_mochiten)

        return _tensa_list

    ##################################
    # 特徴量 1.
    # 局開始時ごとの他家との点差と、最終順位を特徴量として抜き出す
    # [プレイヤーindex, 残局数, 他家との点差1, 他家との点差2, 他家との点差3, 最終順位]のリストを返却
    # 他家との点差は降順に並べる
    ##################################
    def get_diff_score_and_result_rank_per_kyokukaishi(self):
        features_list = []

        for shiai_index, shiai in enumerate(self.shiai_list):

            # 局開始時・プレイヤーごとの持ち点のリストを取得
            all_mochiten_list = shiai.get_mochiten()

            for player_index in range(4):
                # プレイヤーの最終順位を取得
                rank_label = self.get_rank_label(shiai.get_rank_by_index(player_index))

                for kyoku_index, kyoku in enumerate(shiai.kyoku_list):

                    # プレイヤーインデックス, 残局数を特徴に追加
                    features = [player_index, shiai.get_remaining_kyoku_num(kyoku.kyoku_kbn)]

                    # 他家との点差を特徴に追加
                    tensa_list = self._get_tensa_list(shiai_index, kyoku_index, player_index)
                    for tensa in tensa:
                        features.append(tensa)

                    # 特徴の末尾に順位のラベルを追加
                    for label in rank_label:
                        features.append(label)

                    features_list.append(features[:])

        return features_list

    ##################################
    # 特徴量 2.
    # 局・巡目ごとの他家との点差と、シャンテン数を特徴量として抜き出す
    # ラベルは最終順位
    # [プレイヤーindex, 残局数, 巡目, 他家との点差1, 他家との点差2, 他家との点差3, シャンテン数, 最終順位]のリストを返却
    # 他家との点差は降順に並べる
    ##################################
