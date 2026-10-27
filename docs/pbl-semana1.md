# PBL Semana 1: situação-problema EntregaJá

> **Disciplina:** DevOps Tools (ADS · UNIPAR · 2026)
> **Projeto:** TaskFlow, Checkpoint 1 (`v0.1`)
> **Autor:** Fellype Pires (@FellypePires)

## O cenário

A startup de delivery **EntregaJá** tem 3 desenvolvedores: Ana, Bruno e Carla. Eles trocam código por
pendrive e e-mail, em arquivos `.zip`. O servidor de produção é atualizado pela Ana, copiando arquivos por FTP.

Ontem, Bruno enviou uma correção no cálculo do frete. Ao copiar, ele sobrescreveu a tela de cupons que a
Carla fez na semana passada. Os clientes reclamaram, mas ninguém sabe qual versão está em produção nem como
recuperar o trabalho da Carla.

---

## 1. Diagnóstico

Referências usadas:

- **CALMS**: *Culture* (Cultura), *Automation* (Automação), *Lean* (Enxuto), *Measurement* (Medição), *Sharing* (Compartilhamento).
- **Três Caminhos** (*The DevOps Handbook*): **1º Fluxo** (do desenvolvimento para a produção), **2º Feedback** (da produção de volta para o desenvolvimento), **3º Aprendizado contínuo e experimentação**.

| # | Problema observado | Consequência no caso | Pilar CALMS / Caminho |
|---|---|---|---|
| 1 | **Não existe controle de versão.** O código circula em `.zip` por pendrive e e-mail, sem histórico de quem mudou o quê e quando. | A cópia do Bruno apagou a tela de cupons da Carla sem deixar rastro. Não há versão anterior para voltar. | **1º Caminho (Fluxo)**: o trabalho não flui de forma segura e rastreável até a produção. Também **Automation**: a integração do código é manual. |
| 2 | **Integração manual, sem merge.** Cada pessoa copia o próprio `.zip` por cima do código da outra. | Mudanças paralelas (frete × cupons) entram em conflito, e o conflito é "resolvido" apagando trabalho. | **Automation** (sem ferramenta que detecte conflitos) e **Lean** (retrabalho é desperdício: a Carla vai ter que refazer ou caçar o código). |
| 3 | **Ninguém sabe qual versão está em produção.** Deploy por FTP, feito à mão pela Ana, sem tag, release ou registro. | Na hora do problema, ninguém consegue dizer o que mudou nem voltar para a última versão boa. | **Measurement** (não há dado sobre o que foi publicado, quando e por quem) e **1º Caminho (Fluxo)**: não dá para ver o que está em produção. |
| 4 | **Quem avisou do erro foram os clientes.** Não há testes, revisão de código nem monitoramento antes ou depois do deploy. | O defeito chegou à produção e só foi notado por reclamação. | **2º Caminho (Feedback)**: o retorno chega tarde e pela pior fonte. |
| 5 | **Conhecimento e acesso concentrados.** Só a Ana publica, e cada dev só conhece o próprio pedaço. Não há revisão nem visibilidade do trabalho dos colegas. | A Ana é ponto único de falha. O Bruno não sabia que a tela da Carla existia. | **Culture** e **Sharing** (silos, sem responsabilidade compartilhada) e **3º Caminho (Aprendizado)**: o time não tem como aprender com o incidente, porque não sabe o que aconteceu. |

---

## 2. Proposta: fluxo mínimo com Git e GitHub (6 passos)

Fluxo baseado em *GitHub Flow*: a branch `main` é sempre a versão estável e publicável, e todo trabalho
nasce numa branch curta e volta por Pull Request.

1. **Clonar o repositório central (uma vez).**
   O código passa a morar num único repositório no GitHub. Ninguém mais troca `.zip`.
   ```bash
   git clone https://github.com/entregaja/app.git
   cd app
   ```

2. **Criar uma branch para cada tarefa, a partir da `main` atualizada.**
   ```bash
   git switch main
   git pull
   git switch -c fix/calculo-frete
   ```

3. **Trabalhar com commits pequenos e descritivos** (padrão *Conventional Commits*).
   ```bash
   git add .
   git commit -m "fix(frete): corrige arredondamento no cálculo por km"
   ```

4. **Enviar a branch e abrir um Pull Request no GitHub.**
   ```bash
   git push -u origin fix/calculo-frete
   ```
   No PR, um colega revisa o código. Se a `main` mudou nesse meio-tempo (por exemplo, a tela de cupons da
   Carla já entrou), o Git aponta o conflito, e ele é resolvido **juntando** as duas mudanças, sem apagar nenhuma.
   A `main` fica protegida (*branch protection*): só recebe código por PR aprovado.

