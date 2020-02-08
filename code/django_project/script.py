import os,sys
os.system('python manage.py makemigrations spider')
os.system('python manage.py migrate spider')
os.system('python manage.py run')
# print(sys.path)
# print(os.system('pwd'))
# print(os.system('ls'))

# str2 = ['🔥内容简介：', '    ', '玛德莱娜，一位平凡的女性，']
# str3 = ''.join(i.strip() for i in str2)
# print(str3)