# unicode=utf8
import requests
import lxml.etree
import re
from datetime import datetime

class DoubanBook(object):
# 标签列表页
    tag_list_url = "https://book.douban.com/tag/?view=type&icn=index-sorttags-hot"


    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


    def get_tags(self):
        '''获取tag信息'''
        response = requests.get(self.tag_list_url,headers=self.headers)
        html = lxml.etree.HTML(response.content)
        for div in html.xpath("//div[@class='article']/div[2]/div"):
            big_tag = div.xpath("./a/@name")
            small_tags = div.xpath("./table//td/a/text()")
            yield big_tag, small_tags

    def __init__(self, end_offset=980):
        # 偏移量超过980，很可能无法获取数据
        self.end_offset = end_offset

    # 书列表，根据tag名称和offset 20
    book_list_from_tag_url = "https://book.douban.com/tag/{tag_name}?start={offset}&type=T"

    def get_one_page(self, tag_name, offset):
        '''获取书籍主页地址'''
        response = requests.get(self.book_list_from_tag_url.format(tag_name=tag_name, offset=offset),headers=self.headers)
        html = lxml.etree.HTML(response.content)
        book_url_list = html.xpath("//ul[@class='subject-list']/li/div[@class='pic']/a/@href")

        # 判断是否还有后页
        next = html.xpath("//span[@class='next']/a/@href")

        # 如果还有下一页，那么递归
        if next and offset < self.end_offset:
            return True, book_url_list
        else:
            return False, book_url_list

    def get_all_pages(self, tag_name, offset=0):
        '''翻页'''
        # 最后一页判断条件：
        #   1. 判断页面是否还有下一页
        #   2. 判断offset是否超过1000（目前豆瓣超过50页，拿不到数据）

        has_next, url_list = self.get_one_page(tag_name, offset)
        yield int((offset/20)+1), url_list
        if has_next:    # 如果有下一页，递归执行
            yield from self.get_all_pages(tag_name, offset+20)

    # book info中的所有字段
    book_info_details = [("作者", "author"),
                         ("出版社", "publisher"),
                         ("出品方", "producer"),
                         ("原作名", "original_title"),
                         ("译者", "translator"),
                         ("出版年", "publish_time"),
                         ("页数", "page_number"),
                         ("定价", "price"),
                         ("装帧", "pack"),
                         ("丛书", "series"),
                         ("ISBN", "isbn"),
                         ("副标题","subtitle")]

    def get_book_detail(self, book_url):
        '''获取书籍详情
        '''
        response = requests.get(book_url,headers=self.headers)
        html = lxml.etree.HTML(response.content)
        # info内的标签没有规则，xpath很难定位
        info_text_list = html.xpath("//div[@id='info']//text()")
        # 使用正则来处理
        info_str = "".join(info_text_list)    # 全部拼接为字符串
        info_str = re.sub(r"\s", "", info_str)    # 剔除空白字符
        info_str = re.sub(r"\xa0", "", info_str)    # 剔除无用字符

        detail = {}

        # 筛选出info中每一个字段的值
        for filed, filed_name in self.book_info_details:
            # 挨个筛选出字段，如 '作者:[日]东野圭吾出版社'
            ret = re.search("%s:(.*?):" % filed, info_str + ":")
            if ret:
                # 剔除掉 '作者:[日]东野圭吾出版社'末尾的'出版社'，其他同理
                value = re.sub("(作者|出版社|出品方|原作名|译者|出版年|页数|定价|装帧|丛书|ISBN|副标题)$", "", ret.group(1))
                detail[filed_name] = value
            else:
                detail[filed_name] = None

        # 选取标题
        book_title = html.xpath("//div[@id='wrapper']/h1/span/text()")
        detail["title"] = book_title

        # 评分：
        rating_num = html.xpath("//div[@id='interest_sectl']//strong/text()")
        detail["rating_num"] = rating_num

        # 内容简介
        book_summary = html.xpath("//div[@class='related_info']/div[@class='indent'][1]//div[@class='intro']//text()")
        detail["book_summary"] = book_summary

        # 作者简介
        # 注意indent后面那个神奇的空格
        author_summary = html.xpath("//div[@class='related_info']/div[@class='indent ']//div[@class='intro']//text()")
        detail["author_summary"] = author_summary

        return detail


    def clean_detail(self, data):
        '''
        {
          "author": str,     must
          "publisher": str,    must
          "producer": str,
          "original_title": str,
          "translator": str,
          "publish_time": datetime,    must
          "page_number": int,
          "price": float,
          "pack": str,
          "series": str,
          "isbn": str/long int,    must
          "subtitle": str,
          "title": str,    must
          "rating_num": float,    must
          "book_summary": text,    must
          "author_summary": text     must
        }
        '''
        # 1. 数据去重，略
        # 可直接根据ISBN值进行比对，方案较多

        # 2. 数据格式清洗
        yt, mt, st = 1999,1,1
        if data["publish_time"]:
            _ = data["publish_time"].split("-")
            if len(_) is 1:
                print('datetime:',_[0])
                if re.findall(r'(\d+)年.*',_[0]):
                    yt = int(re.findall(r'(\d+)年.*',_[0])[0])
                if re.findall(r'.*(\d)月',_[0]):
                    mt = int(re.findall(r'.*(\d)月',_[0])[0])
                if  re.findall(r'.*(\d)日',_[0]):
                    st = int(re.findall(r'.*(\d)日',_[0])[0])
                # if yt and mt is None and st is None:
                #     dt = datetime(yt,1,1)
                # elif yt and mt and st is None:
                #     dt = datetime(yt,mt,1)
                # elif yt and mt and st :
                #     dt = datetime(yt,mt,st)
                # else:
                #     dt = datetime(int(_[0]),1,1)
                if yt == 1999 and mt==1:
                    dt = datetime(int(_[0]), mt, st)
                else:
                    dt = datetime(yt,mt,st)
                print('dt:',dt)
            elif len(_) is 2:
                dt = datetime(int(_[0]), int(_[1]), 1)
            elif len(_) is 3:
                dt = datetime(int(_[0]), int(_[1]), int(_[2]))
            else:
                raise Exception("Can't trans %s to datetime" % data["publish_time"])
            data["publish_time"] = dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            dt = datetime(yt,mt,st)
            data["publish_time"] = dt.strftime("%Y-%m-%d %H:%M:%S")

        print('page_number:',data["page_number"])
        if data["page_number"] is not None and re.search(r'\d+',data["page_number"]):
            data["page_number"] = int(re.search(r'\d+',data["page_number"]).group())
        else:
            data["page_number"] =0

        print('price:',data["price"])
        if data["price"] is not None and re.search(r"\d+\.?\d?", data["price"]):
            data["price"] = float(re.search(r"\d+\.?\d?", data["price"]).group())
        else:
            data["price"]=0

        data["title"] = data["title"][0].strip()

        if data["rating_num"]:
            data["rating_num"] = float(data["rating_num"][0])
        else:
            data["rating_num"] = 0.0

        if data["book_summary"]:
            data["book_summary"] = "".join([i.strip() for i in data["book_summary"]])
        else:
            data["book_summary"] = ''

        if data["author_summary"]:
            data["author_summary"] = "".join([i.strip() for i in data["author_summary"]])
        else:
            data["author_summary"] = ''
            # 3. 空值赋值/ 是否需要赋值，看需求
        # 略

        return data


    def store_to_json(self, data, filename):
        import json
        with open(filename, "w") as file:
            # ensure_ascii=False，保证存储进去后，不是unicode类型数据
            file.write(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    book_url = "https://book.douban.com/subject/25862578/"

    spider = DoubanBook()

    tags_data = {}
    for bt, st in spider.get_tags():
        tags_data[bt[0]] = st

    detail = spider.get_book_detail(book_url)
    new_detail = spider.clean_detail(detail)
    spider.store_to_json(tags_data, "tags.json")
    spider.store_to_json(new_detail, "%s.json" % new_detail["title"])