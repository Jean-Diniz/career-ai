"""
Modelos de dados para o sistema de carreira.
"""

from typing import List, Optional

from pydantic import BaseModel


class Competencia(BaseModel):
    """Representa uma competência atual da pessoa."""

    area: str
    nivel: str
    experiencia_anos: Optional[int] = None
    detalhes: Optional[str] = None


class ObjetivoCarreira(BaseModel):
    """Representa um objetivo de carreira."""

    cargo_desejado: str
    area_interesse: str
    prazo_anos: Optional[int] = None
    motivacao: Optional[str] = None


class PerfilPessoa(BaseModel):
    """Perfil completo de uma pessoa para análise de carreira."""

    nome: str
    idade: Optional[int] = None
    escolaridade: str
    area_formacao: Optional[str] = None
    competencias_atuais: List[Competencia] = []
    objetivos_carreira: List[ObjetivoCarreira] = []
    disponibilidade_estudo_horas_semana: Optional[int] = None
    preferencia_aprendizado: Optional[str] = None
    recursos_disponiveis: Optional[str] = None


class EtapaTrilha(BaseModel):
    """Representa uma etapa na trilha de estudos."""

    titulo: str
    objetivo: str
    duracao_estimada: str
    atividades: List[str]
    recursos_necessarios: List[str]
    criterios_conclusao: List[str]


class TrilhaEstudos(BaseModel):
    """Trilha de estudos completa."""

    titulo: str
    descricao: str
    duracao_total: str
    etapas: List[EtapaTrilha]
    marcos_verificacao: List[str]
    proximos_passos: List[str]


class AnalisePerfil(BaseModel):
    """Análise de um perfil profissional."""

    pontos_fortes: List[str]
    areas_melhoria: List[str]
    oportunidades_crescimento: List[str]
    recomendacoes_estrategicas: List[str]
    lacunas_competencias: List[str]
    proximos_passos: List[str]


class RecursoEstudo(BaseModel):
    """Representa um recurso de estudo."""

    nome: str
    tipo: str
    descricao: str
    duracao_estimada: str
    custo: str
    url_ou_localizacao: Optional[str] = None


class SugestaoRecursos(BaseModel):
    """Sugestão de recursos de estudo para uma área."""

    area: str
    nivel: str
    cursos_online: List[RecursoEstudo] = []
    livros: List[RecursoEstudo] = []
    certificacoes: List[RecursoEstudo] = []
    projetos_praticos: List[RecursoEstudo] = []
    comunidades_eventos: List[RecursoEstudo] = []
    ferramentas: List[RecursoEstudo] = []
