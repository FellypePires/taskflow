# TaskFlow

API REST de tarefas em Python (FastAPI). Projeto-base da disciplina **DevOps Tools** (ADS · UNIPAR · 2026).

> Este repositório começa **sem nenhuma automação**. A cada semana, sua dupla adiciona uma camada DevOps:
> versionamento → colaboração → CI → containers e deploy → infraestrutura como código → monitoramento.

## Endpoints

| Método | Rota | O que faz |
| --- | --- | --- |
| GET | `/tasks` | Lista todas as tarefas |
| GET | `/tasks/{id}` | Busca uma tarefa pelo id; retorna 404 se não existir |
| GET | `/tasks?done=true` ou `?done=false` | Filtra tarefas por status; sem parâmetro, lista todas |
| POST | `/tasks` | Cria uma tarefa (`{"title": "...", "done": false}`) |
| PUT | `/tasks/{id}` | Atualiza uma tarefa |
| DELETE | `/tasks/{id}` | Remove uma tarefa |

Os dados ficam em memória: reiniciou a API, as tarefas somem.

## Como rodar

Requisito: Python 3.12 ou mais recente.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abra <http://127.0.0.1:8000/docs> para testar os endpoints pelo navegador.

## Como testar

```bash
pytest
```

## Estrutura

```
app/main.py          # a API
tests/test_tasks.py  # 3 testes automatizados
requirements.txt     # dependências com versões fixas
```

---

## Checkpoint 1 (tag `v0.1`): o que sua dupla deve fazer

- [x] Fazer **fork** deste repositório e adicionar o colega como *collaborator* (trabalho individual, sem collaborator)
- [x] Criar um `.gitignore` para Python (inclua `.venv/` e `__pycache__/`)
- [x] Fazer **pelo menos 5 commits** no padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/), dos dois integrantes (trabalho individual)
- [x] Substituir a seção "Integrantes" abaixo e completar este README
- [ ] Adicionar o print do `git log --graph --oneline` do laboratório
- [x] Criar `docs/pbl-semana1.md` com a situação-problema EntregaJá
- [x] Criar a tag: `git tag v0.1` e `git push --tags`

## Checkpoint 2 (tag `v0.2`)

- `GET /tasks/{id}` retorna a tarefa ou HTTP 404.
- `GET /tasks?done=true|false` filtra por status; sem parâmetro, lista tudo.
- Os testes das duas funcionalidades ficam em arquivos separados em `tests/`.
- `docs/pbl-semana2.md` e `docs/conflito.md` registram as atividades da Aula 02.

O código deste checkpoint está preparado em commits locais. Os links de PR, a revisão por
outra pessoa e a evidência visual do conflito precisam corresponder a ações reais no GitHub;
nenhuma delas foi registrada nesta cópia local.

## Integrantes

- Fellype Pires (@FellypePires)
