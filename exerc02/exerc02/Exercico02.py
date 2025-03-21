import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def buscar_palavra_no_site(url_inicial, palavra, profundidade_maxima=3):
    """
    Busca recursivamente uma palavra específica em todas as páginas de um site.

    Parâmetros:
        url_inicial (str): A URL inicial do site.
        palavra (str): A palavra a ser buscada.
        profundidade_maxima (int): A profundidade máxima de navegação (padrão: 3).

    Retorna:
        dict: Um dicionário onde as chaves são URLs e os valores indicam se a palavra foi encontrada.
    """
    # Estruturas para armazenar resultados e evitar loops
    urls_visitados = set()
    resultados = {}

    def buscar_recursivo(url_atual, profundidade_atual):
        # Verifica se atingimos a profundidade máxima ou já visitamos essa URL
        if profundidade_atual > profundidade_maxima or url_atual in urls_visitados:
            return
        urls_visitados.add(url_atual)

        try:
            # Faz a requisição HTTP
            print(f"Buscando em: {url_atual} (Profundidade: {profundidade_atual})")
            response = requests.get(url_atual, timeout=10)
            response.raise_for_status()  # Lança exceção para erros HTTP

            # Analisa o conteúdo HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Verifica se a palavra está no conteúdo da página
            conteudo = soup.get_text().lower()
            palavra_encontrada = palavra.lower() in conteudo
            resultados[url_atual] = palavra_encontrada

            # Extrai todos os links da página
            links = soup.find_all('a', href=True)
            for link in links:
                url_completa = urljoin(url_inicial, link['href'])

                # Garante que só navegamos dentro do mesmo domínio
                if url_completa.startswith(url_inicial):
                    buscar_recursivo(url_completa, profundidade_atual + 1)

        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {url_atual}: {e}")

    # Inicia a busca recursiva
    buscar_recursivo(url_inicial, profundidade_atual=1)
    return resultados

# Exemplo de uso
if __name__ == "__main__":
    url_inicial = input("Digite a URL inicial do site (ex.: https://www.exemplo.com): ")
    palavra = input("Digite a palavra a ser buscada: ")

    resultados = buscar_palavra_no_site(url_inicial, palavra)

    print("\nResultados da busca:")
    for url, encontrada in resultados.items():
        status = "Encontrada" if encontrada else "Não encontrada"
        print(f"{url}: Palavra '{palavra}' {status}")