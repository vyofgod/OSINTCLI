import { writable } from 'svelte/store';

type Theme = 'dark' | 'light';

function createThemeStore() {
  const initial: Theme = (typeof localStorage !== 'undefined' && (localStorage.getItem('theme') as Theme)) || 'dark';
  const { subscribe, set, update } = writable<Theme>(initial);

  const apply = (value: Theme) => {
    if (typeof document !== 'undefined') {
      document.documentElement.classList.toggle('dark', value === 'dark');
      document.documentElement.classList.toggle('light', value === 'light');
    }
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem('theme', value);
    }
  };

  return {
    subscribe,
    toggle: () =>
      update((curr) => {
        const next = curr === 'dark' ? 'light' : 'dark';
        apply(next);
        return next;
      }),
    set: (value: Theme) => {
      apply(value);
      set(value);
    }
  };
}

export const theme = createThemeStore();
