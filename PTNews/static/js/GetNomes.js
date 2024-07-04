function obterNome(nome_jornal){
    switch (nome_jornal){
        case 'DNoticias':
            nome_jornal = 'Diário de Notícias';
            break;
        case 'JNegocios':
            nome_jornal = 'Jornal de Negócios';
            break;
        case 'IOnline':
            nome_jornal = 'Jornal i';
            break;
        case 'NAM':
            nome_jornal = 'Notícias ao Minuto';
            break;
        case 'Renascenca':
            nome_jornal = 'Renascença';
            break;
        case 'SicNoticias':
            nome_jornal = 'SIC Notícias';
            break;
        case 'Eco':
            nome_jornal = 'ECO';
            break;
    }
    return nome_jornal;
}