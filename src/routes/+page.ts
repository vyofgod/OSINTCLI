import type { PageLoad } from './$types';

export const load: PageLoad = () => {
  return {
    capabilities: [
      'Cross-network identity correlation',
      'Confidence-weighted evidence scoring',
      'PDF and JSON export with integrity hash',
      'Inline mock APIs for offline research'
    ]
  };
};
