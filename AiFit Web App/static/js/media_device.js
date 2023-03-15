window.onload = function(){
  if(flag == 'realtimedetection' && timer != null){
    let timer_val = parseInt(timer, 10)*60
    function counter() {
        const minutes = Math.floor(timer_val / 60);
        const seconds = timer_val - minutes * 60;
        document.getElementById("minute").innerHTML = minutes;
        document.getElementById("seconds").innerHTML = seconds;
        timer_val--;
        if(timer_val == 0){
          window.location =  "http://127.0.0.1:8000/analysis?key="+key+"&timer="+timer+"&select_category=0"
        }      
        setTimeout(counter, 1000) 
    }
    counter();
   
 }
}

let inputBtn1 = document.getElementById("increment_btn1");
let inputBtn2 = document.getElementById("increment_btn2");
let value = document.getElementById("increment_value");
let value_in = parseInt(value.value, 10);
let check_form_loader = document.getElementById("check_form_loader")
let a_link = document.getElementById("rtd_btn").href;
document.getElementById("rtd_btn").href = a_link+'&timer='+value_in;
inputBtn1.addEventListener("click",()=>{
  if(value_in>1){
    value_in = value_in - 1
    value.setAttribute("value", String(value_in)+" min");
    inputBtn2.disabled = false
  }else{
    inputBtn1.disabled = true
  }
  document.getElementById("rtd_btn").href = a_link+'&timer='+value_in;
})
inputBtn2.addEventListener("click",()=>{
  if(value_in<10){
    value_in = value_in + 1
    value.setAttribute("value", String(value_in)+" min");
    inputBtn1.disabled = false
  }else{
    inputBtn2.disabled = true
  }
  document.getElementById("rtd_btn").href = a_link+'&timer='+value_in;
})




// let timmer;
// let start = document.getElementById("btnStart");
// let video = document.querySelector("video");

// let vid_i = document.getElementById("video_sc");
// let vid_o = document.getElementById("video_op_sc");
// let constraintObj = {
//   audio: false,
//   video: {
//     facingMode: "user",
//     width: 1280,
//     height: 720,
//     frameRate: 20,
//   },
// };
// let blob;
// // width: 1280, height: 720  -- preference only
// // facingMode: {exact: "user"}
// // facingMode: "environment"

// //handle older browsers that might implement getUserMedia in some way
// if (navigator.mediaDevices === undefined) {
//   navigator.mediaDevices = {};
//   navigator.mediaDevices.getUserMedia = function (constraintObj) {
//     let getUserMedia =
//       navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
//     if (!getUserMedia) {
//       return Promise.reject(
//         new Error("getUserMedia is not implemented in this browser")
//       );
//     }
//     return new Promise(function (resolve, reject) {
//       getUserMedia.call(navigator, constraintObj, resolve, reject);
//     });
//   };
// } else {
//   navigator.mediaDevices
//     .enumerateDevices()
//     .then((devices) => {
//       devices.forEach((device) => {
//         console.log(device.kind.toUpperCase(), device.label);
//         //, device.deviceId
//       });
//     })
//     .catch((err) => {
//       console.log(err.name, err.message);
//     });
// }

// navigator.mediaDevices
//   .getUserMedia(constraintObj)
//   .then(function (mediaStreamObj) {
//     //connect the media stream to the first video element
//     let video = document.querySelector("video");
//     if ("srcObject" in video) {
//       video.srcObject = mediaStreamObj;
//     } else {
//       //old version
//       video.src = window.URL.createObjectURL(mediaStreamObj);
//     }

//     video.onloadedmetadata = function (ev) {
//       //show in the video element what is being captured by the webcam
//       video.play();
//     };

//     //add listeners for saving video/audio
//     let mediaRecorder = new MediaRecorder(mediaStreamObj);
//     let chunks = [];

//     start.addEventListener("click", (ev) => {
//       mediaRecorder.start();
//       start.innerHTML = 'Recording Started ...';
//       start.disabled = true
//       console.log(mediaRecorder.state);
//       timmer = value_in*1000;
//       console.log(timmer)
//       setTimeout(() => {
//         mediaRecorder.stop();
//         start.innerHTML = 'Recording Stopped !!!';
//         console.log(mediaRecorder.state);
//       }, timmer + 1000);
//     });
//     mediaRecorder.ondataavailable = function (ev) {
//       chunks.push(ev.data);
//     };

//     mediaRecorder.onstop = (ev) => {
//       blob = new Blob(chunks, { type: "video/mp4" });
//       check_form_loader.style.display = "block";
//       console.log(mediaStreamObj.getVideoTracks()[0].getSettings().width)
//       console.log(mediaStreamObj.getVideoTracks()[0].getSettings().height)
//       console.log(mediaStreamObj.getVideoTracks()[0].getSettings().frameRate)
//       console.log(blob)
//       getData(blob, id, csrfToken, mediaStreamObj);
//       chunks = [];

//       // vidSave.href = videoURL;
//     };
//   })
//   .catch(function (err) {
//     console.log(err.name, err.message);
//   });

// function getData(blob, id, csrfToken, media_obj) {
//   url = "http://127.0.0.1:8000/check_form/" + id + "/";
//   fetch(url, {
//     method: "post",
//     body: blob,
//     headers: new Headers({
//       Accept: "application/json",
//       "Content-Type": "application/json",
//       "X-CSRFToken": csrfToken,
//     }),
//   })
//     .then((response) => {
//       console.log(response)
//       response.json().then((data) => {
//         console.log(data["category"]);
//         media_obj.getTracks().forEach(function(track) {
//           if (track.readyState == 'live' && track.kind === 'video') {
//               track.stop();
//           }
//         });
      
//       window.location = 'http://127.0.0.1:8000/check_form/'+data["category"]+'?flag=True&key='+data["key"];
//       });

//     })
//     .catch((error) => {
//       console.log(error);
//     });
// }


// function getSearchParameters() {
//   var prmstr = window.location.search.substr(1);
//   return prmstr != null && prmstr != "" ? transformToAssocArray(prmstr) : {};
// }

// function transformToAssocArray( prmstr ) {
//   var params = {};
//   var prmarr = prmstr.split("&");
//   for ( var i = 0; i < prmarr.length; i++) {
//       var tmparr = prmarr[i].split("=");
//       params[tmparr[0]] = tmparr[1];
//   }
//   return params;
// }
// var params = getSearchParameters();
// console.log(params)