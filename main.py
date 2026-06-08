from controllers.main_controller import index
from flask import Flask
from config import Config
from db import db
from logger_config import setup_logger

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
logger = setup_logger()

app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

app.add_url_rule("/gerar-selo", view_func=index, methods=["POST"])

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
