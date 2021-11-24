from os import path

def verifica (func):
    if path.isdir("/home/jonnas/Documentos/lead-mentoring/.git"):
        func()
    else:
        print('Não existe repositório git')

@verifica
def confirma_repositorio():
    print('Existe um repositório git')
