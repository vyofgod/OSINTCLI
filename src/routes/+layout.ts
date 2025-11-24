import type { LayoutLoad } from './$types';

export const load: LayoutLoad = ({ data, url }) => {
  const theme = data?.theme ?? (typeof localStorage !== 'undefined' ? localStorage.getItem('theme') : null);
  return { theme: theme ?? 'dark', url: url.pathname };
};
