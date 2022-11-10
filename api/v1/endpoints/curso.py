from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import HTTPException
from fastapi import Response
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.cursos_model import CursosModel
from schemas.curso_schema import CursoSchema

from core.deps import get_session

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoSchema, summary='Cria um novo curso.', description='Rota para criação de cursos.')
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):

    async with db as session:
        novo_curso = CursosModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)

        session.add(novo_curso)
        await session.commit()
        await session.refresh(novo_curso)
        
        return novo_curso

@router.get('/', response_model=List[CursoSchema])
async def get_cursos(db:AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(CursosModel)
        cursos = await session.execute(query)
        cursos: List[CursosModel] = cursos.scalars().all()

        return cursos
        
@router.get('/{curso_id}', response_model=CursoSchema, status_code=status.HTTP_200_OK)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(CursosModel).filter(CursosModel.id == curso_id)
        curso = await session.execute(query)
        curso: CursosModel = curso.scalar_one_or_none()

        if curso:
            return curso
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')

@router.put('/{curso_id}', response_model=CursoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_curso(curso_id: int, curso: CursoSchema, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(CursosModel).filter(CursosModel.id == curso_id)
        resultado = await session.execute(query)
        resultado: CursosModel = resultado.scalar_one_or_none()

        if resultado:
            resultado.titulo = curso.titulo
            resultado.aulas = curso.aulas
            resultado.horas = curso.horas

            await session.commit()

            return resultado
        
        else:
            raise HTTPException(detail='Curso não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

@router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def put_curso(curso_id: int, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(CursosModel).filter(CursosModel.id == curso_id)
        resultado = await session.execute(query)
        resultado: CursosModel = resultado.scalar_one_or_none()

        if resultado:
            
            await session.delete(resultado)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Curso não encontrado.', status_code=status.HTTP_204_NO_CONTENT)