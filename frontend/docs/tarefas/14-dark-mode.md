# Tarefa 14 — Modo Escuro (Dark Mode com Toggle Manual)

## Objetivo

Implementar modo escuro na aplicação com botão de toggle no header, ao lado do botão "Sair". O tema é controlado por classe `.dark` no `<html>`, persistido em `localStorage`, e respeita a preferência do sistema como valor inicial.

## Contexto

A abordagem anterior (apenas `prefers-color-scheme: system`) não funcionou bem porque os componentes PrimeVue e as cores Tailwind hardcoded não se adaptaram de forma consistente. A nova abordagem usa toggle manual com classe CSS.

## Paleta de Cores — Dark Mode

Pensada para contraste acessível, consistência visual e conforto em ambientes escuros:

| Elemento | Light | Dark |
|---|---|---|
| Fundo principal (body/page) | `bg-gray-50` | `dark:bg-slate-900` |
| Fundo cards/containers | `bg-white` | `dark:bg-slate-800` |
| Fundo header | `bg-white` | `dark:bg-slate-800` |
| Bordas | `border-gray-200` | `dark:border-slate-700` |
| Texto primário | `text-gray-900` | `dark:text-gray-100` |
| Texto secundário | `text-gray-700` | `dark:text-gray-300` |
| Texto terciário/muted | `text-gray-500` | `dark:text-gray-400` |
| Texto quaternário | `text-gray-400` | `dark:text-gray-500` |
| Accent principal | `text-indigo-600` | `dark:text-indigo-400` |
| Accent bg (seleção, chips) | `bg-indigo-50` | `dark:bg-indigo-950` |
| Gradients login | `from-indigo-50 to-purple-100` | `dark:from-slate-900 dark:to-slate-800` |
| Gradients loading | `from-indigo-700 to-purple-800` | `dark:from-slate-900 dark:to-indigo-950` |
| Sugestões não selecionadas | `bg-gray-100 border-gray-200` | `dark:bg-slate-700 dark:border-slate-600` |
| Hover botões/cards | `hover:bg-gray-100` | `dark:hover:bg-slate-700` |
| Barra progresso bg | `bg-gray-100` | `dark:bg-slate-700` |
| Card concluída (ActionItem) | `bg-gray-50 opacity-60` | `dark:bg-slate-800/50` |
| Ícone delete hover | `text-gray-300 hover:text-red-500` | `dark:text-gray-500 hover:text-red-400` |
| Google button | `bg-white border-gray-300` | `dark:bg-slate-800 dark:border-slate-600` |

> Nota: usar `slate` em vez de `gray` no dark mode dá um tom levemente azulado que combina melhor com o accent indigo da aplicação.

## Entregáveis

### 1. Configuração PrimeVue — `main.ts`

Mudar `darkModeSelector` de `'system'` para `'.dark'`:

```typescript
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: { darkModeSelector: '.dark' },
  },
})
```

### 2. Configuração Tailwind CSS v4 — `main.css`

Tailwind v4 usa `prefers-color-scheme` por padrão para `dark:`. Precisamos mudar para selector `.dark`:

```css
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));
```

### 3. Composable `useTheme.ts` — `src/composables/useTheme.ts`

```typescript
// Responsabilidades:
// - Ler preferência do sistema (prefers-color-scheme) como valor inicial
// - Persistir escolha do usuário em localStorage (chave: 'mentoria-theme')
// - Adicionar/remover classe 'dark' no document.documentElement
// - Expor: theme (ref<'light'|'dark'>), isDark (computed), toggle()
```

Lógica:
1. Se existe valor em `localStorage` → usar esse
2. Se não → usar `prefers-color-scheme` do sistema
3. `toggle()` alterna e persiste
4. `watchEffect` aplica classe `.dark` no `<html>`

### 4. Botão de toggle no header — `DefaultLayout.vue`

- Adicionar botão entre o logo e o botão "Sair"
- Ícone: `Sun` (quando dark) / `Moon` (quando light) do Lucide
- Mesmo estilo do botão "Sair" (PrimeVue Button, severity secondary, text, small)
- `aria-label` descritivo: "Alternar para modo escuro" / "Alternar para modo claro"

### 5. Variantes dark em todos os componentes

Arquivos a alterar (18 arquivos):

**Layout:**
- `src/layouts/DefaultLayout.vue`

**Pages:**
- `src/pages/LoginPage.vue`
- `src/pages/HomePage.vue`
- `src/pages/OnboardingPage.vue`
- `src/pages/PlanDetailPage.vue`
- `src/pages/LoadingAIPage.vue`
- `src/pages/AuthCallbackPage.vue`

**Components — Home:**
- `src/components/home/PlanCard.vue`
- `src/components/home/EmptyState.vue`

**Components — Plan:**
- `src/components/plan/PlanHeader.vue`
- `src/components/plan/ProgressCard.vue` (já é escuro, verificar se precisa ajuste)
- `src/components/plan/GapsList.vue`
- `src/components/plan/ActionItem.vue`
- `src/components/plan/ActionTimeline.vue`

**Components — Onboarding:**
- `src/components/onboarding/StepTrajetoria.vue`
- `src/components/onboarding/StepFormacao.vue`
- `src/components/onboarding/StepHabilidades.vue`
- `src/components/onboarding/StepObjetivo.vue`
- `src/components/onboarding/StepRevisao.vue`

**Components — Auth:**
- `src/components/auth/GoogleLoginButton.vue`

### 6. LoginPage — dark mode sem header

A LoginPage não usa DefaultLayout, então o toggle não aparece lá. Isso é ok — ela segue a preferência já salva ou do sistema. Não precisa de toggle na tela de login.

## Regras de Implementação

1. Cada classe de cor light existente deve ganhar sua variante `dark:` correspondente conforme a paleta acima
2. Não remover as classes light — apenas adicionar as variantes dark ao lado
3. Usar `slate` (não `gray`) para backgrounds no dark mode para o tom azulado
4. Labels de formulário: `text-gray-700 dark:text-gray-300`
5. Textos muted: `text-gray-500 dark:text-gray-400`
6. Borders: `border-gray-200 dark:border-slate-700`
7. Backgrounds de cards: `bg-white dark:bg-slate-800`
8. Background principal: `bg-gray-50 dark:bg-slate-900`

## Ordem de Implementação

1. `main.ts` (darkModeSelector → `.dark`)
2. `main.css` (@custom-variant)
3. `composables/useTheme.ts`
4. `DefaultLayout.vue` (toggle + dark classes)
5. Demais componentes (um por um, seguindo a paleta)
6. Build final para validar

## Validação

- [ ] Toggle funciona e persiste entre reloads
- [ ] Preferência do sistema é respeitada no primeiro acesso
- [ ] Componentes PrimeVue (inputs, selects, buttons, datepickers, stepper, tags, chips, progressbar) reagem ao `.dark`
- [ ] Todos os textos têm contraste suficiente no dark mode
- [ ] Gradients da LoginPage e LoadingAIPage ficam coerentes
- [ ] Cards, borders e backgrounds seguem a paleta slate
- [ ] Build passa sem erros
