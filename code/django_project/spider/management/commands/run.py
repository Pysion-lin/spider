from django.core.management.base import BaseCommand

from spider.spider import DoubanBook
from spider.models import BigTag, SmallTag, Book

Spider = DoubanBook()

class Command(BaseCommand):
    help = 'run spider'

    def handle(self, *args, **options):
        for bt, st in Spider.get_tags():
            if not BigTag.objects.filter(btag=bt[0]):
                big_tag = BigTag(btag=bt[0])
                big_tag.save()
                for t in st:
                    small_tag = SmallTag(stag=t, btag=big_tag)
                    small_tag.save()

        for t in SmallTag.objects.all():# 查询小标签出来，逐个下载
            for page, url_list in Spider.get_all_pages(t.stag):  # 获取所有翻页
                for book_url in url_list:  # 遍历列表页
                    detail = Spider.get_book_detail(book_url)
                    print('detail:',detail)
                    detail = Spider.clean_detail(detail)  # 清洗数据
                    print('clearn:',detail)
                    book = Book(**detail)
                    book.save()

