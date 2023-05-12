# 导入模块
import pymysql
import imaplib
import email
from email.header import decode_header

# 设置IMAP服务器和认证信息
imap_server = "imap.gmail.com"
imap_username = "wanlonglongiii@gmail.com"
imap_password = "ovbiornryoqckujk"

# 连接IMAP服务器并登录
with imaplib.IMAP4_SSL(imap_server) as mail:
    mail.login(imap_username, imap_password)

    # 选择收件箱
    mail.select("inbox")

    # 搜索所有标题为“产品用户体验反馈”的邮件
    search_string = '(SUBJECT "User experience feedback")'.encode('UTF-8')
    result, data = mail.uid('search', None, search_string)

    # 连接MySQL数据库
    with pymysql.connect(
        host="localhost",
        user="root",
        password="root123",
        database="mydatabase",
        charset='utf8mb4'
    ) as mydb:
        # 获取数据库操作游标
        with mydb.cursor() as mycursor:
            # 遍历所有邮件的UID并获取RFC822内容
            emails_list = []
            for uid in data[0].split():
                # 获取RFC822格式的邮件内容
                result, data = mail.uid('fetch', uid, '(RFC822)')
                # 获取邮件内容的第二部分
                raw_email = data[0][1]
                # 解析邮件内容
                email_message = email.message_from_bytes(raw_email)

                # 邮件的主题和发件人。
                # 解码邮件主题
                email_subject = decode_header(email_message["Subject"])[0][0]
                # 解码邮件发件人
                email_from = decode_header(email_message["From"])[0][0]
                print(f"Email: {email_subject} from {email_from}")

                # 获取邮件正文
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        # 解码邮件正文
                        email_body = part.get_payload(decode=True).decode()

                # 打印邮件正文
                print(email_body)
                # 将邮件信息存储在列表中
                emails_list.append((email_body, email_from))

            # 插入邮件正文到MySQL中
            sql = "INSERT INTO emails (body, address) VALUES (%s, %s)"
            mycursor.executemany(sql, emails_list)

            mydb.commit()
            # 打印插入的记录数
            print(mycursor.rowcount, "records inserted.")

    # 关闭邮箱
    mail.close()
    # 退出登录
    mail.logout()
