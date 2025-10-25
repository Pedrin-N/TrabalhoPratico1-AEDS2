from faker import Faker
from faker.providers import BaseProvider
from faker.providers import DynamicProvider

fake = Faker('pt_BR')

fake.bothify()
# ##matricula
# print(fake.unique.bothify(text='##.#.####'))
# ##nome
# print(fake.name())
# ##cpf
# print(fake.unique.bothify(text='###.###.###-##'))

nome_do_curso_provider = DynamicProvider (
    provider_name="curso",
    elements=["SJM","CJM", "ENP"],
)

fake.add_provider(nome_do_curso_provider)
# #curso
# print(fake.curso())
  
# ##nome mae
# print(fake.name_female())

# ##nome pai
# print(fake.name_male())
  
# #ano de ingresso
# print(fake.random_int(min=2000, max=2025))

# #CA
# print(fake.bothify(text='#,##'))    

import pickle
import os.path

quant = int(input("Defina o número total de registros a serem gerados: "))
# Gerar lista de registros falsos
alunos = []
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

# Gravar os registros em um arquivo binário (.dat)
with open("alunos.dat", "wb") as arquivo:
    pickle.dump(alunos, arquivo)

print("Registros salvos com sucesso em 'pessoas.dat' ✅")

file_path = r'./alunos.dat'

sz = os.path.getsize(file_path)
print(f'The {file_path} size is', sz, 'bytes')