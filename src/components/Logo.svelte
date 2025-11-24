<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60" class="h-10" aria-label="UmbraTrace logo">
  <defs>
    <linearGradient id="umbraGrad" x1="0%" x2="100%" y1="0%" y2="100%">
      <stop offset="0%" stop-color="#22d3ee" />
      <stop offset="100%" stop-color="#6366f1" />
    </linearGradient>
    <filter id="shadowGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>
  <rect width="200" height="60" rx="12" fill="#0b1220" />
  <path d="M32 46 L52 14 L72 46 Z" fill="url(#umbraGrad)" opacity="0.85" filter="url(#shadowGlow)" />
  <circle cx="52" cy="30" r="6" fill="#0b1220" stroke="#67e8f9" stroke-width="2" />
  <text x="90" y="38" fill="#e5e7eb" font-family="Inter, system-ui" font-size="22" font-weight="700">UmbraTrace</text>
</svg>
