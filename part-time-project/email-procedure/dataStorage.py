# 导入pymysql模块
import pymysql
# 导入getNewEmailFile.py中的email_body和email_from
from getEmailFile import email_body,email_from

# 连接MySQL数据库，需要提供主机名（host）、用户名（user）、密码（password）、数据库名称（database）和字符集（charset
mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="root123",
  database="mydatabase",
  charset='utf8'
)
# 获取数据库操作游标
mycursor = mydb.cursor()

# 插入邮件正文到MySQL中 定义要执行的SQL语句，将邮件正文和发件人地址插入到名为emails的表中的body和address字段中
sql = "INSERT INTO emails (body, address) VALUES (%s, %s)"
# 定义要插入的数据，即邮件正文和发件人地址，使用元组（tuple）来存储
val = (email_body,email_from)
# 执行SQL语句，将数据插入到数据库中
mycursor.execute(sql, val)
# 提交事务，将数据插入到数据库中
mydb.commit()
# 打印插入的记录数
print(mycursor.rowcount, "record inserted.")