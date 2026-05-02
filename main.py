import sys #Serve para interagir com o sistema operacional e com os argumentos na linha de comando
from cpi import load_cycles

def main():
    nomeArquivo = sys.argv[1]
    ciclos = load_cycles(nomeArquivo)


if __name__ == "__main__":
    main()