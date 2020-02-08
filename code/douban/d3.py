import requests
import lxml.etree

class DoubanBook(object):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
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

if __name__ == '__main__':
    # spider = DoubanBook(80)  # 80代表，只获取5页
    # for page, url_list in spider.get_all_pages("小说"):
    #     print(page, url_list)

    spider = DoubanBook()
    for page, url_list in spider.get_all_pages("UCD"):
        print(page, url_list)