import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

# Dicionário de sites para adicionar.
SITES_CONFIG = {
    'g1': {
        'url': 'https://g1.globo.com/',
        'container_selector': 'div.feed-post-body',
        'title_selector': 'a.feed-post-link',
        'link_selector': 'a.feed-post-link',
        'summary_selector': 'div.feed-post-body-resumo',
    },
    'ge_globo': {
        'url': 'https://ge.globo.com/',
        'container_selector': 'div.feed-post-body',
        'title_selector': 'a.feed-post-link',
        'link_selector': 'a.feed-post-link',
        'summary_selector': None, 
    }
}

# Nome do arquivo CSV de saída
OUTPUT_FILE = 'noticias_agregadas.csv'

# Headers para simular um navegador real
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

# Função  para raspar um site com base na configuração fornecida.
def scrape_site(session, site_name, config):
   
    print(f"--- Raspando notícias de: {site_name.upper()} ---")
    base_url = config['url']
    noticias_encontradas = []

    try:
        response = session.get(base_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página de {site_name.upper()}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Usa o seletor do container para encontrar todos os blocos de notícia.
    containers = soup.select(config['container_selector'])

    if not containers:
        print(f"Aviso: Nenhum container de notícia encontrado para {site_name.upper()}. O seletor '{config['container_selector']}' pode estar desatualizado.")
        return []

    for container in containers:
        # Usa .select_one() que retorna o primeiro elemento encontrado ou None.
        title_tag = container.select_one(config['title_selector'])
        title = title_tag.get_text(strip=True) if title_tag else 'N/A'

        link_tag = container.select_one(config['link_selector'])
        if link_tag and link_tag.has_attr('href'):
            # Constrói a URL absoluta, caso o link seja relativo
            link = urljoin(base_url, link_tag['href'])
        else:
            link = 'N/A'
        
        summary = 'N/A'
        if config['summary_selector']:
            summary_tag = container.select_one(config['summary_selector'])
            summary = summary_tag.get_text(strip=True) if summary_tag else 'N/A'
        
        if title != 'N/A' and link != 'N/A':
             noticias_encontradas.append({
                'fonte': site_name.upper(),
                'manchete': title,
                'resumo': summary,
                'link': link
            })
            
    print(f"Encontradas {len(noticias_encontradas)} notícias em {site_name.upper()}.")
    return noticias_encontradas

# Salva uma lista de dicionários em um arquivo CSV.
def salvar_em_csv(dados, nome_arquivo):
    if not dados:
        print("Nenhum dado para salvar.")
        return
        
    fieldnames = ['fonte', 'manchete', 'resumo', 'link']

    try:
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dados)
        print(f"\nDados salvos com sucesso no arquivo '{nome_arquivo}'!")
    except IOError as e:
        print(f"Erro ao salvar o arquivo: {e}")


# Função principal que orquestra o processo de scraping para todos os sites configurados.
def main():
    print("--- Iniciando o Agregador de Notícias ---")
    
    todas_as_noticias = []
    
    with requests.Session() as session:
        # Itera sobre cada site configurado no dicionário SITES_CONFIG.
        for site_name, config in SITES_CONFIG.items():
            noticias_do_site = scrape_site(session, site_name, config)
            todas_as_noticias.extend(noticias_do_site)
            time.sleep(2)
            
    print(f"\n--- Scraping finalizado! ---")
    print(f"Total de notícias agregadas: {len(todas_as_noticias)}")

    salvar_em_csv(todas_as_noticias, OUTPUT_FILE)


if __name__ == '__main__':
    main()