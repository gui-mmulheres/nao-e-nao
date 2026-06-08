from constants.errors import ERROR9
from scripts.email_services import enviar_email, montar_mensagem


def gera_email(cnpj, email):
    try:
        headers, payload = montar_mensagem(cnpj, email)
        enviar_email(headers, payload)
    except Exception as e:
        raise Exception(ERROR9.format(erro=str(e)))  # NOSONAR
