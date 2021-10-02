const videoElement = document.getElementsByClassName('input_video')[0];
    const canvasElement = document.getElementsByClassName('output_canvas')[0];
    const canvasCtx = canvasElement.getContext('2d');
    
    var frame_count = 0;
    var csrf_token = '{{ csrf_token }}';
    var xhr = new XMLHttpRequest();
    
    let x;

    var handInfo = (function(){
        const handInfo = {
          isLeft: false,
          x: 0,
          y: 0,
          isVisible: false,
          setPosCallback: null,
          setHandInfo: (isLeft, x, y, isVisible) => {
            handInfo.isLeft = isLeft
            handInfo.x = x
            handInfo.y = y
            handInfo.isVisible = isVisible
          },
          sendPos: () => {
            if(handInfo.setPosCallback){
              handInfo.setPosCallback([handInfo.isLeft.toString(), handInfo.x.toString(), handInfo.y.toString()].join('/'))
            }
          }
        }

        return handInfo
    })();

    var controller
    const makeController = function(keyDownCallback, keyUpCallback){
      const input = {
        keys: [false, false, false, false],
        keyIndex: {q: 0, w: 1, e: 2, r: 3},
        isPressed: key => input.keys[key],
        keyDown: key => {
          if(!input.keys[key]){
            input.keys[key] = true;
            keyDownCallback(key);
            console.log("Controller : KeyDown " + key);
          }
        },
        keyUp: key => {
          if(input.keys[key]){
            input.keys[key] = false;
            keyUpCallback(key);
            console.log("Controller : KeyUp " + key);
          }
        },
        press: keyName => {
          console.log("Controller : Press " + keyName);
          let key = input.keyIndex[keyName];

          input.keys.map((v, i) => i === key ? input.keyDown(i) : input.keyUp(i));
        }
      };
      console.log("Controller : Init");

      return input;
    }

    function onResults(results) {
      if (results.multiHandedness) {
        // 왼손 & 오른손 2번
        let index = 0
        for (const handedness of results.multiHandedness) {
          const landmarks = results.multiHandLandmarks[index++]

          let x = 0, y = 0;
          for(const landmark of landmarks){
            x += landmark.x;
            y += landmark.y;           
          }
          x /= landmarks.length;
          y /= landmarks.length;

          // 반전
          x = 1 - x
          y = 1 - y

          const isLeft = handedness.label === "Left"
          handInfo.setHandInfo(isLeft, x, y, true)
          handInfo.sendPos()
        }
      }
    }
    
    const hands = new Hands({locateFile: (file) => {
      return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
    }});
    hands.setOptions({
      maxNumHands: 2,
      minDetectionConfidence: 0.8,
      minTrackingConfidence: 0.8
    });
    hands.onResults(onResults);
    
    const camera = new Camera(videoElement, {
      onFrame: async () => {
        await hands.send({image: videoElement});
      },
      width: 1280,
      height: 720
    });
    camera.start();

    // 자바스크립트
    var buildUrl = "{% static 'MG/Build' %}";
    var loaderUrl = buildUrl + "/testMotionGame.loader.js";
    var config = {
      dataUrl: buildUrl + "/testMotionGame.data",
      frameworkUrl: buildUrl + "/testMotionGame.framework.js",
      codeUrl: buildUrl + "/testMotionGame.wasm",
      streamingAssetsUrl: "StreamingAssets",
      companyName: "DefaultCompany",
      productName: "New Unity Project",
      productVersion: "0.10.0",
    };

    var container = document.querySelector("#unity-container");
    var canvas = document.querySelector("#unity-canvas");
    var loadingBar = document.querySelector("#unity-loading-bar");
    var progressBarFull = document.querySelector("#unity-progress-bar-full");
    var fullscreenButton = document.querySelector("#unity-fullscreen-button");
    var mobileWarning = document.querySelector("#unity-mobile-warning");



    var instance;

    if (/iPhone|iPad|iPod|Android/i.test(navigator.userAgent)) {
      container.className = "unity-mobile";
      config.devicePixelRatio = 1;
      mobileWarning.style.display = "block";
      setTimeout(() => {
        mobileWarning.style.display = "none";
      }, 5000);
    } else {
      canvas.style.width = "960px";
      canvas.style.height = "600px";
    }
    loadingBar.style.display = "block";

    var script = document.createElement("script");
    script.src = loaderUrl;
    script.onload = () => {
      createUnityInstance(canvas, config, (progress) => {
        progressBarFull.style.width = 100 * progress + "%";
      }).then((unityInstance) => {
        loadingBar.style.display = "none";
        fullscreenButton.onclick = () => {
          unityInstance.SetFullscreen(1);
          instance=unityInstance
        };
        controller = makeController(key => unityInstance.SendMessage("RhythmCore4Tracks", "KeyDown", key), key => unityInstance.SendMessage("RhythmCore4Tracks", "KeyUp", key));
        handInfo.setPosCallback = handInfo => unityInstance.SendMessage("InputManager", "SetPos", handInfo) 
      }).catch((message) => {
        alert(message);
      });
    };
    document.body.appendChild(script);
    


    
    //모션 동작 보내기


    let v;
    
    function onResults(results) {
      canvasCtx.save();
      canvasCtx.translate(canvasElement.width, 0);
      canvasCtx.scale(-1,1);
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      canvasCtx.drawImage(
          results.image, 0, 0, canvasElement.width, canvasElement.height);
      if (results.multiHandLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
        

          v = JSON.stringify({landmarks})
          

          drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS,
                         {color: '#00FF00', lineWidth: 5});
          drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 2});
        }
      }
      canvasCtx.restore();
    }
    let s=0;

    setInterval(function(){
      $.ajax({
            url: '../landmark_data/',
            type: 'POST',
            data: {'landmarks' : v },
            dataType : 'json',
            beforeSend: function(xhr) {
              xhr.setRequestHeader('X-CSRFToken', csrf_token);
            },
          success:function(res){
              console.log(res)
            if (res['location']=='None'){
              console.log('there is no landmarks');
            }
            else {
              x=NaN;
              console.log(res['location']);
              console.log(instance)

            }
          },
          error:function(){
            x=NaN
            console.log('error')
          }
      })
    }, 100) // n밀리초에 한 번씩 전송 // 해당 페이지가 아니더라도 0.1초에 한번씩 데이터 전송하는 것 같음 (Console에 자꾸 에러 찍힘)
    