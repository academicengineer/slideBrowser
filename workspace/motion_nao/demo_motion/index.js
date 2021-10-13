let _motion;

var session = new QiSession("192.168.1.31:80");
    session.socket().on('connect', function () {
        console.log('QiSession connected!');
        // now you can start using your QiSession
    }).on('disconnect', function () {
        console.log('QiSession disconnected!');
    });


    session.service("ALMotion").done((motion) => {
        _motion = motion;

    }).fail((error) => {
            console.log("An error occurred: " + error);
    });

    var signalLink;
    var serviceDirectory;

    function onServiceAdded(serviceId, serviceName)
    {
        console.log("New service", serviceId, serviceName);
        serviceDirectory.serviceAdded.disconnect(signalLink);
    }

    session.service("ServiceDirectory").done(function (sd) {
        serviceDirectory = sd;
        serviceDirectory.serviceAdded.connect(onServiceAdded).done(function (link) {
            signalLink = link;
        }).fail(function (error) {
            console.log("An error occurred: " + error);
        });
    });
    session.service("ALMemory").done(function (ALMemory) {
        ALMemory.subscriber("FrontTactilTouched").done(function (subscriber) {
            // subscriber.signal is a signal associated to "FrontTactilTouched"
            subscriber.signal.connect(function (state) {
                console.log(state == 1 ? "You just touched my head!" : "Bye bye!");
            });
        });
    });

    function neck_l(){
        _motion.setAngles(["HeadYaw", "HeadPitch"], [1.0, 0.0], 0.1)
    }

    function neck_r(){
        _motion.setAngles(["HeadYaw", "HeadPitch"], [-1.0, 0.0], 0.1)
    }

    function neck_up(){
        _motion.setAngles(["HeadYaw", "HeadPitch"], [0.0, -1.0], 0.1)
    }

    function neck_down(){
        _motion.setAngles(["HeadYaw", "HeadPitch"], [0.0, 1.0], 0.1)
    }

    function neck_default(){
        _motion.setAngles(["HeadYaw", "HeadPitch"], [0.0, 0.0], 0.1)
    }

    function l_shoulder_pitch(){
        _motion.setAngles(["LShoulderPitch", "LShoulderRoll"], [-1.0, 0.0], 0.1)
    }

    function l_shoulder_roll(){
        _motion.setAngles(["LShoulderPitch", "LShoulderRoll"], [1.0, 1.0], 0.1)
    }

    function r_shoulder_pitch(){
        _motion.setAngles(["RShoulderPitch", "RShoulderRoll"], [-1.0, 0.0], 0.1)
    }

    function r_shoulder_roll(){
        _motion.setAngles(["RShoulderPitch", "RShoulderRoll"], [1.0, -1.0], 0.1)
    }

    function l_elbow_roll(){
        _motion.setAngles(["LElbowRoll", "LElbowYaw"], [-1.0, -1.0], 0.1)
    }

    function l_elbow_yaw(){
        _motion.setAngles(["LElbowRoll", "LElbowYaw"], [0.0, 1.0], 0.1)
    }
    
    function r_elbow_roll(){
        _motion.setAngles(["RElbowRoll", "RElbowYaw"], [1.0, 1.0], 0.1)
    }

    function r_elbow_yaw(){
        _motion.setAngles(["RElbowRoll", "RElbowYaw"], [0.0, -1.0], 0.1)
    }

    function l_wrist_yaw(){
        _motion.setAngles("LWristYaw", 1.0, 0.1)
    }

    function r_wrist_yaw(){
        _motion.setAngles("RWristYaw", -1.0, 0.1)
    }

    function l_oepnhand(){
        _motion.openHand("LHand");
    }

    function l_closehand(){
        _motion.closeHand("LHand");
    }

    function r_oepnhand(){
        _motion.openHand("RHand");
    }

    function r_closehand(){
        _motion.closeHand("RHand");
    }

    function clickBtn_neck_l(){
        neck_l();
    }

    function clickBtn_neck_r(){
        neck_r();
    }

    function clickBtn_neck_up(){
        neck_up();
    }

    function clickBtn_neck_down(){
        neck_down();
    }

    function clickBtn_neck_default(){
        neck_default();
    }
    
    function clickBtn_lsp(){   
        l_shoulder_pitch();
    }

    function clickBtn_lsr(){   
        l_shoulder_roll();
    }

    function clickBtn_rsp(){   
        r_shoulder_pitch();
    }

    function clickBtn_rsr(){   
        r_shoulder_roll();
    }

    function clickBtn_ler(){   
        l_elbow_roll();
    }

    function clickBtn_ley(){   
        l_elbow_yaw();
    }

    function clickBtn_rer(){   
        r_elbow_roll();
    }

    function clickBtn_rey(){   
        r_elbow_yaw();
    }

    function clickBtn_lwy(){   
        l_wrist_yaw();
    }

    function clickBtn_rwy(){   
        r_wrist_yaw();
    }

    function clickBtn_loh(){   
        l_oepnhand();
    }

    function clickBtn_lch(){   
        l_closehand();
    }

    function clickBtn_roh(){   
        r_oepnhand();
    }

    function clickBtn_rch(){   
        r_closehand();
    }