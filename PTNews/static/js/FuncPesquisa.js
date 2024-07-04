function pesquisar(tipoPesquisa, searchText, psqExata){
    // Obter a data e hora atual
    var hoje = new Date();

    // Formatar a data e hora
    var dia = ("0" + hoje.getDate()).slice(-2);
    var mes = ("0" + (hoje.getMonth() + 1)).slice(-2);
    var ano = hoje.getFullYear();
    var horas = ("0" + hoje.getHours()).slice(-2);
    var minutos = ("0" + hoje.getMinutes()).slice(-2);
    
    var maxDate = dia + "/" + mes + "/" + ano + " " + horas + ":" + minutos;
    
    $.ajax({
        url: "/api/pesquisa",
        method: "POST",
        contentType: 'application/json',
        data: JSON.stringify({selectedOpt: tipoPesquisa, searchText: searchText, minDate: "18/06/2024 11:11", maxDate: maxDate, jornal: [], psqExata: psqExata}),
        success: function() {
            window.location.href = "/pesquisa";
        },
        error: function(error) {
            console.error("Não foram encontradas noticias", error);
        }
    });
}