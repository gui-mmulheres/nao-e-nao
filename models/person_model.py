from models.person_store_model import person_store_model
from db import db
import uuid


class PersonModel(db.Model):
    __tablename__ = 'pessoa'

    id = db.Column(db.String(36), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    certificado = db.Column(db.String(50), nullable=False)
    lojas = db.relationship(
        'StoreModel', secondary=person_store_model, back_populates='pessoas')

    def __init__(
        self,
        nome,
        cpf,
        certificado
    ):
        self.id = self.gerar_id()
        self.nome = nome
        self.cpf = cpf
        self.certificado = certificado

    def gerar_id(self):
        return str(uuid.uuid4())

    @staticmethod
    def busca_pessoa_cpf(cpf_pessoa):
        pessoa_encontrada = db.session.query(PersonModel).filter_by(
            cpf=cpf_pessoa).first()

        return pessoa_encontrada

    @staticmethod
    def cadastra_pessoa(pessoa, loja):
        pessoa_encontrada = PersonModel.busca_pessoa_cpf(pessoa['cpf'])
        if pessoa_encontrada is None:
            nova_pessoa = PersonModel(
                pessoa['nome'], pessoa['cpf'], pessoa['certificado'])
            nova_pessoa.lojas.append(loja)
            db.session.add(nova_pessoa)
            db.session.commit()
            return nova_pessoa
        else:
            pessoa_atualizada = PersonModel.atualiza_pessoa(
                pessoa_encontrada, pessoa, loja)
            return pessoa_atualizada

    @staticmethod
    def atualiza_pessoa(pessoa, params, loja):
        pessoa.nome = params['nome']
        pessoa.certificado = params['certificado']
        pessoa.lojas.append(loja)

        db.session.commit()

        return pessoa
