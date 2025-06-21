## Construção da Imagem

```bash
docker build -t ollama-image:dev .
```

## Execução do Container

```bash
docker run --rm -p 11434:11434 --name ollama-server ollama-image:dev
```

## Verificando o Serviço

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
        "model": "llama3.2",
        "prompt": "Olá, como você está hoje?",
        "parameters": {
          "max_tokens": 128,
          "temperature": 0.7
        },
        "stream": false
      }'
```