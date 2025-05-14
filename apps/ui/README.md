# Career AI - Interface de Usuário

Este é um projeto [Next.js](https://nextjs.org) que serve como a interface principal do Career AI.

## Requisitos

- Node.js 18.x ou superior
- [Bun](https://bun.sh) 1.0 ou superior

## Configuração

1. Instale as dependências:

```bash
bun install
```

2. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env.local`
   - Preencha as variáveis necessárias

## Desenvolvimento

Para iniciar o servidor de desenvolvimento:

```bash
bun dev
```

Acesse [http://localhost:3000](http://localhost:3000) no seu navegador para ver o resultado.

## Estrutura do Projeto

- `app/` - Diretório principal da aplicação
- `components/` - Componentes reutilizáveis
- `styles/` - Arquivos de estilo
- `public/` - Arquivos estáticos

## Scripts Disponíveis

- `bun dev` - Inicia o servidor de desenvolvimento
- `bun build` - Cria a build de produção
- `bun start` - Inicia o servidor de produção
- `bun lint` - Executa o linter
- `bun test` - Executa os testes

## Tecnologias Utilizadas

- Next.js 14
- React
- Tailwind CSS
- TypeScript
- Bun (runtime e gerenciador de pacotes)

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request
