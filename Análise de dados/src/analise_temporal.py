import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Função para carregar datasets a partir de arquivos CSV
def carregar_dataset(nome_arquivo, pasta):
    try:
        diretorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho_arquivo = os.path.join(diretorio_base, "dados", "processado", pasta, nome_arquivo)
        return pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8')
    except Exception as e:
        print(f"Erro ao carregar {nome_arquivo}: {e}")
        return None

# Função para carregar o arquivo 'dados_temporais.csv' e outros datasets
def carregar_dados():
    dados = {
        "Dados Temporais": carregar_dataset("dados_temporais.csv", "Região"),
        "Sexo Masc 2023": carregar_dataset("sexoMasc2023.csv", "Sexo"),
        "Sexo Fem 2023": carregar_dataset("sexoFem2023.csv", "Sexo"),
        "Idade 2023": carregar_dataset("Idade2023.csv", "Idade")
    }
    return {nome: df for nome, df in dados.items() if df is not None}

# Função para criar gráfico de mortes ao longo dos anos
def grafico_mortes_anos(dados):
    try:
        if 'Ano' in dados.columns and 'Total' in dados.columns:
            mortes_por_ano = dados.groupby('Ano')['Total'].sum().reset_index()
            plt.figure(figsize=(10, 6))
            plt.plot(mortes_por_ano['Ano'], mortes_por_ano['Total'], marker='o', linestyle='-', color='red')
            plt.title('Mortes ao Longo dos Anos')
            plt.xlabel('Ano')
            plt.ylabel('Número de Mortes')
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            print("As colunas 'Ano' e 'Total' não foram encontradas no conjunto de dados.")
    except Exception as e:
        print(f"Erro ao gerar o gráfico: {e}")

# Função para criar gráfico de mortes ao longo dos anos por região
def grafico_mortes_anos_regiao(dados):
    try:
        regioes = ["1 Região Norte", "2 Região Nordeste", "3 Região Sudeste", "4 Região Sul", "5 Região Centro-Oeste"]
        if 'Ano' in dados.columns and all(regiao in dados.columns for regiao in regioes):
            dados_agrupados = dados.groupby('Ano')[regioes].sum().reset_index()
            plt.figure(figsize=(12, 8))
            for regiao in regioes:
                plt.plot(dados_agrupados['Ano'], dados_agrupados[regiao], marker='o', linestyle='-', label=regiao)
            plt.title('Mortes ao Longo dos Anos por Região')
            plt.xlabel('Ano')
            plt.ylabel('Número de Mortes')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            print("As colunas 'Ano' e as colunas de regiões não foram encontradas no conjunto de dados.")
    except Exception as e:
        print(f"Erro ao gerar o gráfico: {e}")

# Função para identificar as principais causas de morte por região e gerar gráficos de barras
def principais_causas_mortes_por_regiao(dados):
    try:
        regioes = ["1 Região Norte", "2 Região Nordeste", "3 Região Sudeste", "4 Região Sul", "5 Região Centro-Oeste"]
        if "Causa - CID-BR-10" in dados.columns:
            causas = dados[["Causa - CID-BR-10"] + regioes].groupby("Causa - CID-BR-10").sum()
            for regiao in regioes:
                principais_causas = causas[regiao].sort_values(ascending=False).head(5)
                print(f"\nPrincipais causas de morte na {regiao}:")
                print(principais_causas)
                plt.figure(figsize=(10, 6))
                principais_causas.plot(kind='bar', color='blue')
                plt.title(f'Principais Causas de Morte na {regiao}')
                plt.xlabel('Causa')
                plt.ylabel('Número de Mortes')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.grid(True, linestyle='--', alpha=0.5)
                plt.show()
        else:
            print("A coluna 'Causa - CID-BR-10' não foi encontrada no conjunto de dados.")
    except Exception as e:
        print(f"Erro ao identificar as principais causas de morte: {e}")

