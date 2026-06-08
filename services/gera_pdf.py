from docx2pdf import convert
from constants.errors import ERROR8
from scripts.env_services import inicializa_env

env = inicializa_env()


def converte_pdf():
    try:
        convert(str(env['output_dir']))
    except Exception as e:
        raise Exception(ERROR8.format(erro=str(e)))  # NOSONAR
