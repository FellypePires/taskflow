# Situação-problema: PagaFácil

> **Disciplina:** DevOps Tools (ADS · UNIPAR · 2026)
> **Projeto:** TaskFlow, Checkpoint 2 (`v0.2`)
> **Autor:** Fellype Pires (@FellypePires)

## Cenário

A fintech PagaFácil tem 12 desenvolvedores e usa GitFlow. As features ficam em branches por
duas a quatro semanas, chegam à `develop` e são publicadas em releases mensais após uma semana
de testes manuais. Uma falha de segurança no login precisa ser corrigida hoje, embora a próxima
release esteja prevista para daqui a três semanas.

## 1. Correção de segurança hoje

O hotfix parte da versão que está em produção. Assim, só a correção de segurança vai para a
release urgente; as demais features ainda não aprovadas não são incluídas.

```bash
git switch main
git pull --ff-only
git switch -c hotfix/corrige-falha-login
# implementar e revisar a correção mínima
git add app/login.py tests/test_login.py
git commit -m "fix(login): corrige falha de autenticação"
git push -u origin hotfix/corrige-falha-login
```

Abre-se um Pull Request pequeno e urgente. Após revisão e testes, o hotfix é integrado à branch
de produção e recebe uma tag de release. Se a linha de produção for `release/1.4`, a mesma
correção deve também chegar à `develop` para não reaparecer na próxima versão:

```bash
git switch release/1.4
git cherry-pick <hash-do-commit-do-hotfix>
# publicar a release corrigida após revisão e validação
git switch develop
git cherry-pick <hash-do-commit-do-hotfix>
```

O hash deve ser obtido com `git log --oneline`; o cherry-pick copia somente o commit da correção.
Em um fluxo sem branches de release permanentes, a equipe pode abrir o hotfix a partir da `main`
e integrá-lo via PR, propagando depois a correção para as branches ainda mantidas.

## 2. Problemas do processo atual

| Problema | Ligação com a aula |
| --- | --- |
| Branches de feature duram semanas e se afastam da linha principal. | Branches longas acumulam divergência e tornam conflitos e integração mais caros. |
| Mudanças chegam em lotes grandes, em vez de integrar continuamente. | Contraria Lean e o 1º Caminho (Fluxo); defeitos e conflitos só aparecem perto da release. |
| Uma correção de três linhas espera três semanas e uma semana de testes manuais. | Falta fluxo rápido e feedback automatizado; o lote e a espera aumentam o risco de segurança. |
| A correção urgente pode não voltar para `develop`. | Falta sincronização entre linhas mantidas; o mesmo defeito pode reaparecer. |

## 3. Estratégia recomendada

Recomendo evoluir para GitHub Flow: `main` protegida, branches curtas, PRs pequenos, revisão e
CI obrigatório antes do merge. Isso reduz a distância entre mudanças e torna possível liberar
correções pequenas sem esperar uma release mensal. Enquanto houver versões antigas em suporte,
manteria branches de release apenas para essas versões e aplicaria nelas os hotfixes necessários.
Trunk-based pode ser uma etapa posterior, quando os testes, a CI e as feature flags forem confiáveis.

## 4. O que precisa existir antes da transição

- Suíte de testes automatizados para os fluxos críticos, começando por falhas conhecidas.
- CI em cada PR, com testes e verificações obrigatórias para proteger `main`.
- Revisão de código e branches curtas com responsáveis e critérios de merge definidos.
- Estratégia para propagar correções às versões ainda suportadas e para voltar uma release.
- Ambiente de staging e monitoramento para validar a correção após publicar.

Esses controles permitem aumentar a frequência de entrega com feedback rápido sem remover as
proteções necessárias para uma fintech.
