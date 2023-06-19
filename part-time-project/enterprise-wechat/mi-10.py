# -*- coding: utf-8 -*-
import schedule
from appium import webdriver
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

# 创建调度器实例
scheduler = BlockingScheduler()


def open_screen():
    cmd1 = "adb shell input keyevent 224"  # 执行 adb 命令唤醒屏幕，需要安装 ADB 工具

    # 解锁操作
    cmd2 = "adb shell input swipe 510 1730 510 500"  # 根据实际情况修改滑动位置

    subprocess.call(cmd1, shell=True)
    time.sleep(2)

    subprocess.call(cmd2, shell=True)
    time.sleep(5)

    # 调用 epterprise-wechat
    enterprise()

# 添加定时任务
# scheduler.add_job(open_screen, 'cron', hour=10, minute=32, second=0)  # 10:15:07)  # 设定每天早上 7 点唤醒屏幕

# 启动调度器
# scheduler.start()


def enterprise():
    print("打开手机，驱动企微")
    desired_caps = dict()
    desired_caps['platformName'] = 'Android'  # 可以写成android
    desired_caps['platformVersion'] = '12'  # 11.1.0等都可以写成11
    desired_caps['deviceName'] = '2693bff3'  # 设备名字可以随便写，但是不可以为空
    desired_caps['appPackage'] = 'com.tencent.wework'
    desired_caps['appActivity'] = 'com.tencent.wework.launch.LaunchSplashActivity'
    desired_caps['skipServerInstallation'] = True
    desired_caps["noReset"] = True
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    print("执行start----------")
    time.sleep(5)  # 等待5秒"

    # 进入工作台页面
    driver.find_element(by='xpath',
                        value='/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.RelativeLayout[4]/android.widget.RelativeLayout/android.widget.TextView').click()
    time.sleep(2)

    # [控制台] 页面下滑·1
    driver.swipe(510, 1730, 510, 500, 1000)

    # 打卡按钮
    driver.find_element(by='xpath',
                        value='/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[5]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.ImageView').click()
    time.sleep(2)

    # 确定打卡
    driver.find_element(by='id', value='com.tencent.wework:id/bli').click()
    time.sleep(2)
    print("执行end----------")
    driver.quit()


# schedule.every().day.at("10:05").do(enterprise)
#
# while True:
#     # 检查是否有定时任务需要执行
#     schedule.run_pending()
#     # 休眠一秒钟，避免过多消耗CPU资源
#     time.sleep(1)

if __name__ == '__main__':
    open_screen()


