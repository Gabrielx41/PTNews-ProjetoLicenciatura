function toggleFullScreen(id, img, tipo) {
    var elem;
    if (tipo === 'image') {
        elem = document.getElementsByClassName(id)[4];
    } else {
        elem = document.getElementById(id).parentNode;
    }

    if (!elem) {
        console.error('Elemento não encontrado:', id);
        return;
    }

    if (!document.fullscreenElement && !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement) {
        if (elem.requestFullscreen) {
            elem.requestFullscreen().then(() => {
                console.log('Entrou em fullscreen');
            }).catch(err => {
                console.error(`Erro ao entrar em fullscreen: ${err.message} (${err.name})`);
            });
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
            document.exitFullscreen().then(() => {
                console.log('Saiu do fullscreen');
            }).catch(err => {
                console.error(`Erro ao sair do fullscreen: ${err.message} (${err.name})`);
            });
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
