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

# NAOのIPアドレス設定
ip = "192.168.11.18"

# 講義スライドの枚数
slide_num=5

# ChromeDriverのパス設定
driver = webdriver.Chrome('C:\\Users\\member\\Desktop\\slideBrowser\\chromedriver.exe')

# 使用するWebカメラの選択
webcam_id=0         # 内臓カメラは1

# NAOのWebサーバをブラウザで起動
driver.get("http://"+ip+"/apps/top.html")

# NAOのトップページ自動起動
driver.find_element_by_id("connect-btn").click()
time.sleep(10)

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

# 作成されたOpenposeの特徴量を計算し，受講状態を推定する関数
def estimate(slide_num):
    for i in range (1,slide_num+1):

        url = "http://"+ip+"/apps/slide0"+str(i)+".html"
        driver.get(url)
        btn = "slide0"+str(i)+"-btn"
        
        # 鼻，首，右肩，左肩，右目，左目，右耳，左耳の特徴量をcsvファイルから取得
        csvfile_label = "learnerPoseOutput0"+str(i)+"label.csv"
        # with open("C:\\openpose\\json\\"+csvfile_label) as f:
        #with open("C:\\openpose\\json\\"+csvfile_label,encoding="utf-8_sig") as f:
        #keypoint = csv.reader(f)
        #l = [row for row in keypoint]
        #print(l)
        df = pd.read_csv("C:\\openpose\\json\\"+csvfile_label,encoding="utf-8_sig")
        # print(df)
        # print(df.query('信頼度P > 0.8'))
        # print(df.query("label=='R_Ear'&'信頼度P<0.25'"))
        
        R_Eye = df.iloc[15]['信頼度P']
        L_Eye = df.iloc[16]['信頼度P']
        R_Ear = df.iloc[17]['信頼度P']
        L_Ear = df.iloc[18]['信頼度P']

        R_Wri = df.iloc[4]['信頼度P']
        L_Wri = df.iloc[7]['信頼度P']
      
        # 受講状態１：聞いていないの判定 
        # 右耳か左耳のいずれかの信頼度が0　または 右耳と左耳の両方の信頼度が0.25以下の場合，
        # 講義意図１：興味を持たせる（注意喚起もしくは注意維持）を実行する
        # NAOの目を光らせる，NAOがパラ言語（ピッチ・音量・速度，間・抑揚）を用いて聞いてくださいとしゃべる
        # if df.query("label=='R_Ear'&'信頼度P<0.25'"):
        if ((R_Eye or L_Eye) == 0) or ((R_Ear or L_Ear) == 0) or (R_Eye or L_Eye) < 0.25 :
            # driver.find_element_by_id("repeat-btn").click()
            # driver.refresh()
            driver.find_element_by_id("back-btn").click()
            # driver.refresh()
            driver.find_element_by_id(btn).click()
            print("受講状態１：聞いていないの判定")

        # 受講状態４：詳細を理解しているの判定
        # 右耳か左耳のいずれかの信頼度が85以上，かつ，右手首もしくは左手首の信頼度を取得できている場合，
        # 講義意図３：講義内容の詳細を理解させる（重要箇所の理解促進もしくは関係の理解促進）を実行する
        # NAOがジェスチャーや，パラ言語（ピッチ・音量・速度，間・抑揚）を用いて，スライド間の接続表現を意識してしゃべる，
        elif (R_Eye or L_Eye) > 0.85 and (R_Wri or L_Wri) > 0:
            driver.find_element_by_id("skip-btn").click()
            driver.find_element_by_tag_name("a").click()
            print("受講状態４：詳細を理解しているの判定")

        # 受講状態３：重要箇所に気づくの判定
        # 右耳か左耳のいずれかの信頼度が85以上の場合，
        # 講義意図３：講義内容の詳細を理解させる（重要箇所の理解促進もしくは関係の理解促進）を実行する
        # NAOがジェスチャーや，パラ言語（ピッチ・音量・速度，間・抑揚）を用いてしゃべる，
        elif  (R_Eye or L_Eye) > 0.85 :
            driver.find_element_by_id("pose-btn").click()
            print("受講状態３：重要箇所に気づくの判定")
    
        # 受講状態２：耳を傾けているの判定 上記以外すべての場合，
        # 講義意図２：重要箇所への集中・理解を促す（注意維持・注意誘導もしくは重要箇所の理解促進）を実行する
        # NAOが学習者の視線を意識し，がジェスチャーや，パラ言語（ピッチ・音量・速度，間・抑揚）を用いてしゃべる，
        else:
            driver.find_element_by_id(btn).click()
            print("受講状態２：耳を傾けているの判定")

# 学習者の受講状態推定に基づく講義を意図的に行う関数
def lecture(slide_num):
    for i in range (1,slide_num+1):
        url = "http://"+ip+"/apps/slide0"+str(i)+".html"
        btn = "slide0"+str(i)+"-btn"
        driver.get(url)
        driver.find_element_by_id(btn).click()
        getImage(i)
        estimate(i)
        time.sleep(5)

lecture(slide_num)