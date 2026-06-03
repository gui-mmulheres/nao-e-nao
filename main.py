from controllers.main_controller import index
from flask import Flask, request
from config import Config
from db import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.add_url_rule("/gerar-selo", view_func=index, methods=["POST"])


@app.before_request
def log_request():
    app.logger.info(
        "Método=%s Path=%s Payload=%s",
        request.method,
        request.path,
        request.get_json(silent=True)
    )


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
