#!/usr/bin/env python3
"""
Script simples para executar o teste de integração A2A.
"""

import logging
import subprocess
import sys
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def executar_teste():
    """Executa o teste de integração completo."""
    processos = []

    try:
        print("🚀 Iniciando teste de integração A2A...")
        print("📋 Verificando se Ollama está rodando...")

        # Verifica se Ollama está rodando
        try:
            import requests

            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama está rodando")
            else:
                print("❌ Ollama não está respondendo corretamente")
                return
        except Exception as e:
            print(f"❌ Ollama não está acessível: {e}")
            print("💡 Certifique-se de que o Ollama está rodando com 'ollama serve'")
            return

        print("\n🔧 Iniciando agente auxiliar...")
        processo_auxiliar = subprocess.Popen(
            [sys.executable, "test_integration_a2a.py", "auxiliar"]
        )
        processos.append(processo_auxiliar)

        # Aguarda um pouco para o auxiliar iniciar
        time.sleep(3)

        print("🚀 Iniciando agente principal...")
        processo_principal = subprocess.Popen(
            [sys.executable, "test_integration_a2a.py", "principal"]
        )
        processos.append(processo_principal)

        # Aguarda os servidores iniciarem
        time.sleep(5)

        print("\n🧪 Executando testes automáticos...")
        processo_teste = subprocess.run(
            [sys.executable, "test_integration_a2a.py", "teste"], timeout=60
        )

        if processo_teste.returncode == 0:
            print("✅ Testes concluídos com sucesso!")
        else:
            print("❌ Testes falharam")

        print("\n📋 Os agentes continuam rodando para teste manual:")
        print("   Agente Principal: http://localhost:5000")
        print("   Agente Auxiliar: http://localhost:5001")
        print("\n💡 Para testar manualmente, use um cliente A2A ou curl:")
        print("   curl -X POST http://localhost:5000/api/message \\")
        print('        -H "Content-Type: application/json" \\')
        print(
            '        -d \'{"text": "Qual o score de carreira para dados avançado?"}\''
        )
        print("\n🛑 Pressione Ctrl+C para parar os agentes")

        # Aguarda interrupção do usuário
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Parando agentes...")

    except Exception as e:
        logger.error(f"Erro no teste: {e}")

    finally:
        # Termina todos os processos
        for processo in processos:
            if processo.poll() is None:
                processo.terminate()
                try:
                    processo.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    processo.kill()


if __name__ == "__main__":
    executar_teste()
