from json import loads
from flask import request
from constants.errors import ERROR1, ERROR2, ERROR3, ERROR4, ERROR5
from constants.questions import QUESTAO1, QUESTAO10, QUESTAO11, QUESTAO12, QUESTAO13, QUESTAO14, QUESTAO15, QUESTAO16, QUESTAO17, QUESTAO18, QUESTAO19, QUESTAO2, QUESTAO20, QUESTAO21, QUESTAO22, QUESTAO23, QUESTAO24, QUESTAO25, QUESTAO26, QUESTAO27, QUESTAO28, QUESTAO29, QUESTAO3, QUESTAO30, QUESTAO31, QUESTAO4, QUESTAO5, QUESTAO6, QUESTAO7, QUESTAO8, QUESTAO9
from utils.cnpj import formatar_cnpj


def valida_formulario():
    form_data = request.json['data']['fields']
    cnpj = obter_resposta(QUESTAO2, form_data)

    if obter_resposta_multipla_escolha(QUESTAO1, form_data) == "SIM":
        raise Exception(ERROR1.format(cnpj=formatar_cnpj(cnpj)))  # NOSONAR

    loja = {
        "cnpj": cnpj,
        "nome_fantasia": obter_resposta(QUESTAO3, form_data),
        "razao_social": obter_resposta(QUESTAO4, form_data),
        "email": obter_resposta(QUESTAO5, form_data),
        "tipo_loja": obter_resposta_multipla_escolha(QUESTAO6, form_data),
        "endereco": obter_resposta(QUESTAO7, form_data),
        "numero_end": obter_resposta(QUESTAO8, form_data),
        "bairro": obter_resposta(QUESTAO9, form_data),
        "municipio": obter_resposta(QUESTAO10, form_data),
        "uf": obter_resposta_multipla_escolha(QUESTAO11, form_data),
        "quant_pessoa_qualificada": obter_resposta(QUESTAO13, form_data)
    }

    loja['tem_pessoa_qualificada'] = valida_criterio(
        obter_resposta_multipla_escolha(QUESTAO12, form_data), ERROR2.format(cnpj=cnpj))
    loja['tem_info_canais'] = valida_criterio(
        obter_resposta_multipla_escolha(QUESTAO14, form_data), ERROR3.format(cnpj=cnpj))
    loja['tem_monitor_imagem'] = valida_criterio(
        obter_resposta_multipla_escolha(QUESTAO15, form_data), ERROR4.format(cnpj=cnpj))
    loja['tem_sinal_sanitario'] = valida_criterio(
        obter_resposta_multipla_escolha(QUESTAO16, form_data), ERROR5.format(cnpj=cnpj))

    loja['pessoas'] = [
        {
            "nome": obter_resposta(QUESTAO17, form_data),
            "cpf": obter_resposta(QUESTAO18, form_data),
            "certificado": obter_resposta(QUESTAO19, form_data)
        }
    ]

    valida_pessoa(loja, form_data, QUESTAO20, QUESTAO21, QUESTAO22)
    valida_pessoa(loja, form_data, QUESTAO23, QUESTAO24, QUESTAO25)
    valida_pessoa(loja, form_data, QUESTAO26, QUESTAO27, QUESTAO28)
    valida_pessoa(loja, form_data, QUESTAO29, QUESTAO30, QUESTAO31)
    print(loja)

    return loja


def obter_resposta(questao, form_data):
    resposta = ""

    for question in form_data:
        if question['key'] == questao:
            resposta = question['value']

    return resposta


def obter_resposta_multipla_escolha(questao, form_data):
    resposta = ""

    for question in form_data:
        if question['key'] == questao:
            for option in question['options']:
                if option['id'] == question['value'][0]:
                    resposta = str(option['text'])

    return resposta


def valida_criterio(criterio_form, erro):
    if criterio_form == "SIM":
        return 1
    else:
        raise Exception(erro)  # NOSONAR


def valida_pessoa(loja, form_data, nome_key, cpf_key, certificado_key):
    nome = obter_resposta(nome_key, form_data)
    cpf = obter_resposta(cpf_key, form_data)
    certificado = obter_resposta(certificado_key, form_data)

    if nome and cpf and certificado:
        loja["pessoas"].append({
            "nome": nome,
            "cpf": cpf,
            "certificado": certificado
        })
