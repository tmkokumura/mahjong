# coding:utf-8

def sort(string, desc=False):
    """
    文字列をソートする
    :param string: str ソート対象の文字列
    :param desc: boolean Trueの場合、降順にソートする
    :return: ソート後の文字列
    """
    char_list = []
    for char in string:
        char_list.append(char)

    if desc:
        char_list.reverse()
    else:
        char_list.sort()

    return "".join(char_list)
