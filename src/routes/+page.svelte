<script lang="ts">
  import Header from '$components/Header.svelte';
  import SearchBar from '$components/SearchBar.svelte';
  import Footer from '$components/Footer.svelte';
  import { goto } from '$app/navigation';
  import { recentSearches } from '$stores/recentSearches';
  import type { PageData } from './$types';

  export let data: PageData;

  const ogSvg = encodeURIComponent(
    `<svg xmlns='http://www.w3.org/2000/svg' width='400' height='200'><rect width='400' height='200' fill='#0b1220'/><text x='40' y='110' fill='#22d3ee' font-size='32' font-family='Inter'>UmbraTrace</text></svg>`
  );

  function handleSearch(term: string) {
    recentSearches.add(term);
    goto(`/results/${encodeURIComponent(term)}`);
  }
</script>

<svelte:head>
  <title>UmbraTrace | Shadow-grade OSINT</title>
  <meta name="description" content="UmbraTrace surfaces cross-network OSINT evidence with exportable reports." />
  <meta property="og:title" content="UmbraTrace OSINT" />
  <meta property="og:description" content="Dark, professional OSINT workspace with mock data." />
  <meta property="og:image" content={`data:image/svg+xml,${ogSvg}`} />
</svelte:head>

<div class="min-h-screen bg-background px-4 pb-10">
  <div class="mx-auto max-w-5xl">
    <Header />
    <main id="main" class="mt-8 space-y-10" aria-label="Main content">
      <section class="rounded-2xl border border-outline/60 bg-surface/60 p-8 shadow-glow">
        <div class="flex flex-col gap-2">
          <p class="text-sm uppercase tracking-[0.2em] text-accent">UmbraTrace</p>
          <h1 class="text-3xl font-semibold text-slate-50">Shadow-grade OSINT search</h1>
          <p class="text-slate-400">Query usernames, emails, or phone numbers. We render realistic mock intelligence instantly.</p>
        </div>
        <div class="mt-6">
          <SearchBar
            placeholder="Search username, email, or phone"
            on:search={(e) => handleSearch(e.detail)}
            suggestions={$recentSearches}
          />
        </div>
        {#if $recentSearches.length}
          <div class="mt-4 flex flex-wrap gap-2 text-sm text-slate-400">
            {#each $recentSearches as item (item.term)}
              <span class="flex items-center gap-2 rounded-full border border-outline/60 px-3 py-1">
                <button class="hover:text-accent" on:click={() => handleSearch(item.term)}>{item.term}</button>
                <button aria-label={`Remove ${item.term}`} on:click={() => recentSearches.remove(item.term)}>✕</button>
              </span>
            {/each}
          </div>
        {/if}
      </section>

      <section class="grid gap-4 rounded-2xl border border-outline/60 bg-surface/60 p-6 shadow-inner md:grid-cols-2">
        <div class="space-y-2">
          <h2 class="text-xl font-semibold">Capabilities</h2>
          <p class="text-slate-400">UmbraTrace focuses on verifiable intelligence and export-ready evidence.</p>
        </div>
        <ul class="space-y-2 text-slate-200">
          {#each data.capabilities as item}
            <li class="flex items-center gap-2">
              <span class="text-accent">◆</span>
              <span>{item}</span>
            </li>
          {/each}
        </ul>
      </section>
    </main>
    <Footer />
  </div>
</div>
