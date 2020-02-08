import pymysql.cursors


class PyMysqlBaseUsage(object):

    def __init__(self,
                 host='localhost',
                 port=3306,
                 user='user',
                 password='passwd',
                 db='db',
                 charset='utf8mb4',
                 cursorclass=pymysql.cursors.DictCursor):

        # 连接到数据库
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset=charset,
            cursorclass=cursorclass)
        print("已建立数据库连接")
    def __del__(self):
        self.connection.close()
        print('数据库已经断开')

    def create_table(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    def drop_table(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    def insert(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
        self.connection.commit()

    def select_all(self, sql, params=None):
        results = None
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
        return results

    def select_many(self, sql, params=None, size=1):
        results = None
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchmany(size)
        return results

    def select_one(self, sql, params=None):
        result = None
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
        return result


if __name__ == '__main__':
    obj = PyMysqlBaseUsage(host='192.168.19.137',password='password',user='root',db='test_db')
    # 建表语句
    # create_sql = '''
    #     CREATE TABLE `test_table` (
    #         `id` int(11) NOT NULL AUTO_INCREMENT,
    #         `colume1` varchar(255) NOT NULL,
    #         `colume2` varchar(255) NOT NULL,
    #         PRIMARY KEY (`id`)
    #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
    #     AUTO_INCREMENT=1;'''
    # obj.create_table(create_sql)

    # 删表语句
    drop_sql = '''DROP TABLE test_table'''
    obj.drop_table(drop_sql)