
import logging
from scripts.celery_services import celery
from services.gera_docx import preenche_modelo
from services.gera_email import gera_email
from services.gera_pdf import converte_pdf

logger = logging.getLogger(__name__)

@celery.task
def processa_selo_task(params):
    try:
        preenche_modelo(params)
        converte_pdf()
        gera_email(params['cnpj'], params['email'])
    except Exception as e:
        logger.exception(str(e))