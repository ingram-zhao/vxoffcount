import xml.etree.ElementTree as ET

def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    # 解析存储xml数据
    xmlData = ET.fromstring(web_data)

    # 判断xml中数据的消息类型
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xmlData)
    elif msg_type == 'image':
        return ImageMsg(xmlData)
    elif msg_type == 'event':
        return EventMsg(xmlData)   


class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        # self.MsgId = xmlData.find('MsgId').text
        self.FromUserName = xmlData.find('FromUserName').text

class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Content = xmlData.find('Content').text.encode("utf-8")

class ImageMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text

class EventMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Event = xmlData.find('Event').text
        self.EventKey = xmlData.find('EventKey').text
    