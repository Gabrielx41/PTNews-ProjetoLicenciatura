var inicio;
var fim;
var paginaAtual = 1;
var totalPaginas = 1;
var totalNoticias = 13;
var selectedOption;
var searchText;
var jornalMessage;

function infoJornais(jornal){
    if (jornal.length === 0) {
        return '';
    } else if (jornal.length === 1) {
        return ` no jornal <strong>${obterNome(jornal[0])}</strong>`;
    } else {
        return ` nos jornais ${jornal.map(j => `<strong>${obterNome(j)}</strong>`).join(', ')}`;
    }
}

function formatarNoticia(data) {
    if ((selectedOption == "percentagem")){
        document.getElementById('container-graficos').style.display = 'flex';
        // document.getElementsByClassName('container-resultados')[0].style.display = 'none';
        var numResultadosSpan = document.getElementById('pesquisa-resultados');
           
      
        document.getElementsByClassName('ordenar-div')[0].style.display = 'none';

        data = data[0];
        var intervalId = setInterval(function() {
            if (totalNoticias !== 13) {
                clearInterval(intervalId);
                var percentagem_num_noticias = data["num_noticias"]
                var resultado = 0;
                console.log(percentagem_num_noticias)
                for (var [chave, valor] of Object.entries(percentagem_num_noticias)) {
                    if (valor === null || valor === undefined || totalNoticias[chave] === 0){
                        valor = 0;
                        percentagem_num_noticias[chave] = 0;
                    }else{
                        percentagem_num_noticias[chave] = (valor/totalNoticias[chave]) * 100
                        resultado += valor;
                    }
                }
                $('#container-graficos').empty();
                if (Object.entries(data["num_noticias"]).length > 0){
                    criarGrafico(percentagem_num_noticias, "Percentagem dedicada por cada jornal para " + searchText);
                }

                if (Object.entries(data["num_sentiment"]).length > 0){
                    criarGraficoPie(data["num_sentiment"], "Análise de sentimentos das notícias para " + searchText);
                    const valores = Object.values(data["num_sentiment"]);
                    resultado = valores.reduce((acumulador, valorAtual) => acumulador + valorAtual, 0);
                }

                numResultadosSpan.innerHTML = 'Foram encontrados <strong> ' + resultado + '</strong> resultados para "<strong>' + searchText + '</strong>".<br><br>Entre <span class="dataSpan"> ' + fim + '</span> e <span class="dataSpan">' + inicio + '</span>.';
                document.getElementsByClassName('container-resultados-info')[0].style.visibility = 'visible';
                document.getElementsByClassName('search-container')[0].style.visibility = 'visible';
                document.getElementById('bottom-section').style.visibility = 'visible';
                document.getElementById('loading2').style.display = 'none';
                $("html, body").animate({ scrollTop: $("#container-graficos").offset().top }, 1000);
            }
        }, 100);
    }
    else if (selectedOption == "imagem"){
        document.getElementById('imagens-container').style.display = 'flex';
        $('#imagens-container').empty();

        data.forEach(function(noticia) {

            var source = obterNome(noticia.source)

            var idNoticia = encodeURIComponent(noticia.id);

            $('#imagens-container').append(`
                <div class="noticia-img">
                    <a href="/noticia/${idNoticia}" style="text-decoration: none; color: inherit">
                        <div class="img-container-pesquisa">
                            ${noticia.images && noticia.images[0] ? `<img src="${noticia.images[0].url}" alt="Imagem da Notícia" class="imagem-pesquisa">` :  `<img src="../static/images/sources/${noticia.source}.png" alt="Imagem da Notícia" class="imagem-noticia">`}
                        </div>
                    </a>
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
        document.getElementsByClassName('search-container')[0].style.visibility = 'visible';
        document.getElementById('bottom-section').style.visibility = 'visible';
        document.getElementById('loading2').style.display = 'none';
        $("html, body").animate({ scrollTop: $("#bottom-section").offset().top }, 1000);
    }
    else if (selectedOption == "grafo"){
        document.getElementsByClassName('container-resultados')[0].style.display = 'none';
        criarGrafoD3(data[0][10], searchText, data);

        document.getElementById('bottom-section').style.visibility = 'visible';
        document.getElementById('container-grafo').style.display = 'flex';
        document.getElementById('opt-grafo').style.display = 'block';
        document.getElementById('slider-container').style.display = 'block';
        document.getElementsByClassName('search-container')[0].style.visibility = 'visible';
        document.getElementById('loading2').style.display = 'none';
        $("html, body").animate({ scrollTop: $("#bottom-section").offset().top }, 1000);
    }else{
        document.getElementById('noticias-container').style.display = 'flex';
        $('#noticias-container').empty();

        data.forEach(function(noticia) {
            var source = obterNome(noticia.source)

            var idNoticia = encodeURIComponent(noticia.id);
            idNoticia = idNoticia.replace(/%/g, '&g&');

            $('#noticias-container').append(`
                <div class="noticia">
                    <div class="container-img">
                        ${noticia.images && noticia.images[0] ? `<img src="${noticia.images[0].url}" alt="Imagem da Notícia" class="imagem-noticia">` : `<img src="../static/images/sources/${noticia.source}.png" alt="Imagem da Notícia" class="imagem-noticia">` }
                    </div>
                    <div class="div-titulo">
                        <h1 class="titulo"><a href="/noticia/${idNoticia}" style="text-decoration: none; color: inherit">${noticia.title || ""}</a></h1>
                    </div>
                    <div class="div-lead">
                        <p class="lead">${truncateText(noticia.lead || "", 180)}</p>
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

        document.getElementsByClassName('search-container')[0].style.visibility = 'visible';
        document.getElementById('bottom-section').style.visibility = 'visible';
        document.getElementById('loading2').style.display = 'none';
        $("html, body").animate({ scrollTop: $("#bottom-section").offset().top }, 1000);
    }
}


$(document).ready(function() {
    var selectedOptDiv = document.getElementById('selectedOpt');
    selectedOption = selectedOptDiv.getAttribute('data-selectedOption');

    $.ajax({
        url: '/api/pesquisa/num_noticias/' + selectedOption,
        type: 'GET',
        success: function(num_noticias) {
                totalNoticias = num_noticias;

                if(selectedOption != "percentagem"){
                    var numResultadosSpan = document.getElementById('pesquisa-resultados');
                    var intervalId = setInterval(function() {
                        if (fim !== undefined && inicio !== undefined) {
                            clearInterval(intervalId);
                            if (selectedOption === "autor"){
                                numResultadosSpan.innerHTML = 'Foram encontrados <strong> ' + totalNoticias + '</strong> resultados da autoria "<strong>' + searchText + '</strong>"'+ jornalMessage +'.<br><br>Entre <span class="dataSpan"> ' + fim + '</span> e <span class="dataSpan">' + inicio + '</span>.';
                            }else{
                                numResultadosSpan.innerHTML = 'Foram encontrados <strong> ' + totalNoticias + '</strong> resultados para "<strong>' + searchText + '</strong>"'+ jornalMessage +'.<br><br>Entre <span class="dataSpan"> ' + fim + '</span> e <span class="dataSpan">' + inicio + '</span>.';
                            }
                            document.getElementsByClassName('container-resultados-info')[0].style.visibility = 'visible';
                            totalPaginas = Math.ceil(totalNoticias / 12);
                            atualizarPaginacao();
                            if(totalPaginas > 1){
                                document.getElementById('pagination').style.display = 'block';
                            }
                        }
                    }, 100);

                    atualizarPaginacao();
                }
            }
    });

    atualizarNoticias()

    $('#ordem').on('change', function() {
        atualizarNoticias();
    });
});

function getOption(selectedOption){
    switch(selectedOption){
        case 'texto':
            return 'Texto';
        case 'autor':
            return 'Autor';
        case 'imagem':
            return 'Imagem';
        case 'grafo':
            return 'Grafo';
        case 'percentagem':
            return 'Percentagem';
    }
}

function atualizarNoticias() {
    document.querySelector(`input[name="userType"][value="${selectedOption}"]`).checked = true;
    var ordem = document.getElementById('ordem').value;

    $.ajax({
        url: '/api/pesquisa/' + selectedOption,
        type: 'GET',
        data: {
            ordem: ordem,
            paginaAtual: paginaAtual
        },
        success: function(response) {
            var data = response.data;
            searchText = response.searchText;
            var jornal = response.jornal;
            
            if (data != null && data.length > 0 && response.fim != undefined && response.inicio != undefined && response.fim != null && response.inicio != null) {
                inicio = timestamp_toDate(response.inicio);
                fim = timestamp_toDate(response.fim);

                jornalMessage = infoJornais(jornal);

                if(response.psqExata){
                    document.getElementById('checkbox').checked = true;
                }

                selecionarJornais(jornal);
                atualizarCalendario(fim, inicio);
                atualizarPaginacao();
            

                document.getElementById('search-bar').value = searchText;

                formatarNoticia(data);
            } else {
                document.getElementsByClassName('search-container')[0].style.display = 'none';
                document.getElementsByClassName('container-resultados')[0].style.display = 'none';
                document.getElementsByTagName('nav')[0].style.display = 'none';
                // document.getElementsByClassName('rodape')[0].style.display = 'none';
                document.getElementById("error").style.display = "flex";
                document.getElementById('loading2').style.display = 'none';
                document.body.style.background = "#a8caeb";
                if(response.fim != undefined && response.inicio != undefined && response.fim != null && response.inicio != null){
                    inicio = timestamp_toDate(response.inicio);
                    fim = timestamp_toDate(response.fim);
                    jornalMessage = infoJornais(jornal);

                    $('#error').html(`
                        <p class="error-message">Não foram encontradas notícias para a pesquisa [${getOption(selectedOption)}]: "<strong>${searchText}</strong>"${jornalMessage}.<br><br> Entre as datas <span class="dataSpan">${fim}</span> e <span class="dataSpan">${inicio}</span>.</p>
                        <a href="/">
                            <button class="error-button">Voltar a pesquisar</button>
                        </a>
                    `);
                }else{
                    const currentDate = new Date();
                    const formattedDate = currentDate.toLocaleString('pt-PT', { 
                        day: '2-digit', 
                        month: '2-digit', 
                        year: 'numeric', 
                        hour: '2-digit', 
                        minute: '2-digit' 
                    }).replace(',', '');
                    $('#error').html(`
                        <p class="error-message">Pesquisa Inválida. Escolha a data entre <strong>19/06/2024 00:25</strong> e <strong>${formattedDate}</strong></span>.</p>
                        <a href="/">
                            <button class="error-button">Voltar a pesquisar</button>
                        </a>
                    `);
                }
            }
        },
        error: function(error) {
            console.log(error);
            window.location.href = '/error';
        },
        complete: function() {
            setTimeout(atualizarNoticias, 900000); // 15 minutos para atualizar
        }
    });
}