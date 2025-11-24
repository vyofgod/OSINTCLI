<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let data: Record<string, unknown>;
  const dispatch = createEventDispatcher<{ close: void }>();

  function copy() {
    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
  }

  function download() {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'result.json';
    a.click();
    URL.revokeObjectURL(url);
  }
</script>

<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4" role="dialog" aria-modal="true">
  <div class="w-full max-w-2xl rounded-2xl bg-background border border-outline p-4 shadow-glow">
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-lg font-semibold">Record JSON</h2>
      <button
        class="rounded-full border border-outline px-3 py-1 text-sm text-slate-200 hover:border-accent/70 focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent"
        on:click={() => dispatch('close')}
      >
        Close
      </button>
    </div>
    <pre class="max-h-96 overflow-auto rounded-lg bg-surface/80 p-3 text-xs text-slate-100">{JSON.stringify(data, null, 2)}</pre>
    <div class="mt-3 flex gap-2">
      <button
        class="rounded-lg border border-outline px-3 py-2 text-sm text-slate-200 hover:border-accent/70 focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent"
        on:click={copy}
      >
        Copy JSON
      </button>
      <button
        class="rounded-lg border border-accent/60 bg-accent/10 px-3 py-2 text-sm text-cyan-100 hover:bg-accent/20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent"
        on:click={download}
      >
        Download JSON
      </button>
    </div>
  </div>
</div>
