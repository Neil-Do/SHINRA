import re

def preprocess_regex_result(reg_result):

    '''
        Chon chuoi dai nhat trong ket qua cua ham regex findall
    '''
    # if
    print(reg_result)
    return_val = []

    # check reg_result 2D iterable or 1D iterable
    if not isinstance(reg_result[0], str): # 2D iterable
        for tuple_ in reg_result:
            max_length_string_index = 0
            for index in range(len(tuple_)):
                if len(tuple_[index]) > len(tuple_[max_length_string_index]):
                    max_length_string_index = index
            return_val.append(tuple_[max_length_string_index])
    else: # 1D iterable
        max_length_string_index = 0
        for index in range(len(reg_result)):
            if len(reg_result[index]) > len(reg_result[max_length_string_index]):
                max_length_string_index = index
        return_val = [reg_result[max_length_string_index]]
    return_val = list(set(return_val))
    print(return_val)
    return return_val



def detect_time(text, opt='add_markdown'):

    '''
        Phat hien cum van ban ve thoi gian

        Input:
            text
            opt:
                - add_markdown      # them tag
                - replace_by_tag    # thay bang tag
        Output:
            them tag <time></time> hoac thay the bang <time/>

    '''

    regex_1 = r"(buổi (sáng|trưa|chiều|tối))"

    time = r"( \d{1,2}(:| (giờ |tiếng ))(\d{1,2}(:|phút (\d{1,2}( giây)?)?)?)?)|(\d{1,2} phút( \d{1,2} giây)?)|( \d{1,2} giây)|(giây (thứ \d{1,2} )?\d{1,2})"

    date = r"((ngày|mồng) (\d{1,2}|hai|ba|bốn|tư|năm|sáu|bảy|tám|chín|mười|mười một|mười hai|mười ba|mười bốn|mười lăm|mười sáu|mười bảy|mười tám|mười chín|hai mươi|hai( mươi)? mốt|hai( mươi)? hai|hai( mươi)? ba|hai( mươi)? (bốn|tư)|hai( mươi)? lăm|hai( mươi)? sáu|hai( mươi)? bảy|hai( mươi)? tám|hai( mươi)? chín|ba mươi|ba( mươi)? mốt)(( tháng |-)(\d{1,2}|giêng|hai|ba|bốn|tư|năm|sáu|bảy|tám|chín|mười một|mười hai|mười)( năm \d{1,4})?)?)|( tháng (\d{1,2}|giêng|hai|ba|bốn|tư|năm|sáu|bảy|tám|chín|mười một|mười hai|mười|chạp)( năm \d{1,4})?)|( năm \d{1,4})"

    date_2 = r"( (\d{1,2}[-/]\d{1,2}([-/]\d{1,4})?)|(\d{1,2}[-/]\d{1,4}) )"

    s = text
    if len(s) == 0:
        return s

    s = s.lower()
    regex_1_result = re.findall(regex_1, s)
    time_result = re.findall(time, s)
    date_result = re.findall(date, s)
    date_2_result = re.findall(date_2, s)

    if opt == "add_markdown":
        if regex_1_result != []:
            list_time_substring = preprocess_regex_result(regex_1_result)
            for sub_string in list_time_substring:
                s = s.replace(sub_string, '<time>' + sub_string + '</time>')
        if time_result != []:
            list_time_substring = preprocess_regex_result(time_result)
            for sub_string in list_time_substring:
                s = s.replace(sub_string, '<time>' + sub_string + '</time>')
        if date_result != []:
            list_time_substring = preprocess_regex_result(date_result)
            for sub_string in list_time_substring:
                s = s.replace(sub_string, '<time>' + sub_string + '</time>')
        if date_2_result != []:
            list_time_substring = preprocess_regex_result(date_2_result)
            for sub_string in list_time_substring:
                s = s.replace(sub_string, '<time>' + sub_string + '</time>')
    elif opt == 'replace_by_tag':
        if regex_1_result != []:
            list_time_substring = preprocess_regex_result(regex_1_result)
            for sub_string in list_time_substring:
                s = s.replace(sub_string, '<time/>')
        if time_result != []:
            list_time_substring = preprocess_regex_result(time_result)
            for sub_string in list_time_substring:
                s = s.replace(sub_string, '<time/>')
        if date_2_result != []:
            list_time_substring = preprocess_regex_result(date_2_result)
            for sub_string in list_time_substring:
                s = s.replace(sub_string, '<time/>')
    else:
        print('Option khong hop le. Tra ve xau rong.')
        return ''

    return s


fi = open('../vi/ex_text', encoding='utf8').read().strip()
fo = open('../vi/temp_file', 'w', encoding='utf8')
s = detect_time(fi)
fo.write(s)
fo.close()
