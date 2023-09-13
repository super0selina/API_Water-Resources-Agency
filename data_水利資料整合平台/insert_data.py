import requests
import csv
import json
import os

filename = './水利資料整合雲平台.csv'

try:
    with open(filename, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            api_url = row['API網址']
            frequency = row['更新頻率']
            if frequency == '不定期:上傳機關依據現場狀況進行上傳週期調整':
                frequency = '不定期'
            title = row['資料標題']
            response = requests.get(api_url)
            data = response.json()
            filename = f'C:/Users/PC/Desktop/AI大數據人才養成/集先鋒/test/data/({frequency}){title}.json'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False, indent=4)
                print(f'已寫入{filename}')
except Exception as e:
    print(f"Error reading CSV file: {e}")