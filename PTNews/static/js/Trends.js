function formatarNoticia(topic, data, botao) {
    // Cria um novo contêiner para o tópico e suas notícias
    var topicContainer = $(`
        <div class="topic-container">
            <h2>"${topic}"</h2>
            <div id="noticias-container" style="display:flex; flex-wrap: wrap; justify-content: ${data.length === 2 ? 'space-evenly' : 'space-bettwen'};"></div>
            <button onclick="pesquisar('texto', '${topic}', true)" class="butVerMais">Ver mais</button>
        </div>
    `);
    if(!botao){
        topicContainer.find('button').css('display', 'none');
    }

    $('#container-topicos').append(topicContainer);

    // Referência ao contêiner de notícias dentro do contêiner do tópico
    var noticiasContainer = topicContainer.find('#noticias-container');

    data.forEach(function(noticia) {
        var source = obterNome(noticia.source);

        var idNoticia = encodeURIComponent(noticia.id);
        idNoticia = idNoticia.replace(/%/g, '&g&');

        noticiasContainer.append(`
            <div class="noticia">
                <div class="container-img">
                    ${noticia.images && noticia.images[0] ? `<img src="${noticia.images[0].url}" alt="Imagem da Notícia" class="imagem-noticia">` : `<img src="../static/images/sources/${noticia.source}.png" alt="Imagem da Notícia" class="imagem-noticia">`}
                </div>
                <div class="div-titulo">
                    <h1 class="titulo"><a href="/noticia/${idNoticia}" style="text-decoration: none; color: inherit">${noticia.title || ""}</a></h1>
                </div>
                <div class="div-lead">
                    <p class="lead">${noticia.lead || ""}</p>
                </div>
                <div class="div-source-published">
                    <div class="source-info">
                        <img src="../static/images/sources/${noticia.source}.png" alt="Logo do jornal" class="img-logo-source">
                        <p class="source">${source || ""}</p>
                    </div>
                    <p class="published">${formatarData(noticia.published) || ""}</p>
                </div>
            </div>
        `);
    });
}


$(document).ready(function() {
    $.ajax({
        url: "/top_topics",
        method: "GET",
        success: function(response) {
            var top_topics = response.top_topics;
            var num_noticias = response.num_noticias;
            if(top_topics.length > 0){
                for (var topicos of top_topics) {
                    for (const [topic, noticias] of Object.entries(topicos)) {
                        if ($(window).width() < 1100) {
                            if (num_noticias[topic] > 4){
                                formatarNoticia(topic, noticias, true);
                            }else{
                                formatarNoticia(topic, noticias, false);
                            }
                        }else{
                            if (num_noticias[topic] > 3){
                                formatarNoticia(topic, noticias.slice(0, -1), true);
                            }else{
                                formatarNoticia(topic, noticias, false);
                            }
                        }
                    }
                }
                document.getElementsByClassName('title')[0].style.display = 'block';
            }else{
                document.getElementById('container-topicos').style.display = 'none';
                document.getElementsByTagName('nav')[0].style.display = 'none';
                // document.getElementsByClassName('rodape')[0].style.display = 'none';
                document.getElementById("error").style.display = "flex";
                document.body.style.background = "#a8caeb";
                
                $('#error').html(`
                    <p class="error-message">Não foram encontradas notícias para os tópicos mais pesquisados das últimas 24 horas.</p>
                    <a href="/">
                        <button class="error-button">Voltar á página inicial</button>
                    </a>
                `);
            }
            document.getElementById('loading2').style.display = 'none';
        },
        error: function(error) {
            document.getElementById('container-topicos').style.display = 'none';
            document.getElementById("error").style.display = "flex";
            $('#error').html(`
                <p class="error-message">Não foram encontrados Tópicos.</p>
                <a href="/">
                    <button class="error-button">Voltar á página inicial</button>
                </a>
            `);
        }
    });
});