5. **Fazer o merge na `main` e marcar a versão.**
   Depois da aprovação, o PR é mergeado e a versão que vai para produção recebe uma tag.
   ```bash
   git switch main
   git pull
   git tag -a v1.4.0 -m "Correção do frete"
   git push --tags
   ```

6. **Atualizar a produção a partir de uma tag, nunca da máquina de alguém.**
   O servidor recebe exatamente o que está na tag:
   ```bash
   # no servidor
   git fetch --tags
   git checkout v1.4.0
   ```
   Assim todos sabem qual versão está no ar (`git describe --tags` no servidor responde na hora). Nas próximas
   semanas esse passo vira automático (CI/CD), sem acesso manual ao servidor.

---

## 3. Recuperação: como trazer a tela de cupons da Carla de volta

Com Git, o trabalho da Carla **não se perde**: o commit dela continua no histórico mesmo depois que outro
commit sobrescreveu os arquivos. A recuperação leva poucos minutos.

**a) Encontrar quando a tela de cupons existia e quando foi removida**
```bash
git log --oneline -- src/telas/cupons/       # histórico só da pasta de cupons
git log --oneline --author="Carla"           # commits da Carla
git log -p -S "CupomForm"                    # commit que adicionou/removeu esse trecho
```

**b) Ver exatamente o que o commit do Bruno mudou**
```bash
git show a1b2c3d --stat                      # a1b2c3d = commit "fix(frete)" do Bruno
```

**c) Recuperar, escolhendo uma das opções:**

- **Restaurar só os arquivos de cupons** a partir do último commit bom da Carla, mantendo a correção do frete:
  ```bash
  git switch -c fix/restaura-cupons
  git restore --source=9f8e7d6 -- src/telas/cupons/   # 9f8e7d6 = commit da Carla
  git commit -m "fix(cupons): restaura tela de cupons sobrescrita"
  ```
- **Desfazer o commit inteiro do Bruno** (se ele só trouxe problema), criando um commit novo que inverte o anterior
  sem reescrever o histórico:
  ```bash
  git revert a1b2c3d
  ```

**d) Publicar a correção pelo fluxo normal:** `git push`, Pull Request, revisão, merge na `main` e nova tag (`v1.4.1`).

Se a branch da Carla ainda existir no GitHub (`feat/tela-cupons`), basta fazer o merge dela de novo na `main`.
E mesmo que algum commit tenha sumido de todas as branches, o `git reflog` local guarda as referências por
semanas.

Na prática, com o fluxo da seção 2 esse incidente nem teria acontecido: o PR do Bruno mostraria um conflito
com a `main`, ou um diff apagando a pasta de cupons, e o revisor barraria antes do merge.

---

## 4. Risco: o que o Git sozinho não resolve

**O deploy manual por FTP continua sendo um ponto cego.**

O Git controla o **código no repositório**, mas não controla **o que está no servidor**. Enquanto a Ana
copiar arquivos por FTP:

- ela pode subir arquivos da pasta local dela, que podem ter alterações não commitadas, estar numa branch
  errada ou estar desatualizada em relação à `main`;
- uma cópia parcial ou interrompida deixa a produção num estado misto (metade da versão nova, metade da
  antiga), que não corresponde a **nenhum** commit;
- alguém pode editar um arquivo direto no servidor (*hotfix* por FTP), e essa mudança nunca volta para o Git.
  O próximo deploy apaga essa correção, e o problema se repete;
- não há registro de quem publicou, quando, nem qual tag. O rollback continua manual e lento;
- nada impede que código sem teste ou sem revisão vá para produção.

Ou seja, mesmo com Git perfeito, **o repositório e a produção podem divergir**, e voltamos ao "ninguém sabe
qual versão está no ar".

**Como mitigar (próximas semanas do TaskFlow):**

- **CI** (GitHub Actions): rodar os testes (`pytest`) em todo PR e bloquear o merge se falharem.
- **CD**: o deploy é feito por um pipeline a partir de uma tag ou da `main`, nunca pela máquina de alguém.
  Acaba o acesso manual por FTP.
- **Artefato imutável** (imagem Docker versionada pela tag): o que roda em produção é exatamente o que foi testado,
  e o rollback é só voltar para a imagem anterior.
- **Monitoramento**: o time descobre o problema antes do cliente (2º Caminho, Feedback).
