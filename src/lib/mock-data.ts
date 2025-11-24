import type { SearchResult } from './types';

interface MockRecord extends SearchResult {
  aliases?: string[];
  emails?: string[];
  phones?: string[];
  locationHint?: string;
}

export const mockResults: MockRecord[] = [
  {
    id: 'tw-hydraclaw',
    type: 'social',
    source: 'Twitter',
    platform: 'Twitter',
    handle: 'hydra_claw',
    confidence: 'high',
    lastSeen: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
    profileUrl: 'https://twitter.com/hydra_claw',
    avatarUrl: 'https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?auto=format&fit=crop&w=200&q=60',
    metadata: {
      bio: 'Threat intel analyst. Shadow networks researcher.',
      followers: 12800,
      following: 320,
      languages: ['en', 'es'],
      tags: ['osint', 'threat-intel']
    },
    aliases: ['umbra analyst'],
    emails: ['hydra@protonmail.com'],
    locationHint: 'Reykjavík'
  },
  {
    id: 'gh-hydraclaw',
    type: 'social',
    source: 'GitHub',
    platform: 'GitHub',
    handle: 'hydra-claw',
    confidence: 'medium',
    lastSeen: new Date(Date.now() - 1000 * 60 * 60 * 24 * 9).toISOString(),
    profileUrl: 'https://github.com/hydra-claw',
    avatarUrl: null,
    metadata: {
      repos: 42,
      company: 'Umbra Labs',
      location: 'Reykjavík',
      languages: ['TypeScript', 'Rust']
    },
    emails: ['hydra@umbra.dev']
  },
  {
    id: 'ig-cipher',
    type: 'social',
    source: 'Instagram',
    platform: 'Instagram',
    handle: 'ciphertrace',
    confidence: 'low',
    lastSeen: new Date(Date.now() - 1000 * 60 * 60 * 72).toISOString(),
    profileUrl: 'https://instagram.com/ciphertrace',
    avatarUrl: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=200&q=60',
    metadata: {
      posts: 120,
      followers: 5600,
      bio: 'Urban exploration + crypto privacy',
      links: ['https://ciphertrace.example/blog']
    },
    aliases: ['ciph3r'],
    phones: ['+12065550111'],
    locationHint: 'Berlin'
  },
  {
    id: 'email-breach',
    type: 'metadata',
    source: 'Leaked Dataset',
    confidence: 'high',
    metadata: {
      email: 'hydra@protonmail.com',
      breach: 'Nightfall Archive 2023',
      passwordHash: 'sha1$8206...redacted',
      salt: 'xv2',
      ip: '185.64.12.10'
    },
    aliases: ['hydra_claw'],
    emails: ['hydra@protonmail.com'],
    locationHint: 'Iceland'
  },
  {
    id: 'phone-signal',
    type: 'metadata',
    source: 'Carrier Lookup',
    confidence: 'medium',
    metadata: {
      phone: '+447911123456',
      carrier: 'Shadow Mobile',
      country: 'UK',
      active: true
    },
    phones: ['+447911123456'],
    locationHint: 'London'
  },
  {
    id: 'darkweb-link',
    type: 'link',
    source: 'Darkweb Monitor',
    confidence: 'low',
    metadata: {
      url: 'http://oniondomain.hidden/posts/umbra',
      context: 'Forum post mentioning alias "umbra analyst"',
      risk: 'medium'
    },
    aliases: ['umbra analyst']
  },
  {
    id: 'img-recon',
    type: 'image',
    source: 'Reverse Image',
    confidence: 'high',
    metadata: {
      url: 'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=600&q=60',
      matches: ['profile avatar on hydra_claw'],
      exif: { device: 'Pixel 8', location: 'Oslo' }
    },
    locationHint: 'Oslo'
  },
  {
    id: 'unused-handle',
    type: 'social',
    source: 'Reddit',
    platform: 'Reddit',
    handle: 'umbra-research',
    confidence: 'medium',
    lastSeen: new Date(Date.now() - 1000 * 60 * 60 * 4).toISOString(),
    profileUrl: 'https://reddit.com/u/umbra-research',
    avatarUrl: null,
    metadata: {
      karma: 2140,
      subreddits: ['r/netsec', 'r/privacy'],
      commentSample: 'Shadow markets discussion'
    },
    aliases: ['umbra research'],
    locationHint: 'Dublin'
  },
  {
    id: 'scant-result',
    type: 'metadata',
    source: 'Public Records',
    confidence: 'low',
    metadata: {
      note: 'Sparse data for partial match only',
      quality: 'weak'
    }
  }
];

export function fuzzyMatch(term: string): MockRecord[] {
  const q = term.toLowerCase();
  return mockResults.filter((record) => {
    const haystacks = [
      record.handle,
      record.source,
      record.platform,
      ...(record.aliases ?? []),
      ...(record.emails ?? []),
      ...(record.phones ?? []),
      record.metadata && JSON.stringify(record.metadata)
    ]
      .filter(Boolean)
      .map((v) => String(v).toLowerCase());

    return haystacks.some((value) => value.includes(q));
  });
}

export function mergeDuplicates(records: MockRecord[]): MockRecord[] {
  const map = new Map<string, MockRecord>();
  records.forEach((rec) => {
    const key = rec.handle ?? rec.id;
    if (!map.has(key)) {
      map.set(key, rec);
      return;
    }
    const existing = map.get(key)!;
    const confidenceOrder: Record<string, number> = { high: 3, medium: 2, low: 1 };
    if (confidenceOrder[rec.confidence] > confidenceOrder[existing.confidence]) {
      existing.confidence = rec.confidence;
    }
    existing.metadata = { ...existing.metadata, ...rec.metadata };
    existing.aliases = Array.from(new Set([...(existing.aliases ?? []), ...(rec.aliases ?? [])]));
    existing.emails = Array.from(new Set([...(existing.emails ?? []), ...(rec.emails ?? [])]));
    existing.phones = Array.from(new Set([...(existing.phones ?? []), ...(rec.phones ?? [])]));
  });
  return Array.from(map.values());
}

export function computeFootprint(records: MockRecord[]): number {
  if (!records.length) return 0;
  const base = records.reduce((score, rec) => {
    const conf = rec.confidence === 'high' ? 1 : rec.confidence === 'medium' ? 0.7 : 0.4;
    return score + conf * 20 + (rec.metadata ? Math.min(15, Object.keys(rec.metadata).length * 2) : 0);
  }, 0);
  return Math.min(100, Math.round(base / records.length));
}

export function topLocations(records: MockRecord[], limit = 3): string[] {
  const counts: Record<string, number> = {};
  records.forEach((rec) => {
    if (!rec.locationHint) return;
    counts[rec.locationHint] = (counts[rec.locationHint] ?? 0) + 1;
  });
  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([loc]) => loc);
}
