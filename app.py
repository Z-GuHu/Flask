import os
import sys
import click


from flask import Flask, render_template, redirect, flash
from flask import url_for, request
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user,login_user, logout_user, login_required

#兼容性处理
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'





#创建程序对象，实例化flask这个类
app = Flask(__name__)
#为了设置 Flask、扩展或是我们程序本身的一些行为，我们需要设置和定义一些配置变量。
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'
# 在扩展类实例化前加载配置############
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app
login_manager = LoginManager(app)
login_manager.login_view = 'login'
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


#创建数据库模型
class User(db.Model, UserMixin):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值



class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份
# 模型类要声明继承 db.Model。
# 每一个类属性（字段）要实例化 db.Column，传入的参数为字段的类型，
# 在 db.Column() 中添加额外的选项（参数）可以对字段进行设置。

#实例化数据库模型后，需要创建数据库表格，并传入数据
# >>> from app import User, Movie  # 导入模型类
# >>> user = User(name='Grey Li')  # 创建一个 User 记录
# >>> m1 = Movie(title='Leon', year='1994')  # 创建一个 Movie 记录
# >>> m2 = Movie(title='Mahjong', year='1996')  # 再创建一个 Movie 记录
# >>> db.session.add(user)  # 把新创建的记录添加到数据库会话
# >>> db.session.add(m1)
# >>> db.session.add(m2)
# >>> db.session.commit()  # 提交数据库会话，只需要在最后调用一次即可
# 在实例化模型类的时候，我们并没有传入 id 字段（主键），因为 SQLAlchemy 会自动处理这个字段。
# 最后一行 db.session.commit() 很重要，只有调用了这一行才会真正把记录提交进数据库，前面的 db.session.add() 调用是将改动添加进数据库会话（一个临时区域）中。


# 查询语句的格式如下：
# <模型类>.query.<过滤方法（可选）>.<查询方法>
    #过滤方法    # filter()	使用指定的规则过滤记录，返回新产生的查询对象
                # filter_by()	使用指定规则过滤记录（以关键字表达式的形式），返回新产生的查询对象
                # order_by()	根据指定条件对记录进行排序，返回新产生的查询对象
                # group_by()	根据指定条件对记录进行分组，返回新产生的查询对象

    #查询方法     # all()	返回包含所有查询记录的列表
                # first()	返回查询的第一条记录，如果未找到，则返回 None
                # get(id)	传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回 None
                # count()	返回查询结果的数量
                # first_or_404()	返回查询的第一条记录，如果未找到，则返回 404 错误响应
                # get_or_404(id)	传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回 404 错误响应
                # paginate()	返回一个 Pagination 对象，可以对记录进行分页处理

# >>> from app import Movie  # 导入模型类
# >>> movie = Movie.query.first()  # 获取 Movie 模型的第一个记录（返回模型类实例）
# >>> movie.title  # 对返回的模型类实例调用属性即可获取记录的各字段数据
# 'Leon'
# >>> movie.year
# '1994'
# >>> Movie.query.all()  # 获取 Movie 模型的所有记录，返回包含多个模型类实例的列表
# [<Movie 1>, <Movie 2>]
# >>> Movie.query.count()  # 获取 Movie 模型所有记录的数量
# 2
# >>> Movie.query.get(1)  # 获取主键值为 1 的记录
# <Movie 1>
# >>> Movie.query.filter_by(title='Mahjong').first()  # 获取 title 字段值为 Mahjong 的记录
# <Movie 2>
# >>> Movie.query.filter(Movie.title=='Mahjong').first()  # 等同于上面的查询，但使用不同的过滤方法
# <Movie 2>


# 更新了 Movie 模型中主键为 2 的记录：
# >>> movie = Movie.query.get(2)
# >>> movie.title = 'WALL-E'  # 直接对实例属性赋予新的值即可
# >>> movie.year = '2008'
# >>> db.session.commit()  # 注意仍然需要调用这一行来提交改动


# 删除了 Movie 模型中主键为 1 的记录：
# >>> movie = Movie.query.get(1)
# >>> db.session.delete(movie)  # 使用 db.session.delete() 方法删除记录，传入模型实例
# >>> db.session.commit()  # 提交改动

#把上边在flask shell执行的命令转换成终端命令，一次性实现数据的增加。
@app.cli.command()
def forge():
    db.create_all()

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

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')





# 自定义命令 initdb，建表

@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息
# flask initdb   命令创建数据库表
# flask initdb --drop  使用 --drop选项删除表格并重新创建


#错误处理函数
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    #return render_template('404.html', user=user), 404  # 返回模板和状态码
    return render_template('404.html'), 404#有了模板上下文处理函数

#模板上下文处理函数
@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}
# 这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用。


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



@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象

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