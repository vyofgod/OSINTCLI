import type { RequestHandler } from './$types';
import { computeFootprint, fuzzyMatch, mergeDuplicates, mockResults, topLocations } from '$lib/mock-data';
import type { FilterState, SearchResult } from '$lib/types';

function applyFilters(results: SearchResult[], filters?: Partial<FilterState>): SearchResult[] {
  let res = results;
  if (filters?.types?.length) {
    res = res.filter((r) => filters.types!.includes(r.type));
  }
  if (filters?.confidence !== undefined) {
    res = res.filter((r) => (r.confidence === 'high' ? 100 : r.confidence === 'medium' ? 60 : 30) >= filters.confidence);
  }
  return res;
}

async function respond(query: string, filters?: Partial<FilterState>) {
  const matches = query ? fuzzyMatch(query) : [];
  const deduped = mergeDuplicates(matches);
  const filtered = applyFilters(deduped, filters);
  const summary = {
    footprintScore: computeFootprint(filtered),
    matchCount: filtered.length,
    topLocations: topLocations(filtered)
  };
  const response = {
    query,
    timestamp: new Date().toISOString(),
    summary,
    results: filtered
  };
  return new Response(JSON.stringify(response), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=60'
    }
  });
}

async function artificialLatency() {
  const ms = 200 + Math.random() * 700;
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export const GET: RequestHandler = async ({ url }) => {
  const q = url.searchParams.get('q') ?? '';
  const filters: Partial<FilterState> = {};
  const conf = url.searchParams.get('confidence') ?? url.searchParams.get('c');
  if (conf) filters.confidence = Number(conf);
  const types = url.searchParams.get('types');
  if (types) filters.types = types.split(',') as FilterState['types'];
  await artificialLatency();
  return respond(q, filters);
};

export const POST: RequestHandler = async ({ request }) => {
  const body = await request.json();
  const q = body.q ?? '';
  const filters = body.filters as Partial<FilterState> | undefined;
  await artificialLatency();
  return respond(q, filters);
};
