from scripts.email_services import enviar_email, montar_mensagem


def gera_email(cnpj, email):
    try:
        headers, payload = montar_mensagem(cnpj, email)
        enviar_email(headers, payload)
    except Exception as e:
        raise Exception(str(e))  # NOSONAR
