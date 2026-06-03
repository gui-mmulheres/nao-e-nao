from models.person_store_model import person_store_model
from db import db
import uuid


class StoreModel(db.Model):
    __tablename__ = "loja"

    id = db.Column(db.String(36), primary_key=True)
    cnpj = db.Column(db.String(14), nullable=False, unique=True)
    nome_fantasia = db.Column(db.String(100), nullable=False)
    razao_social = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    tipo_loja = db.Column(db.String(50), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    numero_end = db.Column(db.String(10), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    municipio = db.Column(db.String(30), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    tem_pessoa_qualificada = db.Column(db.Integer, nullable=False)
    quant_pessoa_qualificada = db.Column(db.Integer, nullable=False)
    tem_info_canais = db.Column(db.Integer, nullable=False)
    tem_monitor_imagem = db.Column(db.Integer, nullable=False)
    tem_sinal_sanitario = db.Column(db.Integer, nullable=False)
    pessoas = db.relationship(
        'PersonModel', secondary=person_store_model, back_populates='lojas')

    def __init__(
        self,
        params
    ):
        self.id = self.gerar_id()
        self.cnpj = params['cnpj']
        self.nome_fantasia = params['nome_fantasia']
        self.razao_social = params['razao_social']
        self.email = params['email']
        self.tipo_loja = params['tipo_loja']
        self.endereco = params['endereco']
        self.numero_end = params['numero_end']
        self.bairro = params['bairro']
        self.municipio = params['municipio']
        self.uf = params['uf']
        self.tem_pessoa_qualificada = params['tem_pessoa_qualificada']
        self.quant_pessoa_qualificada = params['quant_pessoa_qualificada']
        self.tem_info_canais = params['tem_info_canais']
        self.tem_monitor_imagem = params['tem_monitor_imagem']
        self.tem_sinal_sanitario = params['tem_sinal_sanitario']

    def gerar_id(self):
        return str(uuid.uuid4())

    @staticmethod
    def busca_loja_cnpj(cnpj_loja):
        loja_encontrada = db.session.query(StoreModel).filter_by(
            cnpj=cnpj_loja).first()

        return loja_encontrada

    @staticmethod
    def cadastra_loja(loja):
        loja_encontrada = StoreModel.busca_loja_cnpj(loja['cnpj'])
        if loja_encontrada is None:
            nova_loja = StoreModel(loja)
            db.session.add(nova_loja)
            db.session.commit()
            return nova_loja
        else:
            loja_atualizada = StoreModel.atualiza_loja(loja_encontrada, loja)
            return loja_atualizada

    @staticmethod
    def atualiza_loja(loja, params):
        loja.nome_fantasia = params['nome_fantasia']
        loja.razao_social = params['razao_social']
        loja.email = params['email']
        loja.tipo_loja = params['tipo_loja']
        loja.endereco = params['endereco']
        loja.numero_end = params['numero_end']
        loja.bairro = params['bairro']
        loja.municipio = params['municipio']
        loja.uf = params['uf']
        loja.tem_pessoa_qualificada = params['tem_pessoa_qualificada']
        loja.quant_pessoa_qualificada = params['quant_pessoa_qualificada']
        loja.tem_info_canais = params['tem_info_canais']
        loja.tem_monitor_imagem = params['tem_monitor_imagem']
        loja.tem_sinal_sanitario = params['tem_sinal_sanitario']

        db.session.commit()

        return loja
