"""
Teste de integração A2A simples.
Testa comunicação entre agentes usando Ollama para decisão.
"""

import asyncio
import json
import logging
import time
from threading import Thread

import requests
from python_a2a import (
    A2AClient,
    A2AServer,
    Message,
    MessageRole,
    TextContent,
    agent,
    run_server,
    skill,
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@agent(
    name="Agente Auxiliar",
    description="Agente auxiliar que fornece informações específicas",
    version="1.0.0",
)
class AgenteAuxiliar(A2AServer):
    """Agente auxiliar que responde a perguntas específicas."""

    @skill(
        name="Calcular Score de Carreira",
        description="Calcula um score de adequação para uma área de carreira",
        tags=["carreira", "score", "avaliação"],
    )
    def calcular_score_carreira(self, area: str, experiencia: str) -> str:
        """
        Calcula um score simplificado para uma área de carreira.

        Args:
            area: Área de carreira
            experiencia: Nível de experiência

        Returns:
            Score e análise
        """
        scores = {
            "tecnologia": {"iniciante": 7, "intermediário": 8, "avançado": 9},
            "dados": {"iniciante": 6, "intermediário": 8, "avançado": 9},
            "gestão": {"iniciante": 5, "intermediário": 7, "avançado": 8},
            "design": {"iniciante": 6, "intermediário": 7, "avançado": 8},
        }

        area_lower = area.lower()
        experiencia_lower = experiencia.lower()

        score = scores.get(area_lower, {}).get(experiencia_lower, 5)

        resultado = {
            "area": area,
            "experiencia": experiencia,
            "score": score,
            "recomendacao": f"Score {score}/10 para {area} com nível {experiencia}",
            "proximos_passos": f"Considere focar em projetos práticos na área de {area}",
        }

        return json.dumps(resultado, ensure_ascii=False, indent=2)

    def handle_message(self, message: Message) -> Message:
        """Processa mensagens recebidas."""
        try:
            text = message.content.text.lower()

            if "calcular" in text and "score" in text:
                # Extrai informações básicas do texto
                area = "tecnologia"  # padrão
                experiencia = "intermediário"  # padrão

                if "área:" in text:
                    area = text.split("área:")[1].split()[0].strip(",.")
                if "experiência:" in text or "experiencia:" in text:
                    exp_key = (
                        "experiência:" if "experiência:" in text else "experiencia:"
                    )
                    experiencia = text.split(exp_key)[1].split()[0].strip(",.")

                resultado = self.calcular_score_carreira(area, experiencia)

                return Message(
                    content=TextContent(
                        text=f"📊 **Score de Carreira:**\n\n```json\n{resultado}\n```"
                    ),
                    role=MessageRole.AGENT,
                    parent_message_id=message.message_id,
                    conversation_id=message.conversation_id,
                )

            return Message(
                content=TextContent(
                    text="Sou o Agente Auxiliar. Posso calcular scores de carreira. "
                    "Use: 'calcular score área: [área] experiência: [nível]'"
                ),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id,
            )

        except Exception as e:
            logger.error(f"Erro no agente auxiliar: {e}")
            return Message(
                content=TextContent(text=f"Erro: {str(e)}"),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id,
            )


@agent(
    name="Agente Principal",
    description="Agente principal que usa IA para decidir quando chamar outros agentes",
    version="1.0.0",
)
class AgentePrincipal(A2AServer):
    """Agente principal que usa Ollama para decisões."""

    def __init__(self):
        super().__init__()
        self.client_auxiliar = None
        self._conectar_agente_auxiliar()

    def _conectar_agente_auxiliar(self):
        """Conecta com o agente auxiliar."""
        try:
            self.client_auxiliar = A2AClient("http://localhost:5001")
            logger.info("Conectado ao agente auxiliar")
        except Exception as e:
            logger.warning(f"Não foi possível conectar ao agente auxiliar: {e}")

    def _usar_ollama_para_decisao(self, texto: str) -> dict:
        """
        Usa Ollama local para decidir se deve chamar outro agente.

        Args:
            texto: Texto da mensagem do usuário

        Returns:
            Dicionário com decisão e parâmetros
        """
        try:
            prompt = f"""
Analise esta mensagem do usuário e decida se precisa chamar um agente auxiliar:

Mensagem: "{texto}"

O agente auxiliar pode:
- Calcular scores de carreira para diferentes áreas

Responda APENAS com um JSON no formato:
{{
    "precisa_agente_auxiliar": true/false,
    "motivo": "explicação da decisão",
    "acao": "ação específica se precisar do agente",
    "parametros": {{"area": "área", "experiencia": "nível"}}
}}

Se a mensagem menciona score, avaliação, pontuação de carreira, ou perguntas sobre adequação para uma área, responda true.
"""

            # Chamada simples para Ollama local
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.1",
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1},
                },
                timeout=30,
            )

            if response.status_code == 200:
                ollama_response = response.json()["response"]
                logger.info(f"Resposta Ollama: {ollama_response}")

                # Extrai JSON da resposta
                if "{" in ollama_response and "}" in ollama_response:
                    start = ollama_response.find("{")
                    end = ollama_response.rfind("}") + 1
                    json_str = ollama_response[start:end]
                    return json.loads(json_str)

            # Fallback para decisão simples
            return {
                "precisa_agente_auxiliar": "score" in texto.lower()
                or "avalia" in texto.lower(),
                "motivo": "Decisão baseada em palavras-chave",
                "acao": "calcular_score",
                "parametros": {"area": "tecnologia", "experiencia": "intermediário"},
            }

        except Exception as e:
            logger.error(f"Erro ao usar Ollama: {e}")
            return {
                "precisa_agente_auxiliar": False,
                "motivo": f"Erro na IA: {str(e)}",
                "acao": "",
                "parametros": {},
            }

    async def _chamar_agente_auxiliar(self, acao: str, parametros: dict) -> str:
        """Chama o agente auxiliar com os parâmetros especificados."""
        if not self.client_auxiliar:
            return "❌ Agente auxiliar não disponível"

        try:
            if acao == "calcular_score":
                area = parametros.get("area", "tecnologia")
                experiencia = parametros.get("experiencia", "intermediário")

                mensagem = f"calcular score área: {area} experiência: {experiencia}"

                # Criar um objeto Message em vez de passar uma string diretamente
                message_obj = Message(
                    content=TextContent(text=mensagem),
                    role=MessageRole.USER
                )
                
                response_message = await self.client_auxiliar.send_message_async(message_obj)
                return response_message.content.text

        except Exception as e:
            logger.error(f"Erro ao chamar agente auxiliar: {e}")
            return f"❌ Erro na comunicação: {str(e)}"

        return "❌ Ação não reconhecida"

    def handle_message(self, message: Message) -> Message:
        """Processa mensagens usando IA para decisões."""
        try:
            texto = message.content.text

            # Usa Ollama para decidir
            decisao = self._usar_ollama_para_decisao(texto)

            logger.info(f"Decisão da IA: {decisao}")

            if decisao.get("precisa_agente_auxiliar", False):
                # Chama agente auxiliar
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    resultado = loop.run_until_complete(
                        self._chamar_agente_auxiliar(
                            decisao.get("acao", ""), decisao.get("parametros", {})
                        )
                    )
                finally:
                    loop.close()

                resposta = f"""
🤖 **Agente Principal** - Decisão da IA:

**Motivo:** {decisao.get("motivo", "N/A")}

**Resultado do Agente Auxiliar:**
{resultado}

---
*Decisão tomada automaticamente pelo Ollama*
"""
            else:
                resposta = f"""
🤖 **Agente Principal**

**Decisão da IA:** {decisao.get("motivo", "Não precisa de agente auxiliar")}

Posso ajudar diretamente com sua pergunta: "{texto}"

Para testar a comunicação A2A, experimente perguntar sobre "score de carreira" ou "avaliação de área".
"""

            return Message(
                content=TextContent(text=resposta),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id,
            )

        except Exception as e:
            logger.error(f"Erro no agente principal: {e}")
            return Message(
                content=TextContent(text=f"❌ Erro interno: {str(e)}"),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id,
            )


