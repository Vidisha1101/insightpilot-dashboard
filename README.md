[README.html](https://github.com/user-attachments/files/28536493/README.html)
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>InsightPilot — README</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0a0e1a;
      --card: #111827;
      --border: rgba(99,179,237,0.15);
      --accent: #63b3ed;
      --accent2: #9f7aea;
      --accent3: #68d391;
      --text: #e2e8f0;
      --muted: #718096;
    }

    body {
      font-family: 'Space Grotesk', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      padding-bottom: 4rem;
    }

    /* ── HERO ── */
    .hero {
      position: relative;
      padding: 5rem 2rem 3.5rem;
      text-align: center;
      overflow: hidden;
      max-width: 900px;
      margin: 0 auto;
    }
    .hero-grid {
      position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(99,179,237,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,179,237,0.06) 1px, transparent 1px);
      background-size: 40px 40px;
      animation: gridDrift 22s linear infinite;
      pointer-events: none;
    }
    @keyframes gridDrift { to { transform: translate(40px, 40px); } }

    .orb {
      position: absolute; border-radius: 50%;
      filter: blur(70px); pointer-events: none;
      animation: orbFloat 9s ease-in-out infinite;
    }
    .orb1 { width: 320px; height: 320px; background: rgba(99,179,237,0.13); top: -100px; left: 5%; }
    .orb2 { width: 250px; height: 250px; background: rgba(159,122,234,0.1); top: -60px; right: 8%; animation-delay: -4s; }
    .orb3 { width: 200px; height: 200px; background: rgba(104,211,145,0.08); bottom: -70px; left: 48%; animation-delay: -7s; }
    @keyframes orbFloat { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-22px); } }

    .logo-wrap {
      position: relative;
      display: inline-flex; align-items: center; gap: 16px;
      margin-bottom: 1.5rem;
      animation: fadeDown 0.8s cubic-bezier(0.16,1,0.3,1) both;
    }
    .logo-icon {
      width: 60px; height: 60px;
      background: linear-gradient(135deg, #63b3ed 0%, #9f7aea 100%);
      border-radius: 16px; font-size: 28px;
      display: flex; align-items: center; justify-content: center;
      animation: pulseLogo 3s ease-in-out infinite;
    }
    @keyframes pulseLogo {
      0%,100% { box-shadow: 0 0 30px rgba(99,179,237,0.35); }
      50% { box-shadow: 0 0 55px rgba(99,179,237,0.55), 0 0 90px rgba(159,122,234,0.2); }
    }
    .logo-title {
      font-size: 3rem; font-weight: 700; letter-spacing: -0.03em;
      background: linear-gradient(90deg, #63b3ed, #9f7aea, #68d391, #63b3ed);
      background-size: 300%;
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      animation: gradShift 5s ease infinite;
    }
    @keyframes gradShift { 0%,100% { background-position: 0%; } 50% { background-position: 100%; } }

    .hero-sub {
      position: relative;
      font-size: 1.05rem; color: var(--muted); max-width: 580px;
      margin: 0 auto 2rem; line-height: 1.75;
      animation: fadeDown 0.8s 0.15s cubic-bezier(0.16,1,0.3,1) both;
    }
    .hero-sub strong { color: var(--text); font-weight: 500; }

    .badges {
      display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;
      position: relative;
      animation: fadeDown 0.8s 0.28s cubic-bezier(0.16,1,0.3,1) both;
    }
    .badge {
      padding: 5px 15px; border-radius: 100px; font-size: 12px; font-weight: 500;
      letter-spacing: 0.02em; border: 1px solid; transition: transform 0.2s, box-shadow 0.2s;
    }
    .badge:hover { transform: translateY(-2px); }
    .b-blue { background: rgba(99,179,237,0.1); border-color: rgba(99,179,237,0.3); color: #63b3ed; }
    .b-blue:hover { box-shadow: 0 4px 18px rgba(99,179,237,0.25); }
    .b-purple { background: rgba(159,122,234,0.1); border-color: rgba(159,122,234,0.3); color: #9f7aea; }
    .b-green { background: rgba(104,211,145,0.1); border-color: rgba(104,211,145,0.3); color: #68d391; }
    .b-orange { background: rgba(246,173,85,0.1); border-color: rgba(246,173,85,0.3); color: #f6ad55; }

    @keyframes fadeDown {
      from { opacity:0; transform: translateY(-20px); }
      to { opacity:1; transform: translateY(0); }
    }

    /* ── LAYOUT ── */
    .container { max-width: 900px; margin: 0 auto; padding: 0 2rem; }

    .demo-bar {
      background: rgba(17,24,39,0.9); border: 1px solid var(--border);
      border-radius: 10px; margin: 0 auto 0;
      max-width: 900px; padding: 11px 18px;
      display: flex; align-items: center; gap: 10px;
      font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--muted);
      animation: fadeDown 0.8s 0.38s cubic-bezier(0.16,1,0.3,1) both;
    }
    .dots { display: flex; gap: 5px; }
    .dot { width: 10px; height: 10px; border-radius: 50%; }
    .dr { background: #fc5c57; } .dy { background: #fdbc40; } .dg { background: #33c748; }
    .demo-url { flex: 1; color: #a0aec0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
    .live-dot { width: 7px; height: 7px; border-radius: 50%; background: #68d391; animation: livePulse 1.5s ease infinite; }
    @keyframes livePulse {
      0%,100% { box-shadow: 0 0 0 0 rgba(104,211,145,0.5); }
      50% { box-shadow: 0 0 0 5px rgba(104,211,145,0); }
    }
    .live-label { color: #68d391; font-size: 11px; }

    /* ── SECTION ── */
    .section { margin-top: 2.5rem; }
    .sec-label {
      display: flex; align-items: center; gap: 12px;
      font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em;
      color: var(--muted); margin-bottom: 1.1rem;
    }
    .sec-label::before, .sec-label::after {
      content:''; flex: 1; height: 1px; background: var(--border);
    }
    .sec-label::before { flex: 0 0 28px; }

    /* ── OVERVIEW ── */
    .overview {
      font-size: 0.97rem; line-height: 1.85; color: #a0aec0;
      border-left: 2px solid #9f7aea; padding-left: 1.1rem;
    }
    .overview strong { color: var(--text); font-weight: 500; }

    /* ── STATS ── */
    .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px,1fr)); gap: 12px; }
    .stat {
      background: var(--card); border: 1px solid var(--border);
      border-radius: 10px; padding: 1.1rem; text-align: center;
      transition: border-color 0.2s, transform 0.2s;
    }
    .stat:hover { border-color: rgba(99,179,237,0.4); transform: translateY(-3px); }
    .stat-n {
      font-size: 1.7rem; font-weight: 700; letter-spacing: -0.02em;
      background: linear-gradient(90deg, #63b3ed, #9f7aea);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .stat-l { font-size: 0.73rem; color: var(--muted); margin-top: 3px; }

    /* ── FEATURES ── */
    .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px,1fr)); gap: 12px; }
    .feat {
      background: var(--card); border: 1px solid var(--border);
      border-radius: 12px; padding: 1.2rem 1.3rem;
      transition: transform 0.25s, border-color 0.25s, box-shadow 0.25s;
      opacity: 0; animation: cardUp 0.5s cubic-bezier(0.16,1,0.3,1) forwards;
    }
    .feat:hover {
      transform: translateY(-5px);
      border-color: rgba(99,179,237,0.35);
      box-shadow: 0 14px 44px rgba(0,0,0,0.5), 0 0 22px rgba(99,179,237,0.07);
    }
    @keyframes cardUp { to { opacity:1; transform:translateY(0); } }
    .feat:nth-child(1){animation-delay:.05s} .feat:nth-child(2){animation-delay:.1s}
    .feat:nth-child(3){animation-delay:.15s} .feat:nth-child(4){animation-delay:.2s}
    .feat:nth-child(5){animation-delay:.25s} .feat:nth-child(6){animation-delay:.3s}
    .feat-ico {
      width: 42px; height: 42px; border-radius: 11px; font-size: 20px;
      display: flex; align-items: center; justify-content: center; margin-bottom: 11px;
    }
    .feat-name { font-size: 0.9rem; font-weight: 600; margin-bottom: 5px; }
    .feat-desc { font-size: 0.79rem; color: var(--muted); line-height: 1.6; }

    /* ── STACK ── */
    .stack { display: flex; flex-wrap: wrap; gap: 10px; }
    .chip {
      display: inline-flex; align-items: center; gap: 8px;
      background: var(--card); border: 1px solid var(--border);
      border-radius: 8px; padding: 8px 15px;
      font-size: 0.83rem; font-weight: 500;
      transition: transform 0.2s, border-color 0.2s;
    }
    .chip:hover { transform: scale(1.04); border-color: rgba(99,179,237,0.4); }
    .cdot { width: 7px; height: 7px; border-radius: 50%; }

    /* ── CODE ── */
    .code-block {
      background: #0d1117; border: 1px solid var(--border); border-radius: 10px; overflow: hidden;
    }
    .code-head {
      display: flex; align-items: center; justify-content: space-between;
      padding: 10px 16px; border-bottom: 1px solid var(--border);
    }
    .code-lang { font-size: 11px; color: var(--muted); font-family: 'JetBrains Mono', monospace; }
    .copy-btn {
      font-size: 11px; color: var(--muted); background: none; border: none; cursor: pointer;
      padding: 4px 10px; border-radius: 5px; transition: color 0.2s, background 0.2s;
    }
    .copy-btn:hover { color: #63b3ed; background: rgba(99,179,237,0.08); }
    pre {
      padding: 1.1rem 1.4rem; font-family: 'JetBrains Mono', monospace;
      font-size: 0.78rem; line-height: 2; color: #a8b3cf; overflow-x: auto; white-space: pre;
    }
    .cc { color: #4a5568; } .cmd { color: #63b3ed; } .str { color: #68d391; } .fl { color: #f6ad55; }

    /* ── TREE ── */
    .tree {
      background: #0d1117; border: 1px solid var(--border); border-radius: 10px;
      padding: 1.2rem 1.6rem; font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem; line-height: 2.1; color: #a8b3cf;
    }
    .td { color: #63b3ed; } .tn { color: #4a5568; }

    /* ── CTA ── */
    .cta {
      background: var(--card); border: 1px solid var(--border);
      border-radius: 14px; padding: 2rem 2.2rem; margin-top: 2.5rem;
      display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1rem;
      position: relative; overflow: hidden;
    }
    .cta::before {
      content:''; position: absolute; top:0; left:0; right:0; height:2px;
      background: linear-gradient(90deg, #63b3ed, #9f7aea, #68d391, #63b3ed);
      background-size: 300%; animation: gradShift 3s ease infinite;
    }
    .cta h3 { font-size: 1.15rem; font-weight: 600; margin-bottom: 4px; }
    .cta p { font-size: 0.85rem; color: var(--muted); }
    .btns { display: flex; gap: 10px; flex-wrap: wrap; }
    .btn {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 11px 24px; border-radius: 8px; font-size: 0.88rem; font-weight: 600;
      cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; text-decoration: none; border: none;
    }
    .btn-p { background: linear-gradient(135deg, #63b3ed, #9f7aea); color: #fff; }
    .btn-p:hover { transform: translateY(-2px); box-shadow: 0 8px 26px rgba(99,179,237,0.35); }
    .btn-g { background: transparent; color: var(--text); border: 1px solid var(--border); }
    .btn-g:hover { border-color: rgba(99,179,237,0.5); transform: translateY(-2px); }

    /* ── FOOTER ── */
    .footer {
      margin-top: 3rem; padding-top: 1.4rem; border-top: 1px solid var(--border);
      display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 0.8rem;
    }
    .footer p { font-size: 0.8rem; color: var(--muted); }
    .footer a { color: #63b3ed; text-decoration: none; }
    .flinks { display: flex; gap: 10px; }
    .flink {
      font-size: 0.78rem; color: var(--muted); text-decoration: none;
      padding: 4px 10px; border-radius: 6px; border: 1px solid transparent;
      transition: color 0.2s, border-color 0.2s;
    }
    .flink:hover { color: #63b3ed; border-color: var(--border); }
  </style>
</head>
<body>

  <!-- HERO -->
  <div class="hero">
    <div class="hero-grid"></div>
    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    <div class="orb orb3"></div>

    <div class="logo-wrap">
      <div class="logo-icon">📊</div>
      <span class="logo-title">InsightPilot</span>
    </div>

    <p class="hero-sub">
      An intelligent, interactive <strong>data analytics dashboard</strong> built with Python & Streamlit.
      Upload your data, explore trends, and surface insights — no code required.
    </p>

    <div class="badges">
      <span class="badge b-blue">🔵 Python 3.8+</span>
      <span class="badge b-purple">⚡ Streamlit</span>
      <span class="badge b-green">✅ Live on Cloud</span>
      <span class="badge b-orange">📦 Open Source</span>
      <span class="badge b-blue">📈 Interactive Charts</span>
    </div>
  </div>

  <!-- DEMO BAR -->
  <div class="container">
    <div class="demo-bar">
      <div class="dots">
        <div class="dot dr"></div>
        <div class="dot dy"></div>
        <div class="dot dg"></div>
      </div>
      <span class="demo-url">🌐 insightpilot-dashboard.streamlit.app</span>
      <div class="live-dot"></div>
      <span class="live-label">Live</span>
    </div>
  </div>

  <div class="container">

    <!-- OVERVIEW -->
    <div class="section">
      <div class="sec-label">Overview</div>
      <p class="overview">
        <strong>InsightPilot</strong> is a no-code analytics dashboard that lets you explore, filter, and visualize
        datasets instantly. Built for data analysts, students, and business teams who need
        <strong>fast answers from raw data</strong> — no coding required.
        Upload a CSV, configure your metrics, and get a live interactive report in seconds.
      </p>
    </div>

    <!-- STATS -->
    <div class="section">
      <div class="sec-label">At a glance</div>
      <div class="stats">
        <div class="stat"><div class="stat-n">100%</div><div class="stat-l">No-code friendly</div></div>
        <div class="stat"><div class="stat-n">&lt;5s</div><div class="stat-l">Time to insights</div></div>
        <div class="stat"><div class="stat-n">∞</div><div class="stat-l">Dataset rows</div></div>
        <div class="stat"><div class="stat-n">0</div><div class="stat-l">Login required</div></div>
      </div>
    </div>

    <!-- FEATURES -->
    <div class="section">
      <div class="sec-label">Features</div>
      <div class="features">
        <div class="feat">
          <div class="feat-ico" style="background:rgba(99,179,237,0.12);">📂</div>
          <div class="feat-name">CSV Upload</div>
          <div class="feat-desc">Drag & drop any CSV file and instantly preview your dataset with smart column detection.</div>
        </div>
        <div class="feat">
          <div class="feat-ico" style="background:rgba(159,122,234,0.12);">📈</div>
          <div class="feat-name">Interactive Charts</div>
          <div class="feat-desc">Bar, line, scatter, histogram — hover, zoom, and filter with Plotly-powered visualizations.</div>
        </div>
        <div class="feat">
          <div class="feat-ico" style="background:rgba(104,211,145,0.12);">🔎</div>
          <div class="feat-name">Smart Filters</div>
          <div class="feat-desc">Sidebar controls to slice and dice data by any column, date range, or category.</div>
        </div>
        <div class="feat">
          <div class="feat-ico" style="background:rgba(246,173,85,0.12);">📊</div>
          <div class="feat-name">KPI Summary</div>
          <div class="feat-desc">Auto-calculated key metrics — mean, sum, count, and more — as live stat cards.</div>
        </div>
        <div class="feat">
          <div class="feat-ico" style="background:rgba(99,179,237,0.12);">⬇️</div>
          <div class="feat-name">Export Data</div>
          <div class="feat-desc">Download filtered data as CSV directly from the dashboard with one click.</div>
        </div>
        <div class="feat">
          <div class="feat-ico" style="background:rgba(159,122,234,0.12);">☁️</div>
          <div class="feat-name">Cloud Deployed</div>
          <div class="feat-desc">Hosted on Streamlit Community Cloud — accessible from any browser, anywhere, anytime.</div>
        </div>
      </div>
    </div>

    <!-- STACK -->
    <div class="section">
      <div class="sec-label">Tech stack</div>
      <div class="stack">
        <div class="chip"><div class="cdot" style="background:#63b3ed;"></div>Python</div>
        <div class="chip"><div class="cdot" style="background:#f56565;"></div>Streamlit</div>
        <div class="chip"><div class="cdot" style="background:#9f7aea;"></div>Pandas</div>
        <div class="chip"><div class="cdot" style="background:#68d391;"></div>Plotly</div>
        <div class="chip"><div class="cdot" style="background:#f6ad55;"></div>NumPy</div>
        <div class="chip"><div class="cdot" style="background:#fc8181;"></div>HTML / CSS</div>
        <div class="chip"><div class="cdot" style="background:#4fd1c7;"></div>JavaScript</div>
      </div>
    </div>

    <!-- INSTALL -->
    <div class="section">
      <div class="sec-label">Getting started</div>
      <div class="code-block">
        <div class="code-head">
          <span class="code-lang">bash</span>
          <button class="copy-btn" onclick="
            navigator.clipboard.writeText('git clone https://github.com/YOUR_USERNAME/insightpilot\ncd insightpilot\npython -m venv venv\nsource venv/bin/activate\npip install -r requirements.txt\nstreamlit run app.py');
            this.textContent='✓ Copied!';
            setTimeout(()=>this.textContent='⎘ Copy',2000)
          ">⎘ Copy</button>
        </div>
        <pre><span class="cc"># 1. Clone the repo</span>
<span class="cmd">git clone</span> <span class="str">https://github.com/YOUR_USERNAME/insightpilot</span>
<span class="cmd">cd</span> insightpilot

<span class="cc"># 2. Create virtual environment</span>
<span class="cmd">python -m venv</span> venv
<span class="cmd">source</span> venv/bin/activate   <span class="cc"># Windows: venv\Scripts\activate</span>

<span class="cc"># 3. Install dependencies</span>
<span class="cmd">pip install</span> <span class="fl">-r</span> requirements.txt

<span class="cc"># 4. Run the app</span>
<span class="cmd">streamlit run</span> app.py</pre>
      </div>
      <p style="font-size:0.8rem; color:var(--muted); margin-top:8px; padding-left:4px;">
        App opens at
        <code style="color:#63b3ed; font-family:'JetBrains Mono',monospace; font-size:0.78rem;">http://localhost:8501</code>
      </p>
    </div>

    <!-- STRUCTURE -->
    <div class="section">
      <div class="sec-label">Project structure</div>
      <div class="tree">
<span class="td">insightpilot/</span>
├── <span class="td">assets/</span>           <span class="tn"># static files, icons</span>
├── <span class="td">components/</span>       <span class="tn"># reusable UI components</span>
├── <span class="td">pages/</span>            <span class="tn"># multi-page app modules</span>
├── app.py            <span class="tn"># main Streamlit entry point</span>
├── utils.py          <span class="tn"># data processing helpers</span>
├── requirements.txt  <span class="tn"># Python dependencies</span>
└── README.md</div>
    </div>

    <!-- CTA -->
    <div class="cta">
      <div>
        <h3>🚀 Try InsightPilot live</h3>
        <p>No sign-up, no setup. Open the app and drop in your data.</p>
      </div>
      <div class="btns">
        <a class="btn btn-p" href="https://insightpilot-dashboard.streamlit.app/" target="_blank">Open Live App ↗</a>
        <a class="btn btn-g" href="https://github.com/" target="_blank">View on GitHub ↗</a>
      </div>
    </div>

    <!-- FOOTER -->
    <div class="footer">
      <p>Built with ❤️ using <a href="https://streamlit.io" target="_blank">Streamlit</a> · MIT License</p>
      <div class="flinks">
        <a class="flink" href="https://insightpilot-dashboard.streamlit.app/" target="_blank">Live App</a>
        <a class="flink" href="#">GitHub</a>
        <a class="flink" href="#">Issues</a>
      </div>
    </div>

  </div>
</body>
</html>
