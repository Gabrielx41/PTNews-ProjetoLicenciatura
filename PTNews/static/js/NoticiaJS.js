function baixarImage(url) {
    $.ajax({
        url: '/download_image',
        type: 'GET',
        data: { url: url },
        success: function(response) {
            if (response) {
                downloadImage(response);
            } else {
                openImage(response);
                console.log('Erro ao baixar a imagem');
            }
        },
        error: function() {
            openImage(response);
        },
    });
}

function keyword_highlight(content, keywordText) {
    content = content.innerHTML;
    
    content = content.replace(/<b class="keywordContent">/g, '');
    content = content.replace(/<b class="keywordContent" style="color:#7fa2c4;text-decoration-color:black;">/g, '');
    content = content.replace(/<\/b>/g, '');
    content = content.replaceAll(keywordText, '<b class="keywordContent" style="color:#7fa2c4;text-decoration-color:black;">'+keywordText+'</b>');

    document.getElementById("content").innerHTML = content;
    
    applyToggleContentEvent();
}

function applyToggleContentEvent() {
    $('#toggle-content').off('click').on('click', function() {
        var moreText = $('#more-content');
        var buttonText = $(this);

        moreText.slideToggle(1);
        if (buttonText.text() == 'Ler mais') {
            buttonText.text('Mostrar menos');
            document.getElementById('reticencias').style.display = 'none';
        } else {
            buttonText.text('Ler mais');
            document.getElementById('reticencias').style.display = 'inline';
        }
    });
}

var keywordAnterior;
document.addEventListener("DOMContentLoaded", function () {
    var mapaContainer = document.getElementById("mapa");

    document.getElementsByClassName("source")[0].innerHTML = obterNome(document.getElementsByClassName("source")[0].innerHTML);

    if (mapaContainer) {
        mapaContainer.innerHTML = `
            <iframe id="mapFrame" src="/mapa" frameborder="0">
            </iframe>
            <div id="spinner"></div>
        `;

        var mapFrame = document.getElementById("mapFrame");
        var spinner = document.getElementById("spinner");

        var image = document.querySelector('.imagem-noticia');
        try {
            image.addEventListener('dblclick', function() {
                baixarImage(image.src);
            });
        } catch (error) {
            console.log('Erro ao adicionar o evento de clique duplo na imagem');
        }

        mapFrame.onload = function() {
            spinner.style.display = "none";
            mapaContainer.style.display = "block";
        };
    }

    var content = document.getElementById("content");

    var keywords = document.getElementById("keywords").getElementsByTagName("span");

    for (var i = 0; i < keywords.length; i++) {
        keywords[i].addEventListener("click", function() {
            if (keywordAnterior) {
                keywordAnterior.style.color = "black";
            }
            this.style.color = "#7fa2c4";
            keywordText = this.textContent;
            keyword_highlight(content, keywordText);
            keywordAnterior = this;
        });
    }

    $('.keywordContent, .entities ul li span').on('click', function() {
        pesquisar("texto", $(this).text(), true);
    });

    $('.autor-nome').on('click', function() {
        pesquisar("autor", $(this).text(), true);
    });

    applyToggleContentEvent();
});
