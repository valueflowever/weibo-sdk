import requests
from datetime import datetime

from ..spider import run
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

    def get_xsrf_token(self) -> str:
        url = 'https://m.weibo.cn/api/config'
        r = requests.get(url, headers=self.headers).json()
        if r['ok'] == 1 and r['data']['login']:
            return r['data']['st']
        else:
            raise LoginError("login error")

    def post(self, content: str):
        xsrf_token = self.get_xsrf_token()
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
    def update(user_id):
        config = {'user_id_list': [user_id], 'since_date': datetime.now().strftime('%Y-%m-%d')}
        run(config)
