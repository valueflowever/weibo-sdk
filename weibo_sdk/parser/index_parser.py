import logging

from .info_parser import InfoParser
from .parser import Parser
from .util import handle_html, string_to_int
from ..middleware.utils import toggle_cookie

logger = logging.getLogger('spider.index_parser')


class IndexParser(Parser):
    def __init__(self, cookie, user_uri):
        self.user_uri = user_uri
        self.url = 'https://weibo.cn/%s' % user_uri
        selector = handle_html(cookie, self.url)
        if not selector.xpath("//div[@class='u']/table"):
            n_cookie = toggle_cookie(cookie)
            if n_cookie:
                logger.info("正在切换cookie...")
                self.cookie = n_cookie
            else:
                self.cookie = cookie
                logger.info("cookie无法切换")
        else:
            self.cookie = cookie
        self.selector = handle_html(self.cookie, self.url)

    def _get_user_id(self):
        """获取用户id，使用者输入的user_id不一定是正确的，可能是个性域名等，需要获取真正的user_id"""
        user_id = self.user_uri
        url_list = self.selector.xpath("//div[@class='u']//a")
        for url in url_list:
            if (url.xpath('string(.)')) == u'资料':
                if url.xpath('@href') and url.xpath('@href')[0].endswith(
                        '/info'):
                    link = url.xpath('@href')[0]
                    user_id = link[1:-5]
                    break
        return user_id

    def get_user(self):
        """获取用户信息、微博数、关注数、粉丝数"""
        try:
            user_id = self._get_user_id()
            self.user = InfoParser(self.cookie,
                                   user_id).extract_user_info()  # 获取用户信息
            self.user.id = user_id

            user_info = self.selector.xpath("//div[@class='tip2']/*/text()")
            self.user.weibo_num = string_to_int(user_info[0][3:-1])
            self.user.following = string_to_int(user_info[1][3:-1])
            self.user.followers = string_to_int(user_info[2][3:-1])
            return self.user
        except Exception as e:
            logger.exception(e)

    def get_page_num(self):
        """获取微博总页数"""
        try:
            if not self.selector.xpath("//input[@name='mp']"):
                page_num = 1
            else:
                page_num = (int)(self.selector.xpath("//input[@name='mp']")
                                 [0].attrib['value'])
            return page_num
        except Exception as e:
            logger.exception(e)
