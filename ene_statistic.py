import ast
import json
from tqdm import tqdm
import operator

# fi = open('../vi/vi_ENEW_LIST.json').readlines()
fi = open('../vi/vi_ENEW_LIST.json', encoding='utf8')
fo = open('../vi/so_luong_nhan_moi_page.json', 'w', encoding='utf8')
# data = json.load(fi)
stat_data = []
page_dict = {}
# data_stat = {"AUTO.TOHOKU.201906":0, "HAND.AIP.201910":0}
# total_auto = 0
# total_hand = 0
for line in fi:
    data = json.loads(line)
    page_dict[data['title']] = data['pageid']
    stat_data.append([len(data['ENEs']), data['title']])

#
# all_data["total"] = data_stat
#
stat_data = sorted(stat_data, reverse=True)
for i in range(len(stat_data)):
    stat_data[i].append(page_dict[stat_data[i][1]])
# for i in range(len(temp_stat_data)):
    # stat_data[temp_stat_data[i][0]] = temp_stat_data[i][1]
json.dump(stat_data, fo, ensure_ascii=False, indent=4)
fo.flush()
fo.close()
fi.close()
