var graficosAtivos = {};
var colors = [
    'rgba(0, 0, 0, 0.8)',        // Preto
    'rgba(139, 69, 19, 0.6)',    // Castanho
    'rgba(255, 0, 0, 0.6)',      // Vermelho
    'rgba(0, 128, 0, 0.6)',      // Verde
    'rgba(0, 0, 255, 0.6)',      // Azul
    'rgba(255, 255, 0, 0.8)',    // Amarelo
    'rgba(128, 0, 128, 0.6)',    // Roxo
    'rgba(255, 165, 0, 0.6)',    // Laranja
    'rgba(255, 192, 203, 0.7)',  // Rosa
    'rgba(128, 128, 128, 0.6)',   // Cinza
    'rgba(127, 162, 196, 0.8)',  // Azul claro
    'rgba(0, 255, 255, 0.6)',    // Ciano
];

    // Função para criar o gráfico usando Chart.js
function criarGrafico(dados, tipo) {
    var labels = [];
    var data = [];

    if (tipo == 'Análise de sentimentos'){
        var datasets = [];
        var dataPositivo = [];
        var dataNegativo = [];
        var dataNeutro = [];

        for (const [chave, valor] of Object.entries(dados)) {
            labels.push(obterNome(chave));
            dataPositivo.push(valor.Positivo);
            dataNegativo.push(valor.Negativo);
            dataNeutro.push(valor.Neutro);
        }

        datasets = [
            {
                label: 'Positivo',
                data: dataPositivo,
                backgroundColor: 'green',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            },
            {
                label: 'Negativo',
                data: dataNegativo,
                backgroundColor: 'red',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            },
            {
                label: 'Neutro',
                data: dataNeutro,
                backgroundColor: 'yellow',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1
            }
        ]
    }else{
        for (const [chave, valor] of Object.entries(dados)) {
            labels.push(obterNome(chave));
            data.push(valor);
        }
    }

    if (graficosAtivos[tipo]) {
        graficosAtivos[tipo].destroy();
    }

    // Criar o gráfico de barras
    $('#container-graficos').append(
        `
        <div class="div-grafico">
            <a href="#" onclick="toggleFullScreen('${tipo}', this.children[0], 'grafico')">
                <img src="../static/images/fullscreen.png" alt="Full Screen" class="but-fullscreen">
            </a>
            <a href="#" onclick="downloadChart('${tipo}')">
            <img src="../static/images/download.png" alt="Download" class="but-download">
            </a>
          <canvas id="${tipo}"></canvas>
      </div>`
    )
    var ctx = document.getElementById(tipo).getContext('2d');
    graficosAtivos[tipo] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: tipo == "Análise de sentimentos" ? datasets : [{
                data: data,
                backgroundColor: 'rgba(127, 162, 196, 0.8)',
                borderColor: 'black',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        fontSize: 14
                    }
                },
                x: {
                    ticks: {
                        fontSize: 14,
                        autoSkip: false,
                        maxRotation: 45,
                        minRotation: 0
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label;
                            if (tipo == "Análise de sentimentos") {
                                label = context.dataset.label + ': ' + context.raw + "%";
                            }else{
                                label = 'Percentagem: ';
                                label += (context.raw).toFixed(2) + '%';
                            }
                            return label;
                        }
                    },
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    borderColor: '#ddd',
                    borderWidth: 1,
                    titleFont: {
                        size: 16,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 14
                    },
                    bodyColor: '#333',
                    titleColor: '#333',
                    displayColors: false,
                    padding: {
                        top: 10,
                        bottom: 10,
                        left: 10,
                        right: 10
                    },
                },
                title: {
                    display: true,
                    text: tipo,
                    font: {
                        size: 16
                    },
                    padding: {
                        bottom: 30
                    }
                },
                legend: {
                    display: false,
                },
            }
        }
    });
}

