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


def fetch_data(line):
    print(line)
    bot_name = line.split()[0]
    url = line.split()[1]
    cdkey = line.split()[2]

    logger.error(f'{bot_name} {url} {cdkey}')
    try:
        response = requests.post(f'{url}/Api/Command', headers=headers, json={
            "Command": f"REDEEMWALLET {bot_name} {cdkey}"
        })
        logging.info(response.text)
        # 将结果写入到 txt 文件中
        with open('./data/output.txt', 'w', encoding='utf8') as f:
            f.write(f"{response.json()['Result']}\n")
        return
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
