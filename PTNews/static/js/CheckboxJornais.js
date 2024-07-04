const options = [
    { value: "NAM", text: "Notícias ao Minuto" },
    { value: "DNoticias", text: "Diário de Notícias" },
    { value: "JNegocios", text: "Jornal de Negócios" },
    { value: "SicNoticias", text: "SIC Notícias" },
    { value: "Público", text: "Público" },
    { value: "Eco", text: "Eco" },
    { value: "Observador", text: "Observador" },
    { value: "Expresso", text: "Expresso" },
    { value: "IOnline", text: "Jornal i" },
    { value: "Renascenca", text: "Renascença" },
    { value: "Sapo24", text: "Sapo24" }
];

function criarOpcoes() {
    const checkboxContainer = document.getElementById('checkboxContainer');
    var columnCount = 3;
    // Create columns
    if (window.innerWidth < 560) {
      columnCount = 2;
    }

    const rowsPerColumn = Math.ceil(options.length / columnCount);
    for (let i = 0; i < columnCount; i++) {
      const column = document.createElement('div');
      column.className = 'column';
      checkboxContainer.appendChild(column);
    }

    // Add checkboxes to columns
    options.forEach((option, index) => {
      const checkboxId = `checkbox_${option.value}`;  // Unique ID for each checkbox

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.id = checkboxId;
      checkbox.name = 'jornal';
      checkbox.value = option.value;
      checkbox.className = 'checkbox';  // Apply the custom class

      const label = document.createElement('label');
      label.htmlFor = checkboxId;
      label.appendChild(document.createTextNode(option.text));

      const div = document.createElement('div');
      div.appendChild(checkbox);
      div.appendChild(label);

      const column = checkboxContainer.children[Math.floor(index / rowsPerColumn)];
      column.appendChild(div);
    });
}

function getSelectedJornais() {
    const selectedJornais = [];
    const checkboxes = document.querySelectorAll('.checkbox:checked');
    checkboxes.forEach(checkbox => {
      selectedJornais.push(checkbox.value);
    });
    return selectedJornais;
}

function selecionarJornais(jornaisSelecionados) {
  const checkboxes = document.querySelectorAll('.checkbox');
  checkboxes.forEach(checkbox => {
    if (jornaisSelecionados.includes(checkbox.value)) {
      checkbox.checked = true;
    }
  });
}