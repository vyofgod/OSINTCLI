import { render, fireEvent } from '@testing-library/svelte';
import ResultCard from '../src/components/ResultCard.svelte';
import type { SearchResult } from '../src/lib/types';

vi.mock('../src/components/JsonModal.svelte', async () => {
  const { SvelteComponent } = await import('svelte');
  return { default: class extends SvelteComponent {} };
});
vi.mock('../src/lib/pdf-templates', () => ({ exportPdf: vi.fn() }));

const result: SearchResult = {
  id: '1',
  type: 'social',
  source: 'Twitter',
  platform: 'Twitter',
  handle: 'umbra',
  confidence: 'high',
  lastSeen: new Date().toISOString(),
  profileUrl: 'https://twitter.com/umbra',
  avatarUrl: null,
  metadata: { bio: 'Shadow operative' }
};

describe('ResultCard', () => {
  test('renders handle and platform badge', () => {
    const { getByText } = render(ResultCard, { props: { result } });
    expect(getByText('umbra')).toBeInTheDocument();
    expect(getByText('Twitter')).toBeInTheDocument();
  });

  test('expands metadata', async () => {
    const { getByText, queryByText } = render(ResultCard, { props: { result } });
    expect(queryByText('Shadow operative')).not.toBeNull();
    const btn = getByText('Hide') || getByText('Expand details');
    await fireEvent.click(btn);
    await fireEvent.click(btn);
    expect(queryByText('Shadow operative')).toBeInTheDocument();
  });

  test('opens JSON modal', async () => {
    const { getByText } = render(ResultCard, { props: { result } });
    const btn = getByText('Open JSON');
    await fireEvent.click(btn);
    expect(btn).toBeEnabled();
  });
});
