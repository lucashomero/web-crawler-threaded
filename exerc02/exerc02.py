import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Função que será executada por cada thread para processar uma URL
def processar_url(url_atual, palavra, profundidade_atual, profundidade_maxima, url_inicial, urls_visitadas, resultados, lock, threads):
    # Verifica se a profundidade máxima foi atingida
    if profundidade_atual > profundidade_maxima:
        return

    # Garante que a mesma URL não seja visitada mais de uma vez
    with lock:
        if url_atual in urls_visitadas:
            return
        urls_visitadas.add(url_atual)

    try:
        print(f"Buscando em: {url_atual} (Profundidade: {profundidade_atual})")

        # Faz requisição HTTP para obter o conteúdo da página
        response = requests.get(url_atual, timeout=10)
        response.raise_for_status()

        # Faz o parser do HTML usando BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        conteudo = soup.get_text().lower()

        # Verifica se a palavra procurada está no conteúdo da página
        palavra_encontrada = palavra.lower() in conteudo

        # Salva o resultado (True ou False) de forma segura com lock
        with lock:
            resultados[url_atual] = palavra_encontrada

        # Coleta todos os links da página
        links = soup.find_all('a', href=True)
        for link in links:
            url_completa = urljoin(url_inicial, link['href'])

            # Garante que só navegue dentro do mesmo site (domínio)
            if url_completa.startswith(url_inicial):
                # Cria uma nova thread para processar esse novo link
                t = threading.Thread(
                    target=processar_url,
                    args=(url_completa, palavra, profundidade_atual + 1,
                          profundidade_maxima, url_inicial, urls_visitadas,
                          resultados, lock, threads)
                )
                t.start()
                threads.append(t)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url_atual}: {e}")

# Função principal da busca
def buscar_palavra_no_site(url_inicial, palavra, profundidade_maxima=3):
    urls_visitadas = set()  # Armazena URLs já visitadas
    resultados = {}         # Dicionário para guardar os resultados das buscas
    lock = threading.Lock() # Lock para controle de acesso às variáveis compartilhadas
    threads = []            # Lista com todas as threads criadas

    # Inicia a primeira thread com a URL principal
    t_inicial = threading.Thread(
        target=processar_url,
        args=(url_inicial, palavra, 1, profundidade_maxima,
              url_inicial, urls_visitadas, resultados, lock, threads)
    )
    t_inicial.start()
    threads.append(t_inicial)

    # Aguarda todas as threads finalizarem
    for t in threads:
        t.join()

    return resultados

# Execução com URL e palavra fixas
if __name__ == "__main__":
    url_inicial = "https://sigmoidal.ai/"
    palavra = "python"

    # Marca o início da execução
    inicio = time.time()

    # Chama a função de busca paralelizada
    resultados = buscar_palavra_no_site(url_inicial, palavra)

    # Marca o fim da execução
    fim = time.time()

    # Exibe os resultados
    print("\nResultados da busca:")
    for url, encontrada in resultados.items():
        status = "Encontrada" if encontrada else "Não encontrada"
        print(f"{url}: Palavra '{palavra}' {status}")

    # Mostra o tempo total de execução
    print(f"\nTempo de execução: {fim - inicio:.2f} segundos")
