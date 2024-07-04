function downloadImage(nameImage) {
    // Cria um link temporário
    var link = document.createElement('a');
    link.href = "../static/images/" + nameImage + ".png";
    link.download = nameImage + '.png';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function openImage(nameImage){
    var link = document.createElement('a');
    link.href = "../static/images/" + nameImage + ".png";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function downloadSVG() {
    const svgElement = document.querySelector("#container-grafo svg");

    // Serializa o SVG para XML
    const svgXml = new XMLSerializer().serializeToString(svgElement);

    // Cria um canvas para converter o SVG em PNG
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    // Define as dimensões do canvas baseado no SVG
    const svgSize = svgElement.getBoundingClientRect();
    canvas.width = svgSize.width;
    canvas.height = svgSize.height;

    // Função para converter o SVG em PNG usando canvg
    function convertSvgToPng(svgXml, callback) {
        canvg(canvas, svgXml, {
            renderCallback: function() {
                callback(canvas.toDataURL("image/png"));
            }
        });
    }

    // Chama a função para converter o SVG em PNG e iniciar o download
    convertSvgToPng(svgXml, function(pngDataUri) {
        // Cria um link temporário e simula o clique para baixar o arquivo PNG
        const a = document.createElement("a");
        a.href = pngDataUri;
        a.download = "grafo.png";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    });
}