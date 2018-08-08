from fileUtils import FileUtils as fu
from haifuReader import HaifuReader
from haifuAnalyzer import HaifuAnalyzer

# 牌譜を読み込み
haifu_file_name = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\haifu\\totsugekitohoku.txt'
hr = HaifuReader()
shiai_list = hr.read(haifu_file_name)

# 特徴を抽出
ha = HaifuAnalyzer(shiai_list)
result = ha.get_diff_score_and_result_rank_per_kyokukaishi()

# 結果をファイルに書き込み
data_file_name = 'C:\\Users\\okumura.tomoki\\PycharmProjects\\Mahjong\\resource\\data\\data.txt'
fu.write_2d_list(data_file_name, result)