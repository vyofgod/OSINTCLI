<script lang="ts">
  import { theme } from '$stores/theme';
  import { derived } from 'svelte/store';

  const label = derived(theme, ($t) => ($t === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'));
</script>

<button
  type="button"
  class="rounded-full border border-outline bg-surface/80 px-3 py-2 text-sm text-slate-200 shadow-sm hover:border-accent/70 focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent"
  on:click={() => theme.toggle()}
  aria-label={$label}
>
  <span aria-hidden="true">🌓</span>
</button>
