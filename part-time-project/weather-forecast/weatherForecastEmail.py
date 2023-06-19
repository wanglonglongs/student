import smtplib
# 导入smplip
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from weather_forecast import final
import schedule
import time


class sendEmail:
    def __init__(self, recipient: str, sender: str = "wanglonglongiii@163.com", password: str = "IPNXYLLGGCSBPTKH",serverAddress: str = 'smtp.163.com'):
        """
            recipient: 接收者邮箱
            sender:    发送者邮箱
            password:  发送者授权码
            serverAddress: 服务器地址
        """
        self.sender = sender  # 发送者邮箱
        self.password = password  # 授权码
        self.recipient = recipient  # 接收者邮箱
        self.serverAddress = serverAddress  # 服务器地址

    @staticmethod
    def message(title: str, text: str, sender: str, recipient: str, types: str = "plain", name: str = None,
                file: str = None):
        """
            title:  邮件标题
            text:   邮件正文
            types:  文本格式 plain(纯文本)/html(html代码)
            sender:   发送者邮箱
            recipient： 接收者邮箱
            name:   自定义邮件名称
            file:   附件路径
        """
        if file:
            message = MIMEMultipart()
            # 这里的三个参数：第一个为文本内容，第二个文本格式 plain(纯文本)/html(html代码)，第三个 utf-8 设置编码
            message.attach(MIMEText(text, types, 'utf-8'))
            att1 = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = f'attachment; filename="{file}"'  # 设置文件名称
            message.attach(att1)
        else:
            # 这里的三个参数：第一个为文本内容，第二个文本格式 plain(纯文本)/html(html代码)，第三个 utf-8 设置编码
            message = MIMEText(text, types, 'utf-8')
        message['To'] = Header(recipient)  # 接收者
        message['From'] = Header(formataddr((name, sender), "utf-8"))  # 接收者
        message['Subject'] = Header(title, 'utf-8')  # 设置标题
        return message

    def send(self, title: str, text: str, types: str = "plain", name: str = None, file: str = None, ):
        """
            title:  邮件标题
            text:   邮件正文
            types:  文本格式 plain(纯文本)/html(html代码)
            name :  自定义邮件名称
            file:   附件路径
        """
        try:
            print("邮件发送中..")
            mtpObj = smtplib.SMTP_SSL(self.serverAddress)
            # 建立连接
            mtpObj.connect(self.serverAddress, 587)
            # 登录--发送者账号和口令
            mtpObj.login(self.sender, self.password)
            # 设置发送信息
            message = self.message(title, text, self.sender, self.recipient, types=types, name=name,
                                   file=file, )
            # 发送邮件
            mtpObj.sendmail(self.sender, self.recipient, message.as_string())
            print("邮件发送成功")
            mtpObj.quit()
        except smtplib.SMTPException:
            print("无法发送邮件")


def send_weather_email():
    # 拉取当天的天气状况
    # 实例化对象，传入接收者邮箱参数recipient
    p1 = sendEmail(recipient="wanglonglongiii@163.com")
    p2 = sendEmail(recipient="382909759@qq.com")
    p3 = sendEmail(recipient="2139165110@qq.com")
    title = "天气提醒~祝您一天好心情哦"
    text = f"您好，当前日期为{final[0][0]}，天气状况:{final[0][1]},最高温度：{final[0][2]}，最低温度：{final[0][3]}，记得穿合适的衣服呢！" \
           f"您要更好地应对天气变化，预防相关天气状况引起的疾病或其他不适。按时上班哦！"
    p1.send(title=title, text=text, name="上海网络有限公司")
    p2.send(title=title, text=text, name="意大利中文网络有限公司")
    p3.send(title=title, text=text, name="深圳网络有限公司")
    """
    send参数说明:
        title:  必传  邮件标题
        text:   必传  邮件正文
        types:  选传  文本格式 plain(纯文本)/html(html代码) 默认为plain
        name :  选传  自定义邮件名称
        file:   选传  附件路径
    """

# 设置定时任务，每天的特定时间执行send_weather_email函数
schedule.every().day.at("08:40").do(send_weather_email)

while True:
    # 检查是否有定时任务需要执行
    schedule.run_pending()
    # 休眠一秒钟，避免过多消耗CPU资源
    time.sleep(1)