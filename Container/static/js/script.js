

/*// Select the video element
var elem = document.getElementById("myVideo");
var pantalla = document.documentElement;

// Function to toggle full screen
function toggleFullScreen() {
   
   if (!pantalla.fullscreenElement) {
        pantalla.webkitRequestFullscreen();
        elem.requestFullscreen();
        
    } else {
        
        document.exitFullscreen();
        
    }
}

function full_screen){
    pantalla.webkitRequestFullscreen();
    pantalla.requestFullscreen();
}

// Add an event listener to a button click
var button = document.getElementById("fullscreen-button");
button.addEventListener("click", full_Screen);

// Reproduce the video indefinitely
elem.loop = true;
elem.play();

/////////////////////////////////////////////////
/*
document.addEventListener("DOMContentLoaded", function() {
    var video = document.getElementById("myVideo");
    if (video) {
      video.loop = true;
      video.play();
    }
  
    var elem = document.documentElement;
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) {
        console.log("hola");
      elem.webkitRequestFullscreen(); // Safari y Chrome
    } else if (elem.msRequestFullscreen) {
      elem.msRequestFullscreen(); // IE11
    }   
  });

  document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen(); // Safari y Chrome
      } else if (document.msExitFullscreen) {
        document.msExitFullscreen(); // IE11
      }
    }
  });
////////////////////////////////

  // Select the video element
var elem = document.getElementById("myVideo");
var window = document.documentElement;

// Function to toggle full screen
function toggleFullScreen() {
  if (!window.fullscreenElement) {
    window.webkitRequestFullscreen();
    elem.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
}

// Add an event listener to the page load
document.addEventListener("DOMContentLoaded", function() {
  toggleFullScreen();
  elem.loop = true;
  elem.play();
});

// Add an event listener to the Escape key press
document.addEventListener("keydown", function(event) {
  if (event.key === "Escape") {
    toggleFullScreen();
  }
});
*/

// Function to toggle full screen
/*
function toggleFullScreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
    } /*else {
      document.exitFullscreen();
    }
  }
  
  // Add an event listener to a button click
  var button = document.getElementById("fullscreen-button");
  button.addEventListener("click", toggleFullScreen);
  
  // Add an event listener to the Escape key press
  document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
      toggleFullScreen();
    }
  });
  */