<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { onMount } from 'svelte';
  import type { RecentSearchItem } from '$lib/types';

  export let value = '';
  export let suggestions: RecentSearchItem[] = [];
  export let placeholder = 'Search username, email, or phone';

  const dispatch = createEventDispatcher<{ search: string; input: string }>();

  let error = '';
  let inputEl: HTMLInputElement;

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function validate(term: string): boolean {
    error = '';
    if (term.includes('@') && !emailRegex.test(term)) {
      error = 'Please enter a valid email address.';
      return false;
    }
    const digits = term.replace(/\D/g, '');
    if (digits.length && digits.length < 7) {
      error = 'Phone numbers should be at least 7 digits.';
      return false;
    }
    if (!term.trim()) {
      error = 'Query cannot be empty.';
      return false;
    }
    return true;
  }

  function submit() {
    if (!validate(value)) return;
    dispatch('search', value.trim());
  }

  function onKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      event.preventDefault();
      submit();
    }
  }

  onMount(() => {
    inputEl?.focus();
  });
</script>

<div class="space-y-2" aria-live="polite">
  <label class="sr-only" for="search">UmbraTrace search</label>
  <div class="relative">
    <input
      bind:this={inputEl}
      id="search"
      class="w-full rounded-xl bg-surface/80 border border-outline px-4 py-3 text-lg shadow-inner text-slate-50 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-accent"
      bind:value
      on:keydown={onKeydown}
      on:input={(e) => dispatch('input', (e.target as HTMLInputElement).value)}
      autocomplete="off"
      aria-invalid={error ? 'true' : 'false'}
      aria-describedby={error ? 'search-error' : undefined}
      {placeholder}
    />
    <button
      class="absolute right-2 top-2 rounded-lg bg-accent/20 px-4 py-2 text-sm font-semibold text-cyan-100 border border-accent/40 hover:bg-accent/30 focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent"
      type="button"
      on:click={submit}
    >
      Search
    </button>
  </div>
  {#if error}
    <p id="search-error" class="text-sm text-rose-300" role="alert">{error}</p>
  {/if}
  {#if suggestions.length}
    <div class="rounded-lg border border-outline/60 bg-surface/70 p-2" role="list" aria-label="Recent searches">
      <div class="text-xs uppercase tracking-wide text-slate-400 px-2">Recent</div>
      {#each suggestions as item (item.term)}
        <button
          type="button"
          class="flex w-full items-center justify-between rounded-md px-3 py-2 text-left text-slate-200 hover:bg-surface/60 focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent"
          on:click={() => {
            value = item.term;
            submit();
          }}
        >
          <span>{item.term}</span>
          <span class="text-xs text-slate-500">{new Date(item.at).toLocaleDateString()}</span>
        </button>
      {/each}
    </div>
  {/if}
</div>
