
async function enviarImagem(arquivo) {
    const dados = new FormData();
    dados.append("image", arquivo);

    const resposta = await fetch("http://127.0.0.1:8000/image", {
        method: "POST",
        body: dados
    });

    const resultado = await resposta.json();

    if (!resposta.ok) {
        console.error(resultado);
        return;
    }

    const imagem = new Image();
    imagem.src = URL.createObjectURL(arquivo);

    imagem.onload = () => {
        const canvas = document.getElementById("canvas");
        const ctx = canvas.getContext("2d");

        canvas.width = imagem.naturalWidth;
        canvas.height = imagem.naturalHeight;

        ctx.drawImage(imagem, 0, 0);

        for (const p of resultado.results) {
            const largura = p.x2 - p.x1;
            const altura = p.y2 - p.y1;

            // Desenha o retângulo
            ctx.strokeStyle = "#00ff00";
            ctx.lineWidth = Math.max(2, imagem.naturalWidth / 300);
            ctx.strokeRect(p.x1, p.y1, largura, altura);

            // Escreve a classe e a confiança
            const texto =
                `${p.classe} ${(p.confianca * 100).toFixed(1)}%`;

            const tamanhoFonte = Math.max(
                14, imagem.naturalWidth / 50
            );

            ctx.font = `${tamanhoFonte}px Arial`;

            const alturaTexto = tamanhoFonte + 8;
            const larguraTexto = ctx.measureText(texto).width + 8;
            const yTexto = Math.max(0, p.y1 - alturaTexto);

            ctx.fillStyle = "#00ff00";
            ctx.fillRect(p.x1, yTexto, larguraTexto, alturaTexto);

            ctx.fillStyle = "#000000";
            ctx.fillText(texto, p.x1 + 4, yTexto + tamanhoFonte);
        }
    };
}

const campo = document.getElementById("imagem");
const botao = document.getElementById("enviar");

botao.addEventListener("click", () => {
    const arquivo = campo.files[0];

    if (arquivo) {
        enviarImagem(arquivo);
    } else {
        alert("Selecione uma imagem primeiro!");
    }
});