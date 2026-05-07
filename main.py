import sys

# Importa a função responsável por analisar cada linha do assembly
# e transformá-la em uma estrutura organizada
from parser import parseLinha

# Importa a função responsável por construir a tabela de labels
# (tabela de símbolos)
from symbols import construirTabelaLabels

# Importa a função responsável por ler o arquivo CSV contendo
# a quantidade de ciclos de cada instrução
from cpi import load_cycles, calcularCPI

from encoder import codificar  # Chama a função para codificar instruções


def binario_para_hexadecimal(binario_str):
    """Converte uma string binária de 32 bits para hexadecimal (8 caracteres)"""
    return format(int(binario_str, 2), '08x')


def main():
    # VERIFICACAO DOS ARGUMENTOS DA LINHA DE COMANDO
    if len(sys.argv) < 3:
        print("Uso: python main.py <arquivo.asm> <-b|-h>")
        return

    # Obtém o nome do arquivo assembly passado pelo usuário
    nomeArquivo = sys.argv[1]

    # Obtém o formato de saída
    formatoSaida = sys.argv[2]

    # Valida o formato de saída
    if formatoSaida not in ["-b", "-h"]:
        print("Formato inválido. Use -b para binário ou -h para hexadecimal.")
        return

    # Define o nome do arquivo de saída (mesmo nome, extensão diferente)
    if formatoSaida == "-b":
        nomeArquivoSaida = nomeArquivo.replace(".asm", ".bin")
    else:  # formatoSaida == "-h"
        nomeArquivoSaida = nomeArquivo.replace(".asm", ".hex")

    # ==========================================================
    # EXIBICAO DOS PARAMETROS RECEBIDOS
    # ==========================================================
    print("\n=== PARAMETROS RECEBIDOS ===\n")
    print("Arquivo ASM:", nomeArquivo)
    print("Formato de saída:", formatoSaida)
    print("Arquivo de saída:", nomeArquivoSaida)

    # ==========================================================
    # LEITURA DO ARQUIVO ASM
    # ==========================================================
    instrucoes = []

    with open(nomeArquivo) as arquivo:
        for linha in arquivo:
            estrutura = parseLinha(linha)

            if estrutura is not None:
                instrucoes.append(estrutura)

    # ==========================================================
    # EXIBICAO DA SAIDA DO PARSER
    # ==========================================================
    #print("\n=== SAIDA DO PARSER ===\n")
    #for instrucao in instrucoes:
    #    print(instrucao)

    # ==========================================================
    # CONSTRUCAO DA TABELA DE LABELS
    # ==========================================================
    tabelaLabels = construirTabelaLabels(instrucoes)

    print("\n=== TABELA DE LABELS ===\n")
    for label, endereco in tabelaLabels.items():
        print(label, hex(endereco))

    # ==========================================================
    # LEITURA DO CSV DE CICLOS
    # ==========================================================
    tabelaCiclos = load_cycles("ciclos.csv")

    print("\n=== TABELA DE CICLOS ===\n")
    for instrucao, ciclos in tabelaCiclos.items():
        print(instrucao, ciclos)

    # ==========================================================
    # CONTAGEM DAS INSTRUCOES UTILIZADAS
    # ==========================================================
    contagemInstrucoes = {}

    for instrucao in instrucoes:
        nomeInstrucao = instrucao["instrucao"]

        if nomeInstrucao is None:
            continue

        if nomeInstrucao not in contagemInstrucoes:
            contagemInstrucoes[nomeInstrucao] = 0

        contagemInstrucoes[nomeInstrucao] += 1

    print("\n=== QUANTIDADE DE INSTRUCOES ===\n")
    for instrucao, quantidade in contagemInstrucoes.items():
        print(instrucao + ":", quantidade)

    # ==========================================================
    # CODIFICACAO E GERACAO DO ARQUIVO DE SAIDA
    # ==========================================================
    ENDERECO_INICIAL = 0x00400000
    enderecoAtual = ENDERECO_INICIAL

    codigoMaquinaBinario = []  # Lista para armazenar as instruções em binário
    codigoMaquinaHex = []      # Lista para armazenar as instruções em hexadecimal

    #print("\n=== CODIGO DE MAQUINA ===\n")

    for instrucao in instrucoes:
        if instrucao["instrucao"] is None:
            continue

        binario = codificar(instrucao, tabelaLabels, enderecoAtual)
        hexa = binario_para_hexadecimal(binario)

        codigoMaquinaBinario.append(binario)
        codigoMaquinaHex.append(hexa)

        # Exibe na tela no formato escolhido
        #if formatoSaida == "-b":
        #    print(binario)
        #else:
        #    print(hexa)

        enderecoAtual += 4

    # ==========================================================
    # ESCRITA DO ARQUIVO DE SAIDA
    # ==========================================================
    with open(nomeArquivoSaida, 'w') as arquivo_saida:
        if formatoSaida == "-h":
            # Formato hexadecimal com cabeçalho exigido pelo Logisim
            arquivo_saida.write("v2.0 raw\n")
            for linha in codigoMaquinaHex:
                arquivo_saida.write(linha + "\n")
        else:  # formatoSaida == "-b"
            # Formato binário puro (um 0/1 por caractere)
            for linha in codigoMaquinaBinario:
                arquivo_saida.write(linha + "\n")

    #print(f"\n=== ARQUIVO GERADO COM SUCESSO: {nomeArquivoSaida} ===\n")

    # ==========================================================
    # CALCULO DO CPI MEDIO
    # ==========================================================
    totalInstrucoes, totalCiclos, cpi = calcularCPI(contagemInstrucoes, tabelaCiclos)

    print("\n=== CPI MEDIO ===\n")
    print(f"Total de instruções: {totalInstrucoes}")
    print(f"Total de ciclos: {totalCiclos}")
    print(f"CPI médio: {cpi:.2f}")


if __name__ == "__main__":
    main()
