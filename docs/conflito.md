# Conflito de merge do Checkpoint 2

## O que entrou em conflito

No roteiro da Aula 02, as branches `feature/busca-id` e `feature/filtro-status` adicionam linhas
na mesma tabela de endpoints do `README.md`. O Git não consegue decidir a ordem/combinação das
duas edições e marca o trecho para resolução manual. A alteração correspondente no código Python
fica em arquivos/trechos distintos e pode ser integrada separadamente.

Um conflito desse tipo aparece com marcadores semelhantes a:

```text
<<<<<<< HEAD
| GET | `/tasks/{id}` | Busca uma tarefa pelo id |
=======
| GET | `/tasks?done=true` | Filtra tarefas por status |
>>>>>>> feature/filtro-status
```

## Como resolver

O resultado correto preserva as duas rotas. Depois de editar o README e remover os marcadores:

```bash
git switch main
git pull --ff-only
git switch feature/filtro-status
git merge main
# editar README.md: manter as duas linhas da tabela e remover os marcadores
git add README.md
git commit --no-edit
git push
```

## Evidência do Classroom

O professor solicita uma captura do PR mostrando o conflito antes da resolução, em
`docs/img/pr-conflito.png`. Essa imagem depende de abrir as branches e o PR no GitHub. Ela não
foi criada aqui, pois esta cópia não contém esse PR nem uma captura real; não substituí a evidência
por uma imagem simulada.

## Estado desta cópia

As rotas e a documentação local preservam ambas as linhas da tabela. Para concluir o fluxo
colaborativo da atividade, ainda faltam a publicação das branches, o PR, a revisão do colega, a
captura do conflito no GitHub e o merge aprovado.
