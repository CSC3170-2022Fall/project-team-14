import pymysql


# 创建链接
# charset可写可不写
conn = pymysql.connect(host='localhost', user='root', password='root', charset='utf8mb4')
# 创建游标
cursor = conn.cursor()
# 创建数据的sql语句
sql = 'create database if not exists new_db default charset utf8 default collate utf8_general_ci;'
# 执行sql语句
cursor.execute(sql)
# 指定使用数据库
cursor.execute('use new_db;')
# 创建表的sql语句
sql_table = '''create table if not exists hero(
id int primary key auto_increment,
name varchar(20),
age char(4)
);'''
# 执行sql语句
cursor.execute(sql_table)
# 插入数据的sql语句
sql_db = "insert into hero values (1, 'Tom', '20'), (2, 'Tony', '30');"
# 执行sql语句
cursor.execute(sql_db)
# 提交事务
conn.commit()

# 查询sql语句
sql_select = "select * from hero;"
# 执行sql语句
cursor.execute(sql_select)
# 读取数据
"""
# 一次性获取一条数据
a = cursor.fetchone()
# 一次性获取所有数据
a = cursor.fetchall()
"""
a = cursor.fetchall()
for i in a:
    print(i)
