function toggleFullScreen(id, img, tipo) {
    var elem;
    if (tipo == 'image') {
        elem = document.getElementsByClassName(id)[4];
    }else{
        elem = document.getElementById(id).parentNode;
    }

    if (!document.fullscreenElement) {
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.mozRequestFullScreen) { // Firefox
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) { // Chrome, Safari, Opera
            elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) { // IE/Edge
            elem.msRequestFullscreen();
        }
        img.src = "../static/images/exitfullscreen.png";
        img.style.width = "20px";
        img.style.height = "20px";
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) { // Firefox
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) { // Chrome, Safari, Opera
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { // IE/Edge
            document.msExitFullscreen();
        }
        img.src = "../static/images/fullscreen.png";
        img.style.width = "15px";
        img.style.height = "15px";
    }
}