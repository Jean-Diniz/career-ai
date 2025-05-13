# Career AI - Plano de Execução

## 1. Planejamento & Arquitetura

### 1.1 Definição da Arquitetura

- [ ] Criar diagrama de arquitetura geral do sistema
- [ ] Definir padrões de comunicação entre serviços
- [ ] Estabelecer protocolos de segurança e autenticação
- [ ] Documentar decisões técnicas e trade-offs

### 1.2 Estruturação dos Agentes

- [ ] Definir responsabilidades do Agente 1 (Análise de Perfil)
  - [ ] Escopo de análise do LinkedIn
  - [ ] Formato do diagnóstico gerado
  - [ ] Pontos de integração com o sistema principal
- [ ] Definir responsabilidades do Agente 2 (Trilhas e Avaliação)
  - [ ] Processo de análise de vagas
  - [ ] Lógica de geração de trilhas
  - [ ] Sistema de avaliação e feedback

### 1.3 Comunicação entre Serviços

- [ ] Definir protocolo de comunicação (gRPC/REST)
- [ ] Estabelecer formato de mensagens
- [ ] Implementar sistema de filas (RabbitMQ/Redis)
- [ ] Definir estratégia de fallback e retry

## 2. Infraestrutura

### 2.1 Containerização

- [ ] Criar Dockerfile para cada serviço
  - [ ] Backend FastAPI
  - [ ] Agente 1 (LinkedIn Analysis)
  - [ ] Agente 2 (Career Path)
  - [ ] Frontend Next.js
- [ ] Configurar Docker Compose
  - [ ] Definir redes internas
  - [ ] Configurar volumes
  - [ ] Estabelecer dependências entre serviços

### 2.2 Configuração de Ambiente

- [ ] Criar arquivo .env.example
- [ ] Definir variáveis de ambiente necessárias
- [ ] Configurar secrets management
- [ ] Estabelecer ambientes (dev/prod)

## 3. Backend (FastAPI)

### 3.1 Autenticação e Cadastro

- [ ] Implementar sistema de autenticação
- [ ] Criar endpoints de cadastro
- [ ] Integrar com LinkedIn OAuth
- [ ] Implementar validação de perfis

### 3.2 Serviços Core

- [ ] Serviço de Análise de Perfil
  - [ ] Endpoints de integração com Agente 1
  - [ ] Sistema de cache de análises
  - [ ] Validação de dados
- [ ] Serviço de Trilhas
  - [ ] Integração com Agente 2
  - [ ] Sistema de progresso
  - [ ] Gerenciamento de recursos

### 3.3 Banco de Dados

- [ ] Definir schema do banco
- [ ] Implementar migrations
- [ ] Criar modelos de dados
- [ ] Configurar índices e otimizações

## 4. Agentes de IA

### 4.1 Agente 1 (LinkedIn Analysis)

- [ ] Implementar parser do LinkedIn
- [ ] Criar sistema de análise de perfil
- [ ] Desenvolver gerador de diagnóstico
- [ ] Implementar sistema de feedback

### 4.2 Agente 2 (Career Path)

- [ ] Criar analisador de vagas
- [ ] Implementar gerador de trilhas
- [ ] Desenvolver simulador de entrevistas
- [ ] Criar sistema de avaliação

## 5. Frontend (Next.js)

### 5.1 Estrutura Base

- [ ] Configurar projeto Next.js
- [ ] Implementar tema e estilos
- [ ] Configurar shadcn-ui
- [ ] Estabelecer padrões de componentes

### 5.2 Páginas Principais

- [ ] Página de Cadastro
  - [ ] Formulário de LinkedIn
  - [ ] Validações
  - [ ] Feedback visual
- [ ] Interface de Chat
  - [ ] Componente de chat
  - [ ] Sistema de mensagens
  - [ ] Indicadores de status
- [ ] Dashboard
  - [ ] Visualização de perfil
  - [ ] Progresso da trilha
  - [ ] Configurações

## 6. Chat-First Interaction

### 6.1 Sistema de Comandos

- [ ] Implementar parser de comandos
- [ ] Criar sistema de intenções
- [ ] Desenvolver feedback contextual
- [ ] Implementar histórico de interações

### 6.2 Integrações

- [ ] Conectar com serviço de trilhas
- [ ] Integrar com sistema de avaliação
- [ ] Implementar notificações
- [ ] Criar sistema de lembretes

## 7. Documentação

### 7.1 Técnica

- [ ] Documentar arquitetura
- [ ] Criar diagramas de sequência
- [ ] Documentar APIs
- [ ] Criar guias de troubleshooting

### 7.2 Usuário

- [ ] Criar README principal
- [ ] Documentar comandos do chat
- [ ] Criar guias de uso
- [ ] Preparar FAQs

## Próximos Passos

1. Iniciar com a definição da arquitetura e estruturação dos agentes
2. Configurar ambiente de desenvolvimento com Docker
3. Implementar autenticação e integração com LinkedIn
4. Desenvolver os agentes de forma independente
5. Criar interface de chat como ponto central de interação
6. Implementar sistema de trilhas e avaliação
7. Adicionar testes e monitoramento
8. Finalizar documentação

## Observações Importantes

- Manter foco na experiência via chat
- Garantir modularidade dos agentes
- Priorizar segurança e privacidade dos dados
- Manter código limpo e bem documentado
- Implementar feedback contínuo do usuário
