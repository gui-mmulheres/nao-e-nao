from db import db


person_store_model = db.Table('pessoa_loja',
                              db.Column('loja_id', db.String(36), db.ForeignKey(
                                  'loja.id'), primary_key=True),
                              db.Column('pessoa_id', db.String(36), db.ForeignKey('pessoa.id'), primary_key=True))
