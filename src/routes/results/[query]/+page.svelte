<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import Sidebar from '$components/Sidebar.svelte';
  import ResultCard from '$components/ResultCard.svelte';
  import SkeletonCard from '$components/SkeletonCard.svelte';
  import EmptyState from '$components/EmptyState.svelte';
  import Header from '$components/Header.svelte';
  import Footer from '$components/Footer.svelte';
  import { useQuery, QueryClient, QueryClientProvider } from '@tanstack/svelte-query';
  import { search as apiSearch } from '$lib/api';
  import { filters } from '$stores/filters';
  import type { SearchResponse } from '$lib/types';
  import { exportPdf } from '$lib/pdf-templates';
  import { recentSearches } from '$stores/recentSearches';

  const queryClient = new QueryClient();

  export let data: { data: SearchResponse };

  const initial = data.data;

  const queryKey = ['search', initial.query];
  const query = useQuery<SearchResponse>(queryKey, async () => apiSearch(initial.query));

  onMount(() => {
    recentSearches.add(initial.query);
  });

  $: response = query.data ?? initial;

  function filteredResults() {
    const current = response.results;
    let res = current;
    const $f = $filters;
    if ($f.types.length) {
      res = res.filter((r) => $f.types.includes(r.type));
    }
    res = res.filter((r) => (r.confidence === 'high' ? 100 : r.confidence === 'medium' ? 60 : 30) >= $f.confidence);
    return res;
  }

  function exportAll() {
    exportPdf({ query: response.query, summary: response.summary, results: response.results, investigator: 'UmbraTrace Analyst' });
  }
</script>

<svelte:head>
  <title>Results for {response.query} | UmbraTrace</title>
</svelte:head>

<QueryClientProvider client={queryClient}>
  <div class="min-h-screen bg-background px-4 pb-10">
    <div class="mx-auto max-w-6xl">
      <Header />
      <main id="main" class="grid gap-6 md:grid-cols-[280px_1fr]" aria-live="polite">
        <div class="order-2 md:order-1">
          <Sidebar />
        </div>
        <section class="order-1 md:order-2 space-y-4">
          <div class="flex items-center justify-between rounded-2xl border border-outline/60 bg-surface/70 p-4 shadow-glow">
            <div>
              <p class="text-sm text-slate-400">Query</p>
              <h2 class="text-xl font-semibold">{response.query}</h2>
            </div>
            <div class="flex gap-2">
              <button
                class="rounded-lg border border-accent/60 bg-accent/10 px-3 py-2 text-sm text-cyan-100 hover:bg-accent/20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent"
                on:click={exportAll}
              >
                Export full PDF
              </button>
              <button
                class="rounded-lg border border-outline px-3 py-2 text-sm text-slate-200 hover:border-accent/70 focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent"
                on:click={() => goto('/')}
              >
                New search
              </button>
            </div>
          </div>

          <div class="grid gap-4 lg:grid-cols-[2fr_1fr]">
            <div class="space-y-3">
              {#if query.isLoading}
                {#each Array(3) as _}
                  <SkeletonCard />
                {/each}
              {:else if filteredResults().length === 0}
                <EmptyState />
              {:else}
                {#each filteredResults() as result (result.id)}
                  <ResultCard {result} />
                {/each}
              {/if}
            </div>
            <aside class="rounded-2xl border border-outline/60 bg-surface/60 p-4 shadow-inner space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm text-slate-400">Footprint</p>
                  <p class="text-2xl font-semibold">{response.summary.footprintScore}%</p>
                </div>
                <svg width="100" height="100" viewBox="0 0 36 36" aria-hidden="true">
                  <path
                    d="M18 2.0845a 15.9155 15.9155 0 0 1 0 31.831"
                    fill="none"
                    stroke="#1f2937"
                    stroke-width="3"
                  />
                  <path
                    d="M18 2.0845a 15.9155 15.9155 0 0 1 0 31.831"
                    fill="none"
                    stroke="#22d3ee"
                    stroke-dasharray={`${response.summary.footprintScore}, 100`}
                    stroke-width="3"
                  />
                  <text x="18" y="20.35" fill="#e5e7eb" font-size="8" text-anchor="middle">{response.summary.footprintScore}%</text>
                </svg>
              </div>
              <div>
                <p class="text-sm text-slate-400">Top locations</p>
                <ul class="mt-1 space-y-1 text-slate-200">
                  {#if response.summary.topLocations.length}
                    {#each response.summary.topLocations as loc}
                      <li>{loc}</li>
                    {/each}
                  {:else}
                    <li class="text-slate-500">No geo hints</li>
                  {/if}
                </ul>
              </div>
              <div>
                <p class="text-sm text-slate-400">Related identities</p>
                <ul class="mt-1 space-y-1 text-slate-200">
                  {#each response.results.slice(0,3) as r}
                    <li class="truncate">{r.handle ?? r.source}</li>
                  {/each}
                </ul>
              </div>
              <div class="text-xs text-slate-500">{new Date(response.timestamp).toLocaleString()}</div>
            </aside>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  </div>
</QueryClientProvider>
