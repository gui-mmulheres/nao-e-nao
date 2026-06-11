import logging
from typing import cast
from flask import abort, jsonify, make_response
from models.person_model import PersonModel
from models.store_model import StoreModel
from scripts.env_services import inicializa_env
from services.valida_certificado import valida_certificado
from tasks import processa_selo_task
from db import db
from utils.validations import valida_formulario

env = inicializa_env()
logger = logging.getLogger(__name__)


def index():
    response = {}
    try:
        form_tratado = valida_formulario()
        loja = cadastra_banco(form_tratado)
        params = monta_params_task(loja)
        processa_selo_task.delay(params)
    except Exception as e:
        logger.exception(str(e))
        db.session.rollback()
        abort(500, description=str(e))
    response['status'] = 200
    response['message'] = 'Sucesso'
    return make_response(jsonify(response))


def monta_params_task(loja: StoreModel):
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


def cadastra_banco(loja):
    loja_cadastrada = StoreModel.cadastra_loja(loja)

    for pessoa in loja['pessoas']:
        cadastra_pessoa(pessoa, loja_cadastrada)

    return loja_cadastrada


def cadastra_pessoa(pessoa, loja):
    valida_certificado(pessoa)

    PersonModel.cadastra_pessoa(pessoa, loja)
