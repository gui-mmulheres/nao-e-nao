import logging
from typing import cast
from flask import abort, jsonify, make_response, request
from models.person_model import PersonModel
from models.store_model import StoreModel
from scripts.env_services import inicializa_env
from tasks import processa_selo_task
from json import loads
from db import db

env = inicializa_env()
logger = logging.getLogger(__name__)


def index():
    response = {}
    try:
        form_tratado = valida_formulario()
        loja = cadastra_banco(form_tratado)
        params = monta_task(loja)
        processa_selo_task.delay(params)
    except Exception as e:
        logger.exception(str(e))
        db.session.rollback()
        abort(500, description=str(e))
    response['status'] = 200
    response['message'] = 'Sucesso'
    return make_response(jsonify(response))


def monta_task(loja: StoreModel):
    params = {
        "cnpj": loja.cnpj,
        "email": loja.email,
        "razao_social": loja.razao_social,
        "pessoas": []
    }

    loja_pessoas = cast(list, loja.pessoas)

    for pessoa in loja_pessoas:
        params["pessoas"].append({
            "nome": pessoa.nome,
            "certificado": pessoa.certificado
        })

    return params


def valida_formulario():
    store_data = loads(request.form['rawRequest'])

    if store_data['q3_cnpj'] == "SIM":
        raise Exception('Loja não habilitada para selo')  # NOSONAR

    loja = {}
    loja['cnpj'] = store_data['q3_cnpj']
    loja['nome_fantasia'] = store_data['q4_nome_fantasia']
    loja['razao_social'] = store_data['q5_razao_social']
    loja['email'] = store_data['q42_email']
    loja['tipo_loja'] = store_data['q7_tipo_loja']
    loja['endereco'] = store_data['q8_endereco']
    loja['numero_end'] = store_data['q9_numero_end']
    loja['bairro'] = store_data['q10_bairro']
    loja['municipio'] = store_data['q11_municipio']
    loja['uf'] = store_data['q12_uf']
    loja['tem_pessoa_qualificada'] = 1 if store_data['q15_tem_pessoa_qualificada'] == "SIM" else 0
    loja['quant_pessoa_qualificada'] = int(
        store_data['q16_quant_pessoa_qualificada'])
    loja['tem_info_canais'] = 1 if store_data['q17_tem_info_canais'] == "SIM" else 0
    loja['tem_monitor_imagem'] = 1 if store_data['q18_tem_monitor_imagem'] == "SIM" else 0
    loja['tem_sinal_sanitario'] = 1 if store_data['q19_tem_sinal_sanitario'] == "SIM" else 0
    loja['pessoas'] = [
        {
            "nome": store_data["q22_nome_1"],
            "cpf": store_data["q23_cpf_1"],
            "certificado": store_data["q24_certificado_1"]
        }
    ]

    if (store_data["q25_nome_2"].strip() and store_data["q26_cpf_2"].strip() and store_data["q27_certificado_2"].strip()):
        loja['pessoas'].append({
            "nome": store_data["q25_nome_2"],
            "cpf": store_data["q26_cpf_2"],
            "certificado": store_data["q27_certificado_2"]
        })

    if (store_data["q28_nome_3"].strip() and store_data["q29_cpf_3"].strip() and store_data["q30_certificado_3"].strip()):
        loja['pessoas'].append({
            "nome": store_data["q28_nome_3"],
            "cpf": store_data["q29_cpf_3"],
            "certificado": store_data["q30_certificado_3"]
        })

    if (store_data["q31_nome_4"].strip() and store_data["q32_cpf_4"].strip() and store_data["q33_certificado_4"].strip()):
        loja['pessoas'].append({
            "nome": store_data["q31_nome_4"],
            "cpf": store_data["q32_cpf_4"],
            "certificado": store_data["q33_certificado_4"]
        })

    if (store_data["q34_nome_5"].strip() and store_data["q35_cpf_5"].strip() and store_data["q36_certificado_5"].strip()):
        loja['pessoas'].append({
            "nome": store_data["q34_nome_5"],
            "cpf": store_data["q35_cpf_5"],
            "certificado": store_data["q36_certificado_5"]
        })

    return loja


def cadastra_banco(loja):
    loja_cadastrada = StoreModel.cadastra_loja(loja)

    for pessoa in loja['pessoas']:
        cadastra_pessoa(pessoa, loja_cadastrada)

    return loja_cadastrada


def cadastra_pessoa(pessoa, loja):
    certificado_valido = valida_certificado(pessoa['certificado'])

    if not certificado_valido:
        raise Exception('Certificado Inválido')  # NOSONAR

    PersonModel.cadastra_pessoa(pessoa, loja)


def valida_certificado(certificado):
    # acessa url
    print(certificado)
    return True
