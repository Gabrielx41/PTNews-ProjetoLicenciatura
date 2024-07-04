function atualizarNoticias() {
    var selectedOptDiv = document.getElementById('selectedOpt');
    var selectedOption = selectedOptDiv.getAttribute('data-selectedOption');
    optSelected = selectedOption;

    $.ajax({
        url: '/api/pesquisa/' + selectedOption,
        type: 'GET',
        success: function(data) {
            var len_data = data.length;
            if (len_data > 0) {
                document.getElementById("error").style.display = "none";
                totalPaginas = Math.ceil(len_data / 12);
                var paginaAtualData = data.slice((paginaAtual - 1) * 12, paginaAtual * 12);
                
                formatarNoticia(paginaAtualData);
                atualizarPaginacao(totalPaginas);
            } else {
                var pagination = document.getElementById('pagination');
                pagination.style.display = 'none';
                var pesquisa = document.getElementsByClassName('search-container');
                pesquisa[0].style.display = 'none';
                var img_container = document.getElementById('imagens-container');
                img_container.style.display = 'none';
                var container = document.getElementById('noticias-container');
                container.style.display = 'none';
                $('#error').html(`
                    <p class="error-message-psq">Não foram encontradas notícias para a sua pesquisa!</p>
                    <a href="/">
                        <button class="error-button">Página Inicial</button>
                    </a>
                `);
            }
        },
        error: function(error) {
            console.log(error);
            window.location.href = '/error';
        },
        complete: function() {
            setTimeout(atualizarNoticias, 300000); // 5 minutos para atualizar
        }
    });
}