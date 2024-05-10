import pandas as pd
import os

# 读取Excel文件
excel_file = r'I:\1_steam_account\2024-11w8\账号令牌信息-2024-11w8.xlsx'
df = pd.read_excel(excel_file)

# 创建目录
output_dir = r'I:\1_steam_account\2024-11w8\maFile'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 逐行处理数据
for index, row in df.iterrows():
    account_name = row['account']
    ma_content = row['ma_file']

    # 写入文件
    file_path = os.path.join(output_dir, f"{account_name}.maFile")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(ma_content)

print("文件写入完成！")
