# 🎯 Servidor A2A para Trilhas de Estudos Personalizadas

Um servidor A2A (Agent-to-Agent Protocol) que utiliza LangChain e IA generativa para criar trilhas de estudos personalizadas baseadas no diagnóstico de perfil profissional.

> ✨ **Novo**: Teste de integração A2A com comunicação entre agentes usando Ollama para decisões inteligentes!

## 📋 Funcionalidades

### 🤖 Agent Skills (Habilidades do Agente)

1. **Análise de Perfil Profissional** - Analisa competências e identifica lacunas
2. **Geração de Trilha de Estudos** - Cria trilhas personalizadas baseadas em objetivos
3. **Sugestão de Recursos de Estudo** - Recomenda cursos, certificações e materiais

### 🌐 Protocolo A2A

- **Agent Card** - Metadados e capacidades do agente
- **Task Management** - Gerenciamento de tarefas com estados
- **HTTP API** - Endpoints REST padronizados
- **SSE Support** - Atualizações em tempo real via Server-Sent Events

### 🧠 Integrações de IA

- **Google Gemini** (`langchain-google-genai`) - Padrão recomendado
- **Ollama** (`langchain-ollama>=0.3.3`) - Para execução local
- **LangGraph** (`langgraph>=0.5.0`) - Orquestração de agentes avançados
- **Python A2A** (`python-a2a>=0.5.9`) - Protocolo de comunicação entre agentes

### 📊 Interoperabilidade

Compatível com o protocolo A2A para comunicação entre agentes de IA.

## 🧪 Teste de Integração A2A

### 🤖 Demo de Comunicação entre Agentes

Incluímos um teste completo que demonstra comunicação A2A entre dois agentes:

- **Agente Principal**: Usa Ollama para decidir quando chamar outros agentes
- **Agente Auxiliar**: Fornece funcionalidades específicas (cálculo de scores de carreira)

### ⚡ Execução Rápida

```bash
# 1. Certifique-se que Ollama está rodando
ollama serve

# 2. Execute o teste de integração
python run_test.py
```

### 🎯 Como Funciona

```
👤 Usuário: "Qual o score de carreira para tecnologia intermediário?"
    ↓
🤖 Agente Principal (porta 5000)
    ↓
🧠 Ollama: "Precisa chamar agente auxiliar" ✅
    ↓
🔧 Agente Auxiliar (porta 5001): Score 8/10 para tecnologia
    ↓
📤 Resposta combinada: Decisão IA + Resultado
```

### 📖 Documentação Completa

Consulte [`TESTE_A2A.md`](./TESTE_A2A.md) para instruções detalhadas, exemplos e troubleshooting.

## 🚀 Instalação e Configuração

### 1. Pré-requisitos

- Python 3.12+
- `uv` (gerenciador de dependências da Astral)

### 2. Instalação

```bash
# Clone o repositório e navegue até o diretório
cd career-path

# Instale as dependências
uv sync

# Ative o ambiente virtual
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate     # Windows
```

### 3. Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações do Google Gemini (recomendado)
GOOGLE_API_KEY=sua_api_key_do_google

# Configurações do Ollama (opcional)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# Configuração padrão do provedor LLM
DEFAULT_LLM_PROVIDER=google  # ou "ollama"
```

#### Como obter a API Key do Google:

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada

## 📖 Como Usar

### 1. Executando o Servidor Principal

```bash
# Servidor básico na porta 5000
python app/server.py

# Para desenvolvimento, também disponível via módulo:
python -m app.server
```

### 2. Skills Disponíveis

O agente de carreira fornece as seguintes habilidades via protocolo A2A:

- **Analisar Perfil** - Análise detalhada de perfil profissional
- **Gerar Trilha de Estudos** - Trilhas personalizadas baseadas em objetivos
- **Sugerir Recursos** - Recomendações de cursos, certificações e materiais
- **Criar Perfil Exemplo** - Template para testes

### 3. Exemplo de Uso via HTTP

```bash
# Análise de perfil
curl -X POST http://localhost:5000/api/message \
  -H "Content-Type: application/json" \
  -d '{"text": "analisar perfil {...dados JSON...}"}'

