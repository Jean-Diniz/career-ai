"""
Módulo do agente de carreira com integração de IA.
Baseado no tutorial A2A e aproveitando a lógica existente do servidor MCP.
"""

import json
import logging
import os
from typing import Optional

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from app.models import PerfilPessoa

# Carrega variáveis de ambiente
load_dotenv()

logger = logging.getLogger(__name__)

# Constantes
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "google")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")


def create_career_agent(
    ollama_base_url: Optional[str] = None, ollama_model: Optional[str] = None
) -> Optional[CompiledStateGraph]:
    """
    Cria um agente de carreira usando Ollama ou Google GenAI.

    Args:
        ollama_base_url: URL base do servidor Ollama
        ollama_model: Nome do modelo Ollama

    Returns:
        Agente configurado ou None se não foi possível configurar
    """
    try:
        if ollama_model and ollama_base_url:
            logger.info(f"Configurando agente com Ollama: {ollama_model}")
            llm = ChatOllama(
                base_url=ollama_base_url, model=ollama_model, temperature=0.3
            )
        elif GOOGLE_API_KEY:
            logger.info("Configurando agente com Google GenAI")
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY, temperature=0.3
            )
        else:
            logger.warning("Nenhum provedor de IA configurado")
            return None

        agent = create_react_agent(llm, tools=[])
        return agent

    except Exception as e:
        logger.error(f"Erro ao criar agente: {e}")
        return None


async def run_career_agent(agent: CompiledStateGraph, prompt: str) -> str:
    """
    Executa o agente de carreira com um prompt.

    Args:
        agent: Agente configurado
        prompt: Prompt de entrada

    Returns:
        Resposta do agente
    """
    try:
        agent_response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": prompt}]}
        )
        message = agent_response["messages"][-1].content
        return str(message)
    except Exception as e:
        logger.error(f"Erro ao executar agente: {e}")
        return f"Erro ao processar solicitação: {e}"


def get_llm_provider():
    """Retorna a instância do LLM configurado baseado no provedor escolhido."""
    provider = DEFAULT_LLM_PROVIDER.lower()

    if provider == "google":
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY não configurada para usar Google GenAI")

        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY, temperature=0.3
        )

    elif provider == "ollama":
        return ChatOllama(base_url=OLLAMA_BASE_URL, model=OLLAMA_MODEL, temperature=0.3)

    else:
        raise ValueError(
            f"Provedor '{provider}' não suportado. Use 'google' ou 'ollama'"
        )


def criar_prompt_trilha(perfil: PerfilPessoa) -> str:
    """Cria o prompt personalizado para geração da trilha baseado no perfil."""

    competencias_str = ""
    for comp in perfil.competencias_atuais:
        comp_details = f"- {comp.area} (Nível: {comp.nivel}"
        if comp.experiencia_anos:
            comp_details += f", {comp.experiencia_anos} anos"
        if comp.detalhes:
            comp_details += f", Detalhes: {comp.detalhes}"
        comp_details += ")"
        competencias_str += comp_details + "\n"

    objetivos_str = ""
    for obj in perfil.objetivos_carreira:
        obj_details = f"- {obj.cargo_desejado} em {obj.area_interesse}"
        if obj.prazo_anos:
            obj_details += f" (Meta: {obj.prazo_anos} anos)"
        if obj.motivacao:
            obj_details += f" - Motivação: {obj.motivacao}"
        objetivos_str += obj_details + "\n"

    prompt = f"""
Você é um especialista em desenvolvimento de carreira e educação profissional. 
Sua tarefa é criar uma trilha de estudos personalizada e detalhada baseada \
no perfil fornecido.

**PERFIL DA PESSOA:**
Nome: {perfil.nome}
Idade: {perfil.idade if perfil.idade else "Não informado"}
Escolaridade: {perfil.escolaridade}
Área de Formação: {perfil.area_formacao if perfil.area_formacao else "Não informado"}

**COMPETÊNCIAS ATUAIS:**
{competencias_str}

**OBJETIVOS DE CARREIRA:**
{objetivos_str}

**DISPONIBILIDADE E RECURSOS:**
- Horas de estudo por semana: {
        perfil.disponibilidade_estudo_horas_semana
        if perfil.disponibilidade_estudo_horas_semana
        else "Não informado"
    }
- Preferência de aprendizado: {
        perfil.preferencia_aprendizado
        if perfil.preferencia_aprendizado
        else "Não informado"
    }
- Recursos disponíveis: {
        perfil.recursos_disponiveis if perfil.recursos_disponiveis else "Não informado"
    }

**INSTRUÇÕES:**
1. Analise o perfil completo identificando pontos fortes e lacunas
2. Crie uma trilha de estudos estruturada em etapas progressivas
3. Para cada etapa, inclua:
   - Objetivo específico
   - Duração estimada
   - Atividades detalhadas (cursos, projetos, certificações)
   - Recursos necessários
   - Critérios de conclusão
4. Considere a disponibilidade de tempo e recursos da pessoa
5. Priorize competências que mais contribuem para os objetivos
6. Inclua marcos de verificação e próximos passos

Formate a resposta como um JSON estruturado seguindo o modelo de TrilhaEstudos.
"""

    return prompt


