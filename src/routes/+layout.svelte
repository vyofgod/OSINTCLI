<script lang="ts">
  import '$styles/globals.css';
  import { onMount } from 'svelte';
  import { theme } from '$stores/theme';

  onMount(() => {
    const unsubscribe = theme.subscribe((value) => {
      document.documentElement.classList.toggle('dark', value === 'dark');
      document.documentElement.classList.toggle('light', value === 'light');
    });
    return unsubscribe;
  });
</script>

<svelte:head>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
</svelte:head>
<a href="#main" class="skip-link">Skip to content</a>
<slot />
