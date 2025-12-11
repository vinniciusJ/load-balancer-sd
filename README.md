# Balanceador de Carga com NGINX e FastAPI

Este projeto consiste na implementação prática de uma arquitetura de **Sistema Web Distribuído**, desenvolvido como parte da avaliação da disciplina de **Sistemas Distribuídos (2025)**.

O objetivo é demonstrar conceitos fundamentais como **Balanceamento de Carga (Load Balancing)**, **Escalabilidade Horizontal**, **Replicação** e **Tolerância a Falhas**.

---

## Arquitetura da Solução

A solução utiliza **Docker Compose** para orquestrar um ambiente isolado contendo:

* **1x Load Balancer (NGINX):** Atua como Proxy Reverso e ponto único de entrada (Gateway). Recebe o tráfego na porta `8080` e o distribui entre os nós de processamento.

* **3x Servidores de Aplicação (FastAPI):** Réplicas idênticas da aplicação (nós) que processam as requisições. Cada nó possui uma identidade única (`SERVER_NAME`) para fins de demonstração.

O algoritmo de distribuição utilizado pelo NGINX é o **Round-Robin** (padrão), que alterna as requisições sequencialmente entre os servidores disponíveis.

---

## Pré-requisitos

Para executar este projeto, é necessário ter instalado no ambiente:

* [Docker Engine](https://docs.docker.com/engine/install/)

* [Docker Compose](https://docs.docker.com/compose/install/)

---

## Estrutura de Arquivos

A organização do projeto segue o padrão de containerização de microserviços:

```text
.
├── .venv/                   # Ambiente virtual Python
├── app/
│   ├── __pycache__/         # Arquivos de cache compilados do Python
│   └── main.py              # Código fonte da aplicação FastAPI
├── nginx/
│   └── nginx.conf           # Arquivo de configuração do Load Balancer
├── static/
│   └── css/
│       └── styles.css       # Folhas de estilo CSS
├── templates/
│   └── index.html           # Template HTML (Jinja2)
├── .gitignore               # Arquivos ignorados pelo Git
├── .python-version          # Versão do Python definida
├── compose.yml              # Orquestração dos containers (Docker Compose)
├── Dockerfile               # Receita de criação da imagem Docker
├── pyproject.toml           # Definição do projeto e dependências (uv)
├── README.md                # Documentação do projeto
└── uv.lock                  # Arquivo de bloqueio de versões (Lockfile)
```
---

## Como Executar

### Passo a passo

1. Clone o repositório (ou extraia os arquivos na pasta desejada).

2. Abra o terminal na raiz do projeto (onde está o arquivo `compose.yml`).

3. Execute o comando de build e inicialização:

    ```bash
    docker compose up --build
    ```
    _Aguarde até que os logs indiquem que o `nginx` e os servidores (`server_01` a `server_03`) foram iniciados._

---

## Cenários de teste

### Teste de distribuição

1. Abra o navegador em: `http://localhost:8080`

2. Atualize a página várias vezes (`F5` ou `Ctrl+R`).

3. Resultado Esperado: A identificação do servidor e a cor de fundo devem alternar ciclicamente:
    - Requisição 1: Servidor 01
    - Requisição 2: Servidor 02
    - Requisição 3: Servidor 03
    - Requisição 4: Servidor 01 (Reinício do ciclo)

### Teste de Tolerância a Falhas

1. Mantenha o sistema rodando.

2. Em um terminal separado, simule a queda de um dos nós:

    ```bash
    docker stop server_02
    ```
3. Volte ao navegador e continue atualizando a página.

4. Resultado Esperado:

    - O sistema **NÃO** sai do ar (Erro 502 momentâneo pode ocorrer apenas na transição)

    - O NGINX detecta a falha e passa a distribuir o tráfego apenas entre `server_01` e `server_03`.

### Recuperação do Sistema

1. Reinicie o nó que falhou:

    ```bash
    docker start server_02
    ```

2. Resultado Esperado: O servidor 02 volta a receber requisições automaticamente.
---

## Tecnologias e Ferramentas

- **Linguagem**: Python 3.10
- **Framework**: FastAPI
- **Servidor Web/Proxy**: NGINX
- **Containerização**: Docker
- **Frontend**: HTML5 + CSS3 + Jinja2 Templates

---

## Autores

- Nikoly Cover Pereira
- Vinicius de Oliveira Jimenez