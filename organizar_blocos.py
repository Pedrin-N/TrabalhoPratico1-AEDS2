import os
import json
import pickle
from pprint import pprint


def load_json(path='parametros.json'):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo de parâmetros '{path}' não encontrado.")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_alunos(path='alunos.dat'):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo de dados '{path}' não encontrado.")
    with open(path, 'rb') as f:
        return pickle.load(f)


def calcular_tamanho_bloco(registros):
    """Calcula tamanho em bytes de uma lista de registros quando serializada."""
    return len(pickle.dumps(registros))


def organizar(params, registros):
    bloco_size = params['tamanho_bloco_bytes']
    tipo = params.get('tipo_registro', 'variavel')

    os.makedirs('.', exist_ok=True)

    if tipo == 'fixo':
        rec_size = params.get('tamanho_registro_bytes')
        if not rec_size or rec_size <= 0:
            raise ValueError('tamanho_registro_bytes deve ser um inteiro positivo para registros fixos')
        per_block = bloco_size // rec_size
        if per_block <= 0:
            print(f"Atenção: o tamanho do registro ({rec_size} bytes) é maior que o tamanho do bloco ({bloco_size} bytes). Cada registro será gravado em bloco separado.")
            per_block = 1

        blocks = [registros[i:i+per_block] for i in range(0, len(registros), per_block)]

    else:
        espalhamento = params.get('espalhamento', False)
        blocks = []
        cur_block = []
        idx = 0

        while idx < len(registros):
            rec = registros[idx]
            test_block = cur_block + [rec]
            bloco_bytes = calcular_tamanho_bloco(test_block)

            if bloco_bytes <= bloco_size:
                cur_block = test_block
                idx += 1
            else:
                if not cur_block:
                    if not espalhamento:
                        print(f"Aviso: registro isolado com {bloco_bytes} bytes excede tamanho do bloco ({bloco_size} bytes). Gravando em bloco separado.")
                    blocks.append([rec])
                    idx += 1
                else:
                    if espalhamento and len(cur_block) < 2:
                        blocks.append(test_block)
                        idx += 1
                        cur_block = []
                    else:
                        blocks.append(cur_block)
                        cur_block = []

        if cur_block:
            blocks.append(cur_block)

    for idx, bloco in enumerate(blocks, start=1):
        path = f"bloco_{idx}.dat"
        with open(path, 'wb') as out:
            pickle.dump(bloco, out)

    report = {
        'num_registros': len(registros),
        'num_blocos': len(blocks),
        'tamanho_bloco_bytes': bloco_size,
        'tipo_registro': tipo,
    }
    print("Organização concluída:")
    pprint(report)
    return report


def main():
    params = load_json('parametros.json')
    registros = load_alunos('alunos.dat')
    if not isinstance(registros, list):
        print("Formato inesperado em 'alunos.dat' — esperado uma lista de registros.")
        return

    organizar(params, registros)


if __name__ == '__main__':
    main()
