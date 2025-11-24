<script lang="ts">
  import Logo from './Logo.svelte';
  import ThemeToggle from './ThemeToggle.svelte';
</script>

<header class="flex items-center justify-between gap-4 py-4" role="banner">
  <div class="flex items-center gap-3">
    <Logo />
    <p class="text-sm text-slate-400 hidden sm:block">Shadow-grade OSINT workspace</p>
  </div>
  <ThemeToggle />
</header>
