from pymongo import MongoClient

client = MongoClient('192.168.19.137', 27017)
# client = MongoClient('mongodb://IP:27017/')

# 获取数据库，如果没有，会自动创建
db = client.test_db
# db = client['test-db']

# 获取一个collection，mongodb的collection类似mysql的表
collection = db.test_collection
# collection = db['test-collection']

# 插入数据
# mongodb插入的数据是一个json风格的的文档数据，如
data = {
    "title": "解忧杂货店",
    "author": "[日]东野圭吾",
    "publisher": "南海出版公司",
    "info": {
        "producer": "新经典文化",
        "original_title": "ナミヤ雑貨店の奇蹟",
        "translator": "李盈春",
        "publish_time": "2014/05/01",
        "page_number": 291,
        "price": 39.5,
        "pack": "精装",
        "series": "新经典文库·东野圭吾作品"
    },
    "isbn": "9787544270878",
    "rating_num": 8.6,
    "another_data": [1,2,3,"new_data"]
}

# 插入数据
obj = db.book.insert_one(data)
print(obj.inserted_id)

# 查询数据
ret = db.book.find_one({"title":"解忧杂货店"})
print(ret)

# 更新数据
ret = db.book.update({"title":"解忧杂货店"}, {"$set":{"title":"《解忧杂货店》"}})
print(ret)

# 删除数据
# ret = db.book.delete_one({"rating_num":8.6})
# ret = db.book.delete_many({"rating_num":8.6})
# print(ret.deleted_count)