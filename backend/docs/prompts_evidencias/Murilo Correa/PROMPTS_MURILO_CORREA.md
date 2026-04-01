# Prompts - Murilo Correa

## PROMPT 01
Eu preciso que você extraia o modelo do gemini para colocar dentro da variável de ambiente .env

## PROMPT 02
Usando github cli e os steerings de [commit-messages.md](../../../.kiro/steering/commit-messages.md), [git-workflow.md](../../../.kiro/steering/git-workflow.md) faça o commit da feature e crie um pull request

## PROMPT 03
Elabore todos os testes unitários do modulo de backend
- Utilize o Pytest
- Arquivos de testes devem começar com "test_"
- Utilizar estrutura AAA (Arrange, Act, Assert)
- Utilizar mocks isolando banco de dados e APIs
- Utilizar fixtures para conexões e objetos compartilhados, facilitando a reutilização e limpeza de código

## PROMPT 04
Execute todos os testes unitários contidos no backend

## PROMPT 05
Você pode alterar os testes para utilizar uma alternativa ao datetime.utcnow() que não esteja depreciada?

## PROMPT 06
Altere os arquivos de testes do backend para que os mocks contemplem a dialética do postgresql e não sqlite
