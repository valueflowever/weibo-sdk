import pymysql
import json
import random


def get_config(config_path):
    """获取config.json数据"""
    with open(config_path) as f:
        config = json.loads(f.read())
        return config


class MysqlDB:
    def __init__(self):
        self.config = get_config('./config.json')

    def _connect(self):
        config = self.config.get('mysql_config')
        config['db'] = 'weibo'
        conn = pymysql.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['db'],
            charset=config['charset'])
        return conn

    @staticmethod
    def _close(conn, cursor):
        cursor.close()
        conn.close()

    def get(self, sql: str):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        self._close(conn, cursor)
        return result

    def execute_sql(self, sql: str):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
        finally:
            self._close(conn, cursor)


def filter_text(text_list: list) -> list:
    black_word = get_black_word()
    n_list = []
    for text in text_list:
        for w in black_word:
            if w in text:
                return n_list
        if ('【' and '】') in list(set(text)) or text.count('-') > 3 or text.count('#') == 2:
            return n_list
        if len(text) > 1:
            n_list.append(text)
    return n_list


def toggle_cookie(old_cookie) -> str:
    sql = "select cookie from weibo_cookie where is_user = 0"
    result = MysqlDB().get(sql)
    n_list = []
    if result:
        for i in result:
            n_list.append(i[0])
        try:
            n_list.remove(old_cookie)
        except ValueError as e:
            if not n_list:
                return ''
            else:
                return random.choice(n_list)
        else:
            return random.choice(n_list)


def get_black_word() -> list:
    sql = 'select word from black_word where is_delete = 0'
    words = MysqlDB().get(sql)
    black_word_list = []
    for item in words:
        black_word_list.append(item[0])
    return black_word_list