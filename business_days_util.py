from datetime import datetime, timedelta
import argparse
from lib.logtaker import logger
from threading import Lock
import sqlite3
import traceback


class BusinessDaysUtil(object):
    DATETIME_FORMAT = '%Y%m%d'

    HOLIDAYS = [
        '20190101',
        '20190114',
        '20190211',
        '20190321',
        '20190429',
        '20190430',
        '20190501',
        '20190502',
        '20190503',
        '20190504',
        '20190505',
        '20190506',
        '20190715',
        '20190811',
        '20190812',
        '20190916',
        '20190923',
        '20191014',
        '20191022',
        '20191103',
        '20191104',
        '20191123',
        '20200101',
        '20200113',
        '20200211',
        '20200223',
        '20200224',
        '20200320',
        '20200429',
        '20200503',
        '20200504',
        '20200505',
        '20200506',
        '20200723',
        '20200724',
        '20200810',
        '20200921',
        '20200922',
        '20201103',
        '20201123',
        '20201231',
        '20210101',
        '20210111',
        '20210211',
        '20210223',
        '20210320',
        '20210429',
        '20210503',
        '20210504',
        '20210505',
        '20210722',
        '20210723',
        '20210808',
        '20210809',
        '20210920',
        '20210923',
        '20211103',
        '20211123',
        '20211231',
    ]

    _unique_instance = None
    _lock = Lock()
    db_connection = None

    def __new__(cls):
        raise NotImplementedError('Cannot initialize via Constructor')

    @classmethod
    def __internal_new__(cls):
        return super().__new__(cls)

    @classmethod
    def init(cls):
        logger.info('initializing util class....')

        # cls.load_data_from_db()

        if not cls._unique_instance:
            with cls._lock:
                if not cls._unique_instance:
                    cls._unique_instance = cls.__internal_new__()
        return cls._unique_instance

    def load_data_from_db(self):
        logger.info('loading data from db')
        try:
            self.db_connection = sqlite3.connect()
            cur = self.db_connection.corsor()
            cur.execute("SELECT * FROM holidays")
            rows = cur.fetchall()
            return rows
        except Exception as e:
            logger.error(traceback.format_tb(e.__traceback__))

    @classmethod
    def add_n_biz_days(cls, from_date=None, n=None):
        days_to_add = n
        result = datetime.strptime(from_date, cls.DATETIME_FORMAT)
        positive = True if days_to_add > 0 else False
        if positive:
            while days_to_add > 0:
                result += timedelta(days=1)
                if result.weekday() >= 5 or result.strftime(cls.DATETIME_FORMAT) in cls.HOLIDAYS:  # sunday = 6
                    continue
                days_to_add -= 1
        else:
            while days_to_add < 0:
                result -= timedelta(days=1)
                if result.weekday() >= 5 or result.strftime(cls.DATETIME_FORMAT) in cls.HOLIDAYS:  # sunday = 6
                    continue
                days_to_add += 1
        return result.strftime(cls.DATETIME_FORMAT)

    @classmethod
    def get_closest_business_day(cls):
        target = datetime.today()
        while target.weekday() >= 5 or target.strftime(cls.DATETIME_FORMAT) in cls.HOLIDAYS:
            target -= timedelta(days=1)
        return target.strftime(cls.DATETIME_FORMAT)

    @classmethod
    def get_target_two_days(cls, ago, pattern=None):
        t2 = cls.get_closest_business_day()
        t1 = cls.add_n_biz_days(from_date=t2, n=int(ago))
        x2 = datetime.today() - datetime.strptime(t2, cls.DATETIME_FORMAT)
        x1 = datetime.today() - datetime.strptime(t1, cls.DATETIME_FORMAT)
        return t2, t1, x2.days, x1.days

    @staticmethod
    def valid(_from):
        # 20190512
        if len(_from) != 8:
            return False
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments of business days util')
    parser.add_argument('--days_to_add', help='Set how many days to add.')
    parser.add_argument('--from_date', help='From when you want to start. use %Y%m%d format')

    args = parser.parse_args()
    d = BusinessDaysUtil.add_n_biz_days(args.from_date, int(args.days_to_add))
    print(d)
