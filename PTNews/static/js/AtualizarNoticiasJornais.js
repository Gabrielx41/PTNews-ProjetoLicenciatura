function atualizarNoticias() {
    var jornalElement = document.getElementById("jornal");
    var nome_jornal = jornalElement.dataset.nomeJornal;
    

    $.ajax({
        url: '/api/'+ nome_jornal + '/ultimas',
        type: 'GET',
        success: function(data) {
            var len_data = data.length;
            if (len_data > 0) {
                totalPaginas = Math.ceil(len_data / 12);
                var paginaAtualData = data.slice((paginaAtual - 1) * 12, paginaAtual * 12);
                
                formatarNoticia(paginaAtualData);
                atualizarPaginacao(totalPaginas);
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