# Função para gerar gráfico das principais causas de morte para o sexo masculino
def grafico_principais_mortes_sexo_masculino(dados_masculino):
    try:
        if "Causa - CID-BR-10" not in dados_masculino.columns or "Óbitos p/Residênc" not in dados_masculino.columns:
            print("As colunas necessárias não foram encontradas no dataset.")
            return

        dados_agrupados = dados_masculino.groupby("Causa - CID-BR-10")["Óbitos p/Residênc"].sum().reset_index()
        dados_ordenados = dados_agrupados.sort_values("Óbitos p/Residênc", ascending=False)
        principais_causas = dados_ordenados.head(10)

        plt.figure(figsize=(10, 6))
        plt.barh(principais_causas["Causa - CID-BR-10"], principais_causas["Óbitos p/Residênc"], color='skyblue')
        plt.xlabel("Número de Óbitos")
        plt.title("Principais Causas de Morte no Sexo Masculino (2023)")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Erro ao gerar o gráfico: {e}")

# Função para gerar gráfico das principais causas de morte para o sexo feminino
def grafico_principais_mortes_sexo_feminino(dados_feminino):
    try:
        if "Causa - CID-BR-10" not in dados_feminino.columns or "Óbitos p/Residênc" not in dados_feminino.columns:
            print("As colunas necessárias não foram encontradas no dataset.")
            return

        dados_agrupados = dados_feminino.groupby("Causa - CID-BR-10")["Óbitos p/Residênc"].sum().reset_index()
        dados_ordenados = dados_agrupados.sort_values("Óbitos p/Residênc", ascending=False)
        principais_causas = dados_ordenados.head(10)

        plt.figure(figsize=(10, 6))
        plt.barh(principais_causas["Causa - CID-BR-10"], principais_causas["Óbitos p/Residênc"], color='salmon')
        plt.xlabel("Número de Óbitos")
        plt.title("Principais Causas de Morte no Sexo Feminino (2023)")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Erro ao gerar o gráfico: {e}")

# Função para criar gráficos de mortes por faixa etária e causa
def grafico_mortes_por_faixa_etaria(dados_idade):
    try:
        colunas_necessarias = [
            "Causa - CID-BR-10", "Menor 1 ano", "1 a 4 anos", "5 a 9 anos", "10 a 14 anos", 
            "15 a 19 anos", "20 a 29 anos", "30 a 39 anos", "40 a 49 anos", "50 a 59 anos", 
            "60 a 69 anos", "70 a 79 anos", "80 anos e mais", "Idade ignorada", "Total"
        ]
        if not all(col in dados_idade.columns for col in colunas_necessarias):
            print("As colunas necessárias não foram encontradas no dataset.")
            return

        faixas_etarias = colunas_necessarias[1:-1] 
        for faixa in faixas_etarias:
            dados_faixa = dados_idade[["Causa - CID-BR-10", faixa]].sort_values(by=faixa, ascending=False).head(10)
            
            plt.figure(figsize=(10, 6))
            plt.barh(dados_faixa["Causa - CID-BR-10"], dados_faixa[faixa], color='skyblue')
            plt.xlabel("Número de Mortes")
            plt.title(f"Principais Causas de Morte na Faixa Etária: {faixa}")
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.show()

    except Exception as e:
        print(f"Erro ao gerar gráficos por faixa etária: {e}")


# Função para o menu interativo em loop
def menu_interativo():
    dados = carregar_dados()

    if not dados:
        print("Erro ao carregar os dados.")
        return

    while True:
        print("\nEscolha uma opção:")
        print("1 - Gráfico de Mortes ao Longo dos Anos")
        print("2 - Gráfico de Mortes ao Longo dos Anos por Região")
        print("3 - Principais Causas de Morte por Região")
        print("4 - Gráfico de Principais Causas de Morte (Sexo Masculino)")
        print("5 - Gráfico de Principais Causas de Morte (Sexo Feminino)")
        print("6 - Gráfico de Mortes por Faixa Etária e Causa")
        print("7 - Sair")
        
        escolha = input("Digite o número da opção: ")

        if escolha == "1":
            grafico_mortes_anos(dados["Dados Temporais"])
        elif escolha == "2":
            grafico_mortes_anos_regiao(dados["Dados Temporais"])
        elif escolha == "3":
            principais_causas_mortes_por_regiao(dados["Dados Temporais"])
        elif escolha == "4":
            grafico_principais_mortes_sexo_masculino(dados["Sexo Masc 2023"])
        elif escolha == "5":
            grafico_principais_mortes_sexo_feminino(dados["Sexo Fem 2023"])
        elif escolha == "6":
            grafico_mortes_por_faixa_etaria(dados["Idade 2023"])
        elif escolha == "7":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

# Executando o menu interativo
menu_interativo()

