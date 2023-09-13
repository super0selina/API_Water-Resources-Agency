import requests
import csv
from bs4 import BeautifulSoup

url = "https://data.wra.gov.tw/openapi/api/OpenData/openapi"

try:
    response = requests.get(url)
    response.raise_for_status()
    clean_data_json = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    exit()

paths = []
for path in clean_data_json['paths']:
    paths.append(path)

datas_list = []

for p in paths:
    data_dic = {}
    data = clean_data_json['paths'][p]['get']
    data1 = clean_data_json['paths'][p]['servers'][0]['url']

    if data1 == 'https://data.wra.gov.tw/':
        apiurl = data1+'openapi'+p
    elif data1 == 'https://iot.wra.gov.tw/':
        apiurl = 'https://iot.wra.gov.tw'+p
    data_dic['資料標題'] = data['summary']
    data_dic['API網址'] = apiurl

    description = data['description']
    # 使用Beautiful Soup來解析HTML
    soup = BeautifulSoup(description, 'html.parser')

    # 找到包含更新頻率的標籤並取出文本
    update_frequency_tag = soup.find('th', text='更新頻率').find_next('td')
    update_frequency_text = update_frequency_tag.get_text(strip=True)

    data_dic['更新頻率'] = update_frequency_text

    datas_list.append(data_dic)

labels = ['資料標題', 'API網址', '更新頻率']
try:
    with open('C:/Users/PC/Desktop/AI大數據人才養成/集先鋒/test/水利資料整合雲平台.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=labels)
        writer.writeheader()
        writer.writerows(datas_list)
        print('已寫入')
except IOError as e:
    print(f"I/O error: {e}")