import os
import json
import pickle


def carregar_alunos(path='alunos.dat'):
    if not os.path.exists(path):
        print(f"Aviso: '{path}' não existe no diretório atual.")
        return None
    try:
        with open(path, 'rb') as f:
            dados = pickle.load(f)
        return dados
    except Exception as e:
        print(f"Erro ao carregar '{path}': {e}")
        return None


def perguntar_parametros():
    while True:
        try:
            tamanho_bloco = int(input("Qual tamanho máximo do bloco em bytes? "))
            if tamanho_bloco <= 0:
                print("Forneça um inteiro positivo.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Digite um inteiro (ex.: 1024).")

    tipo = None
    while tipo not in ('1', '2'):
        tipo = input("Tipo de registro — digite 1 para 'fixo' ou 2 para 'variável': ").strip()
    tipo_registro = 'fixo' if tipo == '1' else 'variavel'

    params = {
        'tamanho_bloco_bytes': tamanho_bloco,
        'tipo_registro': tipo_registro,
    }

    if tipo_registro == 'fixo':
        while True:
            try:
                tamanho_registro = int(input("Qual o tamanho do registro fixo em bytes? "))
                if tamanho_registro <= 0:
                    print("Forneça um inteiro positivo.")
                    continue
                params['tamanho_registro_bytes'] = tamanho_registro
                break
            except ValueError:
                print("Entrada inválida. Digite um inteiro (ex.: 128).")
    else:
        esp = None
        while esp not in ('s', 'n'):
            esp = input("Haverá espalhamento (overflow)? (s/n): ").strip().lower()
        params['espalhamento'] = True if esp == 's' else False

    with open('parametros.json', 'w', encoding='utf-8') as out:
        json.dump(params, out, ensure_ascii=False, indent=2)

    print("Parâmetros gravados em 'parametros.json':")
    print(json.dumps(params, ensure_ascii=False, indent=2))
    return params


if __name__ == '__main__':
    dados = carregar_alunos()
    if isinstance(dados, list):
        print(f"Arquivo 'alunos.dat' carregado: {len(dados)} registros encontrados.")
    elif dados is not None:
        print(f"Arquivo 'alunos.dat' carregado: tipo = {type(dados)}")

    perguntar_parametros()