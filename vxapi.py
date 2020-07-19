import requests
import json
import time
import configparser

class Weixin(object):
    # appid & appsecret 
    def __init__(self,appid,appsecret):
        self.appid = appid
        self.appsecret = appsecret

    # 获取Access_Token
    def getAccessToken(self):
        with open("./token",mode='r',encoding='utf8') as f:
            access_token = f.readline()
        return access_token

    # 自定义创建菜单
    def createMenus(self):
        access_token = self.getAccessToken()
        url =  "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % (access_token)
        
        formdata = {
            "button":[
            {	
                "type":"view",
                "name":"信息查询",
                # https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxf0e81c3bee622d60&redirect_uri=http%3A%2F%2Fnba.bluewebgame.com%2Foauth_response.php&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect
                "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri=http://www.tangquanmm.com/userinfo/info.html&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect".format(appid=self.appid)
            },
            {	
                "type":"view",
                "name":"信息发布",
                "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri=http://www.tangquanmm.com/userinfo/pinfo.html&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect".format(appid=self.appid)
            },
            {	
                "type":"click",
                "name":"管理员",
                "key":"SendInfo"
            }]
        }

        data = json.dumps(formdata,ensure_ascii=False).encode('utf-8')
        response = requests.post(url, data = data)
        print(response.json())
    
    # 用户管理：创建标签
    def createtag(self,tagname):
        access_token = self.getAccessToken()
        url = "https://api.weixin.qq.com/cgi-bin/tags/create?access_token=%s" % access_token
        data = {
            "tag": {
                "name": tagname
            }
        }
        data = json.dumps(data,ensure_ascii=False).encode('utf-8')
        response = requests.post(url, data = data)
        print(response)

    # 用户管理：获取标签
    def gettags(self):
        access_token = self.getAccessToken()
        url = "https://api.weixin.qq.com/cgi-bin/tags/get?access_token=%s" % access_token
        response = requests.get(url)
        responsedata = json.loads(response.text)
        print(responsedata)
    
    # 用户管理：获取标签下的用户
    def get_user_tag(self,tagid,next_openid=""):
        access_token = self.getAccessToken()
        url = "https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token=%s"  % access_token
        data = {
            "tagid": tagid,
            "next_openid": next_openid
        }
        data = json.dumps(data,ensure_ascii=False).encode('utf-8')
        response = requests.post(url, data = data)
        responsedata = response.json()
        print(responsedata)


    # 用户管理：获取用户信息
    def getuserinfo(self,openid):
        access_token = self.getAccessToken()
        url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token={access_token}&openid={openid}&lang=zh_CN".format(access_token=access_token,openid=openid)
        response = requests.get(url)
        responsedata = response.json()
        print(responsedata)


if __name__ == "__main__":
    # 读取配置文件： appid & appsecret
    config = configparser.ConfigParser()
    config.read("./config.ini")
    appid = config.get('auth','appid')
    appsecret = config.get('auth','appsecret')

    vxapi1 = Weixin(appid,appsecret)
    # wxapi1.getAccessToken()
    vxapi1.createMenus()
    # wxapi1.createtag("VIP")
    # wxapi1.gettags()
    # wxapi1.get_user_tag(2)
    # wxapi1.getuserinfo('oEnPt5uxeExaaeDYfFAi_rP8H53s')
