






    const videoElement = document.getElementsByClassName('input_video')[0];
    const canvasElement = document.getElementsByClassName('output_canvas')[0];
    const canvasCtx = canvasElement.getContext('2d');

    var csrf_token = '{{ csrf_token }}';
    var xhr = new XMLHttpRequest();
    
    let x;
    
    function onResults(results) {
      canvasCtx.save();
      canvasCtx.translate(canvasElement.width, 0);
      canvasCtx.scale(-1,1);
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      canvasCtx.drawImage(
          results.image, 0, 0, canvasElement.width, canvasElement.height);
      if (results.multiHandLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
        

          x = JSON.stringify({landmarks})
          

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
            data: {'landmarks' : x },
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
    
    const hands = new Hands({locateFile: (file) => {
      return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
    }});
    hands.setOptions({
      maxNumHands: 2,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
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
