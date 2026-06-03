from requests import post
from redis import Redis
from msal import PublicClientApplication
from scripts.env_services import inicializa_env
from scripts.pdf_services import anexar_pdf
from scripts.redis_services import RedisTokenCache

env = inicializa_env()


def configurar_email():
    redis_client = Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True
    )

    token_cache = RedisTokenCache(
        redis_client,
        env['cache_key']
    )

    cache = token_cache.load()

    app = PublicClientApplication(
        env['client_id'],
        authority=f"https://login.microsoftonline.com/{env['tenant_id']}",
        token_cache=cache
    )

    accounts = app.get_accounts()

    result = None

    if accounts:
        result = app.acquire_token_silent(
            ["Mail.Send"],
            account=accounts[0]
        )

    if not result:
        flow = app.initiate_device_flow(
            scopes=["Mail.Send"]
        )

        print(flow["message"])

        result = app.acquire_token_by_device_flow(flow)

    token_cache.save(cache)

    if "access_token" not in result:
        print(result)
        raise Exception("Falha ao obter token")  # NOSONAR

    return result['access_token']


def montar_mensagem(cnpj, email):
    token = configurar_email()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "message": {
            "subject": "Selo Não é Não",
            "body": {
                "contentType": "Text",
                "content": "Aqui está seu selo."
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": email
                    }
                }
            ]
        }
    }

    payload["message"]["attachments"] = [
        anexar_pdf(cnpj)
    ]

    return headers, payload


def enviar_email(headers, payload):
    try:
        response = post(
            "https://graph.microsoft.com/v1.0/me/sendMail",
            headers=headers,
            json=payload
        )

        print(response.status_code)
    except Exception as e:
        raise Exception(str(e))  # NOSONAR
