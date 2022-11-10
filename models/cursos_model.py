from core.config import settings
from sqlalchemy import Integer, Column, String

class CursosModel(settings.DBBaseModel):
    __tablename__ = 'cursos'

    id = Column(Integer, primary_key =True, autoincrement=True)
    titulo = Column(String, nullable=False)
    aulas = Column(Integer, nullable=False)
    horas = Column(Integer, nullable=False)