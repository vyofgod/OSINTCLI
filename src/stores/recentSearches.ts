import { writable } from 'svelte/store';
import type { RecentSearchItem } from '$lib/types';

const STORAGE_KEY = 'umbratrace.recent';

function loadInitial(): RecentSearchItem[] {
  if (typeof localStorage === 'undefined') return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    return JSON.parse(raw) as RecentSearchItem[];
  } catch (e) {
    console.error('Failed to parse recent searches', e);
    return [];
  }
}

function persist(value: RecentSearchItem[]) {
  if (typeof localStorage === 'undefined') return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(value.slice(0, 10)));
}

function createStore() {
  const { subscribe, update, set } = writable<RecentSearchItem[]>(loadInitial());
  return {
    subscribe,
    add: (term: string) =>
      update((items) => {
        const filtered = items.filter((i) => i.term !== term);
        const next = [{ term, at: new Date().toISOString() }, ...filtered];
        persist(next);
        return next;
      }),
    remove: (term: string) =>
      update((items) => {
        const next = items.filter((i) => i.term !== term);
        persist(next);
        return next;
      }),
    set: (items: RecentSearchItem[]) => {
      persist(items);
      set(items);
    }
  };
}

export const recentSearches = createStore();
