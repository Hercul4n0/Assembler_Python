#AQUI É ONDE O FILHO CHORA E A MÃE NÃO VÊ.
from registers import obterNumeroRegistrador
from instructions import INSTRUCOES
from utils import paraBinario

#Definindo funcao para codificar instruções tipo R. A função pega uma instrução do tipo R e monta os 32 bits do código de máquina
def codificarR(nome, ops):
    #EXTRAINDO OS REGISTRADORES

    info = INSTRUCOES[nome]

    opcode = info["opcode"]
    function = info["function"]

    #CASO SLL E SRL 
    #Formato: sll $1, $2, 10
    if nome == "sll" or nome == "srl":
        rd = obterNumeroRegistrador(ops[0]) #VERIFICAR COM O CHAT SE É A FUNÇÃO CERTA
        rt = obterNumeroRegistrador(ops[1])
        shamt = int(ops[2])

        rs = 0 #Sempre é 0
    
    #CASO JR
    elif nome == "jr":
        rs = obterNumeroRegistrador(ops[0])
        rt = 0
        rd = 0
        shamt = 0

    #MULT / DIV
    elif nome in ["mult", "multu", "div"]:
        rs = obterNumeroRegistrador(ops[0])
        rt = obterNumeroRegistrador(ops[1])
        rd = 0
        shamt = 0
    
    # PARA MFHI MFLO
    elif nome in ["mfhi", "mflo"]:
        rd = obterNumeroRegistrador(ops[0])
        rs = 0
        rt = 0
        shamt = 0

    #CASO NORMAL
    else:
    #ops representa os operandos da instrução no formato: ["$t0", "$s1", "$s2"]
    #Para instruções tipo R: add rd, rs, rt
    #Sendo assim:
        rd = obterNumeroRegistrador(ops[0]) 
        rs = obterNumeroRegistrador(ops[1])
        rt = obterNumeroRegistrador(ops[2])
        shamt = 0
    #Chamada da funçao (de nome autoexplicativo) para atribuir numero dos registradores as variáveis que representam os operandos

    #CAMPOS FIXOS DO FORMATO R
    #Para instruções add, sub, ect, ambos são sempre 0
    #opcode = 0
    #shamt = 0

    return(
        paraBinario(opcode, 6)+ # opcode -> 6 bits
        paraBinario(rs, 5)+ # rs -> 5 bits
        paraBinario(rt, 5)+ # rt -> 5 bits
        paraBinario(rd, 5)+ # rd -> 5 bits
        paraBinario(shamt, 5)+ # shamt -> 5 bits
        paraBinario(function, 6) #function -> 6 bits
    )

