FROM ollama/ollama:latest

COPY init.sh /init.sh
RUN chmod +x /init.sh

EXPOSE 11434

ENTRYPOINT ["/init.sh"]
