from flask import Flask
#创建程序对象，实例化flask这个类
app = Flask(__name__)

@app.route('/')#注册“请求函数”，参数为url规则字符串
def hello():
    return 'Welcome to My Watchlist!'

#注1
#如果不是在app.py或者wsgi.py文件下
#则需要重新设置环境变量FLASK_APP
#> set FLASK_APP=hello.py         windows cmd
#> $env:FLASK_APP = "hello.py"     windows powershell


#注2
#FLASK_DEBUG打开调试模式
#> $env:FLASK_DEBUG = 1
#或者直接使用   flask run --debug


#注3
#使用python-dotenv自动导入系统环境变量
#.flaskenv储存flask命令行的公开环境变量
#.env储存敏感数据，不应提交到git库；把 .env 添加到 .gitignore文件的末尾来让git忽略它