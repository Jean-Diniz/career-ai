# Integração Career AI - Análise LinkedIn + Trilha de Estudos

## 📋 Resumo da Implementação

Esta integração permite que após a análise do LinkedIn de um usuário, seja automaticamente gerada uma trilha de estudos personalizada usando o agente career-path via python-a2a.

## 🏗️ Arquitetura

```
Usuário se cadastra → Análise LinkedIn (Ollama) → Geração de Trilha (Career-Path Agent) → Salva no Banco
```

## 🔧 Componentes Implementados

### 1. **Dockerfile para Career-Path**

- Criado `apps/career-path/Dockerfile` usando uv para gerenciar dependências
- Expõe porta 5000 para comunicação A2A

### 2. **Modelos de Dados**

- **StudyTrail**: Nova tabela para armazenar trilhas de estudos
- **Schema**: `StudyTrailCreate` e `StudyTrail` para validação
- **Relacionamentos**: User ↔ StudyTrail (one-to-many)

### 3. **Integração A2A**

- Adicionado `python-a2a` como dependência da API
- Função `enqueue_career_path_analysis()` para chamar o agente
- Conversão automática de análise LinkedIn para formato PerfilPessoa

### 4. **Endpoints da API**

- `/users/me/study-trails/` - Lista trilhas do usuário logado
- Processo automático após cadastro do usuário

### 5. **Docker Compose**

- Orquestração completa com todos os serviços
- Rede compartilhada `career-network`
- Volumes persistentes para dados

## 🚀 Como Usar

### 1. Subir o ambiente

```bash
docker-compose up -d
```

### 2. Cadastrar um usuário

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao",
    "email": "joao@email.com",
    "full_name": "João Silva",
    "password": "123456",
    "linkedin_url": "https://linkedin.com/in/joao-silva"
  }'
```

### 3. Verificar trilhas geradas

```bash
# Primeiro fazer login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=joao&password=123456"

# Usar o token para acessar trilhas
curl -X GET "http://localhost:8000/users/me/study-trails/" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 🔄 Fluxo de Execução

1. **Cadastro do Usuário**: API recebe dados + LinkedIn URL
2. **Análise LinkedIn**: Task em background chama Ollama
3. **Geração de Trilha**: Após análise, chama career-path agent
4. **Conversão de Dados**: LinkedIn analysis → PerfilPessoa format
5. **Chamada A2A**: `client.call_skill("Gerar Trilha de Estudos", profile_data)`
6. **Persistência**: Trilha salva no banco vinculada ao usuário

## 📊 Estrutura de Dados

### LinkedIn Analysis → PerfilPessoa

```json
{
  "nome": "João Silva",
  "escolaridade": "Superior",
  "area_formacao": "Tecnologia",
  "competencias_atuais": [
    {
      "area": "Python",
      "nivel": "intermediário",
      "experiencia_anos": 2,
      "detalhes": "Endorsements: 15"
    }
  ],
  "objetivos_carreira": [
    {
      "cargo_desejado": "Desenvolvedor Sênior",
      "area_interesse": "Tecnologia",
      "prazo_anos": 2,
      "motivacao": "Crescimento profissional"
    }
  ]
}
```

### StudyTrail (Banco)

```sql
CREATE TABLE study_trails (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    content TEXT NOT NULL,  -- JSON da trilha completa
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🛠️ Funcionalidades

- ✅ Análise automática do LinkedIn
- ✅ Geração de trilha personalizada
- ✅ Integração A2A com career-path
- ✅ Persistência no banco de dados
- ✅ API para consultar trilhas
- ✅ Dockerização completa
- ✅ Rede compartilhada entre serviços

## 📝 Configuração de Ambiente

### Variáveis necessárias:

```env
# API
DATABASE_URL=postgresql://user:password@db:5432/career_db
SECRET_KEY=your-secret-key-here
OLLAMA_MODEL=llama3.1
OLLAMA_ADDRESS=http://ollama:11434

# Career Path
DEFAULT_LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://ollama:11434
GOOGLE_API_KEY=optional-for-google-genai
```

## 🔍 Troubleshooting

### Verificar logs dos serviços:

```bash
docker-compose logs api
docker-compose logs career-path
docker-compose logs ollama
```

### Verificar conectividade A2A:

```bash
curl http://localhost:5000/health
```

### Verificar banco de dados:

```bash
docker-compose exec db psql -U user -d career_db -c "SELECT * FROM study_trails;"
```

## 🎯 Próximos Passos

1. **Interface Web**: Exibir trilhas na UI
2. **Refinamento**: Melhorar conversão LinkedIn → PerfilPessoa
3. **Notificações**: Alertar usuário quando trilha estiver pronta
4. **Customização**: Permitir edição manual dos perfis
5. **Analytics**: Métricas de uso das trilhas
