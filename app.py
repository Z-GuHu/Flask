from flask import Flask, render_template
from flask import url_for
from markupsafe import escape


name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


#创建程序对象，实例化flask这个类
app = Flask(__name__)








@app.route('/')#注册“请求函数”，参数为url规则字符串
#一个视图函数可以绑定多个url
def index():
    return render_template('index.html', name=name, movies=movies)
# <!--包含变量和运算逻辑的 HTML 或其他格式的文本叫做模板-->
# <!--执行这些变量替换和逻辑计算工作的过程被称为渲染-->
# <!--Flask 会从程序实例所在模块同级目录的 templates 文件夹中寻找模板，-->
# <!--模板渲染引擎——Jinja2 ,Jinja2 的语法和 Python 大致相同,需要添加特定的定界符将 Jinja2 语句和变量标记出来-->
# <!--{{ ... }} 用来标记变量。-->
# <!--{% ... %} 用来标记语句，比如 if 语句，for 语句等。-->
# <!--{# ... #} 用来写注释。-->
# <!--render_template() 函数调用后，变量会被替换为实际的值（包括定界符），语句（及定界符）则会在执行后被移除（注释也会一并移除）-->


@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请访问 http://localhost:5000/test 后在命令行窗口查看输出的 URL）：
    # print(url_for('hello'))  # 生成 hello 视图函数对应的 URL，将会输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    # print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    # print(url_for('user_page', name='peter'))  # 输出：/user/peter
    # print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'


@app.route('/user/<name>')  #路径中添加变量
# /user/<int:number> 会将 URL 中的 number 部分转换成整型。
# 获取变量
def user_page(name):
    return f'User: {escape(name)}'
# 注意 用户输入的数据会包含恶意代码，所以不能直接作为响应返回，需要使用 MarkupSafe（Flask 的依赖之一）提供的 escape() 函数对 name 变量进行转义处理，比如把 < 转换成 &lt;。这样在返回响应时浏览器就不会把它们当做代码执行。




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
# 名字以 . 开头的文件默认会被隐藏，执行 ls 命令时会看不到它们，这时你可以使用 ls -f 命令来列出所有文件.








