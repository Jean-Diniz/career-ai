FROM ollama/ollama:latest

RUN ollama serve & \
    sleep 10 && \
    ollama pull llama3.2 && \
    pkill ollama

EXPOSE 11434

ENTRYPOINT ["sh", "-c", "\
  ollama serve & \
  echo 'Ollama ready.' && wait \
"]
