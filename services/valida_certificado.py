from requests import post
from constants.errors import ERROR10
from scripts.env_services import inicializa_env


env = inicializa_env()


def valida_certificado(pessoa):
    url = str(env['url_validador'])

    payload = {
        "nome": pessoa['nome'],
        "codigo": pessoa['certificado']
    }

    response = post(url, json=payload)
    resultado = (response.json())[0]
    print(resultado)

    if resultado == "Código de validação Inválido":
        raise Exception(ERROR10)  # NOSONAR
