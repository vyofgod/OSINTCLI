<div class="grid gap-4">
  {#each Array(3) as _, i}
    <div class="animate-shimmer shimmer rounded-xl border border-outline/50 bg-surface/60 p-4" aria-busy="true">
      <div class="h-5 w-1/4 bg-white/5 rounded mb-2"></div>
      <div class="h-3 w-1/2 bg-white/5 rounded"></div>
    </div>
  {/each}
</div>
