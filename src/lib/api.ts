import type { FilterState, SearchResponse } from './types';

const headers = { 'Content-Type': 'application/json' };

export async function search(query: string, filters?: Partial<FilterState>): Promise<SearchResponse> {
  const params = new URLSearchParams({ q: query });
  if (filters?.confidence !== undefined) {
    params.set('confidence', String(filters.confidence));
  }
  if (filters?.types?.length) {
    params.set('types', filters.types.join(','));
  }
  const res = await fetch(`/api/search?${params.toString()}`, {
    headers,
    method: 'GET'
  });
  if (!res.ok) throw new Error('Search failed');
  return res.json();
}

export async function postSearch(query: string, filters?: Partial<FilterState>): Promise<SearchResponse> {
  const res = await fetch('/api/search', {
    method: 'POST',
    headers,
    body: JSON.stringify({ q: query, filters })
  });
  if (!res.ok) throw new Error('Search failed');
  return res.json();
}
