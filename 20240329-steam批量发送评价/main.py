import random
import time
import requests

import openpyxl

wb = openpyxl.load_workbook("./data/input.xlsx")
sheet = wb.active

data = []

headers = {
    'accept': 'application/json',
    'Authentication': 'Welcome123',
    'Content-Type': 'application/json'
}

for row in sheet.iter_rows(values_only=True):
    account, content, end_point = row[:3]  # Assuming only 3 columns exist
    if account == 'account':
        continue
    url = f'{end_point}/Api/SIH/{account}/recommendgame'
    data = {
        "AppID": 2786680,
        "Comment": content,
        "RatedUp": 1,
        "Language": "english"
    }
    print(account, content, end_point)
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    random_number = random.randint(1, 10)
    time.sleep(random_number)
