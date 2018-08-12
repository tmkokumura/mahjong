from tenho.tenho import Tenho
from logging import getLogger, StreamHandler, Formatter, FileHandler, DEBUG, INFO

# Log Settings
LOG_DIR = 'log\\'
LOG_FILE = 'main_04_hai_recognition.py.log'
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

tenho = Tenho()

file_name = 'resource\\image\\windowsapp\\window.bmp'
tenho.read_image(file_name)


positions = [[210, 691, 46, 55],
            [257, 691, 46, 55],
            [304, 691, 46, 55],
            [350, 691, 46, 55],
            [396, 691, 46, 55],
            [443, 691, 46, 55],
            [489, 691, 46, 55],
            [535, 691, 46, 55],
            [582, 691, 46, 55],
            [628, 691, 46, 55],
            [675, 691, 46, 55],
            [721, 691, 46, 55],
            [768, 691, 46, 55]]

for position in positions:
    hai = tenho.predict(position[0], position[1], position[2], position[3])
    logger.info('recognized: ' + hai)
tenho.dislpay(0.8)

logger.info('--- end ---')
