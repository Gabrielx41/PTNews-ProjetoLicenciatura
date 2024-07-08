var graficos = [
    'Número de notícias publicadas',
    'Principais pessoas citadas',
    'Organizações com maior destaque',
    'Autores com mais publicações',
    'wordcloud',
    'Análise de sentimentos',
];

function obterDados() {
    $.ajax({
        url: '/api/estatisticas',
        type: 'GET',
        success: function(data) {
            for (var i = 0; i < graficos.length; i++) {
                var tipo = graficos[i];
                dados = data[tipo];
                if (tipo == 'wordcloud') {
                    $('#container-graficos').append(
                        `
                        <div class="div-grafico">
                            <a href="#" onclick="toggleFullScreen('div-grafico', this.children[0], 'image')">
                                <img src="../static/images/fullscreen.png" alt="Full Screen" class="but-fullscreen">
                            </a>
                            <a href="#" onclick="downloadImage('${tipo}')">
                                <img src="../static/images/download.png" alt="Download" class="but-download">
                            </a>
                            <img src="../static/images/wordcloud.png" alt="Wordcloud" class="wordcloud">
                        </div>`
                    );
                } else if (tipo == 'Autores com mais publicações') {
                    criarGraficoPie(dados, tipo);
                } else if (tipo == 'Análise de sentimentos') {
                    criarGrafico(dados, tipo);
                }else{
                    criarGraficoLinhas(dados, tipo);
                }
            }
            document.getElementById('loading2').style.display = 'none';

        },
        error: function() {
            console.log('Erro ao obter as notícias');
            window.location.href = '/error';
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    obterDados(graficos);
});