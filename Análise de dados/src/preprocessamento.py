import os
import pandas as pd  # type: ignore
import diretorio  # type: ignore

# Processa os dados para limpeza e ajustes específicos.
def processar_dados(dados):
    dados.replace("-", pd.NA, inplace=True)

    if "Causa - CID-BR-10" in dados.columns:
        dados["Causa - CID-BR-10"] = (
            dados["Causa - CID-BR-10"]
            .str.normalize('NFKD')
            .str.encode('ASCII', errors='ignore')
            .str.decode('ASCII')
            .str.strip()
            .str.upper()
        )
        dados["Causa - CID-BR-10"] = dados["Causa - CID-BR-10"].str.replace(r"^\.*\s*", "", regex=True)

        valores_totais = []
        for causa in ["088-092", "101-103", "104-113"]:
            linha_causa = dados[dados["Causa - CID-BR-10"].str.contains(causa, regex=True)]
            if not linha_causa.empty:
                valores_totais.append(linha_causa.iloc[-1, -1])
            else:
                valores_totais.append(0)

        valor_final = sum(valores_totais)
        colunas_numericas = dados.select_dtypes(include='number')
        index_maior_valor = colunas_numericas.stack().idxmax()
        dados.at[index_maior_valor] -= valor_final

        dados = dados[
            ~dados["Causa - CID-BR-10"].str.startswith(
                tuple(f"0{i}" for i in range(88, 93)), na=False
            )
        ]
        dados = dados[
            ~dados["Causa - CID-BR-10"].str.startswith(
                tuple(str(i) for i in range(101, 114)), na=False
            )
        ]
    else:
        print("Aviso: Coluna 'Causa - CID-BR-10' não encontrada nos dados.")
    
    return dados

# Carrega, processa e salva um arquivo CSV.
def carregar_e_processar_arquivo(caminho_arquivo, descricao, diretorio_processado):
    try:
        print(f"Caminho encontrado: {caminho_arquivo}")
        dados = diretorio.carregar_arquivo(caminho_arquivo)
        if dados is not None:
            dados = processar_dados(dados)
            caminho_salvar = os.path.join(diretorio_processado, descricao)
            diretorio.salvar_arquivo(dados, caminho_salvar)
        return dados
    except FileNotFoundError:
        print(f"Erro: O arquivo '{descricao}' não foi encontrado no caminho: {caminho_arquivo}")
        return None
    except Exception as e:
        print(f"Erro ao carregar o arquivo '{descricao}': {e}")
        return None

# Carrega e processa todos os arquivos especificados.
def carregar_csv():
    arquivos = [
        ("Região/mortalidade2020.csv", "mortalidade2020.csv", "Região"),
        ("Região/mortalidade2021.csv", "mortalidade2021.csv", "Região"),
        ("Região/mortalidade2022.csv", "mortalidade2022.csv", "Região"),
        ("Região/mortalidade2023.csv", "mortalidade2023.csv", "Região"),
        ("Idade/idade2023.csv", "idade2023.csv", "Idade"),
        ("Sexo/sexoMasc2023.csv", "sexoMasc2023.csv", "Sexo"),
        ("Sexo/sexoFem2023.csv", "sexoFem2023.csv", "Sexo"),
    ]

    diretorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    diretorio_processado = os.path.join(diretorio_base, "dados", "processado")

    # Cria o diretório de processamento
    diretorio.criar_diretorio(diretorio_processado)

    # Cria subdiretórios para cada categoria
    for _, _, categoria in arquivos:
        diretorio.criar_diretorio(os.path.join(diretorio_processado, categoria))

    # Processa e salva os arquivos
    for subcaminho, descricao, categoria in arquivos:
        caminho_arquivo = os.path.join(diretorio_base, "dados", "bruto", subcaminho)
        diretorio_categoria = os.path.join(diretorio_processado, categoria)
        carregar_e_processar_arquivo(caminho_arquivo, descricao, diretorio_categoria)

# Executa o programa principal.
if __name__ == "__main__":
    carregar_csv()
