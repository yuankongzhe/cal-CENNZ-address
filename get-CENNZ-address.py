import requests
import json
from datetime import datetime

def check_timestamp(block_timestamp):
    # 转换Unix时间戳为datetime对象
    timestamp_date = datetime.utcfromtimestamp(block_timestamp)
    
    # 设置目标日期为2024年3月18日
    target_date = datetime(2024, 3, 18)
    
    # 如果block_timestamp的日期在目标日期之前，返回Ture
    return timestamp_date < target_date

def fetch_extrinsics(row=100, page=1, signed="signed"):
    url = "https://service.eks.centralityapp.com/cennznet-explorer-api/api/scan/extrinsics"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en",
        "Content-Type": "application/json;charset=UTF-8",
        "Dnt": "1",
        "Origin": "https://uncoverexplorer.com",
        "Referer": "https://uncoverexplorer.com/extrinsic",
        "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    payload = {
        "row": row,
        "page": page,
        "signed": signed
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        return response.json()['data']['extrinsics']
    else:
        print(f'response.status_code : {response.status_code}')
        print(f'response.text : {response.text}')


# Example usage:
account_id_dict={}     
for i in range(9999):
    print(f'now i is {i}')
    for _ in range(5):
        try:
            result = fetch_extrinsics(row=100, page=i, signed="signed")
            break
        except Exception as e:
            print(e)
    for tx_hash in result:
        tx_account_id=tx_hash['account_id'] 
        tx_function = tx_hash['call_module_function']
        tx_call_module = tx_hash['call_module']
        tx_to_address = tx_hash['params']
        tx_time_data = tx_hash['block_timestamp']
        if check_timestamp(tx_time_data):
            break
        if tx_function == 'batchAll' and tx_call_module =='utility' and '5FPRzdibKdeVdXMSsHgywNL4zWJenkPcVXMrUVuTzdahdPNd' in tx_to_address:
            account_id_dict[tx_account_id] = 1

    if check_timestamp(tx_time_data):
        break
print('-----------------------')
print(account_id_dict.keys())
print(f'now participate address number is : {len(account_id_dict)}')