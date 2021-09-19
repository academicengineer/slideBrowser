import csv
import numpy as np
import scipy

def estimate(slide_num):
    # 鼻，首，右肩，左肩，右目，左目，右耳，左耳の特徴量をcsvファイルから取得
    csvfile_label = "learnerPoseOutput0"+str(slide_num)+"label.csv"
    # with open("C:\\openpose\\json\\"+csvfile_label) as f:
    with open("C:\\openpose\\json\\"+csvfile_label,encoding="utf-8_sig") as f:
        keypoint = csv.reader(f)
        l = [row for row in keypoint]
        r_ear = 
        l_ear =
        r_
        #for row in keypoint:
            #print(row)
        
    # 受講状態１：聞いていないの判定 
    # 右耳か左耳のいずれかの信頼度が0　または 右耳と左耳の両方の信頼度が0.25以下の場合，
    # 講義意図１：興味を持たせる（注意喚起もしくは注意維持）を実行する
    # NAOの目を光らせる，NAOがパラ言語（ピッチ・音量・速度，間・抑揚）を用いて聞いてくださいとしゃべる
    if 

    # 受講状態３：重要箇所に気づくの判定
    # 右耳か左耳のいずれかの信頼度が85以上の場合，
    # 講義意図３：講義内容の詳細を理解させる（重要箇所の理解促進もしくは関係の理解促進）を実行する
    # NAOがジェスチャーや，パラ言語（ピッチ・音量・速度，間・抑揚）を用いてしゃべる，

    # 受講状態４：詳細を理解しているの判定
    # 右耳か左耳のいずれかの信頼度が85以上，かつ，右手首もしくは左手首の信頼度を取得できている場合，
    # 講義意図３：講義内容の詳細を理解させる（重要箇所の理解促進もしくは関係の理解促進）を実行する
    # NAOがジェスチャーや，パラ言語（ピッチ・音量・速度，間・抑揚）を用いて，スライド間の接続表現を意識してしゃべる，

    # 受講状態２：耳を傾けているの判定 上記以外すべての場合，
    # 講義意図２：重要箇所への集中・理解を促す（注意維持・注意誘導もしくは重要箇所の理解促進）を実行する
    # NAOが学習者の視線を意識し，がジェスチャーや，パラ言語（ピッチ・音量・速度，間・抑揚）を用いてしゃべる，

    return 


estimate(1)