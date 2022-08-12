black_word = ['神秘嘉宾', '手把手教你', '开课', '给大家发一个福利', '讲师', '置顶', '原图', '直播连麦']


def filter_text(text_list: list):
    n_list = []
    for text in text_list:
        for w in black_word:
            if w in text:
                return n_list
        if ('【' and '】') in list(set(text)) or text.count('-') > 3 or text.count('#') == 2:
            return n_list
        if len(text) > 1:
            n_list.append(text)
    return n_list
