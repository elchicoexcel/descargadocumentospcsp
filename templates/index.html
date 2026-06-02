<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PCSP Analyzer v2.0 Backend — Plataforma de Contratación</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<style>
  :root {
    --bg: #f6f8fb;
    --surface: #ffffff;
    --surface2: #eef3f8;
    --border: #d8e0ea;
    --border2: #c7d3e0;
    --accent: #0078d4;
    --accent2: #6366f1;
    --accent3: #b45309;
    --text: #162033;
    --text2: #4b5f76;
    --text3: #74869b;
    --red: #dc2626;
    --green: #059669;
    --tag-bg: #edf3f8;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  html { font-size: 16px; scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Mono', monospace;
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
  }

  /* GRID BACKGROUND */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(0,120,212,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,120,212,0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
  }

  body::after {
    content: '';
    position: fixed;
    top: -30%;
    right: -20%;
    width: 800px;
    height: 800px;
    background: radial-gradient(ellipse, rgba(0,120,212,0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }

  /* LAYOUT */
  .shell {
    position: relative;
    z-index: 1;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 24px;
  }

  /* HEADER */
  header {
    padding: 32px 0 0;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
  }

  .logo-block {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .logo-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    opacity: 0.8;
  }

  .logo-title {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.03em;
    line-height: 1;
  }

  .logo-title span {
    color: var(--accent);
  }

  .logo-sub {
    font-size: 11px;
    color: var(--text3);
    margin-top: 2px;
    letter-spacing: 0.02em;
  }

  .header-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: 6px;
    font-size: 11px;
    color: var(--text2);
    letter-spacing: 0.05em;
  }

  .header-badge .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 6px var(--green);
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
  }

  /* DIVIDER */
  .hdiv {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border2) 20%, var(--border2) 80%, transparent);
    margin: 28px 0;
  }

  /* TABS */
  .tabs {
    display: flex;
    gap: 2px;
    margin-bottom: 24px;
  }

  .tab-btn {
    background: none;
    border: 1px solid var(--border);
    color: var(--text3);
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 8px 20px;
    cursor: pointer;
    transition: all 0.15s;
    position: relative;
    overflow: hidden;
  }

  .tab-btn:first-child { border-radius: 6px 0 0 6px; }
  .tab-btn:last-child { border-radius: 0 6px 6px 0; }

  .tab-btn:hover { color: var(--text2); border-color: var(--border2); }

  .tab-btn.active {
    background: var(--surface2);
    border-color: var(--accent);
    color: var(--accent);
  }

  /* SEARCH PANEL */
  .search-panel {
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: 12px;
    padding: 28px;
    position: relative;
    overflow: hidden;
  }

  .search-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent2), var(--accent), var(--accent2));
    opacity: 0.6;
  }

  .panel-label {
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text3);
    margin-bottom: 12px;
  }

  .input-row {
    display: flex;
    gap: 10px;
    align-items: stretch;
  }

  .input-wrap {
    flex: 1;
    position: relative;
  }

  .input-icon {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text3);
    font-size: 13px;
    pointer-events: none;
    transition: color 0.2s;
  }

  input[type="text"] {
    width: 100%;
    background: var(--bg);
    border: 1px solid var(--border2);
    border-radius: 8px;
    color: var(--text);
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    padding: 12px 14px 12px 38px;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
    letter-spacing: 0.02em;
  }

  input[type="text"]:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(0,120,212,0.08);
  }

  input[type="text"]::placeholder { color: var(--text3); }

  .btn-primary {
    background: var(--accent);
    border: none;
    border-radius: 8px;
    color: #ffffff;
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 12px 24px;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.15s;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .btn-primary:hover { background: #0b86df; transform: translateY(-1px); box-shadow: 0 4px 16px rgba(0,120,212,0.3); }
  .btn-primary:active { transform: translateY(0); }
  .btn-primary:disabled { opacity: 0.4; pointer-events: none; }

  .btn-secondary {
    background: var(--surface2);
    border: 1px solid var(--border2);
    border-radius: 8px;
    color: var(--text2);
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    padding: 8px 16px;
    cursor: pointer;
    transition: all 0.15s;
    display: flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
  }

  .btn-secondary:hover { border-color: var(--accent); color: var(--accent); }
  .btn-secondary:disabled { opacity: 0.4; pointer-events: none; }

  .btn-danger {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 8px;
    color: var(--red);
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    padding: 8px 16px;
    cursor: pointer;
    transition: all 0.15s;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .btn-danger:hover { background: rgba(239,68,68,0.2); }

  .hint-text {
    font-size: 11px;
    color: var(--text3);
    margin-top: 10px;
    line-height: 1.6;
  }

  .hint-text code {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 1px 5px;
    font-size: 10px;
    color: var(--accent);
  }

  /* STATUS / LOADING */
  .status-bar {
    display: none;
    align-items: center;
    gap: 12px;
    padding: 14px 18px;
    background: var(--surface2);
    border: 1px solid var(--border2);
    border-radius: 8px;
    margin-top: 16px;
    font-size: 12px;
    color: var(--text2);
  }

  .status-bar.visible { display: flex; }

  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid var(--border2);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    flex-shrink: 0;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  /* ERROR */
  .error-box {
    display: none;
    align-items: flex-start;
    gap: 12px;
    padding: 16px 18px;
    background: rgba(239,68,68,0.05);
    border: 1px solid rgba(239,68,68,0.2);
    border-radius: 8px;
    margin-top: 16px;
    font-size: 12px;
    color: #fca5a5;
    line-height: 1.6;
  }

  .error-box.visible { display: flex; }

  .error-icon { font-size: 16px; flex-shrink: 0; margin-top: 1px; }

  /* RESULTS SECTION */
  #results-section { display: none; margin-top: 32px; }
  #results-section.visible { display: block; }

  /* EXPEDIENTE HEADER */
  .exp-header {
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
  }

  .exp-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,120,212,0.2) 50%, transparent);
  }

  .exp-num-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
    flex-wrap: wrap;
  }

  .exp-num {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.02em;
  }

  .badge {
    font-size: 9px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: 500;
  }

  .badge-cyan { background: rgba(0,120,212,0.1); color: var(--accent); border: 1px solid rgba(0,120,212,0.2); }
  .badge-violet { background: rgba(124,58,237,0.15); color: #a78bfa; border: 1px solid rgba(124,58,237,0.25); }
  .badge-amber { background: rgba(245,158,11,0.1); color: var(--accent3); border: 1px solid rgba(245,158,11,0.2); }
  .badge-green { background: rgba(16,185,129,0.1); color: var(--green); border: 1px solid rgba(16,185,129,0.2); }
  .badge-red { background: rgba(239,68,68,0.1); color: var(--red); border: 1px solid rgba(239,68,68,0.2); }

  .exp-title {
    font-family: 'Instrument Serif', serif;
    font-size: 15px;
    color: var(--text2);
    line-height: 1.5;
    margin-bottom: 12px;
    font-style: italic;
  }

  .exp-meta {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
  }

  .exp-meta-item {
    font-size: 11px;
    color: var(--text3);
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .exp-meta-item span { color: var(--text2); }

  /* SECTION TITLE */
  .section-title {
    font-family: 'Syne', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text3);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  /* ACTIONS BAR */
  .actions-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }

  .select-count {
    font-size: 11px;
    color: var(--text3);
    margin-left: auto;
  }

  .select-count span { color: var(--accent); font-weight: 500; }

  /* DOCS TABLE */
  .docs-table {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
  }

  .docs-head {
    display: grid;
    grid-template-columns: 32px 1fr 90px 120px 100px 40px;
    gap: 0;
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
    padding: 0;
  }

  .docs-head-cell {
    font-size: 9px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text3);
    padding: 10px 12px;
    font-weight: 500;
    border-right: 1px solid var(--border);
  }

  .docs-head-cell:last-child { border-right: none; }

  .doc-row {
    display: grid;
    grid-template-columns: 32px 1fr 90px 120px 100px 40px;
    border-bottom: 1px solid var(--border);
    transition: background 0.1s;
    position: relative;
  }

  .doc-row:last-child { border-bottom: none; }
  .doc-row:hover { background: rgba(255,255,255,0.02); }
  .doc-row.selected { background: rgba(0,120,212,0.04); }

  .doc-row.selected::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 2px;
    background: var(--accent);
  }

  .doc-cell {
    padding: 12px;
    display: flex;
    align-items: center;
    border-right: 1px solid var(--border);
    font-size: 12px;
  }

  .doc-cell:last-child { border-right: none; justify-content: center; }

  .doc-cb {
    width: 14px;
    height: 14px;
    accent-color: var(--accent);
    cursor: pointer;
    flex-shrink: 0;
  }

  .doc-name {
    font-size: 12px;
    color: var(--text);
    line-height: 1.4;
    word-break: break-word;
  }

  .doc-name small {
    display: block;
    font-size: 10px;
    color: var(--text3);
    margin-top: 2px;
  }

  .ext-tag {
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 0.08em;
    padding: 2px 6px;
    border-radius: 3px;
    text-transform: uppercase;
  }

  .ext-pdf { background: rgba(239,68,68,0.15); color: #fca5a5; }
  .ext-xml { background: rgba(16,185,129,0.15); color: #6ee7b7; }
  .ext-html { background: rgba(245,158,11,0.15); color: #fcd34d; }
  .ext-doc { background: rgba(59,130,246,0.15); color: #93c5fd; }
  .ext-xls { background: rgba(16,185,129,0.15); color: #6ee7b7; }
  .ext-zip { background: rgba(124,58,237,0.15); color: #c4b5fd; }
  .ext-default { background: var(--surface2); color: var(--text3); }

  .doc-date { font-size: 11px; color: var(--text2); }
  .doc-status { }

  .dl-btn {
    background: none;
    border: none;
    color: var(--text3);
    cursor: pointer;
    padding: 4px;
    border-radius: 4px;
    transition: all 0.15s;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .dl-btn:hover { color: var(--accent); background: rgba(0,120,212,0.1); }

  /* EMPTY STATE */
  .empty-state {
    text-align: center;
    padding: 48px 24px;
    color: var(--text3);
  }

  .empty-icon { font-size: 40px; margin-bottom: 12px; opacity: 0.4; }

  .empty-state p { font-size: 12px; line-height: 1.8; }

  /* PROGRESS OVERLAY */
  #progress-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(10,12,15,0.85);
    backdrop-filter: blur(8px);
    z-index: 100;
    align-items: center;
    justify-content: center;
  }

  #progress-overlay.visible { display: flex; }

  .progress-card {
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: 16px;
    padding: 32px;
    width: 480px;
    max-width: 90vw;
    position: relative;
    overflow: hidden;
  }

  .progress-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent2), var(--accent));
  }

  .progress-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 6px;
    letter-spacing: -0.01em;
  }

  .progress-sub {
    font-size: 11px;
    color: var(--text3);
    margin-bottom: 24px;
  }

  .progress-bar-wrap {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    height: 8px;
    overflow: hidden;
    margin-bottom: 12px;
  }

  .progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent2), var(--accent));
    border-radius: 6px;
    width: 0%;
    transition: width 0.3s ease;
    box-shadow: 0 0 8px rgba(0,120,212,0.4);
  }

  .progress-pct {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: var(--accent);
    letter-spacing: -0.04em;
    margin-bottom: 4px;
  }

  .progress-status {
    font-size: 11px;
    color: var(--text3);
    margin-bottom: 20px;
    min-height: 16px;
  }

  .progress-log {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 12px;
    max-height: 160px;
    overflow-y: auto;
    font-size: 10px;
    line-height: 1.8;
    color: var(--text3);
  }

  .progress-log .log-ok { color: var(--green); }
  .progress-log .log-err { color: var(--red); }
  .progress-log .log-info { color: var(--text2); }

  .progress-log::-webkit-scrollbar { width: 4px; }
  .progress-log::-webkit-scrollbar-track { background: transparent; }
  .progress-log::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

  /* PROXY INFO */
  .proxy-note {
    background: rgba(245,158,11,0.05);
    border: 1px solid rgba(245,158,11,0.15);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 11px;
    color: var(--text2);
    margin-top: 16px;
    line-height: 1.7;
  }

  .proxy-note strong { color: var(--accent3); }

  /* FOOTER */
  footer {
    margin-top: 64px;
    padding: 24px 0 32px;
    border-top: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: gap;
    gap: 12px;
  }

  .footer-left {
    font-size: 11px;
    color: var(--text3);
    line-height: 1.8;
  }

  .footer-left a { color: var(--accent); text-decoration: none; }
  .footer-left a:hover { text-decoration: underline; }

  .footer-right {
    font-size: 10px;
    color: var(--text3);
    letter-spacing: 0.08em;
  }

  /* TAB CONTENT */
  .tab-content { display: none; }
  .tab-content.active { display: block; }

  /* ANIMATIONS */
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .animate-in { animation: fadeUp 0.3s ease forwards; }

  /* RESPONSIVE */
  @media (max-width: 700px) {
    .docs-head, .doc-row {
      grid-template-columns: 28px 1fr 70px 40px;
    }
    .docs-head-cell:nth-child(3),
    .docs-head-cell:nth-child(4),
    .doc-cell:nth-child(3),
    .doc-cell:nth-child(4) { display: none; }
    .logo-title { font-size: 22px; }
    .progress-card { padding: 24px; }
  }

  /* SECTION GROUPS */
  .doc-group { margin-bottom: 24px; }

  .group-label {
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text3);
    padding: 8px 12px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .group-label .group-count {
    background: var(--bg);
    border: 1px solid var(--border2);
    border-radius: 10px;
    padding: 1px 7px;
    font-size: 9px;
    color: var(--accent);
  }

  .group-label + .docs-table { border-radius: 0 0 10px 10px; }

  /* URL Link */
  .exp-url-link {
    font-size: 10px;
    color: var(--accent);
    text-decoration: none;
    opacity: 0.7;
    transition: opacity 0.15s;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }

  .exp-url-link:hover { opacity: 1; }
