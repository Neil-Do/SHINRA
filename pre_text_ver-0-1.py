import re
from tqdm import tqdm
import sys
import json
import multiprocessing as mp


def preprocess_regex_result(reg_result):

    '''
        Chon chuoi khop dai nhat trong ket qua tra ve cua ham regex findall
    '''

    # print(reg_result)
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
    # print(return_val)
    return return_val


def detect_measurement_unit(text, opt='add_markdown', measurement_unit='mass'):

    '''
        Input:
            text : input text
            opt : add_markdown, replace_by_tag -> chèn markdown tag xung quanh cụm từ, hoặc thay thế cụm từ bằng markdown tag
            measurement_unit : length, mass, area, volume -> xác định từ mô tả chiều dài, khối lượng, diện tích, thể tích

        Output:
            string
    '''

    length_regex = r"( \d+([,.]\d+)?\s+(milimet|milimét|centimet|centimét|decimet|decimét|mét|met|decamet|decamét|hectomet|hectomét|kilomet|kilomét|inch|phút|thước|dặm|trượng|ngũ|xích|tấc|phân|ly|li|hào|ti|hốt|lý|sải|dẫn|bộ|thốn|hải lý|hải lí|mã|yard||feet|ft|mi|mm|m))"

    mass_regex = r"( \d+([,.]\d+)?\s+(gam|cân|kg|tấn|miligram|miligam|ký|ao-xơ|pao|xtôn|tấn|quân|tạ|bình|yến|nén|lạng|đồng|đồng cân|hoa|phân|li|ly|hào|ti|hốt|vi|chỉ))"

    area_regex = r"( \d+([,.]\d+)?\s+(a|hecta|hécta|héc-ta|mét vuông|kilomét vuông|centimét vuông|decimét vuông|decamét vuông|hectomét vuông|héctomét vuông|milimét vuông|mẫu|sào|miếng|xích|thước|than|tấc|thốn|phân|ô|ghế|khấu|khoảnh|li|phương trượng|phương xích|phương thốn|dặm vuông|công|công đất))"

    volume_regex = r"( \d+([,.]\d+)?\s+(phân khối|xentimét khối|centimet khối|cc|ccm|mililit|mililit|ml|mét khối|met khối|đêximét khối|decimet khối|micrôlit|µL|millilit|mL|xentilit|cL|đêxilit|dL|hectôlit|hL|lit|lít|gallon|galông|ga-lông|pint|panh|quart|gill|foot khối|yard khối|thạch|đẩu|thăng|hộc|chước|toát|miếng|giạ|túc|uyên|hiệp))"

    s = text
    if len(s) == 0:
        return s
    s = s.lower()

    str_code = "re.findall(%s_regex, s)"%measurement_unit
    regex_result = eval(str_code)

    if regex_result != []:
        if opt == 'add_markdown':
            list_url_substring = preprocess_regex_result(regex_result)
            for sub_string in list_url_substring:
                s = s.replace(sub_string, '<%s>%s</%s>'%(measurement_unit, sub_string, measurement_unit))
        elif opt == 'replace_by_tag':
            list_url_substring = preprocess_regex_result(regex_result)
            for sub_string in list_url_substring:
                s = s.replace(sub_string, '<%s />'%measurement_unit)

    return s


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


def detect_url(text, opt='add_markdown'):

    '''
        Phat hien url

        Input:
            text
            opt : add_markdown, replace_by_tag
        Output:
            added <time></time> string
    '''

    regex_1 = r"((http|https|file|ftp|info|mailto|news|nntp|snews|rlogin|telnet|tn3270|irc|data|nfs|ldap|man|ssh):[^\s,\\<>{}]+)"

    s = text
    if len(s) == 0:
        return s

    s = s.lower()
    regex_1_result = re.findall(regex_1, s)

    if opt == 'add_markdown':
        if regex_1_result != []:
            list_url_substring = preprocess_regex_result(regex_1_result)
            for sub_string in list_url_substring:
                s = s.replace(sub_string, '<url>' + sub_string + '</url>')
    elif opt == 'replace_by_tag':
            list_url_substring = preprocess_regex_result(regex_1_result)
            for sub_string in list_url_substring:
                s = s.replace(sub_string, '<url />')

    return s


