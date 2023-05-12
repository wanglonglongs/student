# 1，导入所需的模块，包括imaplib、email和decode_header。
# IMAP库，用于邮件的接收
import imaplib
# email库，用于解析邮件
import email
# 解码邮件头
from email.header import decode_header
# 2，设置IMAP服务器和认证信息
# IMAP服务器
imap_server = "imap.gmail.com"
# 用户名
imap_username = "wanlonglongiii@gmail.com"
# 密码
imap_password = "ovbiornryoqckujk"

# 3，连接IMAP服务器并登录
# SSL方式连接IMAP服务器
mail = imaplib.IMAP4_SSL(imap_server)
mail.login(imap_username, imap_password)

# 4，选择收件箱
mail.select("inbox")

# 5，搜索所有标题为“产品用户体验反馈”的邮件
# 搜索字符串
search_string = '(SUBJECT "User experience feedback")'.encode('UTF-8')
# 搜索匹配邮件的UID
result, data = mail.uid('search', None, search_string)

# 6，遍历所有邮件的UID并获取RFC822内容
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


# 7,关闭连接
# 关闭邮箱
mail.close()
# 退出登录
mail.logout()
