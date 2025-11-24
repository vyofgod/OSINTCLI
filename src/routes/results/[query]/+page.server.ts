import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params, url }) => {
  const apiUrl = new URL('/api/search', url);
  apiUrl.searchParams.set('q', params.query);
  const res = await fetch(apiUrl);
  const data = await res.json();
  return { data };
};
