$(document).ready(function() {
    function atualizarUtilizadores() {
        $.ajax({
            url: '/lista/utilizadores',
            type: 'GET',
            success: function(data) {
                $('.userList').empty();
                if (data.length === 1) {
                    $('.userList').append('<tr><td colspan="3">Nenhum utilizador registado</td></tr>');
                } else {
                    data.forEach(function(utilizador) {
                        if(utilizador.username != 'Admin')
                            var row = `
                                <tr>
                                    <td class="td-username">${utilizador.username}</td>
                                    <td>${utilizador.isAdmin ? 'Administrador' : 'Utilizador'}</td>
                                    <td><div class="removeIcon">&#10006;</div></td>
                                </tr>`;
                            $('.userList').append(row);
                    });
                }
            },
        });
    }
    

    atualizarUtilizadores();

    // Adicionar evento de clique ao botão de remoção
    $(document).on('click', '.removeIcon', function() {
        var username = $(this).closest('tr').find('.td-username').text();
        if(username != 'Admin'){
            
            $.ajax({
                url: '/remover/utilizador',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ username: username }),
                success: function(response) {
                    if (response.success) {
                        atualizarUtilizadores();
                        esconderErro('#error-message-remover');
                    } else {
                        console.log('Erro ao remover utilizador');
                        exibirErro('Erro ao remover utilizador.', '#error-message-remover');
                    }
                },
                error: function() {
                    console.log('Erro ao remover utilizador');
                    exibirErro('Erro ao remover utilizador.', '#error-message-remover');
                }
            });
        } else {
            console.log('Não é possível remover o utilizador admin.');
            exibirErro('Não é possível remover o utilizador admin.', '#error-message-remover');
        }
    });

    
    $(document).on('click', '.botao-adicionar', function(event) {
        event.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        var userType = $('input[name="userType"]:checked').val();
    
        if(username && password && userType){
            $.ajax({
                url: '/adicionar/utilizador',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ username: username, password: password, isAdmin: userType }),
                success: function(response) {
                    console.log(response);
                    if (response.success) {
                        $('#username').val('');
                        $('#password').val('');
                        atualizarUtilizadores();
                        esconderErro('#error-message');
                    } else {
                        $('#username').val('');
                        $('#password').val('');
                        exibirErro(response.error, '#error-message');
                    }
                },
                error: function() {
                    console.log('Erro ao adicionar utilizador');
                    $('#username').val('');
                    $('#password').val('');
                    exibirErro('Erro ao adicionar utilizador', '#error-message');
                }
            });
        } else {
            exibirErro('Por favor, preencha todos os campos.', '#error-message');
        }
    });
    
    function exibirErro(mensagem, id) {
        var errorMessage = $(id);
        errorMessage.text(mensagem);
        errorMessage.show();
    }
    
    function esconderErro(id) {
        var errorMessage = $(id);
        errorMessage.hide();
    }
    
});
