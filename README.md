# WebScraperCode

**É um projeto de web scraping básico feito em Python, com o objetivo de puxar informações de um site. Ele busca por um termo específico, navega por todas as páginas de resultados e salva as informações coletadas em um arquivo CSV.**


## Tecnologias e Bibliotecas Utilizadas

-   **Python 3**
-   **Requests:** Para realizar as requisições HTTP.
-   **BeautifulSoup4:** Para fazer o parse do HTML e extrair os dados usando seletores CSS.
-   **urllib:** Para a manipulação e construção de URLs.

## **Como Adicionar um novo Site**

1.  **Escolha o site:** Escolha um site de notícias no geral que você queira pegar informações.

2.  **Abra as ferramentas de desenvolvedor:** No seu navegador (Chrome, Firefox, etc.), vá até o site e pressione `F12` ou clique com o botão direito e vá em "Inspecionar".

3.  **Encontre os seletores CSS:**
    * **Contêiner:** Encontre um elemento HTML que "embrulha" cada notícia na página principal. Clique na ferramenta de seleção (geralmente um ícone de um quadrado com uma seta) e passe o mouse sobre as notícias. Você verá um `div` ou `article` que se repete para cada uma. Clique com o botão direito neste elemento > Copiar > Copiar seletor.
      
    * **Título e link:** Dentro desse contêiner, faça o mesmo para a manchete (que geralmente é o próprio link). Copie o seletor.
      
    * **Resumo (opcional):** Se houver um texto de resumo, copie o seletor dele também.

4.  **Adicione ao dicionário `SITES_CONFIG`:** abra o arquivo `scraper.py` e adicione uma nova entrada ao dicionário `SITES_CONFIG`. Por exemplo:

    ```python
    SITES_CONFIG = {
        'tecmundo': {
            'url': '[urlbase](urlbase)',
            'container_selector': 'div.tec--card__info',
            'title_selector': 'h3.tec--card__title',
            'link_selector': 'a.tec--card__title-link',
            'summary_selector': None, # Não há um resumo fácil de pegar
        }
    }
    ```
5.  **Execute Novamente:** Salve o arquivo e rode `python scraper.py`.

**OBS:** Os sites mudam sua estrutura HTML com o tempo. Se o scraper parar de funcionar para um site específico, o motivo mais provável é que os seletores CSS mudaram. O processo para consertar é o mesmo que foi mostrado.
