import base64
from pathlib import Path
from scripts.env_services import inicializa_env

env = inicializa_env()


def anexar_pdf(cnpj):
    filename = str(Path(str(env['output_dir'])) / f"{cnpj}.pdf")

    with open(filename, "rb") as f:
        return {
            "@odata.type": "#microsoft.graph.fileAttachment",
            "name": filename.split("\\")[-1],
            "contentType": "application/pdf",
            "contentBytes": base64.b64encode(
                f.read()
            ).decode("utf-8")
        }
