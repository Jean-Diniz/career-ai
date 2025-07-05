"""
Servidor de agente de carreira usando python_a2a.
Integra as funcionalidades de IA para análise de perfil, geração de trilhas e sugestões.
"""

import asyncio
import json
import logging

from python_a2a import (
    A2AServer,
    Message,
    MessageRole,
    TextContent,
    agent,
    run_server,
    skill,
)

from app.agent import (
    analisar_perfil_ia,
    create_career_agent,
    gerar_trilha_ia,
    sugerir_recursos_ia,
)
from app.models import Competencia, ObjetivoCarreira, PerfilPessoa

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@agent(
    name="Agente de Carreira AI",
    description="Especialista em desenvolvimento de carreira e educação profissional",
    version="1.0.0",
)
class CareerAgent(A2AServer):
    """Agente de carreira com capacidades de IA para análise e recomendações."""

    def __init__(self):
        super().__init__()
        self.career_agent = None
        self._initialize_agent()

    def _initialize_agent(self):
        """Inicializa o agente de carreira IA."""
        try:
            self.career_agent = create_career_agent()
            if self.career_agent:
                logger.info("Agente de carreira IA inicializado com sucesso")
            else:
                logger.warning("Agente de carreira IA não pôde ser inicializado")
        except Exception as e:
            logger.error(f"Erro ao inicializar agente IA: {e}")

    @skill(
        name="Analisar Perfil",
        description="Analisa um perfil profissional e fornece insights detalhados",
        tags=["análise", "perfil", "carreira"],
    )
    async def analisar_perfil(self, perfil_data: str) -> str:
        """
        Analisa um perfil profissional.

        Args:
            perfil_data: JSON string com dados do perfil

        Returns:
            Análise detalhada do perfil
        """
        try:
            # Parse do JSON do perfil
            perfil_dict = json.loads(perfil_data)
            perfil = PerfilPessoa(**perfil_dict)

            # Análise usando IA
            resultado = await analisar_perfil_ia(perfil, self.career_agent)

            return resultado

        except json.JSONDecodeError:
            return "Erro: Formato JSON inválido para o perfil."
        except Exception as e:
            logger.error(f"Erro ao analisar perfil: {e}")
            return f"Erro ao analisar perfil: {str(e)}"

    @skill(
        name="Gerar Trilha de Estudos",
        description="Gera uma trilha de estudos personalizada baseada no perfil",
        tags=["trilha", "estudos", "educação", "desenvolvimento"],
    )
    async def gerar_trilha(self, perfil_data: str) -> str:
        """
        Gera uma trilha de estudos personalizada.

        Args:
            perfil_data: JSON string com dados do perfil

        Returns:
            Trilha de estudos estruturada
        """
        try:
            # Parse do JSON do perfil
            perfil_dict = json.loads(perfil_data)
            perfil = PerfilPessoa(**perfil_dict)

            # Geração da trilha usando IA
            trilha = await gerar_trilha_ia(perfil, self.career_agent)

            return trilha

        except json.JSONDecodeError:
            return "Erro: Formato JSON inválido para o perfil."
        except Exception as e:
            logger.error(f"Erro ao gerar trilha: {e}")
            return f"Erro ao gerar trilha: {str(e)}"

    @skill(
        name="Sugerir Recursos",
        description="Sugere recursos de estudo para uma área específica",
        tags=["recursos", "cursos", "certificações", "estudo"],
    )
    async def sugerir_recursos(
        self, area: str, nivel: str = "intermediário", tipo: str = "todos"
    ) -> str:
        """
        Sugere recursos de estudo para uma área.

        Args:
            area: Área de interesse
            nivel: Nível de conhecimento (iniciante, intermediário, avançado)
            tipo: Tipo de recurso (cursos, livros, certificações, todos)

        Returns:
            Lista de recursos sugeridos
        """
        try:
            recursos = await sugerir_recursos_ia(area, nivel, tipo, self.career_agent)
            return recursos

        except Exception as e:
            logger.error(f"Erro ao sugerir recursos: {e}")
            return f"Erro ao sugerir recursos: {str(e)}"

    @skill(
        name="Criar Perfil Exemplo",
        description="Cria um exemplo de perfil para testes",
        tags=["exemplo", "template", "perfil"],
    )
    def criar_perfil_exemplo(self) -> str:
        """
        Cria um exemplo de perfil para demonstração.

        Returns:
            JSON string com exemplo de perfil
        """
        perfil_exemplo = PerfilPessoa(
            nome="João Silva",
            idade=28,
            escolaridade="Superior Completo",
            area_formacao="Engenharia da Computação",
            competencias_atuais=[
                Competencia(
                    area="Python",
                    nivel="intermediário",
                    experiencia_anos=3,
                    detalhes="Desenvolvimento web e automação",
                ),
                Competencia(
                    area="JavaScript",
                    nivel="básico",
                    experiencia_anos=1,
                    detalhes="Frontend básico",
                ),
            ],
            objetivos_carreira=[
                ObjetivoCarreira(
                    cargo_desejado="Cientista de Dados",
                    area_interesse="Inteligência Artificial",
                    prazo_anos=2,
                    motivacao="Interesse em machine learning e big data",
                )
            ],
            disponibilidade_estudo_horas_semana=15,
            preferencia_aprendizado="online",
            recursos_disponiveis="cursos online, livros",
        )

        return perfil_exemplo.model_dump_json(indent=2, ensure_ascii=False)

    def _processar_analise_perfil_sync(self, message: Message) -> Message:
        """Processa solicitações de análise de perfil de forma síncrona."""
        try:
            # Extrai JSON do texto se presente
            text = message.content.text
            if "{" in text and "}" in text:
                start = text.find("{")
                end = text.rfind("}") + 1
                perfil_json = text[start:end]

                # Parse do JSON do perfil
                perfil_dict = json.loads(perfil_json)
                perfil = PerfilPessoa(**perfil_dict)

                # Análise usando IA de forma síncrona
                from app.agent import run_career_agent_sync, run_llm_sync
                
                if self.career_agent:
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
                    resultado = run_career_agent_sync(self.career_agent, prompt)
                else:
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
                    resultado = run_llm_sync(prompt)

                return Message(
                    content=TextContent(
                        text=f"📊 **Análise do Perfil:**\n\n{resultado}"
                    ),
                    role=MessageRole.AGENT,
                    parent_message_id=message.message_id,
                    conversation_id=message.conversation_id,
                )
            else:
                return Message(
                    content=TextContent(
                        text="Para analisar um perfil, envie os dados no formato JSON. Use 'exemplo' para ver um template."
                    ),
                    role=MessageRole.AGENT,
                    parent_message_id=message.message_id,
                    conversation_id=message.conversation_id,
                )

        except Exception as e:
            return Message(
                content=TextContent(text=f"Erro ao processar análise: {str(e)}"),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id,
            )

    def _processar_trilha_estudos_sync(self, message: Message) -> Message:
        """Processa solicitações de trilha de estudos de forma síncrona."""
        try:
            text = message.content.text
            if "{" in text and "}" in text:

                # Geração da trilha usando IA de forma síncrona
                from app.agent import run_career_agent_sync, run_llm_sync, criar_prompt_trilha
                
                prompt = criar_prompt_trilha(text)
                
                if self.career_agent:
                    resultado = run_career_agent_sync(self.career_agent, prompt)
                else:
                    resultado = run_llm_sync(prompt)

                return Message(
                    content=TextContent(
                        text=f"🛤️ **Trilha de Estudos:**\n\n{resultado}"
                    ),
                    role=MessageRole.AGENT,
                    parent_message_id=message.message_id,
                    conversation_id=message.conversation_id,
                )
            else:
                return Message(
                    content=TextContent(
                        text="Para gerar uma trilha de estudos, envie os dados do perfil no formato JSON. Use 'exemplo' para ver um template."
                    ),
                    role=MessageRole.AGENT,
                    parent_message_id=message.message_id,
                    conversation_id=message.conversation_id,
                )

        except Exception as e:
            return Message(
                content=TextContent(text=f"Erro ao processar trilha: {str(e)}"),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id,
            )

    def _processar_sugestao_recursos_sync(self, message: Message) -> Message:
        """Processa solicitações de sugestão de recursos de forma síncrona."""
        try:
            text = message.content.text

            # Extrai parâmetros do texto
            area = "tecnologia"  # padrão
            nivel = "intermediário"  # padrão
            tipo = "todos"  # padrão

            # Parse simples de parâmetros
            if "área:" in text or "area:" in text:
                area_match = text.split("área:" if "área:" in text else "area:")[
                    1
                ].split()[0]
                area = area_match.strip(",.")

            if "nível:" in text or "nivel:" in text:
                nivel_match = text.split("nível:" if "nível:" in text else "nivel:")[
                    1
                ].split()[0]
                nivel = nivel_match.strip(",.")

            if "tipo:" in text:
                tipo_match = text.split("tipo:")[1].split()[0]
                tipo = tipo_match.strip(",.")

            # Gera sugestões usando IA de forma síncrona
            from app.agent import run_career_agent_sync, run_llm_sync
            
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
            
            if self.career_agent:
                resultado = run_career_agent_sync(self.career_agent, prompt)
            else:
                resultado = run_llm_sync(prompt)

            return Message(
                content=TextContent(
                    text=f"📚 **Recursos para {area} (nível {nivel}):**\n\n{resultado}"
                ),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id,
            )

        except Exception as e:
            return Message(
                content=TextContent(text=f"Erro ao sugerir recursos: {str(e)}"),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id,
            )



    def handle_message(self, message: Message) -> Message:
        """Processa mensagens de forma síncrona."""
        try:
            if message.content.type != "text":
                return Message(
                    content=TextContent(
                        text="Apenas mensagens de texto são suportadas."
                    ),
                    role=MessageRole.AGENT,
                    parent_message_id=message.message_id,
                    conversation_id=message.conversation_id,
                )

            text = message.content.text.lower()

            # Análise de intenção baseada em palavras-chave
            if any(palavra in text for palavra in ["analisar", "análise", "perfil"]):
                return self._processar_analise_perfil_sync(message)

            elif any(
                palavra in text for palavra in ["trilha", "estudos", "plano", "roadmap"]
            ):
                return self._processar_trilha_estudos_sync(message)

            elif any(
                palavra in text
                for palavra in ["recursos", "cursos", "certificação", "sugerir"]
            ):
                return self._processar_sugestao_recursos_sync(message)

            elif any(palavra in text for palavra in ["exemplo", "template", "demo"]):
                exemplo = self.criar_perfil_exemplo()
                return Message(
                    content=TextContent(
                        text=f"Aqui está um exemplo de perfil:\n\n```json\n{exemplo}\n```"
                    ),
                    role=MessageRole.AGENT,
                    parent_message_id=message.message_id,
                    conversation_id=message.conversation_id,
                )

            elif any(palavra in text for palavra in ["ajuda", "help", "comandos"]):
                return self._gerar_ajuda(message)

            else:
                return self._gerar_resposta_padrao(message)

        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return Message(
                content=TextContent(text=f"Erro interno: {str(e)}"),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id,
            )



    def _gerar_ajuda(self, message: Message) -> Message:
        """Gera mensagem de ajuda."""
        ajuda = """
🤖 **Agente de Carreira AI** - Como posso ajudar:

**📊 Análise de Perfil:**
- Digite "analisar perfil" + dados JSON
- Receba insights sobre pontos fortes, áreas de melhoria e recomendações

**🛤️ Trilha de Estudos:**
- Digite "trilha de estudos" + dados JSON  
- Receba um plano personalizado de desenvolvimento

**📚 Sugestão de Recursos:**
- Digite "sugerir recursos área: [área] nível: [nível] tipo: [tipo]"
- Receba cursos, livros, certificações e projetos recomendados

**📝 Exemplo de Perfil:**
- Digite "exemplo" para ver um template de perfil JSON

**💡 Dicas:**
- Use dados estruturados em JSON para melhores resultados
- Especifique suas competências atuais e objetivos de carreira
- Inclua disponibilidade de tempo e recursos

Digite 'exemplo' para começar!
"""

        return Message(
            content=TextContent(text=ajuda),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id,
        )

    def _gerar_resposta_padrao(self, message: Message) -> Message:
        """Gera resposta padrão para mensagens não reconhecidas."""
        resposta = """
👋 Olá! Sou seu **Agente de Carreira AI**.

Posso ajudar você com:
- 📊 Análise de perfil profissional
- 🛤️ Criação de trilhas de estudos personalizadas  
- 📚 Sugestão de recursos educacionais
- 💡 Orientação de carreira

Digite 'ajuda' para ver todos os comandos disponíveis ou 'exemplo' para ver um template de perfil.

Como posso ajudar você hoje?
"""

        return Message(
            content=TextContent(text=resposta),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id,
        )


if __name__ == "__main__":
    # Cria e executa o agente de carreira
    career_agent = CareerAgent()
    logger.info("Iniciando Agente de Carreira AI em http://0.0.0.0:5000")
    run_server(career_agent, host="0.0.0.0", port=5000)
