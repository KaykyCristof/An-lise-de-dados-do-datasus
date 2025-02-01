import os
import pandas as pd
import scipy.stats as stats  # noqa: F401

# Carrega um dataset de um arquivo CSV
def carregar_dataset(nome_arquivo, pasta):
    try:
        caminho_arquivo = os.path.join(obter_diretorio_base(), "dados", "processado", pasta, nome_arquivo)
        return pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8')
    except Exception as e:
        print(f"Erro ao carregar {nome_arquivo}: {e}")
        return None

# Salva um DataFrame como arquivo CSV
def salvar_dados(dados, nome_arquivo, pasta):
    try:
        caminho_salvamento = os.path.join(obter_diretorio_base(), "dados", "processado", pasta, nome_arquivo)
        dados.to_csv(caminho_salvamento, index=False, sep=';', encoding='utf-8')
        print(f"Dados salvos em: {caminho_salvamento}")
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

# Retorna o diretório base do projeto
def obter_diretorio_base():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carrega e processa todos os arquivos especificados
def carregar_datasets():
    arquivos = {
        "Mortalidade 2020 (Região)": ("mortalidade2020.csv", "Região"),
        "Mortalidade 2021 (Região)": ("mortalidade2021.csv", "Região"),
        "Mortalidade 2022 (Região)": ("mortalidade2022.csv", "Região"),
        "Mortalidade 2023 (Região)": ("mortalidade2023.csv", "Região"),
        "Sexo Masc2023 (Sexo)": ("sexoMasc2023.csv", "Sexo"),
        "Sexo Fem2023 (Sexo)": ("sexoFem2023.csv", "Sexo"),
        "Idade 2023 (Idade)": ("idade2023.csv", "Idade"),
    }
    return {
        nome: carregar_dataset(arquivo, pasta)
        for nome, (arquivo, pasta) in arquivos.items()
        if carregar_dataset(arquivo, pasta) is not None
    }

# Exibe um resumo geral do dataset
def exibir_resumo_geral(dataset):
    print(f"\nResumo do Dataset: {dataset.name}")
    print(f"- Número de Linhas: {dataset.shape[0]}")
    print(f"- Número de Colunas: {dataset.shape[1]}")
    print("\nTipos de Dados:")
    print(dataset.dtypes)
    print("\nValores Ausentes:")
    print(dataset.isnull().sum())
    print("-" * 40)

# Gera estatísticas descritivas do dataset
def exibir_estatisticas_descritivas(dataset):
    print(f"\nEstatísticas Descritivas: {dataset.name}")
    colunas_numericas = dataset.select_dtypes(include=['number'])
    if colunas_numericas.empty:
        print("Nenhuma coluna numérica encontrada.")
        return
    print("\nResumo Estatístico:")
    print(colunas_numericas.describe())
    print("\nValores Extremos:")
    for coluna in colunas_numericas.columns:
        maximo = colunas_numericas[coluna].max()
        minimo = colunas_numericas[coluna].min()
        print(f"- {coluna}: Mínimo = {minimo}, Máximo = {maximo}")
    print("-" * 40)

# Consolida os dados de mortalidade ao longo dos anos
def consolidar_dados_temporais(datasets):
    datasets_mortalidade = {nome: df for nome, df in datasets.items() if "Mortalidade" in nome}
    datasets_consolidados = []
    for nome, dataset in datasets_mortalidade.items():
        ano = int(nome.split()[1])
        dataset['Ano'] = ano
        datasets_consolidados.append(dataset)
    dados_temporais = pd.concat(datasets_consolidados, ignore_index=True)
    salvar_dados(dados_temporais, "dados_temporais.csv", "Região")
    return dados_temporais

# Exibe o menu interativo para o usuário
def menu(datasets):
    while True:
        print("\nMenu de Análises:")
        print("1. Exibir resumo geral dos datasets")
        print("2. Gerar estatísticas descritivas")
        print("3. Sair")
        escolha = input("Escolha uma opção (1-3): ")

        if escolha == "1":
            for nome, dataset in datasets.items():
                dataset.name = nome
                exibir_resumo_geral(dataset)
        elif escolha == "2":
            for nome, dataset in datasets.items():
                dataset.name = nome
                exibir_estatisticas_descritivas(dataset)
        elif escolha == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Ponto de entrada principal do programa
if __name__ == "__main__":
    datasets = carregar_datasets()
    dados_temporais = consolidar_dados_temporais(datasets)
    menu(datasets)
