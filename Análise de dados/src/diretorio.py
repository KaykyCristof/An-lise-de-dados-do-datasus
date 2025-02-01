import os
import pandas as pd

# Cria um diretório, se não existir.
def criar_diretorio(diretorio):
    """
    Cria um diretório caso ele não exista.
    """
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

# Salva o DataFrame processado como um arquivo CSV.
def salvar_arquivo(dados, caminho_arquivo):
    """
    Salva o DataFrame como um arquivo CSV no caminho especificado.
    """
    diretorio = os.path.dirname(caminho_arquivo)
    criar_diretorio(diretorio)
    dados.to_csv(caminho_arquivo, index=False, encoding='utf-8', sep=';')
    print(f"Arquivo processado salvo em: {caminho_arquivo}")

# Carrega um arquivo CSV como DataFrame.
def carregar_arquivo(caminho_arquivo):
    """
    Carrega um arquivo CSV como um DataFrame.
    """
    try:
        print(f"Carregando arquivo: {caminho_arquivo}")
        dados = pd.read_csv(caminho_arquivo, encoding='utf-8', sep=';', on_bad_lines='skip')
        return dados
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao carregar o arquivo '{caminho_arquivo}': {e}")
        return None
