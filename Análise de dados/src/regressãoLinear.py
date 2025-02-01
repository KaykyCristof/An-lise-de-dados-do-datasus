import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
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

# Função para corrigir inconsistências no dataset
def corrigir_inconsistencias(df):
    df.columns = df.columns.str.strip()
    df.fillna(0, inplace=True)

    colunas_numericas = df.columns[1:-2] 
    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0)
    df.rename(columns={
        "Causa - CID-BR-10": "Causa",
        "1 Região Norte": "Região Norte",
        "2 Região Nordeste": "Região Nordeste",
        "3 Região Sudeste": "Região Sudeste",
        "4 Região Sul": "Região Sul",
        "5 Região Centro-Oeste": "Região Centro-Oeste",
        "Total": "Total Geral",
        "Ano": "Ano"
    }, inplace=True)

    df.drop_duplicates(inplace=True)

    return df

# Função para carregar e corrigir o dataset
def carregar_e_corrigir_dados():
    dados = carregar_dataset("dados_temporais.csv", "Região")
    if dados is not None:
        dados_corrigidos = corrigir_inconsistencias(dados)
        dados_agrupados = dados_corrigidos.groupby('Ano').sum().reset_index()
        dados_agrupados['Total Geral'] = np.log1p(dados_agrupados['Total Geral'])  # log(1+x)
        return dados_agrupados[['Ano', 'Total Geral']]
    else:
        print("Erro ao carregar o dataset.")
        return None

# Função para construir o modelo de regressão linear
def construir_modelo_regressao(df):
    X = df[['Ano']].values 
    y = df['Total Geral'].values 

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo_linear = LinearRegression()
    modelo_linear.fit(X_train, y_train)

    y_pred_linear = modelo_linear.predict(X_test)

    mse_linear = mean_squared_error(y_test, y_pred_linear)
    r2_linear = r2_score(y_test, y_pred_linear)

    print(f"Erro Quadrático Médio (MSE - Linear): {mse_linear:.2f}")
    print(f"Coeficiente de Determinação (R² - Linear): {r2_linear:.2f}")

    anos_futuros = np.array([[2024], [2025], [2026], [2027]])
    previsoes_futuras_linear = modelo_linear.predict(anos_futuros)

    for ano, previsao_linear in zip(anos_futuros.flatten(), previsoes_futuras_linear):
        print(f"Previsão para o ano {ano} (Linear): {np.expm1(previsao_linear):.0f} mortes")

    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', alpha=0.6, label='Dados Reais')
    
    anos_completos = np.vstack((X, anos_futuros)) 
    plt.plot(anos_completos, modelo_linear.predict(anos_completos), color='red', linewidth=2, label='Regressão Linear')

    plt.xlabel('Ano')
    plt.ylabel('Total de Mortes')
    plt.title('Regressão Linear para Previsão de Mortes Totais por Ano')
    plt.legend()
    plt.grid(True)
    plt.show()

    return modelo_linear

# Exemplo de uso das funções
if __name__ == "__main__":
    dataset_corrigido = carregar_e_corrigir_dados()
    if dataset_corrigido is not None:
        print("Dataset corrigido e agregado com sucesso!")
        print(dataset_corrigido.head())
        modelo_linear = construir_modelo_regressao(dataset_corrigido)
