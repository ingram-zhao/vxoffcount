import hashlib
import web
import receive
import reply
import requests
import configparser
import datetime
from vxapi import Weixin

# 初始化配置信息
config = configparser.ConfigParser()
config.read("./config.ini")
path = config.get('default','path')
appid = config.get('auth','appid')
appsecret = config.get('auth','appsecret')

render = web.template.render(path)
db = web.database(
        dbn = config.get('db','dbn'),
		host =  config.get('db','host'),
        user =  config.get('db','user'),
        port =  int(config.get('db','port')),
        pw =  config.get('db','password'),
        db =  config.get('db','dbname'),
    )

# 实例化->获取access_token
vx = Weixin(appid,appsecret)

# 判断用户是否是VIP用户（星标用户: id = 2）
def isVip(openid):
    access_token = vx.getAccessToken()
    url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token={access_token}&openid={openid}&lang=zh_CN".format(access_token=access_token,openid=openid)
    response = requests.get(url)
    responsedata = response.json()
    if 2 in responsedata['tagid_list']:
        return True 
    return False


class Handle(object):
    # 验证开发者服务器
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            # 1. 获取 signature timestamp nonce echostr
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            
            # 2. 配置Token
            token = "sjh123456"

            # 3. 放入列表中排序并使用sha1加密lista得到hashcode
            lista = [token, timestamp, nonce]
            lista.sort()
            liststr = ''.join(lista)
            sha1 = hashlib.sha1()
            sha1.update(liststr.encode("utf-8"))
            hashcode = sha1.hexdigest()

            # 4. 如果hashcode == signature 确定该数据源是微信后台；返回echostr提供微信后台认证Token
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
                
        except Exception:
            print("数据源认证流程失败！")

    # 接收用户信息
    def POST(self):
        webData = web.data()
        recMsg = receive.parse_xml(webData)
        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            content = '您好！我是平台管理员，有任何问题或建议都联系我15305170962(微信同号)'
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            return replyMsg.send()

        elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'image':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            mediaID = recMsg.MediaId
            replyMsg = reply.ImageMsg(toUser,fromUser,mediaID)
            return replyMsg.send()
        
        elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'event' and recMsg.Event == 'CLICK' and recMsg.EventKey == 'SendInfo':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            content = '您好！我是平台管理员，有任何问题或建议都联系我15305170962(微信同号)' 
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            return replyMsg.send()

        else:
            return "success"


class Pageauth(object):
    # 网页授权域名验证
     def GET(self):
        with open('MP_verify_aCCh0nG79zVP0KPc.txt','r+') as f:
            authcode = f.readline()
        return authcode


# 信息查询菜单功能
class Info(object):
    '''
    判断用户是否是VIP用户：
        1： render.info()   --> /userinfo/info.html   --> 苗木信息
        0:  render.index()  --> /user/info/index.html   --> 公告信息
    '''
    def GET(self,name): 
        try: 
            data = web.input()          
            # 1.用户同意授权，获取code
            code = data.code
            global appid
            global appsecret
            # 2.通过code换取网页access_token
            url =  "https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code".format(appid=appid,secret=appsecret,code=code)
            response = requests.get(url)
            responsedict = response.json()
            page_access_token = responsedict["access_token"]
            openid = responsedict["openid"]

            # 3. 拉取用户信息(需scope为 snsapi_userinfo)
            url = "https://api.weixin.qq.com/sns/userinfo?access_token={page_access_token}&openid={openid}&lang=zh_CN".format(page_access_token=page_access_token,openid=openid)
            response = requests.get(url)
            responsedata = response.json()
            
            # 4. 判断用户是否是会员（星标用户）
            openid = responsedata['openid']
            res = isVip(openid)
            if res:
                records = db.query('select * from infos order by createtime desc')
                return render.info(records)
            return render.index()
        except Exception as e:
            return render.index()


# 信息发布菜单功能
class Pinfo(object):
    '''   
    判断用户是否是VIP用户：
        0： render.index()   --> /userinfo/index.html   --> 公告
        1:  render.pinfo()  --> /user/info/pinfo.html   --> 苗木信息发布平台
    '''
    def GET(self,name): 
        try: 
            data = web.input()
            
            # 1.用户同意授权，获取code
            code=data.code
            global appid 
            global appsecret

            # 2.通过code换取网页access_token
            url =  "https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code".format(appid=appid,secret=appsecret,code=code)
            response = requests.get(url)
            responsedict = response.json()
            page_access_token = responsedict["access_token"]
            openid = responsedict["openid"]

            # 3. 拉取用户信息(需scope为 snsapi_userinfo)
            url = "https://api.weixin.qq.com/sns/userinfo?access_token={page_access_token}&openid={openid}&lang=zh_CN".format(page_access_token=page_access_token,openid=openid)
            response = requests.get(url)
            responsedata = response.json()
            
            # 4. 判断用户是否是会员（星标用户）
            openid = responsedata['openid']
            res = isVip(openid)
            if res: 
                return render.pinfo()
            return render.index()

        except Exception as e:
            print(e)
            return render.index()
            

# 信息发布：网页
class Pushinfo(object):
    '''
    苗木信息发布： 发布完成之后跳转到苗木信息网页

    '''
    def POST(self):
        data = web.input()
        name = data.name
        iphone = data.iphone
        address = data.address
        info = data.info
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.insert('infos', name = name, iphone = iphone, address = address, info = info, createtime = dt)
        records = db.query('select info,createtime from infos order by createtime desc')
        return render.info(records)