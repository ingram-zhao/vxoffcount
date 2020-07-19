import sys
import web
from handle import Handle,Pageauth,Info,Pinfo,Pushinfo
# from Mylog import Log

urls = (
    '/', 'Handle',
    '/MP_verify_aCCh0nG79zVP0KPc.txt', 'Pageauth',
    '/userinfo/info.html(.*)', 'Info',
    '/userinfo/pinfo.html(.*)', 'Pinfo',
    '/userinfo/pushinfo', 'Pushinfo'
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
    
