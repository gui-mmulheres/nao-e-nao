import os
from scripts.env_services import inicializa_env

env = inicializa_env()

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///dados.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)