def executar_agente_auxiliar():
    """Executa o agente auxiliar em thread separada."""
    auxiliar = AgenteAuxiliar()
    logger.info("🔧 Iniciando Agente Auxiliar na porta 5001")
    run_server(auxiliar, host="0.0.0.0", port=5001)


def executar_agente_principal():
    """Executa o agente principal."""
    principal = AgentePrincipal()
    logger.info("🚀 Iniciando Agente Principal na porta 5000")
    run_server(principal, host="0.0.0.0", port=5000)


async def teste_comunicacao():
    """Teste automático da comunicação entre agentes."""
    logger.info("🧪 Iniciando teste de comunicação A2A")

    # Aguarda os servidores iniciarem
    await asyncio.sleep(3)

    try:
        # Conecta com o agente principal
        client = A2AClient("http://localhost:5000")

        # Testa mensagem que deve chamar o agente auxiliar
        logger.info("📤 Testando mensagem que requer agente auxiliar...")
        
        # Criar um objeto Message em vez de passar uma string diretamente
        message_obj = Message(
            content=TextContent(
                text="Qual o score de carreira para tecnologia com experiência intermediário?"
            ),
            role=MessageRole.USER
        )
        
        response = await client.send_message_async(message_obj)

        logger.info("📥 Resposta recebida:")
        logger.info(response.content.text)

        # Testa mensagem simples
        logger.info("📤 Testando mensagem simples...")
        
        # Criar outro objeto Message para a segunda mensagem
        message_obj2 = Message(
            content=TextContent(text="Olá, como você pode me ajudar?"),
            role=MessageRole.USER
        )
        
        response2 = await client.send_message_async(message_obj2)

        logger.info("📥 Resposta recebida:")
        logger.info(response2.content.text)

        logger.info("✅ Teste de comunicação concluído")

    except Exception as e:
        logger.error(f"❌ Erro no teste: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "auxiliar":
            executar_agente_auxiliar()
        elif sys.argv[1] == "principal":
            executar_agente_principal()
        elif sys.argv[1] == "teste":
            asyncio.run(teste_comunicacao())
        else:
            print("Uso: python test_integration_a2a.py [auxiliar|principal|teste]")
    else:
        # Executa ambos os agentes
        print("🚀 Iniciando teste de integração A2A...")
        print("📋 Para testar manualmente:")
        print("   Terminal 1: python test_integration_a2a.py auxiliar")
        print("   Terminal 2: python test_integration_a2a.py principal")
        print("   Terminal 3: python test_integration_a2a.py teste")
        print("\n🔧 Executando agente auxiliar em background...")

        # Inicia agente auxiliar em thread
        thread_auxiliar = Thread(target=executar_agente_auxiliar, daemon=True)
        thread_auxiliar.start()

        # Aguarda um pouco para o auxiliar iniciar
        time.sleep(2)

        print("🚀 Executando agente principal...")
        executar_agente_principal()
