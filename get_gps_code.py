import requests
import json
import time
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

tqdm.pandas(desc="my bar!")


def get_gps(address, coo, ak):
    # 相关参数
    proxies = {"http": "代理地址"}
    city = coo
    coordtype = 'gcj02ll'
    output = 'json'
    gps_result = pd.DataFrame(columns=('city','address', 'lng', 'lat'))
    for i in range(0,address.shape[0]):
        address1 = address.iloc[i,7]
        # 形成url
        url = 'http://api.map.baidu.com/geocoding/v3/?address=%s&city=%s&output=%s&ak=%s&ret_coordtype=%s' \
              % (address1, city, output, ak, coordtype)
        r = requests.get(url, proxies=proxies)
        info = BeautifulSoup(r.text,'lxml')
        if eval(info.p.text)['status'] == 0:
            lng = eval(info.p.text)['result']['location']['lng']
            lat = eval(info.p.text)['result']['location']['lat']
            data = [city, address1, lng, lat]
            gps_result.loc[i] = data
    return gps_result
    
    
if __name__ == "__main__":
    kkk = "您的ak"
    address = pd.read_csv('address.csv',delimiter="\t")
    get_gps(address, "**市", kkk).to_csv("gps_result.csv",encoding='utf_8_sig')
