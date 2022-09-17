feather.replace();

const controls = document.querySelector('.controls');
const cameraOptions = document.querySelector('.video-options>select');
const video = document.querySelector('video');
const canvas = document.querySelector('canvas');
const screenshotImage = document.querySelector('img');
const buttons = [...controls.querySelectorAll('button')];
let streamStarted = false;



const [play, pause, screenshot] = buttons;

const constraints = {
  video: {
    width: {
      min: 1280,
      ideal: 1920,
      max: 2560,
    },
    height: {
      min: 720,
      ideal: 1080,
      max: 1440
    },
  }
};

const getCameraSelection = async () => {
  const devices = await navigator.mediaDevices.enumerateDevices();
  const videoDevices = devices.filter(device => device.kind === 'videoinput');
  const options = videoDevices.map(videoDevice => {
    return `<option value="${videoDevice.deviceId}">${videoDevice.label}</option>`;
  });
  cameraOptions.innerHTML = options.join('');
};

play.onclick = () => {
  
  if (streamStarted) {
    video.play();
    play.classList.add('d-none');
    pause.classList.remove('d-none');
    return;
  }
  if ('mediaDevices' in navigator && navigator.mediaDevices.getUserMedia) {
    const updatedConstraints = {
      ...constraints,
      deviceId: {
        exact: cameraOptions.value
      }
    };
    startStream(updatedConstraints);
  }
};

const startStream = async (constraints) => {
  const stream = await navigator.mediaDevices.getUserMedia(constraints);
  handleStream(stream);
};

const handleStream = (stream) => {
  video.srcObject = stream;
  play.classList.add('d-none');
  pause.classList.remove('d-none');
  screenshot.classList.remove('d-none');
  streamStarted = true;
};

getCameraSelection();

cameraOptions.onchange = () => {
  const updatedConstraints = {
    ...constraints,
    deviceId: {
      exact: cameraOptions.value
    }
  };
  startStream(updatedConstraints);
};

const pauseStream = () => {
  video.pause();
  play.classList.remove('d-none');
  pause.classList.add('d-none');
};

const doScreenshot = () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  screenshotImage.src = canvas.toDataURL();
  sendImage(screenshotImage.src);
  screenshotImage.classList.remove('d-none');

};

const sendImage = async (image) => {
    
    const headline = document.getElementById("textToUser");
    const alertbox = document.getElementById("alertbox");
    const alerticon = document.getElementById("alerticon");
    const spinner = document.getElementById("spinner");
    headline.innerHTML = "<strong>Scanning</strong> for a familiar face...";
    alertbox.className = "alert alert-info d-flex align-items-center";
    alerticon.setAttribute("href","#info-fill");
    spinner.setAttribute("hidden","False");
    //>>>NOTE: on development mode use the localhost url (line 110), on server deployment use the server domain (line 111).
    // const url = "http://localhost:8000/fr-image/";
    const url = "https://cuinclass-app-xbilh.ondigitalocean.app/fr-image/";
    try {
      const response = await axios.post(url, image);
      console.log(response.data);
      // headline.innerHTML = response.data;
      if (response.data=="None"){
        headline.innerHTML = "<strong>Sorry, I couldn't recognize you.</strong> Try again or talk to the lecturer";
        alertbox.className = "alert alert-warning d-flex align-items-center";
        alerticon.setAttribute("href","#exclamation-triangle-fill");
      }
      else { 
        let responseText = response.data;
        const splitText = responseText.split("_");
        let finalText = splitText[0];
        headline.innerHTML = "Welcome to class <strong>"+finalText+"</strong>";
        alertbox.className = "alert alert-success d-flex align-items-center";
        alerticon.setAttribute("href","#check-circle-fill");
      }
    }catch (error) {
      console.error(error)
      headline.innerHTML = "<strong>There was a problem in the scanning process.</strong> Try again or talk to the lecturer"
      alertbox.className = "alert alert-danger d-flex align-items-center";
      alerticon.setAttribute("href","#exclamation-triangle-fill");
    }
    
};


pause.onclick = pauseStream;
screenshot.onclick = doScreenshot;