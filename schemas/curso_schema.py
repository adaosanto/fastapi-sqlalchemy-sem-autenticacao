from typing import Optional
from pydantic import BaseModel as SCBaseModel
from pydantic import validator

class CursoSchema(SCBaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int
    
    class Config:
        orm_mode = True

    @validator('titulo')
    def validar_titulo(cls, value: str):
        if len(value) <= 3:
            raise ValueError('Titulo do curso deve ter mais de 3 caracteres.')
        
        return value