# CRUD_POO

Aplicação na lingaguem Python, onde por meio da Programação Orientada Objeto (POO), cadastra equipamentos e vulnerabilidades.

# Gerenciador de Ativos de TI e Vulnerabilidades

O **Gerenciador de Ativos** é uma aplicação em linha de comando desenvolvida em Python utilizando Programação Orientada a Objetos (POO). O sistema permite cadastrar, consultar, atualizar e deletar dispositivos de rede (Notebooks, Smart TVs, Smartphones, etc.), além de associar e gerenciar vulnerabilidades de segurança para cada ativo.

Os dados são persistidos automaticamente em um arquivo local no formato JSON (array de objetos) e a aplicação está totalmente pronta para ser executada de forma resiliente dentro de containers Docker.

#🚀 Funcionalidades

- ***CRUD de Ativos***: Cadastro, leitura, atualização e exclusão de equipamentos com ID único.
- ***Gestão de Vulnerabilidades***: Associação de falhas de segurança aos ativos com níveis de severidade (Baixa, Média, Alta, Crítica) e status (Aberta, Em tratamento, Corrigida, Aceita).
- ***Persistência em JSON***: Salvamento automático e carregamento reativo de dados para evitar perdas.

# 🛠️ Tecnologias Utilizadas

- **Python 3.14.4** (POO, Manipulação de JSON e manipulação dinâmica de atributos)
