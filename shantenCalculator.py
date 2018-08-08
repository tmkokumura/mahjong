#coding:utf-8

class ShantenCalculator():

    ##################################
    # 対子候補のインデックスを返却する
    ##################################
    def getAtamaIndex(self, tehai):
        atamaIndex = []
        for i in range(len(tehai) - 1):
            if tehai[i] == tehai[i + 1]:
                atamaIndex.append(i)
        return atamaIndex

    ##################################
    # index番目で指定した対子をアタマとして抜き出す
    ##################################
    def removeAtama(self, tehai, index, count) :
        resultTehai = tehai[:]
        if tehai[index] == tehai[index + 1]:
            resultTehai.pop(index)
            resultTehai.pop(index)
            count += 1
        else:
            print("[ERROR]指定された位置に対子がありません。")
            print("tehai:{0}".format(tehai))
            print("index:{0]".format(index))
        return resultTehai, count

    ##################################
    # 刻子をすべて抜き出す
    ##################################
    def removeKotsu(self, tehai, count):
        resultTehai = tehai[:]
        for i in range(len(tehai) - 2):
            if tehai[i] == tehai[i + 1] and tehai[i + 1] == tehai[i + 2]:
                resultTehai.pop(i)
                resultTehai.pop(i)
                resultTehai.pop(i)
                count += 1
                return self.removeKotsu(resultTehai, count)
        return resultTehai, count

    ##################################
    # 順子をすべて抜き出す
    ##################################
    def removeJuntsu(self, tehai, count):
        resultTehai = tehai[:]
        for i in range(len(tehai) - 2):
            if tehai[i] + 1 == tehai[i + 1] and tehai[i + 1] + 1 == tehai[i + 2]:
                resultTehai.pop(i)
                resultTehai.pop(i)
                resultTehai.pop(i)
                count += 1
                return self.removeJuntsu(resultTehai, count)
        return resultTehai, count

    ##################################
    # ターツをすべて抜き出す
    ##################################
    def removeTatsu(self, tehai, count):
        resultTehai = tehai[:]
        for i in range(len(tehai) - 1):
            if tehai[i] == tehai[i + 1] or tehai[i] + 1 == tehai[i + 1] or tehai[i] + 2 == tehai[i + 1]:
                resultTehai.pop(i)
                resultTehai.pop(i)
                count += 1
                return self.removeTatsu(resultTehai, count)
        return resultTehai, count

    #################################
    # 面子の数からシャンテン数を計算する
    #################################
    def calcShantenFromMentsukoho(self, atamaNum, kotsuNum, juntsuNum, tatsuNum):
        while kotsuNum + juntsuNum + tatsuNum > 4:
            tatsuNum -= 1

        return 8 - 2 * (kotsuNum + juntsuNum) - atamaNum - tatsuNum

    #################################
    # 標準手のシャンテン数を計算する
    #################################
    def calcShantenNormal(self, tehai):
        # シャンテン数
        shanten = 8

        # アタマ候補のインデックスを取得
        atamaIndex = self.getAtamaIndex(tehai)
        #print("アタマ候補のインデックスを取得しました。（インデックス：{0}）".format(atamaIndex))

        # すべてのアタマ候補についてループ
        for item in atamaIndex:
            #print("---対子についてループ（対子インデックス：{0}）---".format(item))

            # メンツ数のカウント
            atamaNum = 0;
            kotsuNum = 0;
            juntsuNum = 0;
            tatsuNum = 0;

            # アタマを取り除く
            tehai2, atamaNum = self.removeAtama(tehai, item, atamaNum)
            #print("アタマを取り除きました。（残りの牌：{0}）".format(tehai2))

            # すべての刻子を取り除く
            tehai3, kotsuNum = self.removeKotsu(tehai2, kotsuNum)
            #print("刻子を{0}個取り除きました。（残りの牌：{1}）".format(kotsuNum, tehai3))

            # すべての順子を取り除く
            tehai4, juntsuNum = self.removeJuntsu(tehai3, juntsuNum)
            #print("順子を{0}個取り除きました。（残りの牌：{1}）".format(juntsuNum, tehai4))

            # すべてのターツを取り除く
            tehai5, tatsuNum = self.removeTatsu(tehai4, tatsuNum)
            #print("ターツを{0}個取り除きました。（残りの牌：{1}）".format(tatsuNum, tehai5))

            # シャンテン数を計算する
            tmpShanten = self.calcShantenFromMentsukoho(atamaNum, kotsuNum, juntsuNum, tatsuNum)
            #print("シャンテン数：{0}".format(tmpShanten))

            # シャンテン数の最小値を更新する
            if tmpShanten < shanten:
                shanten = tmpShanten

        return shanten

    ################################
    # 国士無双のシャンテン数を計算する
    ################################

    ################################
    # 七対子のシャンテン数を計算する
    ################################