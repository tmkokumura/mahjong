from logging import getLogger, StreamHandler, Formatter, FileHandler, DEBUG, INFO
from feature.bag_of_visual_words import BagOfVisualWords

# Log Settings
LOG_DIR = 'log\\'
LOG_FILE = 'main_01_bag_of_visual_words.py.log'
logger = getLogger('main')
log_fmt = Formatter('%(asctime)s %(name)s %(lineno)d [%(levelname)s][%(funcName)s] %(message)s')
log_handler = StreamHandler()
log_handler.setLevel(INFO)
log_handler.setFormatter(log_fmt)
logger.addHandler(log_handler)
log_handler = FileHandler(LOG_DIR + LOG_FILE, 'a')
log_handler.setFormatter(log_fmt)
logger.setLevel(DEBUG)
logger.addHandler(log_handler)

logger.info('--- start ---')

# 変数の初期化
src_dir = 'resource\\image\\windowsapp\\template'
vw_file_name = 'resource\\visual_words\\visual_words.txt'
file_name_X = 'resource\\data\\x.txt'
file_name_Y = 'resource\\data\\y.txt'

# 1.BagOfVisualWordsインスタンスの初期化
logger.info('--- init BagOfVisualWords ---')
bvw = BagOfVisualWords(detector=BagOfVisualWords.AKAZE)

# 2.Visual Wordsの生成
logger.info('--- create visual words ---')
bvw.create_visual_words(src_dir)
bvw.save_visual_words(vw_file_name)

# 3. データセットの作成
logger.info('--- create data sets ---')
bvw.load_visual_words(vw_file_name)
bvw.create_data_set(src_dir)
bvw.save_data_set(file_name_X, file_name_Y)
