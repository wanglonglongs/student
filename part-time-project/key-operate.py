import time
import win32api, win32con
from selenium import webdriver
driver = webdriver.Chrome()
driver.get('https://www.baidu.com/')
driver.maximize_window()
time.sleep(3)
# 按下CTRL键
win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
# 按下Shift键
win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
# 按下字母P键
win32api.keybd_event(ord('P'), 0, 0, 0)
# 松开字母P键
win32api.keybd_event(ord('P'), 0, win32con.KEYEVENTF_KEYUP, 0)
# 松开Shift键
win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
# 松开CTRL键
win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
time.sleep(3)
# 按下Enter键
win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
# 松开Enter键
win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
time.sleep(3)