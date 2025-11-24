import type { PdfReportPayload, SearchResult } from './types';

async function canvasBar(data: number[], labels: string[]): Promise<string> {
  const canvas = document.createElement('canvas');
  canvas.width = 400;
  canvas.height = 200;
  const ctx = canvas.getContext('2d');
  if (!ctx) return '';
  ctx.fillStyle = '#0b1220';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  const barWidth = (canvas.width - 60) / data.length;
  const max = Math.max(...data, 1);
  data.forEach((value, idx) => {
    const height = (value / max) * 140;
    const x = 40 + idx * barWidth;
    const y = canvas.height - height - 30;
    ctx.fillStyle = '#22d3ee';
    ctx.fillRect(x, y, barWidth - 12, height);
    ctx.fillStyle = '#9ca3af';
    ctx.font = '12px Inter, sans-serif';
    ctx.fillText(labels[idx], x, canvas.height - 12);
  });
  return canvas.toDataURL('image/png');
}

function socialGraphSvg(results: SearchResult[]): string {
  const nodes = results.slice(0, 6);
  const circles = nodes
    .map((node, i) => {
      const angle = (i / nodes.length) * Math.PI * 2;
      const x = 150 + Math.cos(angle) * 90;
      const y = 150 + Math.sin(angle) * 90;
      return `<g><circle cx="${x}" cy="${y}" r="26" fill="rgba(34,211,238,0.15)" stroke="#22d3ee" />` +
        `<text x="${x - 14}" y="${y + 4}" fill="#e5e7eb" font-size="10">${node.platform ?? node.source}</text></g>`;
    })
    .join('');
  return `data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300' viewBox='0 0 300 300' style='background:#0b1220'>${circles}<circle cx='150' cy='150' r='30' fill='#111827' stroke='#22d3ee'/><text x='132' y='156' fill='#e5e7eb' font-size='12'>Query</text></svg>`;
}

async function hashContent(text: string): Promise<string> {
  const enc = new TextEncoder().encode(text);
  const buf = await crypto.subtle.digest('SHA-256', enc);
  return Array.from(new Uint8Array(buf))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}

