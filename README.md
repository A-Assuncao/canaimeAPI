# Canaimé API

API REST para extração e disponibilização de dados do sistema Canaimé, utilizando web scraping com Playwright.

## Funcionalidades

- Web scraping automatizado do sistema Canaimé
- Extração de dados de presos (Código, Ala, Cela e Nome)
- API REST com FastAPI para acesso aos dados
- Autenticação HTTP Basic para proteção dos endpoints
- Agendamento de tarefas para atualização periódica dos dados
- Deploy na Vercel

## Requisitos

- Python 3.13+
- Playwright
- FastAPI
- Pandas
- APScheduler
- Uvicorn

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/A-Assuncao/canaimeapi.git
cd canaimeapi
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
# No Windows
.venv\Scripts\activate
# No Linux/Mac
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -e .
```

4. Instale os navegadores do Playwright:
```bash
playwright install chromium
```

5. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## Uso

### Execução Local

Para iniciar a aplicação localmente:

```bash
python main.py
```

A API estará disponível em `http://127.0.0.1:8000`.

### Endpoints

- `/api/v1/dados` - Retorna os dados dos presos (requer autenticação)
- `/api/v1/status` - Retorna o status do serviço (requer autenticação)
- `/docs` - Documentação interativa da API

## Deploy na Vercel

Para fazer o deploy na Vercel, siga estes passos:

1. Instale a Vercel CLI:
```bash
npm install -g vercel
```

2. Faça login na Vercel:
```bash
vercel login
```

3. Configure as variáveis de ambiente na Vercel:
```bash
vercel env add
```
Adicione todas as variáveis do arquivo `.env.example`.

4. Faça o deploy:
```bash
vercel --prod
```

### Configurações Importantes para a Vercel

- A Vercel tem limitações de tempo de execução, o que pode afetar o scraping de sites mais complexos
- O Playwright na Vercel requer a configuração `PLAYWRIGHT_BROWSERS_PATH=0`
- Para funções agendadas na Vercel, considere usar Vercel Cron Jobs

## Estrutura do Projeto

```
canaimeapi/
├── api/                  # Diretório para integração com Vercel
│   ├── __init__.py
│   └── index.py          # Ponto de entrada para a Vercel
├── canaimeapi/
│   ├── api/              # Módulo da API
│   │   ├── __init__.py
│   │   ├── auth.py       # Autenticação
│   │   └── router.py     # Rotas da API
│   ├── scraper/          # Módulo de scraping
│   │   ├── __init__.py
│   │   └── crawler.py    # Scraper do Canaimé
│   ├── __init__.py
│   ├── app.py            # Aplicação FastAPI
│   └── scheduler.py      # Agendador de tarefas
├── .env.example          # Exemplo de variáveis de ambiente
├── .gitignore
├── main.py               # Ponto de entrada local
├── pyproject.toml        # Configuração do projeto
├── README.md
└── vercel.json           # Configuração da Vercel
```

## Licença

MIT