function criarGraficoLinhas(dados, tipo) {
    var labels = [];
    var datasets = [];
    var num = 0;

    if (tipo == 'Principais pessoas citadas' || tipo == 'Organizações com maior destaque') {
        const jornais = Object.keys(dados);
    
        // Obter todas as datas únicas
        const labelsSet = new Set();
        jornais.forEach(jornal => {
            Object.keys(dados[jornal]).forEach(date => {
                labelsSet.add(date);
            });
        });
    
        // Converter as datas no formato "dd/mm/yyyy" para objetos Date
        labels = Array.from(labelsSet).map(date => {
            const [day, month, year] = date.split('/');
            return new Date(`${year}-${month}-${day}`);
        });
    
        // Ordenar as datas
        labels.sort((a, b) => a - b);
    
        // Converter de volta para o formato "dd/mm/yyyy"
        labels = labels.map(date => {
            const day = String(date.getDate()).padStart(2, '0');
            const month = String(date.getMonth() + 1).padStart(2, '0'); // Month is zero-based
            const year = date.getFullYear();
            return `${day}/${month}/${year}`;
        });
    
        // Cores embaralhadas
        colors = shuffleColors(colors);
    
        jornais.forEach(jornal => {
            const dataValues = [];
            labels.forEach(date => {
                const topPerson = dados[jornal][date] ? dados[jornal][date][0] : null;
                const count = dados[jornal][date] ? dados[jornal][date][1] : 0;
                dataValues.push({ topPerson, count });
            });
    
            datasets.push({
                label: obterNome(jornal),
                data: dataValues.map(d => d.count),
                backgroundColor: colors[num],
                borderColor: colors[num],
                borderWidth: 2,
                fill: false,
                tension: 0.25,
                pointRadius: 1.5,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: colors[num],
                topPersons: dataValues.map(d => d.topPerson)
            });
            num += 1;
        });
    
        datasets.sort((a, b) => {
            const sumA = a.data.reduce((acc, curr) => acc + curr, 0);
            const sumB = b.data.reduce((acc, curr) => acc + curr, 0);
            return sumB - sumA; // Decrescente
        });
    } else {
        const jornais = Object.keys(dados);
    
        labels = Object.keys(dados['Total']);
    
        // Converter as datas no formato "dd/mm/yyyy" para objetos Date
        labels = labels.map(date => {
            const [day, month, year] = date.split('/');
            return new Date(`${year}-${month}-${day}`);
        });
    
        // Ordenar as datas
        labels.sort((a, b) => a - b);
    
        // Converter de volta para o formato "dd/mm/yyyy"
        labels = labels.map(date => {
            const day = String(date.getDate()).padStart(2, '0');
            const month = String(date.getMonth() + 1).padStart(2, '0'); // Month is zero-based
            const year = date.getFullYear();
            return `${day}/${month}/${year}`;
        });
    
        colors = shuffleColors(colors);
    
        jornais.forEach(jornal => {
            const dataValues = [];
            labels.forEach(date => {
                const value = dados[jornal][date] || 0;
                dataValues.push(value);
            });
    
            datasets.push({
                label: obterNome(jornal),
                data: dataValues,
                backgroundColor: colors[num],
                borderColor: colors[num],
                borderWidth: 2,
                fill: false,
                tension: 0.25,
                pointRadius: 1.5,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: colors[num]
            });
            num += 1;
        });
        datasets.sort((a, b) => {
            const sumA = a.data.reduce((acc, curr) => acc + curr, 0);
            const sumB = b.data.reduce((acc, curr) => acc + curr, 0);
            return sumB - sumA; // Decrescente
        });
    }
    

    if (graficosAtivos[tipo]) {
        graficosAtivos[tipo].destroy();
    }

    // Criar o gráfico de linhas
    $('#container-graficos').append(
        `
        <div class="div-grafico">
        <a href="#" onclick="toggleFullScreen('${tipo}', this.children[0], 'grafico')">
            <img src="../static/images/fullscreen.png" alt="Full Screen" class="but-fullscreen">
        </a>
        <a href="#" onclick="downloadChart('${tipo}')">
          <img src="../static/images/download.png" alt="Download" class="but-download">
        </a>
          <canvas id="${tipo}"></canvas>
      </div>`
    )
    var ctx = document.getElementById(tipo).getContext('2d');
    graficosAtivos[tipo] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        fontSize: 14
                    },
                    grid: {
                        color: 'rgba(127, 162, 196, 0.2)'
                    }
                },
                x: {
                    ticks: {
                        fontSize: 14,
                        autoSkip: true,
                        maxRotation: 90,
                        minRotation: 0
                    },
                    grid: {
                        color: 'transparent'
                    }
                }
            },

            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    position: 'nearest',
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label;
                            if (label) {
                                label += ': ';
                            }
                            if((tipo == 'Principais pessoas citadas' || tipo == 'Organizações com maior destaque') && context.dataset.topPersons[context.dataIndex] != null){
                                label += "[" + context.dataset.topPersons[context.dataIndex] + " : " + context.parsed.y + "]";
                            }else{
                                label += context.parsed.y;
                            }
                            return label;
                        }
                    },
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    borderColor: '#ddd',
                    borderWidth: 1,
                    titleFont: {
                        size: 16,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 14
                    },
                    bodyColor: '#333',
                    titleColor: '#333',
                    displayColors: true,
                    padding: {
                        top: 10,
                        bottom: 10,
                        left: 10,
                        right: 10
                    },
                },
                title: {
                    display: true,
                    text: tipo,
                    font: {
                        size: 16
                    },
                    padding: {
                        bottom: 30
                    }
                }
            }
        }
    });
}