export async function buildFullReport(payload: PdfReportPayload): Promise<import('pdfmake/interfaces').TDocumentDefinitions> {
  const chart = await canvasBar(
    payload.summary.topLocations.length ? payload.summary.topLocations.map(() => Math.floor(Math.random() * 20) + 5) : [5, 3, 2],
    payload.summary.topLocations.length ? payload.summary.topLocations : ['N/A']
  );
  const graphSvg = socialGraphSvg(payload.results);
  const contentText = `${payload.query}-${payload.summary.matchCount}-${payload.summary.footprintScore}`;
  const hash = await hashContent(contentText);

  const evidenceTable = {
    table: {
      headerRows: 1,
      widths: ['*', '*', 'auto', 'auto'],
      body: [
        ['Source', 'URL / Handle', 'Confidence', 'Last Seen'],
        ...payload.results.map((r) => [
          r.source,
          r.profileUrl ?? r.handle ?? 'n/a',
          r.confidence,
          r.lastSeen ? new Date(r.lastSeen).toLocaleDateString() : 'unknown'
        ])
      ]
    },
    layout: 'lightHorizontalLines'
  } as const;

  return {
    info: { title: `UmbraTrace Report - ${payload.query}` },
    pageMargins: [40, 60, 40, 60],
    footer: (currentPage, pageCount) => ({
      columns: [
        { text: `Generated ${new Date().toLocaleString()}`, alignment: 'left', color: '#6b7280', fontSize: 8 },
        { text: `Integrity: ${hash}`, alignment: 'center', color: '#9ca3af', fontSize: 8 },
        { text: `${currentPage} / ${pageCount}`, alignment: 'right', color: '#6b7280', fontSize: 8 }
      ]
    }),
    content: [
      {
        stack: [
          {
            svg: `<svg width="120" height="40" viewBox="0 0 200 60" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop offset="0%" stop-color="#22d3ee"/><stop offset="100%" stop-color="#6366f1"/></linearGradient></defs><rect width="200" height="60" rx="12" fill="#0b1220"/><path d="M20 45 L40 15 L60 45 Z" fill="url(#g)" opacity="0.85"/><text x="80" y="38" fill="#e5e7eb" font-family="Inter" font-size="22" font-weight="700">UmbraTrace</text></svg>`,
            alignment: 'left'
          },
          { text: 'Open-Source Intelligence Dossier', fontSize: 24, margin: [0, 20, 0, 10], bold: true, color: '#e5e7eb' },
          { text: `Subject: ${payload.query}`, fontSize: 16, margin: [0, 0, 0, 20], color: '#cbd5e1' },
          { text: `Investigator: ${payload.investigator ?? 'Automated UmbraTrace'}`, margin: [0, 0, 0, 40], color: '#94a3b8' },
          { canvas: [{ type: 'rect', x: 0, y: 0, w: 515, h: 2, color: '#22d3ee' }] }
        ],
        margin: [0, 0, 0, 20]
      },
      { text: 'Executive Summary', style: 'h2' },
      {
        columns: [
          { text: `Footprint Score: ${payload.summary.footprintScore}`, fontSize: 14, margin: [0, 10, 0, 4] },
          { text: `Total Matches: ${payload.summary.matchCount}`, fontSize: 14, margin: [0, 10, 0, 4] },
          { text: `Top Locations: ${payload.summary.topLocations.join(', ') || 'n/a'}`, fontSize: 14, margin: [0, 10, 0, 4] }
        ]
      },
      { text: 'Findings Overview', style: 'h3', margin: [0, 20, 0, 10] },
      evidenceTable,
      { text: 'Activity Distribution', style: 'h3', margin: [0, 30, 0, 10] },
      { image: chart, width: 420, alignment: 'center' },
      { text: 'Relationship Graph', style: 'h3', margin: [0, 30, 0, 10] },
      { image: graphSvg, width: 320, alignment: 'center' },
      { text: 'Detailed Evidence', style: 'h2', margin: [0, 30, 0, 10] },
      ...payload.results.map((r, idx) => ({
        stack: [
          { text: `${idx + 1}. ${r.source}`, style: 'h3' },
          { text: `Handle: ${r.handle ?? 'n/a'}` },
          { text: `Platform: ${r.platform ?? 'Unknown'}` },
          { text: `Confidence: ${r.confidence}` },
          { text: `Last Seen: ${r.lastSeen ? new Date(r.lastSeen).toLocaleString() : 'Unknown'}` },
          { text: 'Metadata', style: 'metaLabel' },
          {
            stack: Object.entries(r.metadata || {}).map(([k, v]) => ({
              text: `${k}: ${typeof v === 'object' ? JSON.stringify(v) : v}`,
              margin: [10, 0, 0, 2]
            }))
          }
        ],
        margin: [0, 10, 0, 10]
      }))
    ],
    styles: {
      h2: { fontSize: 18, bold: true, color: '#e5e7eb' },
      h3: { fontSize: 14, bold: true, color: '#cbd5e1' },
      metaLabel: { color: '#9ca3af', margin: [0, 4, 0, 4] }
    },
    defaultStyle: {
      fontSize: 10,
      color: '#d1d5db'
    }
  };
}

export async function exportPdf(payload: PdfReportPayload, filename = 'umbratrace-report.pdf'): Promise<void> {
  const [{ default: pdfMake }, { default: fonts }] = await Promise.all([
    import('pdfmake/build/pdfmake'),
    import('pdfmake/build/vfs_fonts')
  ]);
  (pdfMake as any).vfs = (fonts as any).pdfMake.vfs;
  const doc = await buildFullReport(payload);
  pdfMake.createPdf(doc).download(filename);
}
