#!/usr/bin/env python

# Toshiyuki SHIMAZAKI

# 課題
# 1) Webカメラとkinectカメラのdeviceidが定まらない
# 2) sshNAOConnectでNAOにpythonコマンドを渡しても実行されない
# 3) NodeJSサーバとNAOと同期
# 4) 行列計算結果の判定
# 5) Openposeの視線画像を保存できない

# ----------------------------------------------------------
# NAOの接続情報を設定
# 
# IP_ADDRESS = '192.168.1.4'
IP_ADDRESS = '192.168.11.18'
USER_NAME = 'nao'
PASSWORD = 'kashi-lab'
# KEY_FILENAME = '/Users/macuser/.ssh/aws.pem'
# ----------------------------------------------------------

# インポート
import cv2          # OpenCV
import subprocess   # コマンドプロンプトの操作に利用
import os           # コマンドプロンプトの操作に利用
import shutil       # ファイルの移動に利用
import paramiko     # NAOにsshする際に利用
import dlib         # 機械学習系ライブラリ
import imutils      # OpenCVの補助
from imutils import face_utils
import numpy as np
import json
import pandas as pd
import csv
from pandas.io.json import json_normalize
import pprint

# NAOにssh接続するためのsshクライアントの作成のための関数

def sshNAOConnect(nao_pose_command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    # 上記で設定したIPアドレス，ユーザー名，キーファイルを渡す
    client.connect(IP_ADDRESS,
                          username=USER_NAME,
                          password=PASSWORD,
                          # key_filename=KEY_FILENAME,
                          timeout=5.0)

    stdin, stdout, stderr = client.exec_command(nao_pose_command)

    # テストコマンド実行結果を変数に格納
    cmd_result = ''
    for line in stdout:
        cmd_result += line

    # テストコマンド実行結果を出力
    print(cmd_result)

    # ssh接続断
    client.close()
    del client, stdin, stdout, stderr

# NAOにssh接続できているかテストコマンドの実行
sshtest = "ls"
sshNAOConnect(sshtest)