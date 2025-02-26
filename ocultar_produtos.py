import requests

# Configurações
API_KEY = 09d935dca1449b3ad045
URL_BASE = 'https://api.awsli.com.br/v1/'
HEADERS = {'Authorization': f'{API_KEY}', 'Content-Type': 'application/json'}

def obter_produtos():
    """Busca todos os produtos da loja."""
    url = f'{URL_BASE}produto/'
    produtos = []
    while url:
        resposta = requests.get(url, headers=HEADERS)
        dados = resposta.json()
        produtos.extend(dados['data'])
        url = dados.get('paging', {}).get('next')  # Paginação
    return produtos

def verificar_estoque(produto):
    """Verifica o estoque de um produto."""
    id_produto = produto['id']
    url = f'{URL_BASE}produto/{id_produto}/estoque/'
    resposta = requests.get(url, headers=HEADERS)
    dados = resposta.json()
    return sum(item['estoque'] for item in dados['data'])

def ocultar_produto(id_produto):
    """Define o produto como inativo (invisível na loja)."""
    url = f'{URL_BASE}produto/{id_produto}'
    dados = {'situacao': 'I'}
    resposta = requests.patch(url, headers=HEADERS, json=dados)
    if resposta.status_code == 200:
        print(f'Produto {id_produto} ocultado com sucesso.')
    else:
        print(f'Erro ao ocultar produto {id_produto}: {resposta.text}')

def main():
    produtos = obter_produtos()
    print(f'{len(produtos)} produtos encontrados.')
    for produto in produtos:
        estoque = verificar_estoque(produto)
        if estoque <= 0:
            ocultar_produto(produto['id'])

if __name__ == '__main__':
    main()
