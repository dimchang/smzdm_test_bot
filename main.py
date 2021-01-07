"""
什么值得买自动签到脚本
使用github actions 定时执行
@author : stark
"""
import requests,os
from sys import argv

from config import global_config
from j_logger import logger
from serverchan_push import push_to_wechat
import json
class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = eval(global_config.getRaw('config', 'DEFAULT_HEADERS'))
        #print(self.session.headers)
        #print(self.session.headers['Accept'])

    def __json_check(self, msg):
        """
        对请求 盖乐世社区 返回的数据进行进行检查
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            #print(result)
            return True
        except Exception as e:
            print(f'Error : {e}')            
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        self.session.headers['Cookie'] = cookies    

    def checkin(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            if  global_config.getRaw('messenger', 'enable')=='true':
                SERVERCHAN_SECRETKEY = global_config.getRaw('messenger', 'sckey')
                result=msg.json()['data']['checkin_num']
                print(result)
                #logger.info('检测到 SCKEY: {}'.format(SERVERCHAN_SECRETKEY))
                push_to_wechat(text = '什么值得买每日签到@'+str(result),
                            desp = msg,
                            secretKey = SERVERCHAN_SECRETKEY)
            return msg.json()

        return msg.content




if __name__ == '__main__':
    sb = SMZDM_Bot()
    #print(global_config.getRaw('config', 'cookies_String'))
    sb.load_cookie_str(global_config.getRaw('config', 'cookies_String'))
    #cookies = os.environ["COOKIES"]
    #sb.load_cookie_str(cookies)
    res = sb.checkin()
    #print(res)
    logger.info(res)
    
