# Situação-problema: EduTech Saber

> **Disciplina:** DevOps Tools (ADS · UNIPAR · 2026)
> **Projeto:** TaskFlow, Checkpoint 3 (`v0.3`)
> **Autor:** Fellype Pires (@FellypePires)

## Cenário

A EduTech Saber publica uma plataforma de ensino. As mudanças ficam semanas em branches,
os testes manuais acontecem perto da entrega e bugs conhecidos voltam a aparecer. A equipe
quer encurtar o feedback sem parar as releases.

## 1. Diagnóstico: problemas e práticas de CI

| Problema do processo | Prática de CI que ajuda |
| --- | --- |
| Branches longas só são integradas antes do lançamento. | Integrar frequentemente em branches curtas e sincronizar com a branch principal. |
| Testes manuais concentrados no fim do ciclo. | Automatizar testes e executá-los a cada push e Pull Request. |
| Erros de estilo e integração são percebidos tarde. | Rodar lint e testes no pipeline e publicar um resultado visível no PR. |
| Bugs corrigidos voltam em alterações futuras. | Criar teste de regressão para cada bug conhecido antes ou junto da correção. |

## 2. Pipeline proposto

1. **Checkout do commit** — o pipeline verifica exatamente o código enviado no push/PR.
2. **Preparação do Python e dependências** — usa Python 3.12 e instala as versões declaradas.
3. **Lint com Ruff** — acusa problemas simples e inconsistências antes de executar a suíte.
4. **Testes automatizados com cobertura** — executa `pytest` e exige pelo menos 70% de cobertura.
5. **Resultado obrigatório no PR** — o check verde permite solicitar revisão/merge; o vermelho
   aponta o log para corrigir. Em `main`, o mesmo fluxo mantém feedback após cada push.

Executar o pipeline em todo PR oferece feedback rápido antes do merge. A verificação no push
para `main` também cobre commits integrados e ajuda a detectar regressões.

## 3. Teste de regressão para `nota_final(n1, n2)`

Sem uma regra de cálculo fornecida no enunciado, assumo que a nota final é a média aritmética
das duas notas e que cada nota deve estar entre 0 e 10:

```python
import pytest

from app.notas import nota_final


@pytest.mark.parametrize(
    ("n1", "n2", "esperado"),
    [(8, 6, 7), (0, 10, 5), (7.5, 8.5, 8)],
)
def test_nota_final_calcula_media(n1, n2, esperado):
    assert nota_final(n1, n2) == esperado


@pytest.mark.parametrize("nota", [-0.1, 10.1])
def test_nota_final_rejeita_nota_fora_da_faixa(nota):
    with pytest.raises(ValueError):
        nota_final(nota, 7)
```

Esse é um exemplo de teste para o caso proposto; o repositório TaskFlow não possui módulo de
notas, portanto o código é ilustrativo e não foi conectado à API de tarefas.

## 4. Adoção sem interromper as releases

- Manter o calendário atual enquanto o pipeline roda primeiro em modo informativo, sem bloquear
  os merges existentes.
- Começar pelos bugs já conhecidos: reproduzir cada um com um teste de regressão, corrigir e
  deixar o teste permanente na suíte.
- Tornar o check obrigatório primeiro em um fluxo pequeno ou projeto piloto, acompanhando tempo
  de execução e falsos positivos.
- Corrigir falhas do pipeline em branches curtas; reservar uma pequena capacidade de cada ciclo
  para testes e estabilidade.
- Depois de a equipe confiar nos resultados, exigir o check verde em PRs e ampliar a cobertura
  gradualmente, sem tentar atingir 100% de uma vez.
