# import sys
# print(sys.path)
# print(sys.platform)
# sys.path.insert(0,'/root/code')
# print(sys.path)
import re


str = """<div>
    <p>岗位职责：</p>
    <p>完成推荐算法、数据统计、接口、后台等服务器端相关工作</p>
    <p><br></p>
    <p>必备要求：</p>
    <p>良好的自我驱动力和职业素养，工作积极主动、结果导向</p>
    <p> <br></p>
    <p>技术要求：</p>
    <p>1、一年以上 Python 开发经验，掌握面向对象分析和设计，了解设计模式</p>
    <p>2、掌握HTTP协议，熟悉MVC、MVVM等概念以及相关WEB开发框架</p>
    <p>3、掌握关系数据库开发设计，掌握 SQL，熟练使用 MySQL/PostgreSQL 中的一种<br></p>
    <p>4、掌握NoSQL、MQ，熟练使用对应技术解决方案</p>
    <p>5、熟悉 Javascript/CSS/HTML5，JQuery、React、Vue.js</p>
    <p> <br></p>
    <p>加分项：</p>
    <p>大数据，数理统计，机器学习，sklearn，高性能，大并发。</p>
    </div> """


match = re.sub(r"<[^>]*>|&nbsp;|\s",'',str)
# print(match)

str1 = 'asdfa dsafdf asfwghaf'
# match1 = re.match(r'.*',str,re.S)
# match1 = re.match(r"<(?P<p1>\w*)><(?P<p2>\w*)>.*</(?P=p2)></(?P=p2)>",str,re.S)
# match1 = re.match(r"<(?P<nbp1>\w*)>\s*<\w*>.?",str,re.S)
# match1 = re.sub(r"<[^>]*>|\s",'',str)
# match1 = re.findall(r'<p.*?>.*?</p>',str,re.M)
# print(match1)
# print(len(match1))

# if match1:
#     print(match1.group())
#     print(len(match1.group()))

# with open('./yarn-root-resourcemanager-hadoop-master.log','r') as log:
#     logs = log.read()

# match2 = re.search(r'(INFO\s.*)',logs,re.M)
# if match2:
#     print(match2.group())

# string = r'cs_item_sk[\s=]*(\d*?1+)\s+.+?true\s*(\d+)$'
string = r'.*2640'
# string = r'cs_item_sk'
# pattern = re.compile(string)

with open('./test.log', 'r') as f:
    for line in f.readlines():
        line = line.strip()
        # line = 'where cs_item_sk =997'
        m = re.findall(string,line)
        print(m)
        # if m is not None:
        #     print(m.groups())