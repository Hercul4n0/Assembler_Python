import sys

# Importa a função responsável por analisar cada linha do assembly
# e transformá-la em uma estrutura organizada
from parser import parseLinha

# Importa a função responsável por construir a tabela de labels
# (tabela de símbolos)
from symbols import construirTabelaLabels

# Importa a função responsável por ler o arquivo CSV contendo
# a quantidade de ciclos de cada instrução
from cpi import load_cycles

from encoder import codificar #Chama a função para codificar instruções


def main():

    # VERIFICACAO DOS ARGUMENTOS DA LINHA DE COMANDO

    # sys.argv guarda os parâmetros passados pelo terminal
    #
    # Exemplo: python main.py teste.asm -b
    #
    # sys.argv vira:
    #
    # [
    #   "main.py",
    #   "teste.asm",
    #   "-b"
    # ]
    #
    # Portanto:
    #
    # sys.argv[1] -> nome do arquivo ASM
    # sys.argv[2] -> formato de saída
    #
    # Se o usuário não fornecer os parâmetros necessários,
    # o programa exibe mensagem de uso e encerra.
    #
    if len(sys.argv) < 3:

        print("Uso: python main.py <arquivo.asm> <-b|-h>")

        return


    # Obtém o nome do arquivo assembly passado pelo usuário
    #
    # Exemplo:
    # teste.asm
    #
    nomeArquivo = sys.argv[1]


    # Obtém o formato de saída
    #
    # -b -> saída binária
    # -h -> saída hexadecimal
    #
    formatoSaida = sys.argv[2]


    # ==========================================================
    # EXIBICAO DOS PARAMETROS RECEBIDOS
    # ==========================================================

    print("\n=== PARAMETROS RECEBIDOS ===\n")

    print("Arquivo ASM:", nomeArquivo)

    print("Formato de saída:", formatoSaida)


    # ==========================================================
    # LEITURA DO ARQUIVO ASM
    # ==========================================================

    # Lista que armazenará todas as instruções parseadas
    #
    # Cada elemento da lista será um dicionário como:
    #
    # {
    #     "label": "L1",
    #     "instrucao": "add",
    #     "operandos": ["$t0", "$t1", "$t2"]
    # }
    #
    instrucoes = []


    # Abre o arquivo assembly informado pelo usuário
    #
    # "arquivo" passa a representar o arquivo aberto
    #
    with open(nomeArquivo) as arquivo:


        # Percorre cada linha do arquivo
        #
        for linha in arquivo:


            # Envia a linha para o parser
            #
            # O parser:
            # - remove comentários
            # - identifica labels
            # - separa instrução e operandos
            #
            estrutura = parseLinha(linha)


            # Ignora linhas vazias
            #
            # O parser retorna None quando a linha está vazia
            #
            if estrutura is not None:


                # Adiciona a estrutura parseada na lista
                #
                # append() adiciona um elemento ao final da lista
                #
                instrucoes.append(estrutura)


    # ==========================================================
    # EXIBICAO DA SAIDA DO PARSER
    # ==========================================================

    # Exibe todas as estruturas produzidas pelo parser
    #
    # Isso serve para validar:
    # - tokenização
    # - labels
    # - operandos
    #
    print("\n=== SAIDA DO PARSER ===\n")


    # Percorre todas as instruções parseadas
    #
    for instrucao in instrucoes:


        # Exibe a estrutura gerada pelo parser
        #
        print(instrucao)


    # ==========================================================
    # CONSTRUCAO DA TABELA DE LABELS
    # ==========================================================

    # Constrói a tabela de símbolos do programa
    #
    # Exemplo:
    #
    # {
    #     "L1": 0x00400000,
    #     "L2": 0x00400004
    # }
    #
    tabelaLabels = construirTabelaLabels(instrucoes)


    # ==========================================================
    # EXIBICAO DA TABELA DE LABELS
    # ==========================================================

    print("\n=== TABELA DE LABELS ===\n")


    # items() percorre:
    # chave -> valor
    #
    # Nesse caso:
    # label -> endereço
    #
    for label, endereco in tabelaLabels.items():


        # hex() converte o inteiro para hexadecimal
        #
        print(label, hex(endereco))


    # ==========================================================
    # LEITURA DO CSV DE CICLOS
    # ==========================================================

    # Lê o arquivo ciclos.csv e gera um dicionário:
    #
    # {
    #     "add": 1,
    #     "sub": 1,
    #     "mult": 32
    # }
    #
    tabelaCiclos = load_cycles("ciclos.csv")


    # ==========================================================
    # EXIBICAO DA TABELA DE CICLOS
    # ==========================================================

    print("\n=== TABELA DE CICLOS ===\n")


    # Percorre todas as instruções da tabela
    #
    for instrucao, ciclos in tabelaCiclos.items():


        # Exibe:
        # instrução -> ciclos
        #
        print(instrucao, ciclos)


    # ==========================================================
    # CONTAGEM DAS INSTRUCOES UTILIZADAS
    # ==========================================================

    # Dicionário responsável por contar quantas vezes
    # cada instrução aparece no programa
    #
    contagemInstrucoes = {}


    # Percorre todas as instruções parseadas
    #
    for instrucao in instrucoes:


        # Obtém o nome da instrução
        #
        # Ex:
        # add
        # sub
        # beq
        #
        nomeInstrucao = instrucao["instrucao"]


        # Ignora labels sem instrução
        #
        # Exemplo:
        #
        # loop:
        #
        if nomeInstrucao is None:

            continue


        # Se a instrução ainda não estiver no dicionário,
        # inicializa a contagem com zero
        #
        if nomeInstrucao not in contagemInstrucoes:

            contagemInstrucoes[nomeInstrucao] = 0


        # Incrementa a quantidade de ocorrências
        #
        contagemInstrucoes[nomeInstrucao] += 1


    # ==========================================================
    # EXIBICAO DA QUANTIDADE DE INSTRUCOES
    # ==========================================================

    print("\n=== QUANTIDADE DE INSTRUCOES ===\n")


    # Percorre o dicionário de contagem
    #
    for instrucao, quantidade in contagemInstrucoes.items():


        # Exibe:
        #
        # add: 5
        # sub: 2
        #
        print(instrucao + ":", quantidade)

    #CODIFICACAO NA MAIN
    from encoder import codificar

    print("\n=== CODIGO DE MAQUINA ===\n")

    ENDERECO_INICIAL = 0x00400000
    enderecoAtual = ENDERECO_INICIAL

    codigoMaquina = []

    for instrucao in instrucoes:

        if instrucao["instrucao"] is None:
            continue

        binario = codificar(instrucao, tabelaLabels, enderecoAtual)

        codigoMaquina.append(binario)

        print(binario)

        enderecoAtual += 4
# ==============================================================
# PONTO DE ENTRADA DO PROGRAMA
# ==============================================================

# Verifica se o arquivo atual está sendo executado diretamente
#
# Se verdadeiro:
# executa a função main()
#
if __name__ == "__main__":
    main()
