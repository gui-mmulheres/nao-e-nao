import logging
from typing import cast
from flask import abort, jsonify, make_response, request
from constants.errors import ERROR1, ERROR2, ERROR3, ERROR4, ERROR5
from models.person_model import PersonModel
from models.store_model import StoreModel
from scripts.env_services import inicializa_env
from services.valida_certificado import valida_certificado
from tasks import processa_selo_task
from json import loads
from db import db
from utils.cnpj import formatar_cnpj

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

    if store_data['q2_empresa_habilitada'] == "SIM":
        raise Exception(ERROR1.format(  # NOSONAR
            cnpj=formatar_cnpj(store_data['q3_cnpj'])))

    loja = {
        "cnpj": store_data['q3_cnpj'],
        "nome_fantasia": store_data['q4_nome_fantasia'],
        "razao_social": store_data['q5_razao_social'],
        "email": store_data['q42_email'],
        "endereco": store_data['q8_endereco'],
        "numero_end": store_data['q9_numero_end'],
        "bairro": store_data['q10_bairro'],
        "municipio": store_data['q11_municipio'],
        "uf": store_data['q12_uf'],
        "quant_pessoa_qualificada": int(store_data['q16_quant_pessoa_qualificada'])
    }

    if isinstance(store_data['q7_tipo_loja'], dict):
        loja['tipo_loja'] = store_data['q7_tipo_loja']['other']
    else:
        loja['tipo_loja'] = store_data['q7_tipo_loja']

    loja['tem_pessoa_qualificada'] = valida_criterio(
        store_data['q15_tem_pessoa_qualificada'], ERROR2.format(cnpj=formatar_cnpj(store_data['q3_cnpj'])))
    loja['tem_info_canais'] = valida_criterio(
        store_data['q17_tem_info_canais'], ERROR3.format(cnpj=formatar_cnpj(store_data['q3_cnpj'])))
    loja['tem_monitor_imagem'] = valida_criterio(
        store_data['q18_tem_monitor_imagem'], ERROR4.format(cnpj=formatar_cnpj(store_data['q3_cnpj'])))
    loja['tem_sinal_sanitario'] = valida_criterio(
        store_data['q19_tem_sinal_sanitario'], ERROR5.format(cnpj=formatar_cnpj(store_data['q3_cnpj'])))

    loja['pessoas'] = [
        {
            "nome": store_data["q22_nome_1"],
            "cpf": store_data["q23_cpf_1"],
            "certificado": store_data["q24_certificado_1"]
        }
    ]

    valida_pessoa(loja, store_data, "q25_nome_2",
                  "q26_cpf_2", "q27_certificado_2")
    valida_pessoa(loja, store_data, "q28_nome_3",
                  "q29_cpf_3", "q30_certificado_3")
    valida_pessoa(loja, store_data, "q31_nome_4",
                  "q32_cpf_4", "q33_certificado_4")
    valida_pessoa(loja, store_data, "q34_nome_5",
                  "q35_cpf_5", "q36_certificado_5")

    return loja


def valida_criterio(criterio_form, erro):
    if criterio_form == "SIM":
        return 1
    else:
        raise Exception(erro)  # NOSONAR


def valida_pessoa(loja, store_data, nome_key, cpf_key, certificado_key):
    nome = store_data.get(nome_key, "").strip()
    cpf = store_data.get(cpf_key, "").strip()
    certificado = store_data.get(certificado_key, "").strip()

    if nome and cpf and certificado:
        loja["pessoas"].append({
            "nome": nome,
            "cpf": cpf,
            "certificado": certificado
        })


def cadastra_banco(loja):
    loja_cadastrada = StoreModel.cadastra_loja(loja)

    for pessoa in loja['pessoas']:
        cadastra_pessoa(pessoa, loja_cadastrada)

    return loja_cadastrada


def cadastra_pessoa(pessoa, loja):
    valida_certificado(pessoa)

    PersonModel.cadastra_pessoa(pessoa, loja)
