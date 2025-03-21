from PIL import Image
import threading
import time
import os

# Função que processa uma faixa da imagem (linha por linha)
def processar_faixa(imagem_rgb, imagem_pb, y_inicio, y_fim):
    largura = imagem_rgb.size[0]
    for y in range(y_inicio, y_fim):
        for x in range(largura):
            r, g, b = imagem_rgb.getpixel((x, y))
            luminancia = int(0.299 * r + 0.587 * g + 0.114 * b)
            imagem_pb.putpixel((x, y), luminancia)

# Função principal
def converter_para_preto_e_branco_com_threads():
    try:
        # Caminho fixo da imagem de entrada
        caminho_imagem = r"D:\fotos wlp\image_0144"

        if not os.path.exists(caminho_imagem):
            print(f"Imagem não encontrada: {caminho_imagem}")
            return

        imagem_rgb = Image.open(caminho_imagem).convert("RGB")
        largura, altura = imagem_rgb.size
        imagem_pb = Image.new("L", (largura, altura))

        num_threads = 4
        threads = []
        faixa_altura = altura // num_threads

        inicio_tempo = time.time()

        # Cria as threads para processar faixas da imagem
        for i in range(num_threads):
            y_inicio = i * faixa_altura
            y_fim = altura if i == num_threads - 1 else (i + 1) * faixa_altura
            t = threading.Thread(target=processar_faixa, args=(imagem_rgb, imagem_pb, y_inicio, y_fim))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        fim_tempo = time.time()

        # Caminho fixo de saída
        caminho_saida = r"C:\Users\lucas\Downloads\imagem_pb.jpg"
        imagem_pb.save(caminho_saida)

        print(f"Imagem convertida com sucesso! Salva em: {caminho_saida}")
        print(f"Tempo de execução com threads: {fim_tempo - inicio_tempo:.2f} segundos")

    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")

# Executa
if __name__ == "__main__":
    converter_para_preto_e_branco_com_threads()