</style>
</head>
<body>

<div class="shell">
  <header>
    <div class="logo-block">
      <div class="logo-eyebrow">Analizador de Licitaciones</div>
      <div class="logo-title">PCSP <span>Analyzer</span></div>
      <div class="logo-sub">Plataforma de Contratación del Sector Público · España</div>
    </div>
    <div class="header-badge">
      <div class="dot"></div>
      backend real · contrataciondelestado.es
    </div>
  </header>

  <div class="hdiv"></div>

  <!-- TABS -->
  <div class="tabs">
    <button class="tab-btn active" onclick="switchTab('exp')">Por Expediente</button>
    <button class="tab-btn" onclick="switchTab('url')">Por URL Directa</button>
  </div>

  <!-- TAB: EXPEDIENTE -->
  <div class="tab-content active" id="tab-exp">
    <div class="search-panel">
      <div class="panel-label">Número de expediente</div>
      <div class="input-row">
        <div class="input-wrap">
          <span class="input-icon">⌗</span>
          <input type="text" id="input-exp" placeholder="Ej: 2024/001234  ó  GE-2024-0001" onkeydown="if(event.key==='Enter')searchByExp()">
        </div>
        <button class="btn-primary" onclick="searchByExp()" id="btn-search-exp">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
          Buscar
        </button>
      </div>
      <p class="hint-text">
        Se buscará en licitaciones y contratos menores de la plataforma. Formatos aceptados: <code>EXP-2024-001</code>, <code>2024/00123</code>, etc.
      </p>
      <div class="proxy-note">
        <strong>⚠ Nota técnica:</strong> El acceso a contrataciondelestado.es requiere un proxy CORS para peticiones desde el navegador.
        La aplicación intenta descarga real usando varios proxies CORS públicos y conserva el formato original de cada archivo.
        Para producción estable se recomienda desplegar un backend/proxy propio server-side.
      </div>
    </div>
  </div>

  <!-- TAB: URL -->
  <div class="tab-content" id="tab-url">
    <div class="search-panel">
      <div class="panel-label">URL directa del expediente</div>
      <div class="input-row">
        <div class="input-wrap">
          <span class="input-icon">🔗</span>
          <input type="text" id="input-url" placeholder="https://contrataciondelestado.es/wps/portal/plataforma/buscar/resultado/...  " onkeydown="if(event.key==='Enter')searchByUrl()">
        </div>
        <button class="btn-primary" onclick="searchByUrl()" id="btn-search-url">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          Acceder
        </button>
      </div>
      <p class="hint-text">
        Pega la URL completa del detalle del expediente. Ejemplo:<br>
        <code>https://contrataciondelestado.es/wps/portal/plataforma/buscar/resultado/detalle?...</code>
      </p>
    </div>
  </div>

  <!-- STATUS -->
  <div class="status-bar" id="status-bar">
    <div class="spinner"></div>
    <span id="status-text">Conectando con la plataforma…</span>
  </div>

  <!-- ERROR -->
  <div class="error-box" id="error-box">
    <span class="error-icon">⚠</span>
    <div id="error-text"></div>
  </div>

  <!-- RESULTS -->
  <div id="results-section">

    <!-- EXP HEADER -->
    <div class="exp-header animate-in" id="exp-header">
      <div class="exp-num-row">
        <span class="exp-num" id="r-exp-num">—</span>
        <span class="badge badge-cyan" id="r-tipo">Licitación</span>
        <span class="badge badge-green" id="r-estado">Publicado</span>
      </div>
      <div class="exp-title" id="r-titulo">—</div>
      <div class="exp-meta">
        <div class="exp-meta-item">Órgano: <span id="r-organo">—</span></div>
        <div class="exp-meta-item">Importe: <span id="r-importe">—</span></div>
        <div class="exp-meta-item">Publicación: <span id="r-fecha">—</span></div>
        <a class="exp-url-link" id="r-link" href="#" target="_blank">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          Ver en plataforma
        </a>
      </div>
    </div>

    <!-- ACTIONS -->
    <div class="actions-bar animate-in" style="animation-delay:0.05s">
      <button class="btn-secondary" onclick="selectAll()">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
        Seleccionar todo
      </button>
      <button class="btn-secondary" onclick="deselectAll()">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>
        Deseleccionar
      </button>
      <button class="btn-primary" id="btn-zip" onclick="downloadZip()" disabled>
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        Descargar ZIP
      </button>
      <div class="select-count"><span id="sel-count">0</span> seleccionados</div>
    </div>

    <!-- DOC GROUPS -->
    <div id="doc-groups"></div>

  </div>

