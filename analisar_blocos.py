import os
import json
import pickle
import glob
from typing import List, Dict, Tuple


def carregar_parametros(path='parametros.json') -> Dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo '{path}' não encontrado. Execute parametros.py primeiro.")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def encontrar_blocos() -> List[str]:
    blocos = glob.glob('bloco_*.dat')
    if not blocos:
        raise FileNotFoundError("Nenhum arquivo bloco_*.dat encontrado. Execute organizar_blocos.py primeiro.")
    return sorted(blocos, key=lambda x: int(x.split('_')[1].split('.')[0]))


def calcular_tamanho_real(registros: List) -> int:
    return len(pickle.dumps(registros))


def analisar_blocos():
    params = carregar_parametros()
    blocos = encontrar_blocos()
    tamanho_maximo = params['tamanho_bloco_bytes']
    
    total_bytes_uteis = 0
    total_bytes_alocados = 0
    blocos_parciais = 0
    ocupacao = []
    
    print("\nMapa de ocupação dos blocos:")
    print("-" * 80)

    BAR_WIDTH = 40

    for bloco_path in blocos:
        with open(bloco_path, 'rb') as f:
            registros = pickle.load(f)
            bytes_usados = calcular_tamanho_real(registros)

        percentual = (bytes_usados / tamanho_maximo) * 100
        ocupacao.append(percentual)
        total_bytes_uteis += bytes_usados
        total_bytes_alocados += tamanho_maximo

        if bytes_usados < tamanho_maximo:
            blocos_parciais += 1

        try:
            bloco_num = int(os.path.splitext(bloco_path)[0].split('_')[1])
        except Exception:
            bloco_num = bloco_path

        filled = int(min(percentual, 100.0) / 100.0 * BAR_WIDTH)
        empty = BAR_WIDTH - filled
        bar = '█' * filled + ' ' * empty
        overflow_note = ''
        if percentual > 100:
            overflow_note = f' (+{percentual-100:.1f}% overflow)'

        print(f"Bloco {bloco_num:>3}: {bytes_usados:>6} bytes |{bar}| {percentual:6.1f}%{overflow_note}")
    
    ocupacao_media = sum(ocupacao) / len(ocupacao) if ocupacao else 0.0
    eficiencia = (total_bytes_uteis / total_bytes_alocados) * 100 if total_bytes_alocados else 0.0

    print("\nResumo do armazenamento:")
    print("-" * 80)
    print(f"{'Total de blocos:':<35}{len(blocos):>10}")
    print(f"{'Blocos parcialmente utilizados:':<35}{blocos_parciais:>10}")
    print(f"{'Percentual médio de ocupação:':<35}{ocupacao_media:>9.1f} %")
    print(f"{'Eficiência de armazenamento:':<35}{eficiencia:>9.1f} %")
    print(f"{'Total bytes úteis:':<35}{total_bytes_uteis:>10,} bytes")
    print(f"{'Total bytes alocados:':<35}{total_bytes_alocados:>10,} bytes")


if __name__ == '__main__':
    try:
        analisar_blocos()
    except Exception as e:
        print(f"Erro: {e}")