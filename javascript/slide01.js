$(function(){
    var qis, ip, als = {};

    // 接続ボタンclickイベント
    $('#slide01-btn').on('click', function(){
        // 入力IP取得
        ip = $('#ip').val();
        // NAOqi Session 生成
        qis = new QiSession(ip);
        // 接続
        qis.socket()
        .on('connect', function(){
            // 接続成功
            console.log('[CONNECTED]');

            // ALTextToSpeechを使う
            qis.service('ALAnimatedSpeech').done(function(aas){
                als.alAnimatedSpeech = aas;
                //console.log('接続成功');
                aas.say('皆さん，おはようございます。今日はいい天気ですね');
            });

            // 接続断
            //console.log('[DISCONNECTED]');
        })
        .on('error', function(){
            // 接続エラー
            console.log('[CONNECTION ERROR]');
            qis.service('ALAnimatedSpeech').done(function(aas){
                als.alAnimatedSpeech = aas;
                aas.say('NAO、起動に失敗しました');
            });
        });
    });

    // テストボタンclickイベント
        $('#slide-btn').on('click', function(){
        // 講義開始
        const promise = new Promise((resolve) => {
            console.log('[SLIDE01]');
            window.open('lec01.png', '_blank');
            qis.service('ALAnimatedSpeech').done(function(aas){
                als.alAnimatedSpeech = aas;
                aas.say('それでは講義を始めます。よろしくお願いいたします。今日は，学習工学特論の第一回目の講義です。それでは，スライドを御覧ください。。学習工学は，人間の学びをモデルとしてデザインし，デザインに基づく学習支援システムの開発と評価を行う研究分野です。人間の学びとは？という問いを知識工学や認知科学の理論を応用した学術研究分野です');
            });
            resolve();
        }).then(() => {
            console.log('[SLIDE02]');
            //location.href = 'lec02.png';
            qis.service('ALAnimatedSpeech').done(function(aas){
                als.alAnimatedSpeech = aas;
                aas.say('いかがでしょうか。質問はありますか。特に柏原研究室では「学習モデル作りこそeLearning研究の本質」と捉え、先進的なeLearningの実現を目指して研究を進めています。今日は，学習工学特論の第一回目の講義でした。これで講義を終わります。ありがとうございました。');
            });
        });
        
        //　画像認識結果から学習者の受講状況取得
    
        // 受講状況がうつ伏せ状態の場合
    
        // 受講状況がうなづきの場合
            
        // 視線が適切でない場合
    
        //　例外処理
        
        //講義スライドに画面遷移

    })
    .on('disconnect', function(){
        //if(als.alTextToSpeech) als.alTextToSpeech.say('接続失敗です');
        qis.service('ALAnimatedSpeech').done(function(ins){
            ins.say('こんにちは、僕はNAO先生です');
        });
    });
});

            /*
            qis.service('ALPhotoCaptureProxy').done(function(apc){
                als.alPhotoCaptureProxy = apc;
                apc.takePicture();
            });
            */

            /*
            qis.service('ALRobotPosture').done(function(arp){
                als.alRobotPosture = arp;
                arp.goToPosture('StandInit', 1.0);
                arp.goToPosture('SitRelax', 1.0);
                arp.goToPosture('StandZero', 1.0);
                arp.goToPosture('LyingBelly', 1.0);
                arp.goToPosture('LyingBack', 1.0);
                arp.goToPosture('Stand', 1.0);
                arp.goToPosture('Crouch', 1.0);
                arp.goToPosture('Sit', 1.0);
            });
            */
