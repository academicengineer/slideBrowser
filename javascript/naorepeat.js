$(function(){
    var qis, ip, als = {};
    // ポーズボタンclickイベント
    $('#naorepeat-btn').on('click', function(){
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
                aas.say('もう一度，スライドの説明を繰り返します');
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
