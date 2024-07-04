function formatarNoticia(data) {
    $('#noticias-container').empty();
    data.forEach(function(noticia) {

        var source = obterNome(noticia.source)

        var encodedId = encodeURIComponent(noticia.id);

        encodedId = encodedId.replace(/%/g, '&g&');

        $('#noticias-container').append(`
            <div class="noticia">
                <div class="container-img">
                    ${noticia.images && noticia.images[0] ? `<img src="${noticia.images[0].url}" alt="Imagem da Notícia" class="imagem-noticia">` : `<img src="../static/images/sources/${noticia.source}.png" alt="Imagem da Notícia" class="imagem-noticia">`}
                </div>
                <div class="div-titulo">
                    <h1 class="titulo"><a href="/noticia/${encodedId}" style="text-decoration: none; color: inherit">${noticia.title || ""}</a></h1>
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
    document.getElementsByClassName('container-ordem')[0].style.visibility = 'visible';
    document.getElementById('loading2').style.display = 'none';
    $('html, body').animate({scrollTop: 0}, 1000);
}

var paginaAtual = 1;
var totalPaginas = 1;
var totalNoticias = 13;
var nome_jornal;
var inicio;
var fim;
$(document).ready(function() {
    var jornalElement = document.getElementById("jornal");
    nome_jornal = jornalElement.dataset.nomeJornal;

    $.ajax({
        url: '/api/'+ nome_jornal + '/ultimas/num_noticias',
        type: 'GET',
        success: function(response) {
                totalNoticias = response.num_noticias;
                var numResultadosSpan = document.getElementById('num-resultados');
                if (nome_jornal != '24h') {
                    numResultadosSpan.innerHTML = 'Foram encontrados <strong> ' + totalNoticias + '</strong> resultados para o jornal <strong>' + obterNome(nome_jornal) + '</strong>.';
                }else{
                    numResultadosSpan.innerHTML = 'Foram encontrados <strong> ' + totalNoticias + '</strong> resultados nas <strong>últimas 24 horas</strong>.';
                }
                document.getElementsByClassName('container-resultados-info')[0].style.visibility = 'visible';
                totalPaginas = Math.ceil(totalNoticias / 12);
                var fim = timestamp_toDate(response.fim)
                var inicio = timestamp_toDate(response.inicio)
                document.getElementById('info-data').innerHTML = '<br><br>Entre <span class="dataSpan"> ' + fim + '</span> e <span class="dataSpan">' + inicio + '</span>.';
                
                atualizarPaginacao();
            }
    });

    atualizarNoticias()

    $('#ordem').on('change', function() {
        atualizarNoticias();
    });
});

function atualizarNoticias() {
    var ordem = document.getElementById('ordem').value;

    $.ajax({
        url: '/api/'+ nome_jornal + '/ultimas',
        type: 'GET',
        data: {
            ordem: ordem,
            paginaAtual: paginaAtual,
        },
        success: function(response) {
            data = response.dados;

            if (totalNoticias > 0) {
                totalPaginas = Math.ceil(totalNoticias / 12);

                formatarNoticia(data);
                atualizarPaginacao();
                if(totalPaginas > 1){
                    document.getElementById('pagination').style.display = 'block';
                }
            } else {
                console.log('Erro ao obter as notícias');
                window.location.href = '/error';
            }
        },
        error: function() {
            console.log('Erro ao obter as notícias');
            window.location.href = '/error';
        },
        complete: function() {
            setTimeout(atualizarNoticias, 300000); // 5 minutos para atualizar
        }
    });
}