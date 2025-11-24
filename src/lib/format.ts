import type { Confidence } from './types';

export function confidenceColor(confidence: Confidence): string {
  switch (confidence) {
    case 'high':
      return 'text-emerald-300 bg-emerald-900/40 border-emerald-500/70';
    case 'medium':
      return 'text-amber-200 bg-amber-900/40 border-amber-500/70';
    default:
      return 'text-rose-200 bg-rose-900/40 border-rose-500/60';
  }
}

export function confidenceLabel(confidence: Confidence): string {
  return confidence.charAt(0).toUpperCase() + confidence.slice(1);
}

export function formatTimestamp(value?: string): string {
  if (!value) return 'Unknown';
  const date = new Date(value);
  return `${date.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })} ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
}

export function badgeForPlatform(platform?: string): string {
  if (!platform) return 'Source';
  return platform;
}

export function footprintProgress(score: number): string {
  return `${Math.min(100, Math.max(0, score))}%`;
}
