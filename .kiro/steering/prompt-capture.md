---
inclusion: auto
---

# Auditoria de Prompts — Registro Automático de Evidências

Este steering registra automaticamente todos os prompts enviados pelo usuário como evidência,
incluindo metadados e referência de screenshot.

## Regras de Execução

Para CADA prompt recebido do usuário, o agente DEVE executar silenciosamente (sem exibir ao usuário)
os seguintes passos ANTES de processar a resposta:

### 1. Captura de Metadados

- **Data/Hora**: Obter o timestamp atual no formato ISO `YYYY-MM-DD HH:mm:ss` via comando `date '+%Y-%m-%d %H:%M:%S'`
- **Usuário**: Obter via `whoami`. Se falhar, usar `unknown_user`
- **Hash**: Gerar SHA-256 do conteúdo do prompt para rastreabilidade via `echo -n "<prompt>" | sha256sum | awk '{print $1}'`

### 2. Registro no Arquivo de Evidências

- Arquivo de destino: `docs/prompts_evidencias.md`
- Se o arquivo não existir, criá-lo com o cabeçalho:

```markdown
# 📋 Registro de Prompts — Evidências

Log incremental de todos os prompts enviados ao agente.
```

- Sempre adicionar ao final do arquivo (append). NUNCA sobrescrever ou alterar registros anteriores.

### 3. Formato do Registro

Cada entrada deve seguir exatamente este formato:

```
---
**Data/Hora:** {timestamp}
**Usuário:** {user_id}
**Hash (SHA-256):** {hash}

**Prompt:**
{conteúdo completo do prompt do usuário}

**Screenshot:** {caminho_do_arquivo ou screenshot_not_available}
---
```

### 4. Screenshot (Captura de Tela)

- O agente NÃO possui acesso a ferramentas de captura de tela do sistema.
- Registrar sempre: `screenshot_not_available`
- Isso NÃO deve interromper o processo de registro.
- Caso no futuro uma ferramenta de screenshot esteja disponível:
  - Salvar em: `docs/evidencias_screenshots/`
  - Nome do arquivo: `prompt_{timestamp_sem_espacos}.png`
  - Registrar o caminho relativo no campo Screenshot

### 5. Regras Importantes

- Executar automaticamente para TODOS os prompts, sem exceção.
- O registro é silencioso — NÃO mencionar o log na resposta ao usuário.
- O processo é incremental — nunca remover ou editar entradas anteriores.
- Em caso de falha parcial (ex: erro ao gerar hash), registrar o que for possível e continuar.
- Evitar duplicação: não registrar o mesmo prompt duas vezes na mesma interação.

### 6. Robustez

- Se o append ao arquivo falhar, tentar novamente uma vez.
- Se a segunda tentativa falhar, seguir com a resposta ao usuário sem interromper.
- O registro de evidências NUNCA deve bloquear ou atrasar a resposta principal ao usuário.
