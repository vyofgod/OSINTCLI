<script lang="ts">
  import { onMount } from 'svelte';
  import type { SearchResult } from '$lib/types';
  import { badgeForPlatform, confidenceColor, confidenceLabel, formatTimestamp } from '$lib/format';
  import { exportPdf } from '$lib/pdf-templates';

  export let result: SearchResult;

  let expanded = false;
  let JsonModal: typeof import('./JsonModal.svelte').default | null = null;
  let showJson = false;

  onMount(async () => {
    const module = await import('./JsonModal.svelte');
    JsonModal = module.default;
  });

  function avatarFor(result: SearchResult): string {
    if (result.avatarUrl) return result.avatarUrl;
    const label = (result.handle ?? result.source ?? 'U').slice(0, 2).toUpperCase();
    const hash = Array.from(label).reduce((acc, char) => acc + char.charCodeAt(0), 0);
    const hue = hash % 360;
    return `data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64'><rect width='64' height='64' fill='hsl(${hue},60%,20%)'/><text x='32' y='38' font-size='22' text-anchor='middle' fill='%23e5e7eb' font-family='Inter'>${label}</text></svg>`;
  }

  function downloadSinglePdf() {
    exportPdf(
      {
        query: result.handle ?? result.source,
        summary: { footprintScore: 10, matchCount: 1, topLocations: [] },
        results: [result]
      },
      `${result.handle ?? 'result'}.pdf`
    );
  }
</script>

<article class="rounded-xl border border-outline/70 bg-surface/80 p-4 shadow-md focus-within:outline focus-within:outline-2 focus-within:outline-accent" tabindex="0">
  <header class="flex items-center gap-4">
    <img src={avatarFor(result)} alt={`Avatar for ${result.handle ?? result.source}`} loading="lazy" class="h-12 w-12 rounded-full border border-outline object-cover" />
    <div class="flex-1">
      <div class="flex items-center gap-2">
        <p class="text-lg font-semibold">{result.handle ?? result.source}</p>
        <span class="rounded-full border px-2 py-0.5 text-xs {confidenceColor(result.confidence)}">{confidenceLabel(result.confidence)}</span>
        <span class="rounded-full bg-white/5 px-2 py-0.5 text-xs text-slate-300">{badgeForPlatform(result.platform)}</span>
      </div>
      <p class="text-sm text-slate-400">{result.profileUrl ?? result.source}</p>
    </div>
    <div class="text-right text-xs text-slate-500">
      <p>Last seen</p>
      <p>{formatTimestamp(result.lastSeen)}</p>
    </div>
  </header>

  <div class="mt-3 text-sm text-slate-200">
    {#if result.metadata.bio}
      <p>{result.metadata.bio as string}</p>
    {:else}
      <p>Data points available: {Object.keys(result.metadata).length}</p>
    {/if}
  </div>

  <div class="mt-4 flex gap-3">
    <button
      class="rounded-lg border border-outline px-3 py-2 text-sm text-slate-200 hover:border-accent/70 focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent"
      type="button"
      on:click={() => (expanded = !expanded)}
    >
      {expanded ? 'Hide' : 'Expand'} details
    </button>
    <button
      class="rounded-lg border border-outline px-3 py-2 text-sm text-slate-200 hover:border-accent/70 focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent"
      type="button"
      on:click={() => (showJson = true)}
      disabled={!JsonModal}
    >
      Open JSON
    </button>
    <button
      class="rounded-lg border border-accent/60 bg-accent/10 px-3 py-2 text-sm text-cyan-100 hover:bg-accent/20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent"
      type="button"
      on:click={downloadSinglePdf}
    >
      Export PDF
    </button>
  </div>

  {#if expanded}
    <div class="mt-4 space-y-2 rounded-lg bg-background/80 p-3 text-sm text-slate-100 border border-outline/60" aria-label="Metadata">
      {#each Object.entries(result.metadata) as [key, value]}
        <div class="flex justify-between gap-3 border-b border-outline/40 pb-1 last:border-0">
          <span class="text-slate-400">{key}</span>
          <span class="text-right">{typeof value === 'object' ? JSON.stringify(value) : String(value)}</span>
        </div>
      {/each}
    </div>
  {/if}

  {#if JsonModal && showJson}
    <svelte:component this={JsonModal} data={result} on:close={() => (showJson = false)} />
  {/if}
</article>
