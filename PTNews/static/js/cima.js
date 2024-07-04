// Função que faz scroll suave até o topo da página
function topFunction() {
    if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

window.onscroll = function() {
    scrollFunction();
};

function scrollFunction() {
    if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
        document.getElementById("scrollTopBtn").style.display = "block";
    } else {
        document.getElementById("scrollTopBtn").style.display = "none";
    }
}
