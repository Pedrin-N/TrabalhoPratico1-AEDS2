"""
Este arquivo apenas chama as funções dos módulos locais (executar dentro da
pasta `tp1`).
"""

from glob import glob
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

try:
    import gerar_dados
    import parametros
    import organizar_blocos
    import analisar_blocos
    import resetar
except Exception as e:
    print("Erro ao importar módulos locais. Certifique-se de que os arquivos estão em 'tp1' e execute este script com Python.")
    print(e)
    sys.exit(1)


def main():
    resetar.resetar_projeto()
    
    print("=== Gerar dados ===")
    gerar_dados.gerar_dados()

    print("\n=== Parâmetros ===")
    params = parametros.perguntar_parametros()

    registros = parametros.carregar_alunos()
    if registros is None:
        print("Nenhum registro disponível para organizar. Saindo.")
        return

    print("\n=== Organizar blocos ===")
    organizar_blocos.organizar(params, registros)

    print("\n=== Análise de blocos ===")
    analisar_blocos.analisar_blocos()

if __name__ == '__main__':
    main()

