FROM ollama/ollama:latest

EXPOSE 11434

ENTRYPOINT ["sh", "-c", "\
  ollama serve & \
  echo 'Waiting for Ollama to start...' && sleep 10 && \
  echo 'Pulling model llama3.2...' && ollama pull llama3.2 && \
  echo 'Ollama ready.' && wait \
"]
