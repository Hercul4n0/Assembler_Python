ENDERECO_INICIAL = 0x00400000


def construirTabelaLabels(instrucoes):

    tabelaLabels = {}

    enderecoAtual = ENDERECO_INICIAL


    for instrucao in instrucoes:

        # Ignora linhas vazias
        if instrucao is None:
            continue


        label = instrucao["label"]


        # Se existir label, salva endereço
        if label is not None:

            tabelaLabels[label] = enderecoAtual


        # Labels sozinhas NÃO ocupam memória
        #
        # Só incrementa se houver instrução
        #
        if instrucao["instrucao"] is not None:

            enderecoAtual += 4


    return tabelaLabels