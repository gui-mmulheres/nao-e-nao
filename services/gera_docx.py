from pathlib import Path
from docxtpl import DocxTemplate
from scripts.env_services import inicializa_env

env = inicializa_env()


def preenche_modelo(params):
    try:
        if not Path(str(env['model_docx'])).exists():
            raise FileNotFoundError("Modelo Word não encontrado")
        
        filename = Path(str(env['output_dir'])) / f"{params['cnpj']}.docx"
        data = {}
        data['cnpj'] = params['cnpj']
        data['razao_social'] = params['razao_social']
        data['pessoas'] = params['pessoas']
        

        doc = DocxTemplate(str(env['model_docx']))
        doc.render(data)
        doc.save(filename)
    except Exception as e:
        raise Exception(str(e)) # NOSONAR