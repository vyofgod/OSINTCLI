import { writable } from 'svelte/store';
import type { FilterState, ResultType } from '$lib/types';

const DEFAULT_TYPES: ResultType[] = ['social', 'metadata', 'link', 'image'];

export const filters = writable<FilterState>({ confidence: 0, types: DEFAULT_TYPES });
