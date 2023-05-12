import pymysql
import pandas as pd
# 连接数据库
mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="root123",
  database="mydatabase",
  charset='utf8mb4'
)

# 创建游标
cursor = mydb.cursor()

# 查询数据
sql = "SELECT * FROM emails;"
cursor.execute(sql)

# 获取查询结果
result = cursor.fetchall()
for row in result:
    print(row)
  # 创建DataFrame
    df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])

# 导出数据到Excel文件
df.to_excel("产品反馈信息表.xlsx", index=False)

print("已经成功将信息写入到excel中")

# 关闭连接
mydb.close()