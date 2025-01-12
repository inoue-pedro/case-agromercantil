import requests
import hashlib
import time
import os

# URL do site a ser monitorado
url = 'https://exemplo.com'

# Caminho para armazenar o hash do HTML anterior
hash_file_path = 'previous_hash.txt'

# Função para calcular o hash de um conteúdo HTML
def get_html_hash(html_content):
    return hashlib.md5(html_content.encode('utf-8')).hexdigest()

# Função para fazer a requisição e obter o HTML da página
def get_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Erro ao acessar {url}: {response.status_code}")
        return None

# Função para verificar se houve mudança no layout
def check_layout_change(current_html):
    # Tenta carregar o hash anterior do arquivo
    if os.path.exists(hash_file_path):
        with open(hash_file_path, 'r') as f:
            previous_hash = f.read()
        
        current_hash = get_html_hash(current_html)
        
        if current_hash != previous_hash:
            print("Mudança detectada no layout!")
            # Salva o novo hash para comparação futura
            with open(hash_file_path, 'w') as f:
                f.write(current_hash)
        else:
            print("Nenhuma mudança detectada.")
    else:
        # Se for a primeira vez que o script está rodando, salva o hash inicial
        current_hash = get_html_hash(current_html)
        with open(hash_file_path, 'w') as f:
            f.write(current_hash)
        print("Primeira execução, hash salvo.")

# Função principal para rodar o scraper em intervalos regulares
def run_scraper():
    while True:
        print(f"Acessando {url}...")
        html_content = get_html_content(url)
        
        if html_content:
            check_layout_change(html_content)
        
        # Intervalo de tempo entre as requisições (por exemplo, 1 hora)
        time.sleep(3600)  # 3600 segundos = 1 hora

# Rodar o scraper
if __name__ == "__main__":
    run_scraper()