</div><!-- /shell -->

<!-- PROGRESS OVERLAY -->
<div id="progress-overlay">
  <div class="progress-card">
    <div class="progress-title">Generando ZIP del expediente</div>
    <div class="progress-sub" id="prog-sub">Preparando descarga…</div>
    <div class="progress-pct" id="prog-pct">0%</div>
    <div class="progress-bar-wrap">
      <div class="progress-bar-fill" id="prog-bar"></div>
    </div>
    <div class="progress-status" id="prog-status">Iniciando…</div>
    <div class="progress-log" id="prog-log"></div>
  </div>
</div>

<div class="shell">
  <footer>
    <div class="footer-left">
      Desarrollado por <a href="https://twitter.com/AlexRico" target="_blank">@AlexRico</a> ·
      Datos públicos de <a href="https://contrataciondelestado.es" target="_blank">contrataciondelestado.es</a><br>
      Uso exclusivo con datos de acceso público · Sin almacenamiento de información
    </div>
    <div class="footer-right">PCSP Analyzer v2.0 Backend · real + compatibilidad</div>
  </footer>
</div>

<script>
let allDocuments = [];
let expedienteData = {};

function switchTab(tab) {
  document.querySelectorAll('.tab-btn').forEach((b,i) => b.classList.toggle('active', (i===0 && tab==='exp') || (i===1 && tab==='url')));
  document.getElementById('tab-exp').classList.toggle('active', tab==='exp');
  document.getElementById('tab-url').classList.toggle('active', tab==='url');
  hideError(); hideStatus();
}
function showStatus(msg){ const bar=document.getElementById('status-bar'); document.getElementById('status-text').textContent=msg; bar.classList.add('visible'); }
function hideStatus(){ document.getElementById('status-bar').classList.remove('visible'); }
function showError(msg){ hideStatus(); const box=document.getElementById('error-box'); document.getElementById('error-text').innerHTML=msg; box.classList.add('visible'); }
function hideError(){ document.getElementById('error-box').classList.remove('visible'); }
async function apiJson(url, opts){ const r=await fetch(url, opts); const data=await r.json().catch(()=>({error:'Respuesta no JSON'})); if(!r.ok) throw new Error(data.error||`HTTP ${r.status}`); return data; }

