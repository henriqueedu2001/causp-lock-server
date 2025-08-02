# CAUSP-LOCK API

Backend em FastAPI para geração, assinatura e monitoramento de QR Codes em tranca eletrônica.

## Visão Geral

Este serviço expõe uma API REST para:

* Gerar e assinar QR Codes (payload + HMAC-SHA1).
* Persistir informações de cada QR (payload, assinatura, timestamps) em SQLite.
* Fornecer endpoints para criar, listar e inspecionar QRs (e, opcionalmente, servir as imagens).

## Pré-requisitos

* Python 3.8 ou superior
* Git (para clonar o repositório)
* `pip` e (opcional) `virtualenv`
* SQLite (embutido no Python, sem instalação extra)

## Instalação

1. **Clone o repositório**

   ```bash
   git clone <URL_DO_REPO> CAUSP-LOCK-SERVER
   cd CAUSP-LOCK-SERVER/api
   ```

2. **Crie e ative o ambiente virtual** (recomendado)

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # Linux/macOS
   # .\.venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

## Configuração de Variáveis de Ambiente

No diretório `api/`, crie um arquivo `.env` com:

```dotenv
DATABASE_URL=sqlite:///./qrcodes.db
SECRET_KEY=minha_chave_muito_secreta
```

* `DATABASE_URL`: caminho para o arquivo SQLite (persistente em disco).
* `SECRET_KEY`: string usada para gerar o HMAC (podendo ser texto simples ou hex).

> **Importante:** adicione `.env` ao seu `.gitignore` para não comitar informações sensíveis.

## Estrutura de Pastas

```
CAUSP-LOCK-SERVER/
├── api/                  # root do serviço FastAPI
│   ├── .venv/            # ambiente virtual
│   ├── .env              # variáveis de ambiente
│   ├── requirements.txt
│   ├── static/           # (opcional) arquivos de imagem gerados
│   │   └── qrcodes/
│   └── src/              # código-fonte da API
│       ├── main.py       # app FastAPI e configuração
│       ├── database.py   # engine e sessão SQLModel
│       ├── models.py     # definição do modelo QRCode
│       ├── crud.py       # funções de criação/listagem/consulta
│       ├── routers.py    # endpoints REST
│       ├── auth/         # módulos de chave secreta e assinatura
│       └── qr_code/      # encoder e generator de QR Codes
├── qrcode_lib/           # bibliotecas do QR (fora da API)
└── tests/                # testes unitários (encoder/generator)
```

## Executando o Servidor

No terminal, dentro de `CAUSP-LOCK-SERVER/api`:

```bash
source .venv/bin/activate      # ative o .venv
uvicorn src.main:app --reload  # inicia o servidor em http://127.0.0.1:8000
```

* `--reload` reinicia automaticamente ao detectar mudanças no código.

## Endpoints Disponíveis

### Documentação Interativa

* Swagger UI:  `GET /docs`
* ReDoc:        `GET /redoc`

### Gerenciamento de QR Codes

| Método             | Rota                                   | Descrição                                         |
| ------------------ | -------------------------------------- | ------------------------------------------------- |
| `GET`              | `/qrcodes/`                            | Lista todos os QRs cadastrados.                   |
| `POST`             | `/qrcodes/?payload=...&expires_at=...` | Cria um novo QR com payload e data de expiração.  |
| `GET`              | `/qrcodes/{id}`                        | Obtém detalhes de um QR específico.               |
| `GET`              | `/qrcodes/{id}/image`                  | Retorna a imagem PNG gerada em tempo de execução. |
| Arquivos estáticos | `/static/qrcodes/{id}.png`             | (Se configurado) serve o PNG salvo em disco.      |

## Exemplos com `curl`

```bash
# Listar todos os QRs
curl http://127.0.0.1:8000/qrcodes/

# Criar um QR (via query string)
curl -X POST "http://127.0.0.1:8000/qrcodes/?payload=usuario:matheus;door:mamadeira&expires_at=2025-08-05T12:00:00"

# Obter um QR específico
curl http://127.0.0.1:8000/qrcodes/1

# Buscar a imagem dinâmica
curl http://127.0.0.1:8000/qrcodes/1/image --output qr1.png
```

