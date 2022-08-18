import requests
from datetime import datetime
from lxml import etree
import time

from ..spider import run, logger
from ..exception import LoginError


class Poster:
    def __init__(self, cookie):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/12.0 Mobile/15A372 Safari/604.1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://m.weibo.cn',
            'Host': 'm.weibo.cn',
            'Accept': 'application/json, text/plain, */*',
            'Connection': 'keep-alive',
            'Referer': 'https://m.weibo.cn/compose/',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'MWeibo-Pwa': '1',
            'cookie': cookie
        }
        self.cn_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/12.0 Mobile/15A372 Safari/604.1',
            'referer': 'https://weibo.cn/',
            'cookie': self.headers['cookie']
        }

    def get_xsrf_token(self) -> str:
        url = 'https://m.weibo.cn/api/config'
        r = requests.get(url, headers=self.headers).json()
        if r['ok'] == 1 and r['data']['login']:
            return r['data']['st']
        else:
            logger.error(LoginError)
            return ''

    def post(self, content: str):
        xsrf_token = self.get_xsrf_token()
        if not xsrf_token:
            return "login failed"
        url = 'https://m.weibo.cn/api/statuses/update'
        params = {
            'content': content,
            'st': xsrf_token,
            '_spr': 'screen:2560x1440',
        }
        res = requests.post(url, headers=self.headers, params=params)
        if res.status_code == 200 and res.json()['ok'] == 1:
            return "success"
        else:
            return "failed"

    @staticmethod
    def update(user_id, cookie):
        config = {'cookie': cookie, 'user_id_list': [user_id], 'since_date': datetime.now().strftime('%Y-%m-%d')}
        run(config)

    def get_cn_st(self):
        url = 'https://weibo.cn/'
        for i in range(3):
            try:
                resp = requests.get(url, headers=self.cn_headers)
                selector = etree.HTML(resp.content)
                st = selector.xpath('//div/form/@action')[0].split('=')[-1]
            except AttributeError as e:
                logger.error(e)
            else:
                return st
            time.sleep(1)

    def weibo_exist(self, content_id):
        url = f'https://weibo.cn/comment/{content_id}'
        for i in range(3):
            try:
                resp = requests.get(url, headers=self.cn_headers)
                selector = etree.HTML(resp.content)
                info = selector.xpath("//div[@class='me']")
            except AttributeError as e:
                logger.error(e)
            else:
                return info
            time.sleep(1)

    def delete(self, content_id):
        weibo_not_exist = self.weibo_exist(content_id)
        if weibo_not_exist:
            return "none"
        st = self.get_cn_st()
        if not st:
            return "failed"
        delete_url = f'https://weibo.cn/mblog/del?type=del&id={content_id}&act=delc&rl=0&st={st}'
        d = requests.get(delete_url, headers=self.cn_headers)
        if d.status_code == 200:
            info_exist = self.weibo_exist(content_id)
            if info_exist:
                return "success"
            else:
                return "failed"
        else:
            return "failed"
