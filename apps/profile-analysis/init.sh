#!/bin/sh

ollama serve &
sleep 10
ollama pull llama3.2
pkill ollama
ollama serve
