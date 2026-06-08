from pathlib import Path
from docxtpl import DocxTemplate
from constants.errors import ERROR6, ERROR7
from scripts.env_services import inicializa_env
from utils.cnpj import formatar_cnpj

env = inicializa_env()


def preenche_modelo(params):
    try:
        if not Path(str(env['model_docx'])).exists():
            raise FileNotFoundError(ERROR6)

        filename = Path(str(env['output_dir'])) / f"{params['cnpj']}.docx"
        data = {}
        data['cnpj'] = formatar_cnpj(params['cnpj'])
        data['razao_social'] = params['razao_social']
        data['pessoas'] = params['pessoas']

        doc = DocxTemplate(str(env['model_docx']))
        doc.render(data)
        doc.save(filename)
    except Exception as e:
        raise Exception(ERROR7.format(erro=str(e)))  # NOSONAR
