function atualizarCalendario(dateMin, dateMax){
    flatpickr('#datetimepickerMax', {
        enableTime: true,
        dateFormat: 'd/m/Y H:i',
        locale: {
            firstDayOfWeek: 0,
            weekdays: {
                shorthand: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
                longhand: ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'],
            },
            months: {
                shorthand: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                longhand: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            },
        },
        time_24hr: true,
        defaultDate: dateMax,
        maxDate: new Date(),
        minDate: "18/06/2024 11:11" //É preciso alterar a função pesquisa da FuncPesquisa.js
    });

    flatpickr('#datetimepickerMin', {
        enableTime: true,
        dateFormat: 'd/m/Y H:i',
        locale: {
            firstDayOfWeek: 0,
            weekdays: {
                shorthand: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
                longhand: ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'],
            },
            months: {
                shorthand: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                longhand: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            },
        },
        time_24hr: true,
        defaultDate: dateMin,
        maxDate: new Date(),
        minDate: "18/06/2024 11:11"
    });
}

document.addEventListener('DOMContentLoaded', function() {
    atualizarCalendario("18/06/2024 11:11", new Date());
});