import csv #Serve para leitura de arquivos csv, coisa que o trabalho exige. É necessário ler a instrução, ler a quantidade de ciclos e calcular o CPI

#print(sys.argv) # sys.argv é uma lista com os parâmetros de texto recebidos pelo sys do prompt. Ele exibe a lista de parametros separados por espaçamento

def load_cycles(nomeArquivo): #Transforma o conteúdo do arquivo csv em dicionario

    #nomeArquivo = sys.argv[1]

    ciclos = {} #Cria um dicionário vazio 


    with open(nomeArquivo) as f: #Instrução para operar e ler arquivos sem se preocupar com fechamento
        leitor = csv.DictReader(f) #Usa dict reader para atribuir um iterador de dicionarios em leitor, tornando o resultado mais legível

        for linha in leitor: #Percorre cada linha do arquivo ciclos.csv
            instrucao = linha["Instrucao"] #Obtém o nome da instrução

            ciclos_instrucao = int(linha["Ciclos"]) #Obtém a quantidade de ciclos ao passar por cada linha lendo o conteúdo do cabeçalho Ciclos 
            #int() converte String para inteiro

            ciclos[instrucao] = ciclos_instrucao #Armazena no dicionário:
            #Chave -> nome da instrução
            #valor -> quantidade de ciclos 
            #Ex: Instrucao: add e Ciclos: 1
            #ciclos["add"] = 1
            # Armazena add: 1 em Ciclos (ln 8)

            #Exibe os valores lidos no csv:
            #print(linha["Instrucao"], linha["Ciclos"])

            #Dicionarios serão muito usados para listar os registradores e "opcodes"
    return ciclos
        