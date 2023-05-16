#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import zipfile
import logging
from datetime import datetime

import pymysql
import schedule

def scan_folder(source_folder):
    """
    扫描源文件夹中的文件和子文件夹，并返回文件列表
    """
    file_list = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    print("正在执行扫描文件以及子文件......")
    return file_list


def backup_files(source_folder, backup_folder):
    """
    备份文件到指定文件夹
    """
    file_list = scan_folder(source_folder)  # 获取文件列表
    for file_path in file_list:
        target_path = file_path.replace(source_folder, backup_folder)  # 构建目标文件路径
        os.makedirs(os.path.dirname(target_path), exist_ok=True)  # 创建目标文件夹（包括父文件夹）
        shutil.copy2(file_path, target_path)  # 复制文件到目标路径
    print("正在执行备份文件夹到指定文件夹中......")


def compress_backup_folder(backup_folder, backup_zip):
    """
    压缩备份文件夹为档案文件
    """
    with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
        for root, dirs, files in os.walk(backup_folder):
            if root == backup_zip:
                continue
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, backup_folder))
        print("压缩备份文件")


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def log_backup_info(source_folder, backup_folder,backup_zip):
    """
    数据备份信息导入到数据库
    """
    # 连接MySQL数据库，需要提供主机名（host）、用户名（user）、密码（password）、数据库名称（database）和字符集（charset
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="root123",
        database="mydatabase",
        charset='utf8'
    )# 获取数据库操作游标
    mycursor = mydb.cursor()

    folder_path = r"F:\backup"
    size = get_folder_size(folder_path)
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # 插入邮件正文到MySQL中 定义要执行的SQL语句，将邮件正文和发件人地址插入到名为emails的表中的body和address字段中
    sql = "INSERT INTO backup_recording(size,formatted_time,source_folder,backup_folder,backup_zip) VALUES (%s,%s,%s,%s,%s)"
    # 定义要插入的数据，即文件大小,源文件地址，目标文件地址，压缩文件地址，备份时间等信息，使用元组（tuple）来存储
    val = (size,formatted_time,source_folder,backup_folder,backup_zip)
    # 执行SQL语句，将数据插入到数据库中
    mycursor.execute(sql, val)
    # 提交事务，将数据插入到数据库中
    mydb.commit()
    # 打印插入的记录数
    print(mycursor.rowcount, "record inserted.")
    """
    记录备份信息到日志文件
    """
    logging.basicConfig(filename='backup_log.txt', level=logging.DEBUG)
    logging.info(f"文件大小为：{size}kb,备份时间为：{formatted_time},源文件地址为: {source_folder}, 备份文件地址为: {backup_folder},压缩文件地址为：{backup_zip}")
    print(f"文件大小为：{size}kb,备份时间为：{formatted_time},源文件地址为: {source_folder}, 备份文件地址为: {backup_folder},压缩文件地址为：{backup_zip}")
    exit()


def main():
    # 主程序入口
    source_folder = 'F:\photo'  # 源文件夹路径
    backup_folder = 'F:\imager'  # 备份文件夹路径
    backup_zip = r'F:\backup\backup.zip'  # 备份档案文件路径
    try:
        backup_files(source_folder, backup_folder)  # 备份文件
        compress_backup_folder(backup_folder, backup_zip)  # 压缩备份文件夹
        log_backup_info(source_folder, backup_folder,backup_zip)  # 记录备份信息

    except Exception as e:
        logging.error(f"An error occurred during backup: {str(e)}")
        exit()

