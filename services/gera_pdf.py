from docx2pdf import convert
from scripts.env_services import inicializa_env

env = inicializa_env()


def converte_pdf():
    try:
        convert(str(env['output_dir']))
    except Exception as e:
        raise Exception(str(e))  # NOSONAR
