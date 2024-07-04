function formatarData(published) {
    var dataAtual = new Date();
    var dataPublicacao = new Date(published * 1000); // Multiplicar por 1000 para converter para milissegundos

    var diferencaMilissegundos = dataAtual - dataPublicacao;
    var diferencaMinutos = Math.floor(diferencaMilissegundos / (1000 * 60));
    var diferencaHoras = Math.floor(diferencaMilissegundos / (1000 * 60 * 60));
    
    if (diferencaHoras < 24) {
        if (diferencaMinutos < 60) {
            if (diferencaMinutos <= 1){
                return `Há 1 minuto`;
            } else {
                return `Há ${diferencaMinutos} minutos`;
            }
        } else {
            if (diferencaMinutos < 120){
                return `Há 1 hora`;
            } else {
                return `Há ${diferencaHoras} horas`;
            }
        }
    } else {
        var dia = dataPublicacao.getDate();
        var mes = dataPublicacao.getMonth() + 1; // O mês começa de 0
        var ano = dataPublicacao.getFullYear();

        // Adicionar zero à esquerda se o dia ou mês for menor que 10
        if (dia < 10) dia = '0' + dia;
        if (mes < 10) mes = '0' + mes;

        var dataFormatada = dia + "/" + mes + "/" + ano;
        return dataFormatada;
    }
}

function getCurrentDateTime() {
    var now = new Date();
    var year = now.getFullYear();
    var month = String(now.getMonth() + 1).padStart(2, '0'); // Mês começa de 0
    var day = String(now.getDate()).padStart(2, '0');
    var hours = String(now.getHours()).padStart(2, '0');
    var minutes = String(now.getMinutes()).padStart(2, '0');

    return `${year}-${month}-${day}T${hours}:${minutes}`;
}

function getYesterday() {
    var now = new Date();
    // Obter o dia atual
    var day = now.getDate();
    // Subtrair 1 do dia atual para obter o dia anterior
    var yesterday = new Date(now);
    yesterday.setDate(day - 1);
  
    var year = yesterday.getFullYear();
    var month = String(yesterday.getMonth() + 1).padStart(2, '0');
    var day = String(yesterday.getDate()).padStart(2, '0');
    var hours = String(yesterday.getHours()).padStart(2, '0');
    var minutes = String(yesterday.getMinutes()).padStart(2, '0');
  
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  }

function timestamp_toDate(data) {
    var dataPublicacao = new Date(data * 1000);
    var year = dataPublicacao.getFullYear();
    var month = String(dataPublicacao.getMonth() + 1).padStart(2, '0');
    var day = String(dataPublicacao.getDate()).padStart(2, '0');
    var hours = String(dataPublicacao.getHours()).padStart(2, '0');
    var minutes = String(dataPublicacao.getMinutes()).padStart(2, '0');
    return `${day}/${month}/${year} ${hours}:${minutes}`;
}