def get_important_data(source_text):

    '''
        Input:
            source_text
        Output:
            important_data = {
                "markdown_tag" : markdown_tag_set, # tap hop cac markdown trong input
                "italic_word" : italic_set, # tap hop cac string duoc in nghieng
                "bold_word" : bold_set, # tap hop cac string duoc in dam
                "meta" : note_set, # tap hop cac metadata luu trong {{  }}
                "word_with_link" : link_set # tap hop cac string duoc dinh kem link
            }
    '''

    s = source_text

    # cac markdown tag, vi du <math></math>
    markdown_tag = re.findall(r"\<[^/].+?\>", s)
    markdown_tag_set = []
    for e in markdown_tag:
        markdown_tag_set.append(e)

    # noi dung meta, dat trong {{  }}
    note = re.findall(r"\{\{((.)+)\}\}", s)
    note_set = set()
    for e in note:
        note_set.add(e[0])

    # regex italic code
    italic = re.findall(r"[^']\'\'([^'].+?)\'\'", s)
    italic_set = []
    for e in italic:
        italic_set.append(e)


    # bold text - in dam
    bold = re.findall(r"\'\'\'(.+?)\'\'\'", s)
    bold_set = []
    for e in bold:
        bold_set.append(e)


    # chuoi van ban duoc dinh kem link
    text_with_link = re.findall(r"(\[\[\w.+?\w\]\])", s)
    link_set = set()
    for e in text_with_link:
        if e =='':
            continue
        link_set.add(e)

    important_data = {
        "markdown_tag" : list(markdown_tag_set),
        "italic_word" : list(italic_set),
        "bold_word" : list(bold_set),
        "meta" : list(note_set),
        "word_with_link" : list(link_set)
    }

    return important_data


def get_number_of_line_in_file(file_path):

    fi = open(file_path)
    count = 0
    for line in fi:
        count += 1
    fi.close()

    return count


def parallel_processing(data_dict, njobs=0):

    '''
        Input:
            data_dict : {
                function_name1 : {
                    page_id1 : [source_text1, function_opt1],
                    page_id2 : [source_text2, function_opt2],
                    ...
                },
                ...
            }
            default njobs = max_cpu // 2

        Output:
            data_dict : {
                function_name1 : {
                    page_id1 : result_1,
                    page_id2 : result_2,
                    ...
                },
                ...
            }
    '''
    pool = mp.Pool(njobs)
    if njobs==0:
        pool = mp.Pool(mp.cpu_count() // 2)

    total_results = {}
    for function_name in data_dict:

        list_page_id = list(data_dict[function_name].keys())
        list_arguments_function = list(data_dict[function_name].values())

        str_code = "pool.starmap(%s, list_arguments_function)"%function_name
        print(str_code)

        results = list(eval(str_code))
        results_dict = {}
        for i in range(len(list_page_id)):
            page_id = list_page_id[i]
            results_dict[page_id] = results[i]
        total_results[function_name] = results_dict

    return total_results


if __name__ == "__main__":

    fi = open('../vi/vi-trial-wiki-20190121-cirrussearch-content-trial-3.json', encoding='utf8')
    fo = open('../vi/temp_file', 'w', encoding='utf8')
    all_data = json.load(fi)
    data_dict = {
        'detect_time' : {
            all_data[0]['index']['_id'] : [ all_data[1]['source_text'], 'add_markdown'],
            all_data[2]['index']['_id'] : [ all_data[3]['source_text'], 'add_markdown'],
        },
        'detect_url': {
            all_data[4]['index']['_id'] : [ all_data[5]['source_text'], 'add_markdown'],
            all_data[6]['index']['_id'] : [ all_data[7]['source_text'], 'add_markdown'],
        },
        'get_important_data' : {
            all_data[8]['index']['_id'] : [all_data[9]['source_text']],
        }
    }

    total_results = parallel_processing(data_dict, njobs=5)
    json.dump(total_results, fo, ensure_ascii=False, indent=4)


    fi.close()
    fo.flush()
    fo.close()
