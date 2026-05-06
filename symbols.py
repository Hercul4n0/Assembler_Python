def construirTabelaLabels(instrucoes):
    ENDERECO_INICIAL = 0x00400000 #DEFININDO ENDERECO INICIAL PRA SER UTILIZADO

    
    #INICIA UM DICIONARIO VAZIO PRA TABELA DE LABELS
    tabelaLabels = {}

    #DEFINE POR ORA QUE O ENDERECO ATUAL É IGUAL AO INICIAL
    enderecoAtual = ENDERECO_INICIAL

    #PARA CADA INSTRUÇÃO EM INSTRUÇÕES:
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