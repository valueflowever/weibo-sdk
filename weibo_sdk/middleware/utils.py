def filter_text(text_list: list):
    n_list = []
    for i in text_list:
        if ('【' and '】') in list(set(i)) or i.count('-') > 3:
            break
        elif '神秘嘉宾' in i:
            break
        else:
            n_list.append(i)
    return n_list
