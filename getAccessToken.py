# encoding: utf-8

import time
import logging
import configparser
import requests

# 定义日志
logger = logging.getLogger('test')
logger.setLevel(level=logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

file_handler = logging.FileHandler('./logs/getAccessToken.log')
file_handler.setLevel(level=logging.INFO)
file_handler.setFormatter(formatter)

# 读取配置
config = configparser.ConfigParser()
config.read("./config.ini")
appid = config.get('auth','appid')
appsecret = config.get('auth','appsecret')

def getNewAccessToken():
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appid,appsecret)
    response = requests.get(url)
    responsedata = response.json()
    if 'access_token' not in responsedata:
        logger.error('errcode: %s , errmsg: %s' % (responsedata['errcode'],responsedata['errmsg']))
        return False
    access_token = responsedata["access_token"]
    with open("./token",mode='w',encoding='utf8') as f:
        f.write(access_token)
    logger.info('getNewAcessToken Success！') 
    
def looptask():
    while True:
        getNewAccessToken()
        time.sleep(7000)

if __name__ == "__main__":
    logger.addHandler(file_handler)
    looptask()


