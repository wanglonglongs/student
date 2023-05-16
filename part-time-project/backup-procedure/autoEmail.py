#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from aotu_backup import main
# 发送方邮箱地址和密码
sender_email = "wanglonglongiii@163.com"
password = "IPNXYLLGGCSBPTKH"

# 收件方邮箱地址
recipient_email = "wanglonglongiii@163.com"

# 构建邮件
msg = MIMEMultipart()
msg['Subject'] = '相册备份文件'  # 邮件主题
msg['From'] = sender_email  # 发件人
msg['To'] = recipient_email  # 收件人

# 执行备份操作
main()

# 邮件正文
text = MIMEText('新备份的照片，请查收', 'plain')
msg.attach(text)
# 附件
with open(r'F:\backup\backup.zip', 'rb') as f:
    attachment = MIMEApplication(f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename='backup.zip')
    msg.attach(attachment)

# 发送邮件
with smtplib.SMTP('smtp.163.com', 25) as smtp:
    smtp.login(sender_email, password)
    smtp.sendmail(sender_email, recipient_email, msg.as_string())
    print("已发送完成")

# schedule.every().day.at("22:00").do(main)  # 定时执行主程序