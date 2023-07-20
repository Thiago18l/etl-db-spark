#!/bin/bash
#Author: Thiago lopes

log_date=$(date +"%Y-%m-%d %H:%M:%S")

load_env_file() {
  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ $line =~ ^[[:alnum:]] ]]; then
      export "$line"
    fi
  done < "$1"
}

ENV_FILE=".env"

if [ -f $ENV_FILE ]; then
    load_env_file $ENV_FILE
    
    # executa o programa
    run

      # Desfaz a exportação das variáveis
    unset DATABASE_URL
    unset DEBUG
    unset PATH_FILES
else
    echo "$log_date - DEBUG - ERRO CÓDIGO: $? - ENV NÃO ENCONTRADO" 2>&1
fi