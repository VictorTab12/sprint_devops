#!pip install google-search-results
from serpapi import GoogleSearch


params = {
  "engine": "google_shopping",
  "q": "tv",
  "tbs": "mr:1,pdtr0:708987%7C709001!708995!1000526",
  "api_key": "2f2afff318fb54275b1c90320748f68c46177611d91b99c226a4101debd44cd0"
}

search = GoogleSearch(params)
results = search.get_dict()
filters = results["filters"]
def format_price(price_str):
    """
    Formata a string de preço, removendo caracteres indesejados
    e convertendo para um valor numérico.
    """
    # Remover o "R$" e espaços
    clean_price = price_str.replace("R$", "").strip()

    # Remover pontos de milhar e substituir vírgulas decimais por ponto
    clean_price = clean_price.replace(".", "").replace(",", ".")

    # Converter para float
    try:
        return float(clean_price)
    except ValueError:
        return None  # Retorna None se não conseguir converter

def search_products_or_services(query, location, num_results=3, sort_by="rating_desc"):
    """
    Realiza uma busca no Google Shopping usando SerpApi, comparando produtos
    ou serviços com base em preço e avaliação.

    :param query: O termo de busca (ex.: "laptop" ou "reparo de computadores").
    :param location: A localização da busca (ex.: "São Paulo, São Paulo, Brazil").
    :param num_results: Número de resultados a exibir.
    :param sort_by: Critério de ordenação ("price_asc", "price_desc", "rating_asc", "rating_desc").
    :return: Relatório detalhado com os melhores resultados.
    """
    # Configuração dos parâmetros da pesquisa
    params = {
        "q": query,
        "tbm": "shop",  # Pesquisa no Google Shopping
        "location": location,
        "hl": "pt-BR",
        "gl": "br",
        "api_key": "1a316514948c0ae8d114b67d500a23bd5282e4564b67ca6c0fa0bd1d1f296e64"  # Substitua pela sua chave de API SerpApi
    }

    # Executando a pesquisa
    search = GoogleSearch(params)
    results = search.get_dict()

    # Extraindo os resultados
    shopping_results = results.get("shopping_results", [])

    if shopping_results:
        # Filtrando resultados por avaliação e preço
        filtered_results = [
            {
                'title': result['title'],
                'price': format_price(result['price']),
                'rating': float(result.get('rating', '0')),
                'source': result['source'],
                'link': result.get('link', 'N/A'),
                'reviews': result.get('reviews', 'N/A')
            }
            for result in shopping_results
            if 'price' in result and 'rating' in result
        ]

        # Definindo a ordenação
        if sort_by == "price_asc":
            sorted_results = sorted(filtered_results, key=lambda x: x['price'])
        elif sort_by == "price_desc":
            sorted_results = sorted(filtered_results, key=lambda x: x['price'], reverse=True)
        elif sort_by == "rating_asc":
            sorted_results = sorted(filtered_results, key=lambda x: x['rating'])
        elif sort_by == "rating_desc":
            sorted_results = sorted(filtered_results, key=lambda x: x['rating'], reverse=True)
        else:
            sorted_results = filtered_results

        # Gerando relatório detalhado
        report = f"Relatório de comparação para: '{query}' em {location}\n"
        report += "=" * 50 + "\n"
        for i, result in enumerate(sorted_results[:num_results]):
            report += f"Opção {i + 1}:\n"
            report += f"Produto/Serviço: {result['title']}\n"
            report += f"Preço: R${result['price']:.2f}\n"
            report += f"Avaliação: {result['rating']} estrelas\n"
            report += f"Número de Avaliações: {result['reviews']}\n"
            report += f"Loja/Fornecedor: {result['source']}\n"
            report += f"Link: {result['link']}\n"
            report += "-" * 50 + "\n"
        return report
    else:
        return "Nenhum resultado encontrado."


# Exemplo de uso
location = "São Paulo, São Paulo, Brazil"
query = "ps4"  # Pode ser alterado para qualquer produto ou serviço
print(search_products_or_services(query, location, sort_by="rating_desc"))