async function searchByExp(){
  const val=document.getElementById('input-exp').value.trim();
  if(!val){ showError('Introduce un número de expediente.'); return; }
  hideError(); showStatus('Buscando expediente con backend local…'); document.getElementById('results-section').classList.remove('visible');
  try { const data=await apiJson(`/api/search?exp=${encodeURIComponent(val)}`); renderResults(data.expediente, data.documents); }
  catch(e){ showError(`No se pudo obtener el expediente: ${escapeHtml(e.message)}<br><br>Prueba con la URL directa exacta del expediente. Si la Plataforma exige sesión o captcha, no será posible automatizar esa descarga.`); }
}
async function searchByUrl(){
  const val=document.getElementById('input-url').value.trim();
  if(!val){ showError('Introduce una URL válida.'); return; }
  if(!/^https?:\/\//i.test(val)){ showError('La URL debe comenzar por <code>https://</code>'); return; }
  hideError(); showStatus('Leyendo expediente con backend local…'); document.getElementById('results-section').classList.remove('visible');
  try { const data=await apiJson(`/api/url?url=${encodeURIComponent(val)}`); renderResults(data.expediente, data.documents); }
  catch(e){ showError(`No se pudo acceder a la URL indicada: ${escapeHtml(e.message)}<br><br>Comprueba que es la URL exacta del detalle del expediente y no la portada.`); }
}

function renderResults(expInfo, docs){
  hideStatus(); expedienteData=expInfo||{}; allDocuments=(docs||[]).map((d,i)=>({...d, id:d.id||('d'+i)}));
  document.getElementById('r-exp-num').textContent=expedienteData.numero||'Sin número';
  document.getElementById('r-titulo').textContent=expedienteData.titulo||'Título no disponible';
  document.getElementById('r-organo').textContent=expedienteData.organo||'—';
  document.getElementById('r-importe').textContent=expedienteData.importe||'—';
  document.getElementById('r-fecha').textContent=expedienteData.fecha||'—';
  document.getElementById('r-tipo').textContent=expedienteData.tipo||'Expediente';
  const estadoEl=document.getElementById('r-estado'); estadoEl.textContent=expedienteData.estado||'Disponible';
  estadoEl.className='badge '+((/anulad/i.test(estadoEl.textContent))?'badge-red':(/adjudic/i.test(estadoEl.textContent)?'badge-violet':'badge-green'));
  const linkEl=document.getElementById('r-link'); linkEl.href=expedienteData.url||'#';
  const groups={}; allDocuments.forEach(d=>{ const k=d.section||'Documentos'; (groups[k]=groups[k]||[]).push(d); });
  const container=document.getElementById('doc-groups'); container.innerHTML='';
  if(!allDocuments.length){ container.innerHTML='<div class="empty-state"><div class="empty-icon">📂</div><p>No se encontraron documentos descargables en este expediente.<br>La página puede requerir sesión, usar contenido dinámico no visible para el backend o no contener documentos públicos.</p></div>'; }
  else Object.keys(groups).forEach(section=>{
    const wrap=document.createElement('div'); wrap.className='doc-group animate-in';
    wrap.innerHTML=`<div class="group-label">${getSectionIcon(section)} ${escapeHtml(section)} <span class="group-count">${groups[section].length}</span></div><div class="docs-table"><div class="docs-head"><div class="docs-head-cell"></div><div class="docs-head-cell">Documento</div><div class="docs-head-cell">Tipo</div><div class="docs-head-cell">Fecha</div><div class="docs-head-cell">Estado</div><div class="docs-head-cell"></div></div>${groups[section].map(renderDocRow).join('')}</div>`;
    container.appendChild(wrap);
  });
  document.getElementById('results-section').classList.add('visible'); updateSelCount(); document.getElementById('results-section').scrollIntoView({behavior:'smooth',block:'start'});
}
function getSectionIcon(section){ if(/anuncio/i.test(section)&&/anulad/i.test(section)) return '🚫'; if(/anuncio/i.test(section)) return '📋'; if(/otro/i.test(section)) return '📎'; return '📄'; }
function renderDocRow(doc){
  const ext=(doc.ext||'bin').replace('.','').toLowerCase(); const extClass={pdf:'ext-pdf',xml:'ext-xml',html:'ext-html',htm:'ext-html',doc:'ext-doc',docx:'ext-doc',xls:'ext-xls',xlsx:'ext-xls',zip:'ext-zip',rar:'ext-zip'}[ext]||'ext-default';
  const status=doc.status||'Disponible'; const badge=/anulad/i.test(status)?'badge-red':'badge-green';
  return `<div class="doc-row" id="row-${doc.id}"><div class="doc-cell"><input type="checkbox" class="doc-cb" id="cb-${doc.id}" onchange="onCbChange()" title="Seleccionar"></div><div class="doc-cell"><div class="doc-name">${escapeHtml(doc.name||'Documento')}<small>${escapeHtml(doc.url||'')}</small></div></div><div class="doc-cell"><span class="ext-tag ${extClass}">${escapeHtml(ext.toUpperCase())}</span></div><div class="doc-cell doc-date">${escapeHtml(doc.date||'—')}</div><div class="doc-cell doc-status"><span class="badge ${badge}">${escapeHtml(status)}</span></div><div class="doc-cell"><button class="dl-btn" onclick="downloadSingle('${doc.id}')" title="Descargar"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg></button></div></div>`;
}
function onCbChange(){ allDocuments.forEach(d=>{ const cb=document.getElementById('cb-'+d.id), row=document.getElementById('row-'+d.id); if(cb&&row) row.classList.toggle('selected',cb.checked); }); updateSelCount(); }
function getSelected(){ return allDocuments.filter(d=>{ const cb=document.getElementById('cb-'+d.id); return cb&&cb.checked; }); }
function updateSelCount(){ const n=getSelected().length; document.getElementById('sel-count').textContent=n; document.getElementById('btn-zip').disabled=n===0; }
function selectAll(){ allDocuments.forEach(d=>{ const cb=document.getElementById('cb-'+d.id), row=document.getElementById('row-'+d.id); if(cb){cb.checked=true; if(row) row.classList.add('selected');} }); updateSelCount(); }
function deselectAll(){ allDocuments.forEach(d=>{ const cb=document.getElementById('cb-'+d.id), row=document.getElementById('row-'+d.id); if(cb){cb.checked=false; if(row) row.classList.remove('selected');} }); updateSelCount(); }
function downloadSingle(id){ const doc=allDocuments.find(d=>d.id===id); if(!doc) return; const url=`/api/download?url=${encodeURIComponent(doc.url)}&filename=${encodeURIComponent(buildDownloadFilename(doc))}`; window.location.href=url; }
async function downloadZip(){
  const selected=getSelected(); if(!selected.length) return;
  const overlay=document.getElementById('progress-overlay'); overlay.classList.add('visible');
  document.getElementById('prog-sub').textContent=`${selected.length} documento(s) seleccionado(s)`; document.getElementById('prog-pct').textContent='10%'; document.getElementById('prog-bar').style.width='10%'; document.getElementById('prog-status').textContent='Solicitando ZIP al backend…'; document.getElementById('prog-log').textContent='Descargando documentos desde servidor local…';
  try{
    const r=await fetch('/api/zip',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({expediente:expedienteData,documents:selected})});
    if(!r.ok){ const data=await r.json().catch(()=>({error:'Error generando ZIP'})); throw new Error(data.error); }
    const blob=await r.blob(); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=buildZipName(); a.click(); URL.revokeObjectURL(a.href);
    document.getElementById('prog-pct').textContent='100%'; document.getElementById('prog-bar').style.width='100%'; document.getElementById('prog-status').textContent='ZIP generado correctamente'; setTimeout(()=>overlay.classList.remove('visible'),1500);
  } catch(e){ document.getElementById('prog-status').textContent='Error: '+e.message; setTimeout(()=>overlay.classList.remove('visible'),3500); }
}
function buildDownloadFilename(doc){ const base=sanitizeFilename(doc.name||'documento')||'documento'; const ext=(doc.ext||inferExtFromUrl(doc.url)||'bin').replace(/^\./,'').toLowerCase(); return base.toLowerCase().endsWith('.'+ext)?base:`${base}.${ext}`; }
function inferExtFromUrl(url){ try{ const m=new URL(url,location.href).pathname.match(/\.([a-z0-9]{2,5})$/i); return m?m[1].toLowerCase():''; }catch(e){return '';} }
function buildZipName(){ const exp=sanitizeFilename((expedienteData&&expedienteData.numero)||'expediente')||'expediente'; const d=new Date(), p=n=>String(n).padStart(2,'0'); return `${exp}_${d.getFullYear()}${p(d.getMonth()+1)}${p(d.getDate())}_${p(d.getHours())}${p(d.getMinutes())}.zip`; }
function sanitizeFilename(name){ return String(name||'').replace(/[<>:"/\\|?*\x00-\x1F]/g,'_').substring(0,80).trim(); }
function escapeHtml(s){ return String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
document.getElementById('progress-overlay').addEventListener('click',function(e){ if(e.target===this) this.classList.remove('visible'); });
</script>
</body>
</html>