#PARA INSTRUCOES DO TIPO I
def codificarI(nome, ops, tabelaLabels, enderecoAtual):
    #Esta função basicamente transforma instrucoes tipo I em 32 bits binarios
    #OBTEM INFORMACOES DA INSTRUCAO

    #Busca na tabela opcode e tipo

    info = INSTRUCOES[nome]
    opcode = info["opcode"] #Busca opcode em info que recebe INSTRUCOES

    # CASO 1: INSTRUCAO ADDI
    if nome in ["addi", "addiu", "andi", "ori", "slti"]:
    
        rt = obterNumeroRegistrador(ops[0])
        rs = obterNumeroRegistrador(ops[1])
        imediato = int(ops[2])


    #CASO 2: SE FOR UMA INSTRUCAO BEQ (BRANCH)
    elif nome == "beq":
        #Formato: beq rs, rt, label
        #Ex: beq $t0, $t1, L1
        #Labels são nomes que marcam uma posição no código. Um label registra uma posição de código em um endereço de memória, e esse endereço permite saltos no código

        #Obtendo numero dos registadores
        rs = obterNumeroRegistrador(ops[0])
        rt = obterNumeroRegistrador(ops[1])

        #Nome do label
        label = ops[2]  #ln 62* (terceira posicao)

        enderecoLabel = tabelaLabels[label] #Busca o endereco do label na tabela de símbolos. Ex: L1 -> 0x00400000

        #CALCULO DO OFFSET (MUITO IMPORTANTE)
        #O offset representa de forma grosseira quantas instrucoes o endereco atual do PC precisa pular até chegar no endereço do Label (em número de instrucoes). Isso acontece pq o MIPS usa endereçamento relativo ao pc
        #FORMULA: offset = (enderecoLabel - (PC + 4)) / 4
        #PC é o enderecoAtual
        #Cada instrucao possui 4 bytes -> divide por 4

        imediato = (enderecoLabel - (enderecoAtual + 4))//4
    elif nome in ["lw", "sw"]:
        rt = obterNumeroRegistrador(ops[0])
        #print("DEBUG LW/SW:", ops)
        offset, resto = ops[1].split("(")
        rs = obterNumeroRegistrador(resto.replace(")", ""))

        imediato = int(offset)

    elif nome == "bne":

        rs = obterNumeroRegistrador(ops[0])
        rt = obterNumeroRegistrador(ops[1])

        label = ops[2]
        enderecoLabel = tabelaLabels[label]

        imediato = (enderecoLabel - (enderecoAtual + 4))//4

    elif nome == "lui":
        rt = obterNumeroRegistrador(ops[0])
        rs = 0
        imediato = int(ops[1])






    #MONTAGEM DO CODIGO BINARIO
    #Formato I (32 bits):
    #opcode (6 bits)
    # rs (5 bits)
    # rt (5 bits)
    # imm (16 bits)
    # total = 32 bits
    return (
        #opcode -> 6 bits
        paraBinario(opcode, 6)+

        #rs -> 5 bits
        paraBinario(rs, 5)+

        #rt - > 5 bits
        paraBinario(rt, 5)+

        #imediato -> 16 bits
        #"& 0xFFFF" vai garantir que o valor permaneça em 16 bits (importante para valores negaticos)
        paraBinario(imediato & 0xFFFF, 16)
    )

#PARA INSTRUCOES TIPO J
def codificarJ(nome, ops, tabelaLabels):
    #Instruções tipo j são instruções que permitem saltos no código.
    #Ex: j L1 -> Vá para o endereço marcado por L1

    #OBTER O OPCODE
    #eX:J -> 2
    opcode = INSTRUCOES[nome]["opcode"]

    #OBTER O LABEL
    #Ex: ["L2"] -> L2
    label = ops[0]

    # DEBUG (TEMPORÁRIO)
    #print("LABEL:", label)
    #print("ENDERECO ORIGINAL:", hex(tabelaLabels[label]))

    #BUSCA O ENDERECO REAL DO LABEL
    #Ex: L2 -> 0x00400004
    endereco = tabelaLabels[label]


    # AJUSTE PARA FORMATO J (26 BITS)

    #No MIPS:
    #Os dois bits menos significativos sempre sao zero, então não são armazenados. Por isso, desloca 2 bits a direita (divide por 4)

    endereco = (endereco >> 2) & 0x03FFFFFF #Desloca o valor de endereco 2 bits pra direita (CONSERTADO)

#   DEBUG (TEMPORÁRIO)
    #print("ENDERECO SHIFTADO:", hex(endereco))
    #print("BINARIO:", paraBinario(endereco, 26))

    #MONTAGEM DO BINARIO
    #FORMATO J
    #Opcode 6 bits
    #endereco 26 bits

    binOpcode = paraBinario(opcode, 6)
    binEndereco = paraBinario(endereco, 26)

# DEBUG
    #print("VALOR FINAL:", endereco)
    #print("BINARIO DIRETO:", bin(endereco))
    #print("FORMAT:", format(endereco, "026b"))
    #print("BIN ENDERECO (sua funcao):", binEndereco)

    return binOpcode + binEndereco

def codificar(instrucao, tabelaLabels, enderecoAtual):

    nome = instrucao["instrucao"]
    operandos = instrucao["operandos"]

    tipo = INSTRUCOES[nome]["tipo"]


    if tipo == "R":
        return codificarR(nome, operandos)
    elif tipo == "I":
        return codificarI(nome, operandos, tabelaLabels, enderecoAtual)
    elif tipo == "J":
        return codificarJ(nome, operandos, tabelaLabels)