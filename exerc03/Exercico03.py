from PIL import Image
from tkinter import Tk, filedialog

def converter_para_preto_e_branco_manual():

    try:
        root = Tk()
        root.withdraw()

        caminho_imagem = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.gif"), ("Todos os arquivos", "*.*")]
        )

        if not caminho_imagem:
            print("Nenhuma imagem foi selecionada.")
            return

        imagem = Image.open(caminho_imagem)
        imagem = imagem.convert("RGB")  # Garante que a imagem esteja no modo RGB
        largura, altura = imagem.size
        imagem_preto_branco = Image.new("L", (largura, altura))

        # Itera sobre cada pixel da imagem

        for x in range(largura):
            for y in range(altura):
                r, g, b = imagem.getpixel((x, y))
                luminancia = int(0.299 * r + 0.587 * g + 0.114 * b)
                imagem_preto_branco.putpixel((x, y), luminancia)

        caminho_saida = filedialog.asksaveasfilename(
            title="Salvar imagem em preto e branco",
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("Todos os arquivos", "*.*")]
        )

        if not caminho_saida:
            print("Operação de salvamento cancelada.")
            return

        # Salva a imagem em preto e branco no caminho especificado

        imagem_preto_branco.save(caminho_saida)
        print(f"Imagem convertida com sucesso! Salva em: {caminho_saida}")

    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")

# Exemplo de uso

if __name__ == "__main__":
    converter_para_preto_e_branco_manual()