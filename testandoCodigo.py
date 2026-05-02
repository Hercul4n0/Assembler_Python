from parser import parseLinha


linhas = [

    "add $t0, $t1, $t2",

    "loop: sub $s0, $s1, $s2",

    "j fim # salto",

    "",

    "fim:"
]


for linha in linhas:

    resultado = parseLinha(linha)

    print(resultado)