async def gerar_trilha_ia(
    perfil: PerfilPessoa, agent: Optional[CompiledStateGraph] = None
) -> str:
    """
    Gera uma trilha de estudos usando IA baseada no perfil.

    Args:
        perfil: Perfil da pessoa
        agent: Agente configurado (opcional)

    Returns:
        Trilha de estudos em formato JSON
    """
    try:
        prompt = criar_prompt_trilha(perfil)

        if agent:
            response = await run_career_agent(agent, prompt)
        else:
            # Fallback para LLM direto
            llm = get_llm_provider()
            response = await llm.ainvoke(prompt)
            response = (
                response.content if hasattr(response, "content") else str(response)
            )

        return response

    except Exception as e:
        logger.error(f"Erro ao gerar trilha com IA: {e}")
        return f"Erro ao gerar trilha: {e}"


async def analisar_perfil_ia(
    perfil: PerfilPessoa, agent: Optional[CompiledStateGraph] = None
) -> str:
    """
    Analisa um perfil profissional usando IA.

    Args:
        perfil: Perfil da pessoa
        agent: Agente configurado (opcional)

    Returns:
        Análise do perfil
    """
    try:
        prompt = f"""
Analise o seguinte perfil profissional e forneça insights detalhados:

{json.dumps(perfil.model_dump(), indent=2, ensure_ascii=False)}

Forneça uma análise incluindo:
1. Pontos fortes identificados
2. Áreas de melhoria
3. Oportunidades de crescimento
4. Recomendações estratégicas
5. Lacunas de competências para os objetivos
6. Sugestões de próximos passos

Seja específico e construtivo na análise.
"""

        if agent:
            response = await run_career_agent(agent, prompt)
        else:
            llm = get_llm_provider()
            response = await llm.ainvoke(prompt)
            response = (
                response.content if hasattr(response, "content") else str(response)
            )

        return response

    except Exception as e:
        logger.error(f"Erro ao analisar perfil com IA: {e}")
        return f"Erro ao analisar perfil: {e}"


async def sugerir_recursos_ia(
    area: str,
    nivel: str = "intermediário",
    tipo: str = "todos",
    agent: Optional[CompiledStateGraph] = None,
) -> str:
    """
    Sugere recursos de estudo usando IA.

    Args:
        area: Área de interesse
        nivel: Nível de conhecimento
        tipo: Tipo de recurso
        agent: Agente configurado (opcional)

    Returns:
        Lista de recursos sugeridos
    """
    try:
        prompt = f"""
Sugira recursos de estudo específicos para:
- Área: {area}
- Nível: {nivel}
- Tipo de recurso: {tipo}

Inclua:
1. Cursos online recomendados (com plataformas)
2. Livros essenciais
3. Certificações relevantes
4. Projetos práticos sugeridos
5. Comunidades e eventos
6. Ferramentas e tecnologias

Para cada recurso, forneça:
- Nome/título
- Descrição breve
- Duração/esforço estimado
- Custo aproximado
- Link ou onde encontrar (quando possível)

Priorize recursos atualizados e bem avaliados.
"""

        if agent:
            response = await run_career_agent(agent, prompt)
        else:
            llm = get_llm_provider()
            response = await llm.ainvoke(prompt)
            response = (
                response.content if hasattr(response, "content") else str(response)
            )

        return response

    except Exception as e:
        logger.error(f"Erro ao sugerir recursos com IA: {e}")
        return f"Erro ao sugerir recursos: {e}"
