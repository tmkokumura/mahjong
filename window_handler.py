import win32gui
import win32ui
import win32con
from PIL import Image


def screenshot(file_name=None):
    """
    スクリーンキャプチャを取る
    :param file_name: 画像ファイル名
    :return:
    """

    width = 1920
    height = 1080
    # SCREEN_SCALING_FACTOR = 1.5
    window = win32gui.GetDesktopWindow()
    window_dc = win32ui.CreateDCFromHandle(win32gui.GetWindowDC(window))
    compatible_dc = window_dc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(window_dc, width, height)
    compatible_dc.SelectObject(bmp)
    compatible_dc.BitBlt((0, 0), (width, height), window_dc, (0, 0), win32con.SRCCOPY)
    img = Image.frombuffer('RGB', (width, height), bmp.GetBitmapBits(True), 'raw', 'BGRX', 0, 1)
    if file_name is not None:
        img.save(file_name)
    return img
