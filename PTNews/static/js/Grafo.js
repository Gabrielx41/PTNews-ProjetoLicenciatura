var num_coocorrencias = 10;
var primeira = true;
function criarGrafoD3(graphDataInicial, target, dados) {
    $('#container-grafo').empty();
    $('#opt-grafo').empty();
    
    // Definir margens e dimensões do gráfico
    var margin = { top: 60, right: 20, bottom: 40, left: 20 };
    var width = window.innerWidth - margin.left - margin.right;
    var height = window.innerHeight - margin.top - margin.bottom - 75;

    // Selecionar o container do gráfico
    var container = d3.select("#container-grafo");
    var options = d3.select("#opt-grafo");
    var sliderWrapper = d3.select("#slider-container");

    // Criação do SVG dentro do container
    const svg = container.append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Adicionar título ao grafo
    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", -(margin.top / 2) + 20)
        .attr("text-anchor", "middle")
        .style("font-size", "20px")
        .style("font-weight", "bold")
        .text("Grafo de Co-ocorrência para \"" + target + "\"");

    if (window.innerWidth < 768) {
        svg.select("text")
            .style("font-size", "5vw");
    }

    // Calcular o peso máximo e mínimo
    const maxWeight = d3.max(graphDataInicial.links, d => d.weight);
    const minWeight = d3.min(graphDataInicial.links, d => d.weight);

    // Função para normalizar os pesos
    function normalizeWeight(weight) {
        const minDistance = 1; // Distância mínima
        const maxDistance = 4; // Distância máxima
        return minDistance + ((weight - minWeight) / (maxWeight - minWeight)) * (maxDistance - minDistance);
    }

    // Função para mapear os pesos para cores
    const colorScale = d3.scaleSequential(d3.interpolateViridis).domain([minWeight, maxWeight]);

    // Configuração da simulação de força
    const simulation = d3.forceSimulation(graphDataInicial.nodes)
        .force("link", d3.forceLink(graphDataInicial.links).id(d => d.id).distance(d => 350 / normalizeWeight(d.weight)))
        .force("charge", d3.forceManyBody().strength(-300))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .on("tick", ticked);

    // Grupo para os links
    const linkGroup = svg.append("g")
        .attr("class", "links");

    // Grupo para os nós
    const nodeGroup = svg.append("g")
        .attr("class", "nodes");

    // Criar os links
    const link = linkGroup.selectAll("line")
        .data(graphDataInicial.links)
        .enter()
        .append("line")
        .attr("stroke-width", 2)
        .attr("stroke", d => colorScale(d.weight));

    // Criar os labels dos links
    const linkLabels = linkGroup.selectAll(".link-label")
        .data(graphDataInicial.links)
        .enter()
        .append("g")
        .attr("class", "link-label");

    linkLabels.append("rect")
        .attr("width", 40)
        .attr("height", 20)
        .attr("fill", "#F1F3F5")
        .attr("rx", 5)
        .attr("ry", 5)
        .attr("x", -20)
        .attr("y", -10);

    linkLabels.append("text")
        .text(d => d.weight)
        .attr("font-size", "12px")
        .attr("fill", "black")
        .attr("text-anchor", "middle");

    // Criar os nós
    const node = nodeGroup.selectAll(".node")
        .data(graphDataInicial.nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    node.append("circle")
        .attr("r", 25)
        .attr("fill", "lightblue")
        .attr("stroke", "#50789F");

    // Dimensões do retângulo para o texto do nó
    const rectWidth = 60;
    const rectHeight = 20;

    node.append("rect")
        .attr("width", rectWidth)
        .attr("height", rectHeight)
        .attr("fill", "#F1F3F5")
        .attr("rx", 5)
        .attr("ry", 5)
        .attr("x", -rectWidth / 2)
        .attr("y", 26);

    node.append("text")
        .text(d => d.id)
        .attr("font-size", "14px")
        .attr("fill", "black")
        .attr("text-anchor", "middle")
        .style("cursor", "pointer")
        .attr("dy", "40px")
        .on("click", function(d) {
            pesquisar("grafo", d.id, false);
        });

    // Função ticked para atualizar elementos no gráfico
    function ticked() {
        link.attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        linkLabels.attr("transform", function(d) {
            const x = (d.source.x + d.target.x) / 2;
            const y = (d.source.y + d.target.y) / 2;
            return "translate(" + x + "," + y + ")";
        });

        node.attr("transform", function(d) {
            // Limitar a posição dos nós dentro das margens, considerando a altura do título
            d.x = Math.max(rectWidth / 2, Math.min(width - rectWidth / 2, d.x));
            d.y = Math.max(rectHeight / 2 + margin.top, Math.min(height - rectHeight / 2, d.y));
            return "translate(" + d.x + "," + d.y + ")";
        });
    }

    // Funções para manipulação de eventos de drag dos nós
    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    options.append("img")
    .attr("src", "../static/images/centrar.png")
    .attr("width", 20)
    .attr("height", 20)
    .style("cursor", "pointer")
    .on("click", function() {
        simulation.alphaTarget(1).restart();
    });

    options.append("img")
    .attr("src", "../static/images/download.png")
    .attr("width", 23)
    .attr("height", 23)
    .style("cursor", "pointer")
    .style("float", "right")
    .on("click", function() {
        downloadSVG();
    });
    if(primeira){        
        sliderWrapper.append("span")
            .attr("id", "sliderLabel")
            .text("Número de palavras co-ocorrentes: " + num_coocorrencias);
    
        sliderWrapper.append("input")
            .attr("type", "range")
            .attr("min", 5)
            .attr("max", 20)
            .attr("value", num_coocorrencias)
            .attr("id", "rangeSlider")
            .style("margin", "0")
            .on("input", function() {
                d3.select("#sliderLabel").text("Número de palavras co-ocorrentes: " + this.value);
                num_coocorrencias = parseInt(this.value);
                updateSliderProgress(num_coocorrencias, this.min, this.max);
                criarGrafoD3(dados[0][parseInt(this.value)], target, dados);
            });
    
        function updateSliderProgress(value, min, max) {
            const percentage = ((value - min) / (max - min)) * 100;
            document.getElementById('rangeSlider').style.background = `linear-gradient(to right, #50789F ${percentage}%, #ddd ${percentage}%)`;
        }
    
        updateSliderProgress(num_coocorrencias, 5, 20);
        primeira = false;
    }
    return svg;
}