# Criar exemplo de perfil
curl -X POST http://localhost:5000/api/message \
  -H "Content-Type: application/json" \
  -d '{"text": "exemplo"}'
```

### 2. Exemplo de Perfil de Entrada

```json
{
  "nome": "Ana Silva",
  "idade": 28,
  "escolaridade": "Superior Completo",
  "area_formacao": "Administração de Empresas",
  "competencias_atuais": [
    {
      "area": "Excel",
      "nivel": "Avançado",
      "experiencia_anos": 5,
      "detalhes": "Domínio de fórmulas avançadas, tabelas dinâmicas"
    },
    {
      "area": "Python",
      "nivel": "Iniciante",
      "experiencia_anos": 1,
      "detalhes": "Conhecimento básico em automação"
    }
  ],
  "objetivos_carreira": [
    {
      "cargo_desejado": "Analista de Dados Sênior",
      "area_interesse": "Ciência de Dados",
      "prazo_anos": 2,
      "motivacao": "Combinar negócios com análise de dados"
    }
  ],
  "disponibilidade_estudo_horas_semana": 10,
  "preferencia_aprendizado": "Prático com projetos reais",
  "recursos_disponiveis": "Orçamento R$ 500/mês para cursos"
}
```

### 4. Testando Localmente

```bash
# Execute o teste de integração A2A completo
python run_test.py

# Teste específico via cliente A2A
python test_integration_a2a.py teste
```

## 📁 Estrutura do Projeto

```
career-path/
├── app/
│   ├── __init__.py            # Script principal CLI
│   ├── server.py              # Servidor A2A principal
│   ├── agent.py               # Lógica do agente IA
│   └── models.py              # Modelos de dados Pydantic
├── test_integration_a2a.py    # 🧪 Teste de integração A2A
├── run_test.py                # 🚀 Script para executar testes
├── TESTE_A2A.md              # 📖 Documentação do teste A2A
├── pyproject.toml             # Configuração do projeto
├── uv.lock                    # Lock file das dependências
└── README.md                  # Esta documentação
```

## 🔧 Desenvolvimento

### Executar Testes

#### 🧪 Teste de Integração A2A (Recomendado)

```bash
# Teste automático completo
python run_test.py

# Ou execute manualmente em 3 terminais:
# Terminal 1: python test_integration_a2a.py auxiliar
# Terminal 2: python test_integration_a2a.py principal
# Terminal 3: python test_integration_a2a.py teste
```

#### 🚀 Servidor Principal

```bash
# Inicie o servidor principal
python app/server.py

# Teste com curl
curl -X POST http://localhost:5000/api/message \
     -H "Content-Type: application/json" \
     -d '{"text": "Crie um exemplo de perfil"}'
```

### Configuração com Ollama

Para usar Ollama localmente:

```bash
# Instalar ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Baixar modelo recomendado
ollama pull llama3.1

# Executar servidor
ollama serve
```

## 🎉 Começar Agora

### 🧪 Teste Rápido (Recomendado)

```bash
# 1. Instalar dependências
uv sync

# 2. Configurar Ollama
ollama serve

# 3. Executar teste de integração A2A
python run_test.py
```

### 🚀 Para Desenvolvimento

```bash
# 1. Configurar variáveis de ambiente
cp .env.example .env
# Edite .env com suas API keys

# 2. Executar servidor principal
python app/server.py

# 3. Testar funcionalidades
python test_integration_a2a.py teste
```

### 📖 Próximos Passos

- **Para testar A2A**: Consulte [`TESTE_A2A.md`](./TESTE_A2A.md)
- **Para desenvolvimento**: Use o servidor principal em `app/server.py`
- **Para produção**: Configure autenticação e deploy adequado

## 🛠️ Personalização

### Adicionar Novas Skills

1. Defina novos modelos em `app/models.py`
2. Implemente a lógica em `app/agent.py`
3. Adicione skills ao servidor em `app/server.py`
4. Teste com `test_integration_a2a.py`
5. Documente as novas funcionalidades
