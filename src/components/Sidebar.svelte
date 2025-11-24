<script lang="ts">
  import { page } from '$app/stores';
  import { derived, get } from 'svelte/store';
  import { filters } from '$stores/filters';
  import type { ResultType } from '$lib/types';
  import { goto } from '$app/navigation';

  const typeOptions: ResultType[] = ['social', 'metadata', 'link', 'image'];

  const filterText = derived(filters, ($f) => `${$f.confidence}+ | ${$f.types.length} types`);

  function toggleType(type: ResultType) {
    filters.update((curr) => {
      const exists = curr.types.includes(type);
      const nextTypes = exists ? curr.types.filter((t) => t !== type) : [...curr.types, type];
      updateUrl({ types: nextTypes });
      return { ...curr, types: nextTypes };
    });
  }

  function updateConfidence(value: number) {
    filters.update((curr) => {
      updateUrl({ confidence: value });
      return { ...curr, confidence: value };
    });
  }

  function updateUrl(partial: { confidence?: number; types?: ResultType[] }) {
    const current = new URL(get(page).url);
    if (partial.confidence !== undefined) current.searchParams.set('c', String(partial.confidence));
    if (partial.types) current.searchParams.set('types', partial.types.join(','));
    goto(`${current.pathname}?${current.searchParams.toString()}`, { replaceState: true, keepfocus: true, noScroll: true });
  }
</script>

<aside class="w-full space-y-6 rounded-2xl bg-surface/60 p-4 shadow-glow border border-outline/60">
  <div class="flex items-center justify-between">
    <div>
      <p class="text-sm text-slate-400">Filters</p>
      <p class="text-lg font-semibold">Signal refine</p>
    </div>
    <span class="text-xs text-slate-500" aria-live="polite">{ $filterText }</span>
  </div>
  <div>
    <label class="flex items-center justify-between text-sm text-slate-300" for="confidence">Minimum confidence</label>
    <input
      id="confidence"
      type="range"
      min="0"
      max="100"
      step="10"
      class="w-full accent-accent"
      on:change={(e) => updateConfidence(Number((e.target as HTMLInputElement).value))}
      aria-valuemin="0"
      aria-valuemax="100"
      aria-valuenow={$filters.confidence}
    />
    <p class="text-xs text-slate-500">{$filters.confidence}% or higher</p>
  </div>
  <div class="space-y-3">
    <p class="text-sm text-slate-300">Sources</p>
    {#each typeOptions as type}
      <label class="flex items-center gap-3 text-slate-200">
        <input
          type="checkbox"
          class="h-4 w-4 rounded border-outline bg-surface/80"
          checked={$filters.types.includes(type)}
          on:change={() => toggleType(type)}
        />
        <span class="capitalize">{type}</span>
      </label>
    {/each}
  </div>
</aside>
