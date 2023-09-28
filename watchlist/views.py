from flask import request

import click
from flask import flash, redirect, url_for, render_template
from flask_login import current_user, login_required, logout_user, login_user

from watchlist import app, db
from watchlist.models import User, Movie



@app.route('/', methods=['GET', 'POST'])#注册“请求函数”，参数为url规则字符串
#一个视图函数可以绑定多个url
def index():

    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('index'))  # 重定向到主页
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
            # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html',  movies=movies)
# <!--包含变量和运算逻辑的 HTML 或其他格式的文本叫做模板-->
# <!--执行这些变量替换和逻辑计算工作的过程被称为渲染-->
# <!--Flask 会从程序实例所在模块同级目录的 templates 文件夹中寻找模板，-->
# <!--模板渲染引擎——Jinja2 ,Jinja2 的语法和 Python 大致相同,需要添加特定的定界符将 Jinja2 语句和变量标记出来-->
# <!--{{ ... }} 用来标记变量。-->
# <!--{% ... %} 用来标记语句，比如 if 语句，for 语句等。-->
# <!--{# ... #} 用来写注释。-->
# <!--render_template() 函数调用后，变量会被替换为实际的值（包括定界符），语句（及定界符）则会在执行后被移除（注释也会一并移除）-->

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


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
# 提示 在 Python 脚本里，url_for() 函数需要从 flask 包中导入，而在模板中则可以直接使用，因为 Flask 把一些常用的函数和对象添加到了模板上下文（环境）里。



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






@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    # 它会返回对应主键的记录，如果没有找到，则返回404错误响应
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录



@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required  # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页




@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')

@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页