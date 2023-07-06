# -*- coding: utf-8 -*-
import datetime
import random
from appium import webdriver
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# 创建调度器实例
scheduler = BlockingScheduler()


def send_email():
    # Email configuration
    sender_email = 'wanglonglongiii@163.com'
    receiver_email = '1367446518@qq.com'
    password = 'IPNXYLLGGCSBPTKH'

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message['From'] = f'AutoClock <{sender_email}>'
    message['To'] = receiver_email
    message['Subject'] = '今日打卡情况,请查收'

    # Attach the screenshot to the email
    with open('screenshot.png', 'rb') as f:
        image_data = f.read()
    image = MIMEImage(image_data, name='screenshot.png')
    message.attach(image)

    # 获取当前日期和时间
    current_datetime = datetime.datetime.now()
    # 格式化当前日期和时间为字符串
    current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    # Add text content to the email
    text = f"""
        当前时间为:   {current_datetime_str}   
        请查看打卡截图,确保已成功打卡。
    """
    text_part = MIMEText(text, 'plain')
    message.attach(text_part)

    # Send the email
    server = smtplib.SMTP('smtp.163.com', 25)
    server.starttls()
    server.login(sender_email, password)
    server.send_message(message)
    server.quit()
    print("打卡信息，已发送至邮箱")


def enterprise():
    print("1，打开手机，驱动企微")
    desired_caps = dict()
    desired_caps['platformName'] = 'Android'  # 可以写成android
    desired_caps['platformVersion'] = '6.0.1'  # 根据版本号码进行修改
    desired_caps['deviceName'] = 'f4c7ce96'  # 设备名字可以随便写，可以使用adb命令进行查看
    desired_caps['appPackage'] = 'com.tencent.wework'
    desired_caps['appActivity'] = 'com.tencent.wework.launch.LaunchSplashActivity'
    desired_caps['skipServerInstallation'] = True
    desired_caps["noReset"] = True  # 保存设备的缓存信息
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    print("已驱动企业微信")
    time.sleep(15)  # 等待5秒"

    # 截图
    driver.save_screenshot("screenshot.png")

    # Send the screenshot via email
    print("2.发动打卡信息")
    send_email()

    driver.quit()
    print("企业微信已退出")


def open_screen():
    cmd1 = "adb shell input keyevent 224"  # 执行 adb 命令唤醒屏幕

    # 解锁操作
    cmd2 = "adb shell input swipe 350 950 350 500"  # 根据实际情况修改滑动位置

    cmd3 = "adb shell input keyevent 26"  # 锁屏

    subprocess.call(cmd1, shell=True)
    time.sleep(2)

    subprocess.call(cmd2, shell=True)
    time.sleep(5)

    # 调用 epterprise-wechat
    enterprise()
    time.sleep(5)

    subprocess.call(cmd3, shell=True)
    print("程序运行结束，需查看邮箱"+f"    时间:{datetime.datetime.now()}")


# 添加定时任务
minute = random.randint(10,29)
print(minute)
scheduler.add_job(open_screen, 'cron', day_of_week='mon-fri', hour=8, minute=minute)  # 预设定每天早上唤醒屏幕(除却周六日)
# 启动调度器
scheduler.start()

if __name__ == '__main__':
    while True:
        time.sleep(2)
