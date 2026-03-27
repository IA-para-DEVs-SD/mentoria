# 📋 Registro de Prompts — Evidências

Log incremental de todos os prompts enviados ao agente.

---
**Data/Hora:** 2026-03-26 07:30:00
**Usuário:** taiane
**Hash (SHA-256):** 909afdc3e856f45dfe383c6eb79da1c446d1b4233cf5a66e9345d9c4c2806f0e

**Prompt:**
Com base no arquivo Requisitos.me crie sugira 3 tasks necessárias, definindo título e descrição do que deve ser feito.

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 07:40:00
**Usuário:** taiane
**Hash (SHA-256):** 2128f222fd673537474ff5efb82d6d8cd8968a22fdf35f6e8240911966e17ca2

**Prompt:**
Atualize o reame.md com base nesses tópicos: Padrão de tópicos do README Nome do Projeto Breve descrição do projeto Sumário de documentações Tecnologias utilizadas Instruções de instalação / uso Integrantes do grupo: Willian Silvano Maira é nosso Bardo do time; Taiane Baldin é nossa Paladna do time; e os demais são os Magos do time: Murilo Henrique da Silva Pires; Murilo Barcelos Corrêa; Paulo Sérgio Nunes Gonçalves.

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 07:45:00
**Usuário:** taiane
**Hash (SHA-256):** 75cbf655cd6460de1209a21824d4f9a0867e3a9f9ffceece5f9fbecdcd1480dc

**Prompt:**
Realise um commit nessa branch seguindo o seguinte padrão de versionamento semântico: "tipo: breve descrição descrição mais detalhada (opcional)" Tipos: feat: Nova funcionalidade docs: Documentações fix: Correções refactor: Refatorações tests: Testes unitários, etc

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 07:47:00
**Usuário:** taiane
**Hash (SHA-256):** 1e84eec4ebcbceaa43e9ebd78aad0f6558bc7f4fbd5262a8f8287ba18e9bd114

**Prompt:**
faça

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 07:50:00
**Usuário:** taiane
**Hash (SHA-256):** d01397160fded165265fef993b425081f23a50f573c816b8b0ab1898c7f6c09d

**Prompt:**
gere um steering para criação de user stories que são issues dentro do github dentro do seguinte board https://github.com/orgs/IA-para-DEVs-SD/projects/24/views/2. Você deve gerar o título e a descrição da task.

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 07:55:00
**Usuário:** taiane
**Hash (SHA-256):** 55ebe2d2426991a3e710ccb408a5516fb2f151f8b7e4b719513039b9b1ca25c4

**Prompt:**
gere as tasks no github, separando tasks para frontend e backend para cada uma das user stories do PRD (Requisitos.md)

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 08:00:00
**Usuário:** taiane
**Hash (SHA-256):** 63e9afe5eab783c308b16bb6411bf9b568b3cc24f37e81140362b352a0cf30ee

**Prompt:**
crie uma task para dockerização do projeto

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 08:03:00
**Usuário:** taiane
**Hash (SHA-256):** 63a62699079821db1ea3ef2b01916ec835666d6ad2fa7c151ef312074c22ebb9

**Prompt:**
ajuste o steering gitbub-issues.md para sempre que uma task for criada ela seja vinculada ao board do projeto https://github.com/orgs/IA-para-DEVs-SD/projects/24

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 08:06:00
**Usuário:** taiane
**Hash (SHA-256):** 5ec8b633deb2215a67de31acc3ca2f5d4cdedcb5320292fc70e172ec1f88fb3e

**Prompt:**
commite a feature issue-40

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 08:08:00
**Usuário:** taiane
**Hash (SHA-256):** 32d45252b4be4e028de6f9afddf053db1b1371a06c7ed25acb12cdb69aeaeb44

**Prompt:**
crie o pull request

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 08:10:00
**Usuário:** taiane
**Hash (SHA-256):** 9ba040f4e92f9c07f337139c5cfa0a398940a2479ef6aef6b88279fe46dc0bdd

**Prompt:**
faça o pull request

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 08:12:00
**Usuário:** taiane
**Hash (SHA-256):** 53492957fe09fbdeb1aa0f7921a7a5446983afdcb3a9fe3d6fb8a177c6246eb7

**Prompt:**
crie uma task de ajuste do steering github-issues

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 08:15:00
**Usuário:** taiane
**Hash (SHA-256):** ff6bc305b127fe49846f31ece8c57aa9020e18674518a60a0ac22c8e1a4e03ab

**Prompt:**
crie uma issue para elaboração do steering das capturas dos prompts

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 08:21:06
**Usuário:** taiane
**Hash (SHA-256):** 7fcbf267e1bc53d44824cc19c180af850fb1ee099c517aec8537900dc17a58c6

**Prompt:**
Agora sim, com a branch correta, Quero que você crie um STEERING RULE persistente para auditoria de prompts utilizados pelo usuário. Objetivo: Registrar automaticamente todos os prompts enviados pelo usuário como evidência, incluindo metadados e, se possível, captura de tela (print). Requisitos: 1. Para cada prompt recebido: Capturar o conteúdo completo do prompt, Capturar data e hora no formato ISO (YYYY-MM-DD HH:mm:ss), Identificar o usuário. 2. Estrutura de armazenamento: Salvar no arquivo /docs/prompts_evidencias.md, sempre append, nunca sobrescrever. 3. Formato padronizado com separadores. 4. Screenshot com fallback. 5. Processo silencioso e incremental. 6. Robustez contra falhas parciais. 7. Hash SHA-256 para rastreabilidade.

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 08:25:00
**Usuário:** taiane
**Hash (SHA-256):** 47221785dc97703703726a324e3e64e61a3941e33b3fdc672c7ddd2068555925

**Prompt:**
agora commite a branch e gere o pull request

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 08:28:00
**Usuário:** taiane
**Hash (SHA-256):** 8ee3a49a045b80c32405361985f31be23bc1a1b06c1e977e9343af82e994a334

**Prompt:**
commite as alterações realizadas

**Screenshot:** screenshot_not_available
---

---
**Data/Hora:** 2026-03-26 08:32:00
**Usuário:** taiane
**Hash (SHA-256):** b4f0eb44c512194b8d8f66af0d1467850d72e51778909911fdcbb73c455adb8a

**Prompt:**
atuelize o prompt_evidencias.md com os prompts que temos no histórico por favor

**Screenshot:** screenshot_not_available
---
