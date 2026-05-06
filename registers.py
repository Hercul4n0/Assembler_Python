REGISTRADORES = {

    "$zero": 0,

    "$t0": 8,
    "$t1": 9,
    "$t2": 10,
    "$t3": 11,
    "$t4": 12,
    "$t5": 13,
    "$t6": 14,
    "$t7": 15,

    "$s0": 16,
    "$s1": 17,
    "$s2": 18,
    "$s3": 19,
    "$s4": 20,
    "$s5": 21,
    "$s6": 22,
    "$s7": 23
}

def obterNumeroRegistrador(registrador):

    #Caso 1: Formato numérico -> $16
    if registrador[1:].isdigit(): #Usa isdigit para verificar se todo caractere em uma string é um digito e se a string não é vazia
        return int(registrador[1:]) #Usa "fatiamento" para ir do item 1 até o final da lista de strings. Retorna o valor da variavel registrador no formato inteiro a partir do segundo caractere.
        # Ex: $16 -> Pula $ e retorna 16 inteiro
    
    #Caso 2: Formato simbólico -> $t0
    if registrador in REGISTRADORES: #Verifica se o registrador está contido no dicionario de registradores
        return REGISTRADORES[registrador] #Se estiver, retorna o valor correspondente
    
    #Caso inválido
    raise ValueError(f"Registrador inválido: {registrador}") #Mostra que o registrador inserido não consta como um registrador válido, pois Não está presente em REGISTRADORES

    #Isso é importante pois o encoder precisará gerar rs, rt, rd -> 5 bits.
    #Exemplo: add $t0, $s1, $s2
    #$t0 -> 8 -> 01000
    #$s1 -> 17 -> 10001
    #s2 -> 18 -> 10010

    #ESTA BIBLIOTECA VAI RESOLVER O PROBLEMA DE OBTER O NUMERO DO REGISTRADOR A PARTIR DE UM ARQUIVO ASSEMBLY