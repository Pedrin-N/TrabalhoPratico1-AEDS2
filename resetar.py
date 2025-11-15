import glob
import os

def resetar_projeto():
    for arquivo in glob.glob("*.dat"):
        os.remove(arquivo)
    print("Todos os arquivos .dat foram removidos.\n")
