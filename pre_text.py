import os
import json
from tqdm import tqdm

fi = open('../vi/vi-trial-wiki-20190121-cirrussearch-content-trial-2.json')
fo = open('../vi/vi-trial-wiki-20190121-cirrussearch-content-trial-3.json', 'w', encoding='utf8')

content = fi.read()
fo.write('[' + content + ']')
# for i in tqdm(range(len(fi) - 1)):
#     line = fi[i]
#     if fi[i].strip() == '}' and fi[i+1].strip() == '{':
#         line = "},"
#     fo.write(line)

# for i in tqdm(range(10)):
#     line = fi.readline()
#     fi.readline()
#     data = json.loads(line)
#     data = json.dump(data, fo, indent=4, ensure_ascii=False)
#     fo.write('\n')
#     if i % 2 == 1:
#         fo.write('\n')
#         fo.write('\n')
#     fo.write(data + '\n')


fo.flush()
fo.close()
fi.close()