function shuffleColors(colors) {
    // Cria uma cópia do array de cores para não modificar o original
    let shuffledColors = colors.slice();

    // Embaralha o array de cores usando o algoritmo Fisher-Yates
    for (let i = shuffledColors.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffledColors[i], shuffledColors[j]] = [shuffledColors[j], shuffledColors[i]];
    }

    return shuffledColors;
}

function criarGraficoPie(dados, tipo) {
    var labels = [];
    var data = [];
    var total_noticias = 0;

    let entries = Object.entries(dados);

    // Ordenar - ordem crescente
    entries.sort((a, b) => b[1] - a[1]);

    if (tipo != "Autores com mais publicações") {
        colors = [];
        total_noticias = 0;
        for (const [chave, valor] of entries) {
            total_noticias += valor;
            if (chave == "Positivo") {
                colors.push('green');
            } else if (chave == "Negativo") {
                colors.push('red');
            } else {
                colors.push('yellow');
            }
            labels.push(chave);
            data.push(valor);
        }
    }else{
        for (const [chave, valor] of entries) {
            labels.push(chave);
            data.push(valor);
        }
    }

    if (graficosAtivos[tipo]) {
        graficosAtivos[tipo].destroy();
    }

    // Criar o gráfico de linhas
    $('#container-graficos').append(
        `
        <div class="div-grafico">
            <a href="#" onclick="toggleFullScreen('${tipo}', this.children[0], 'grafico')">
                <img src="../static/images/fullscreen.png" alt="Full Screen" class="but-fullscreen">
            </a>
            <a href="#" onclick="downloadChart('${tipo}')">
            <img src="../static/images/download.png" alt="Download" class="but-download">
            </a>
            <canvas id="${tipo}"></canvas>
      </div>`
    )

    var ctx = document.getElementById(tipo).getContext('2d');
    graficosAtivos[tipo] = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: tipo == "Autores com mais publicações" ? shuffleColors(colors) : colors,
                borderColor: 'white',
                borderWidth: 1,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label;
                            if (tipo == "Autores com mais publicações") {
                                label = 'Número de notícias escritas: ' + context.raw;
                            }else{
                                label = 'Percentagem: ' + ((context.raw)/total_noticias * 100).toFixed(2) + '%';
                            }
                            return label;
                        }
                    },
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    borderColor: '#ddd',
                    borderWidth: 1,
                    titleFont: {
                        size: 16,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 14
                    },
                    bodyColor: '#333',
                    titleColor: '#333',
                    displayColors: true,
                    padding: {
                        top: 10,
                        bottom: 10,
                        left: 10,
                        right: 10
                    },
                },
                title: {
                    display: true,
                    text: tipo,
                    font: {
                        size: 16
                    },
                    padding: {
                        bottom: 30
                    }
                }
            }
        }
    });
}


function downloadChart(id) {
    var canvas = document.getElementById(id);
    var image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
    var link = document.createElement('a');
    link.download = id + '.png';
    link.href = image;
    link.click();
}