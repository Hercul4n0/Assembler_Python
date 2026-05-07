import csv

def load_cycles(nomeArquivo):
    """Transforma o conteúdo do arquivo csv em dicionario"""
    ciclos = {}

    with open(nomeArquivo) as f:
        leitor = csv.DictReader(f)
        
        for linha in leitor:
            instrucao = linha["Instrucao"].strip()  # Remove espaços extras
            # Remove espaços em branco ao redor do valor
            ciclos_instrucao = int(linha["Ciclos"].strip())
            ciclos[instrucao] = ciclos_instrucao

    return ciclos


def calcularCPI(contagemInstrucoes, tabelaCiclos):
    """Calcula o CPI médio do programa"""
    totalInstrucoes = 0
    totalCiclos = 0
    instrucoesNaoEncontradas = []

    for instrucao, quantidade in contagemInstrucoes.items():
        # Verifica se a instrução existe na tabela de ciclos
        if instrucao in tabelaCiclos:
            ciclos = tabelaCiclos[instrucao]
            totalInstrucoes += quantidade
            totalCiclos += quantidade * ciclos
        else:
            # Se a instrução não for encontrada, avisa e usa um valor padrão (1 ciclo)
            instrucoesNaoEncontradas.append(instrucao)
            # Avisa sobre instrução não encontrada (opcional)
            print(f"AVISO: Instrução '{instrucao}' não encontrada no CSV. Usando 1 ciclo como padrão.")
            totalInstrucoes += quantidade
            totalCiclos += quantidade * 1  # Valor padrão de 1 ciclo

    # Exibe instruções não encontradas se houver alguma
    if instrucoesNaoEncontradas:
        print(f"\nInstruções não encontradas no arquivo CSV: {instrucoesNaoEncontradas}")
        print("Considere adicioná-las ao arquivo ciclos.csv para um cálculo mais preciso.\n")

    # Evita divisão por zero
    if totalInstrucoes == 0:
        return 0, 0, 0
    
    cpi = totalCiclos / totalInstrucoes
    return totalInstrucoes, totalCiclos, cpi