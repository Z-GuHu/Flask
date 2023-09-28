from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist.__init__ import db



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
