# -*- coding: utf-8 -*-
import schedule
from appium import webdriver
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

# 创建调度器实例
# scheduler = BlockingScheduler()
#
#
# def enterprise():
#     print("打开手机，驱动企微")
#     desired_caps = dict()
#     desired_caps['platformName'] = 'Android'  # 可以写成android
#     desired_caps['platformVersion'] = '6.0.1'  # 等都可以写成11
#     desired_caps['deviceName'] = 'f4c7ce96'  # 设备名字可以随便写，但是不可以为空
#     desired_caps['appPackage'] = 'com.tencent.wework'
#     desired_caps['appActivity'] = 'com.tencent.wework.launch.LaunchSplashActivity'
#     desired_caps['skipServerInstallation'] = True
#     desired_caps["noReset"] = True
#     driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
#     print("执行start----------")
#     time.sleep(20)  # 等待5秒"
#
#     # 截图
#     driver.save_screenshot("screenshot.png")

    # # 进入工作台页面
    # # 脆弱xpath
    # driver.find_element(by='xpath',value="/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.RelativeLayout[4]/android.widget.RelativeLayout/android.widget.TextView").click()
    # time.sleep(2)
    #
    # # [控制台] 页面下滑·1
    # driver.swipe(350,1000,350,500, 1200)
    #
    # # 打卡按钮 进入打卡页面
    # driver.find_element(by='xpath',value='/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[7]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.ImageView').click()
    # time.sleep(3)
    #
    # # 校验是否已经打卡
    # expected_title = "上班打卡"
    # actual_title = driver.find_element(by='id',value='com.tencent.wework:id/b3x').text
    # print(actual_title)
    # time.sleep(2)
    # if actual_title == expected_title:
    #     print("未打卡，执行打卡操作")
    #     driver.tap([(366, 782)], 500)
    #     print("打卡成功")
    # else:
    #     print("已经打卡")
    # print("执行end----------")
    # driver.quit()
    # print("执行end----------")


def open_screen():
    cmd1 = "adb shell input keyevent 224"  # 执行 adb 命令唤醒屏幕

    # 解锁操作
    cmd2 = "adb shell input swipe 350 950 350 500"  # 根据实际情况修改滑动位置

    cmd3 = "adb shell input keyevent 26"  # 锁屏

    subprocess.call(cmd1, shell=True)
    time.sleep(2)

    subprocess.call(cmd2, shell=True)

    # 调用 epterprise-wechat
    # enterprise()

    subprocess.call(cmd3, shell=True)

#
# # 添加定时任务
# scheduler.add_job(open_screen,'cron', day_of_week='mon-fri', hour=8, minute=18) # 预设定每天早上 8.20 点唤醒屏幕(除却周六日)
# # 启动调度器
# scheduler.start()


if __name__ == '__main__':
    open_screen()


