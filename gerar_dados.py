from faker import Faker
from faker.providers import DynamicProvider
import pickle
from pprint import pprint


fake = Faker('pt_BR')

nome_do_curso_provider = DynamicProvider(
    provider_name="curso",
    elements=["SJM", "CJM", "ENP"],
)
fake.add_provider(nome_do_curso_provider)


def gerar_dados():
    alunos = []
    quant = int(input("Defina o número total de registros a serem gerados: "))
    for _ in range(quant):
        pessoa = {
            "matricula": fake.unique.bothify(text='##.#.####'),
            "nome": fake.name(),
            "cpf": fake.unique.bothify(text='###.###.###-##'),
            "curso": fake.curso(),
            "nome_da_mae": fake.name_female(),
            "nome_do_pai": fake.name_male(),
            "ano_de_ingresso": fake.random_int(min=2000, max=2025),
            "ca": fake.bothify(text='#,##')
        }
        alunos.append(pessoa)

    with open("alunos.dat", "wb") as arquivo:
        pickle.dump(alunos, arquivo)
    print("Registros salvos com sucesso em 'alunos.dat'")

    dez_primeiros = int(input("Você deseja visualizar os 10 primeiros registros? (1 - Sim, 0 - Não) "))
    if dez_primeiros == 1:
        pprint(alunos[:10])
    else: 
        pass

if __name__ == "__main__":
    gerar_dados()   