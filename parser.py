import re #Biblioteca de regex padrão do python -> serve para filtrar padrôes de texto.

#O objetivo do parser é basicamente a parte de "compilar". Ele deve ser responsavel por transformar instruções em estruturas organizadas que o codificador consiga usar
#O PARSER DEVE:
#Remover comentários, ignorar linhas vazias, detectar labels, separar instruções e operandos e gerar estrutura padronizada

#Para cada linha do .asm, o parser deve gerar algo como:
#"label": nome,
#"instrucao": "add",
#"operandos": ["$t0","$t1","$t2"]

#E para linhas com label:
#   Entrada:
#       L1: add $t0, $t1, $t2
#   Saída
#       {
#           "label": "L1",
#           "instrucao": "add",
#           "operandos": ["$t0", "$t1", "$t2"]
#       }


def removerComentarios(linha):
    return linha.split("#")[0]


def extrairLabel(linha):
    match = re.match(r"^\s*([A-Za-z_]\w*):", linha) #Ignora os espaços no início da linha, captura um label valido, seguido de :. Se encontrar o label, match vira um objeto Match. E os elementos que estão dentro do colchetes representam o conjunto de caracteres permitidos de serem capturados.
    if match:
        return match.group(1)
    return None

def removerLabel(linha): #remove a label da linha
    return re.sub(r"^\s*[A-Za-z_]\w*:\s*", "", linha)

#Função tokenizar
def tokenizar(linha): #Quebrar texto em pedaços significativos, e estes pedaços são chamados tokens
#Exemplo
#   Linha assembly: add $t0, $t1, $t2
#   Após tokenização: ["add", "$t0", "$t1", "$t2"]
#Tokenizar seria transformar texto bruto em unidades léxicas
    return re.split(r"[,\s]+", linha.strip())


def parseLinha(linha):
    #remove comentários
    linha = removerComentarios(linha)

    #Remove espaços extras
    linha = linha.strip()

    #Ignora linhas vazias
    if not linha: #Se a linha não possuir valor
        return None #Retorna nada
    
    #Extrai o label
    label = extrairLabel(linha)

    #Remove o label da linha
    linhaSemLabel = removerLabel(linha)

    #Tokeniza
    tokens = tokenizar(linhaSemLabel)

    if len(tokens) == 0 or tokens[0] == "":

        return {
            "label": label,
            "instrucao": None,
            "operandos": []
        }

    instrucao = tokens[0]

    operandos = tokens[1:]

    return {
        "label": label,
        "instrucao": instrucao,
        "operandos": operandos
    }

