# Career AI - Análise de Carreira

Este é o módulo de análise de carreira do Career AI, responsável por processar e analisar dados de carreira dos usuários.

## Requisitos

- Python 3.12 ou superior
- [uv](https://github.com/astral-sh/uv) (gerenciador de pacotes Python)

## Configuração

1. Crie e ative um ambiente virtual:

```bash
# Usando virtualenv
uv venv
source .venv/bin/activate  # Linux/Mac
# ou
.\.venv\Scripts\activate  # Windows
```

2. Instale as dependências:

```bash
uv sync
```

3. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`
   - Preencha as variáveis necessárias, incluindo:
     - Chaves de API para serviços de IA
     - Configurações de banco de dados
     - Credenciais de serviços externos

## Desenvolvimento

Para iniciar o servidor de desenvolvimento:

```bash
uv run -m app.main
```

## Estrutura do Projeto

- `src/` - Código fonte principal
  - `analyzers/` - Analisadores de perfil
  - `models/` - Modelos de IA
  - `services/` - Serviços de processamento
  - `utils/` - Utilitários
- `tests/` - Testes automatizados
- `data/` - Dados de treinamento e modelos
- `scripts/` - Scripts de automação

## Scripts Disponíveis

- `ruff format .` - Formata o código
- `ruff check .` - Executa o linter

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Documentação da API

A documentação completa da API está disponível em `/docs` quando o servidor estiver rodando.
