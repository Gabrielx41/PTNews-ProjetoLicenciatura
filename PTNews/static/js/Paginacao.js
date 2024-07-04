function atualizarPaginacao() {
    var paginas = [];
    var numPaginasVisiveis = window.innerWidth < 600 ? 3 : 5;
    var inicio = Math.max(1, paginaAtual - Math.floor(numPaginasVisiveis / 2));
    var fim = Math.min(totalPaginas, inicio + numPaginasVisiveis - 1);

    if (fim - inicio + 1 < numPaginasVisiveis) {
        inicio = Math.max(1, fim - numPaginasVisiveis + 1);
    }

    for (var i = inicio; i <= fim; i++) {
        paginas.push(i);
    }

    // Atualizar os links da paginação
    $('#um').text(paginas[0] || '');
    $('#dois').text(paginas[1] || '');
    $('#tres').text(paginas[2] || '');
    $('#quatro').text(paginas[3] || '');
    $('#cinco').text(paginas[4] || '');
    $('#ultimo').text(totalPaginas);

    // Atualizar classes para a página atual
    $('#um').toggleClass('pagina-atual', paginaAtual === paginas[0]);
    $('#dois').toggleClass('pagina-atual', paginaAtual === paginas[1]);
    $('#tres').toggleClass('pagina-atual', paginaAtual === paginas[2]);
    $('#quatro').toggleClass('pagina-atual', paginaAtual === paginas[3]);
    $('#cinco').toggleClass('pagina-atual', paginaAtual === paginas[4]);

    // Atualizar a visibilidade do botão de avançar/recuar
    $('#recuar').toggleClass('escondido', paginaAtual === 1);
    $('#avancar').toggleClass('escondido', paginaAtual === totalPaginas);
    $('#tres').toggleClass('escondido', paginas.length < 3);
    $('#quatro').toggleClass('escondido', paginas.length < 4);
    $('#cinco').toggleClass('escondido', paginas.length < 5);
    $('#primeiro').toggleClass('escondido', totalPaginas <= numPaginasVisiveis || 1 >= paginaAtual - Math.floor(numPaginasVisiveis / 2));
    $('#ellipsis1').toggleClass('escondido', totalPaginas <= numPaginasVisiveis || 1 >= paginaAtual - Math.floor(numPaginasVisiveis / 2));
    $('#ultimo').toggleClass('escondido', totalPaginas <= numPaginasVisiveis || paginaAtual >= totalPaginas - Math.floor(numPaginasVisiveis / 2));
    $('#ellipsis2').toggleClass('escondido', totalPaginas <= numPaginasVisiveis || paginaAtual >= totalPaginas - Math.floor(numPaginasVisiveis / 2));

}

$(document).ready(function() {
    $('#recuar').click(function() {
        if (paginaAtual > 1) {
            paginaAtual--;
            atualizarNoticias();
        }
    });

    $('#avancar').click(function() {
        if (paginaAtual < totalPaginas) {
            paginaAtual++;
            atualizarNoticias();
        }
    });

    $('#um, #dois, #tres, #quatro, #cinco').click(function() {
        paginaAtual = parseInt($(this).text());
        atualizarNoticias();
    });

    $('#ultimo').click(function() {
        paginaAtual = totalPaginas;
        atualizarNoticias();
    });
    
    $('#primeiro').click(function() {
        paginaAtual = 1;
        atualizarNoticias();
    });

    atualizarPaginacao();
});
