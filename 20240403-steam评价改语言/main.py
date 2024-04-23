import requests
import logging
import concurrent.futures

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, filename='app.log',
                    encoding='utf8')
# 获取根记录器
logger = logging.getLogger()
# 创建一个控制台处理程序，用于输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
# 创建一个日志格式器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
# 将控制台处理程序添加到根记录器中
logger.addHandler(console_handler)

headers = {
    "accept": "application/json",
    "Authentication": "Welcome123",
    "Content-Type": "application/json-patch+json"
}

target_appId = "2744150"


def fetch_data(line):
    bot_name = line.split("\t")[0]
    url = line.split("\t")[1]
    try:
        response1 = requests.post(f'{url}/Api/SIH/{bot_name}/RecommendedId', headers=headers, json={
            "AppId": target_appId,
            "ReviewUrl": ""
        })
        logging.info(f'获取评测ID：{response1.text}')
        if not response1 or response1.text is None or response1.text == '':
            return
        res_data = response1.json()
        review_id = res_data['Result'][bot_name]['Result']

        response2 = requests.post(f'{url}/Api/SIH/{bot_name}/ViewPage', headers=headers, json={
            "Url": "https://steamcommunity.com/userreviews/update/" + review_id,
            "Referer": "https://steamcommunity.com",
            "BodyDatas": {
                "language": "english"
            },
            "Post": True,
            "Response": True,
            "GuestNum": 0
        })
        logging.info(f'评测修改语言：{response2.text}')
        return response2.json()['Result']
    except Exception as e:
        logger.error(f'{url} 请求失败：{e}')
        return None


# 读取文本文件
with open("./data/input.txt", "r") as file:
    # 初始化一个空数组，用于存储提取的数据
    data_array = []

    # 遍历每一行数据
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # 提交任务
        futures = [executor.submit(fetch_data, line.strip()) for line in file if line.strip()]

        # 处理完成的任务
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                data_array.append(result)

# 将结果写入到 txt 文件中
with open('./data/output.txt', 'w', encoding='utf8') as f:
    for results in data_array:
        for key, value in results.items():
            f.write(f"{key}: {value}\n")
