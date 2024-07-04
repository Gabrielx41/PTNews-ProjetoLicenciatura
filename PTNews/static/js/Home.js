// Função para submeter o formulário
function submitForm() {
    var searchText = $("#search-bar").val();
    var selectedOption = $("input[name='userType']:checked").val();
    var jornal = getSelectedJornais();
    var checkbox = document.getElementById('checkbox').checked;
    var minDate = document.getElementById("datetimepickerMin").value;
    var maxDate = document.getElementById("datetimepickerMax").value;

    $.ajax({
        url: "/api/pesquisa",
        method: "POST",
        contentType: 'application/json',
        data: JSON.stringify({selectedOpt: selectedOption, searchText: searchText, minDate: minDate, maxDate: maxDate, jornal: jornal, psqExata: checkbox}),
        success: function() {
            window.location.href = "/pesquisa";
        },
        error: function(error) {
            console.error("Não foram encontradas noticias", error);
        }
    });
}

var searchBar;
document.addEventListener("DOMContentLoaded", function () {
    var showOptionsToggle = document.getElementById("show-options-toggle");
    var advancedOptions = document.getElementById("container-advanced-options");
    searchBar = document.getElementById("search-bar");
    
    criarOpcoes();

    showOptionsToggle.addEventListener("change", function () {
        if (this.checked) {
            document.getElementsByClassName("label-pesquisa-avancada")[0].innerHTML = "Fechar";
            advancedOptions.style.display = "block";
            $("html, body").animate({ scrollTop: $(".search-container").offset().top }, 1000);
        } else {
            document.getElementsByClassName("label-pesquisa-avancada")[0].innerHTML = "Pesquisa Avançada";
            advancedOptions.style.display = "none";
        }
    });

    searchBar.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            if (!searchBar.value) {
                    searchBar.value = "Portugal";
            }
            submitForm();
        }
    });

    $(".search-icon").on("click", function () {
        if (!searchBar.value) {
                searchBar.value = "Portugal";
        }
        submitForm();
    });

    $('.but-radio input:radio').on('click', function() {
        if (!searchBar.value) {
                searchBar.value = "Portugal";
        }
        submitForm();
    });
});