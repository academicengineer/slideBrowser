import time
from selenium import webdriver
import cv2          # OpenCV
import subprocess   # コマンドプロンプトの操作に利用
import os           # コマンドプロンプトの操作に利用
import shutil       # ファイルの移動に利用
import dlib         # 機械学習系ライブラリ
import imutils      # OpenCVの補助
from imutils import face_utils
import numpy as np
import json
import pandas as pd
import csv
from pandas.io.json import json_normalize
import pprint

# ChromeDriverのパス設定
driver = webdriver.Chrome('C:\\Users\\member\\Desktop\\slideBrowser\\chromedriver.exe')

# 使用するWebカメラの選択
webcam_id=0         # 内臓カメラは1

# 講義スライドの枚数
slide_num=5

# NAOのWebサーバをブラウザで起動
driver.get('http://192.168.11.18/apps/top.html')

# NAOのテスト起動
driver.find_element_by_id("connect-btn").click()
# time.sleep(10)

# Openposeで姿勢推定するための学習者の画像をWebカメラで撮影するための関数
def getImage(slide_num):
    os.chdir("C://openpose")
    print("Webカメラで姿勢を撮影します"+str(slide_num)+"回目:")
    capture = cv2.VideoCapture(webcam_id)
    poseret, poseframe = capture.read()
    poseid = "learnerPose0"+ str(slide_num)
    poseimage =  poseid + ".jpg"
    cv2.imwrite(poseimage, poseframe)
    shutil.move(poseimage,"examples//media")
    # shutil.move(poseimage,"poseimage")
    print(poseimage+"を撮影しました")
     # Openposeにより姿勢推定を実行し，jsonファイルを出力
    print("視線推定を開始します"+str(slide_num)+"回目:")
    cmd = "bin\OpenPoseDemo.exe --image_dir examples\media\ --write_json ."
    # cmd = "bin\OpenPoseDemo.exe --image_dir examples\media\ --face --hand  --write_json ."
    print(poseimage)
    poseres = subprocess.call(cmd, shell=True)
    jsonfile = poseid + "_keypoints.json"
    shutil.move(jsonfile,"json")
    print(jsonfile+"を作成しました")

    # json から必要な評価指標のみ抽出した csv　ファイルを作成する
    os.chdir("C://openpose//json")

    #poseid = "learnerPose0"+ str(i)
    #jsonfile = str((poseid + "_keypoints.json"))
    #print(jsonfile)
    
    # JSONファイルを開き，読み込む
    json_open = open(jsonfile, 'r')
    json_load = json.load(json_open)

    # JSONファイルの加工
    data = np.array(json_load['people'][0]['pose_keypoints_2d']).reshape(-1,3)
    df_label = pd.DataFrame(data, columns=['X座標','Y座標','信頼度P'], index=['Nose','Neck','R_Sholder','R_Elbow','R_Wrist','L_Sholder','L_Elbow','L_Wrist','Hip','R_Hip','R_nee','R_Ankle','L_Hip','L_Knee','L_Ankle','R_Eye','L_Eye','R_Ear','L_Ear','L_foot1','L_foot2','L_foot3','R_foot1','R_foot2','R_foot3'])

    # columnsを表示させる時は上記のコメントアウトを外し，下記をコメントアウト
    df = pd.DataFrame(data, index=['Nose','Neck','R_Sholder','R_Elbow','R_Wrist','L_Sholder','L_Elbow','L_Wrist','Hip','R_Hip','R_nee','R_Ankle','L_Hip','L_Knee','L_Ankle','R_Eye','L_Eye','R_Ear','L_Ear','L_foot1','L_foot2','L_foot3','R_foot1','R_foot2','R_foot3'])

    # 削除する姿勢座標を選択
    drop_index = ['R_Elbow','R_Wrist','L_Elbow','L_Wrist','Hip','R_Hip','R_nee','R_Ankle','L_Hip','L_Knee','L_Ankle','L_foot1','L_foot2','L_foot3','R_foot1','R_foot2','R_foot3']
    
    # 削除
    df = df.drop(drop_index, axis=0)

    # CSVに掃き出し
    csvfile_label = "learnerPoseOutput0"+str(slide_num)+"label.csv"
    csvfile = "learnerPoseOutput0"+str(slide_num)+".csv"
    #print(csvfile)

    # df.to_csv(csvfile, encoding='utf-8')

    # indexを表示させる時は上記のコメントアウトを外し，下記をコメントアウト
    df_label.to_csv(csvfile_label, encoding='utf-8')
    df.to_csv(csvfile, encoding='utf-8', index=False)
    print(csvfile_label+"と"+csvfile+"を作成しました")

def lecture(slide_num):
    for i in range (1,slide_num):
        url = "http://192.168.11.18/apps/slide0"+str(i)+".html"
        btn = "slide0"+str(i)+"-btn"
        driver.get(url)
        driver.find_element_by_id(btn).click()
        getImage(i)
        time.sleep(10)

lecture(slide_num)