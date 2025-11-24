export type Confidence = 'high' | 'medium' | 'low';

export type ResultType = 'social' | 'metadata' | 'link' | 'image';

export interface SearchResult {
  id: string;
  type: ResultType;
  source: string;
  handle?: string;
  platform?: string;
  confidence: Confidence;
  lastSeen?: string;
  profileUrl?: string;
  avatarUrl?: string | null;
  metadata: Record<string, unknown>;
}

export interface SearchSummary {
  footprintScore: number;
  matchCount: number;
  topLocations: string[];
}

export interface SearchResponse {
  query: string;
  timestamp: string;
  summary: SearchSummary;
  results: SearchResult[];
}

export interface FilterState {
  confidence: number;
  types: ResultType[];
}

export interface RecentSearchItem {
  term: string;
  at: string;
}

export interface PdfReportPayload {
  query: string;
  summary: SearchSummary;
  results: SearchResult[];
  investigator?: string;
}
