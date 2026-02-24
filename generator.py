"""
Portfolio HTML Generator
3 ta chiroyli template: dark, light, creative
"""

from jinja2 import Template


DARK_TEMPLATE = """<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{{ full_name }} — Portfolio</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap" rel="stylesheet"/>
  <style>
    :root {
      --bg: #0a0a0f;
      --surface: #13131a;
      --border: #1e1e2e;
      --accent: #7c3aed;
      --accent2: #06b6d4;
      --text: #e2e8f0;
      --muted: #64748b;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Syne', sans-serif;
      overflow-x: hidden;
    }
    /* Noise overlay */
    body::before {
      content: '';
      position: fixed; inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
      pointer-events: none; z-index: 9999;
    }

    /* HERO */
    .hero {
      min-height: 100vh;
      display: flex; flex-direction: column; justify-content: center;
      padding: 80px 10%;
      position: relative;
      overflow: hidden;
    }
    .hero::after {
      content: '';
      position: absolute;
      width: 600px; height: 600px;
      background: radial-gradient(circle, rgba(124,58,237,0.15) 0%, transparent 70%);
      top: -100px; right: -100px;
      border-radius: 50%;
    }
    .hero-label {
      font-family: 'Space Mono', monospace;
      color: var(--accent);
      font-size: 0.75rem;
      letter-spacing: 4px;
      text-transform: uppercase;
      margin-bottom: 20px;
      opacity: 0; animation: fadeUp 0.6s 0.2s forwards;
    }
    .hero h1 {
      font-size: clamp(3rem, 8vw, 7rem);
      font-weight: 800;
      line-height: 1;
      letter-spacing: -3px;
      background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      opacity: 0; animation: fadeUp 0.6s 0.4s forwards;
    }
    .hero-profession {
      margin-top: 16px;
      font-size: 1.25rem;
      color: var(--accent2);
      font-weight: 600;
      opacity: 0; animation: fadeUp 0.6s 0.6s forwards;
    }
    .hero-bio {
      margin-top: 24px;
      max-width: 600px;
      line-height: 1.8;
      color: var(--muted);
      font-size: 1rem;
      opacity: 0; animation: fadeUp 0.6s 0.8s forwards;
    }
    .hero-contacts {
      margin-top: 40px;
      display: flex; flex-wrap: wrap; gap: 12px;
      opacity: 0; animation: fadeUp 0.6s 1s forwards;
    }
    .contact-btn {
      padding: 10px 22px;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text);
      text-decoration: none;
      font-family: 'Space Mono', monospace;
      font-size: 0.8rem;
      transition: all 0.3s;
      background: var(--surface);
    }
    .contact-btn:hover {
      border-color: var(--accent);
      color: var(--accent);
      transform: translateY(-2px);
    }

    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* SECTIONS */
    section {
      padding: 80px 10%;
      border-top: 1px solid var(--border);
    }
    .section-label {
      font-family: 'Space Mono', monospace;
      color: var(--accent);
      font-size: 0.7rem;
      letter-spacing: 4px;
      text-transform: uppercase;
      margin-bottom: 40px;
    }
    .section-title {
      font-size: 2.5rem;
      font-weight: 800;
      margin-bottom: 48px;
      letter-spacing: -1px;
    }

    /* SKILLS */
    .skills-grid {
      display: flex; flex-wrap: wrap; gap: 10px;
    }
    .skill-tag {
      padding: 8px 18px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
      font-family: 'Space Mono', monospace;
      font-size: 0.8rem;
      transition: all 0.3s;
    }
    .skill-tag:hover {
      border-color: var(--accent);
      background: rgba(124,58,237,0.1);
    }

    /* EXPERIENCE */
    .exp-list { display: flex; flex-direction: column; gap: 24px; }
    .exp-item {
      display: grid; grid-template-columns: 180px 1fr;
      gap: 20px; padding: 24px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      transition: border-color 0.3s;
    }
    .exp-item:hover { border-color: var(--accent); }
    .exp-period {
      font-family: 'Space Mono', monospace;
      font-size: 0.75rem;
      color: var(--accent2);
      padding-top: 4px;
    }
    .exp-role { font-size: 1.1rem; font-weight: 600; }
    .exp-company { color: var(--muted); font-size: 0.9rem; margin-top: 4px; }

    /* PROJECTS */
    .projects-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
    }
    .project-card {
      padding: 28px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      transition: all 0.3s;
      position: relative; overflow: hidden;
    }
    .project-card::before {
      content: '';
      position: absolute; top: 0; left: 0; right: 0;
      height: 2px;
      background: linear-gradient(90deg, var(--accent), var(--accent2));
      transform: scaleX(0); transition: transform 0.3s;
    }
    .project-card:hover { transform: translateY(-4px); border-color: var(--accent); }
    .project-card:hover::before { transform: scaleX(1); }
    .project-name { font-size: 1.1rem; font-weight: 700; margin-bottom: 8px; }
    .project-desc { color: var(--muted); font-size: 0.9rem; line-height: 1.6; }
    .project-link {
      display: inline-block; margin-top: 16px;
      color: var(--accent2);
      text-decoration: none;
      font-family: 'Space Mono', monospace;
      font-size: 0.75rem;
    }
    .project-link:hover { color: var(--accent); }

    /* FOOTER */
    footer {
      padding: 40px 10%;
      border-top: 1px solid var(--border);
      text-align: center;
      color: var(--muted);
      font-family: 'Space Mono', monospace;
      font-size: 0.75rem;
    }

    @media (max-width: 768px) {
      .hero { padding: 60px 5%; }
      section { padding: 60px 5%; }
      .exp-item { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <section class="hero">
    <p class="hero-label">// Portfolio</p>
    <h1>{{ full_name }}</h1>
    <p class="hero-profession">{{ profession }}</p>
    <p class="hero-bio">{{ bio }}</p>
    <div class="hero-contacts">
      {% if email %}<a href="mailto:{{ email }}" class="contact-btn">📧 {{ email }}</a>{% endif %}
      {% if phone %}<a href="tel:{{ phone }}" class="contact-btn">📱 {{ phone }}</a>{% endif %}
      {% if github %}<a href="https://{{ github }}" target="_blank" class="contact-btn">🐙 GitHub</a>{% endif %}
      {% if linkedin %}<a href="https://{{ linkedin }}" target="_blank" class="contact-btn">💼 LinkedIn</a>{% endif %}
    </div>
  </section>

  {% if skills %}
  <section>
    <p class="section-label">// Skills</p>
    <h2 class="section-title">Ko'nikmalar</h2>
    <div class="skills-grid">
      {% for skill in skills %}
      <span class="skill-tag">{{ skill }}</span>
      {% endfor %}
    </div>
  </section>
  {% endif %}

  {% if experience %}
  <section>
    <p class="section-label">// Experience</p>
    <h2 class="section-title">Tajriba</h2>
    <div class="exp-list">
      {% for exp in experience %}
      <div class="exp-item">
        <div class="exp-period">{{ exp.period }}</div>
        <div>
          <div class="exp-role">{{ exp.role }}</div>
          <div class="exp-company">{{ exp.company }}</div>
        </div>
      </div>
      {% endfor %}
    </div>
  </section>
  {% endif %}

  {% if projects %}
  <section>
    <p class="section-label">// Projects</p>
    <h2 class="section-title">Loyihalar</h2>
    <div class="projects-grid">
      {% for p in projects %}
      <div class="project-card">
        <div class="project-name">{{ p.name }}</div>
        <div class="project-desc">{{ p.desc }}</div>
        {% if p.link %}<a href="https://{{ p.link }}" class="project-link" target="_blank">→ Ko'rish</a>{% endif %}
      </div>
      {% endfor %}
    </div>
  </section>
  {% endif %}

  <footer>
    <p>{{ full_name }} &copy; 2024 &mdash; Made with Portfolio Bot</p>
  </footer>
</body>
</html>"""


LIGHT_TEMPLATE = """<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{{ full_name }} — Portfolio</title>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@300;400;700;900&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet"/>
  <style>
    :root {
      --bg: #faf9f7;
      --surface: #ffffff;
      --accent: #d4522a;
      --text: #1a1a1a;
      --muted: #8a8a8a;
      --border: #e8e4de;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'DM Sans', sans-serif;
    }
    .hero {
      min-height: 100vh;
      display: grid;
      grid-template-columns: 1fr 1fr;
      align-items: center;
    }
    .hero-left {
      padding: 80px;
      border-right: 1px solid var(--border);
    }
    .hero-right {
      padding: 80px;
      display: flex; flex-direction: column; gap: 32px;
    }
    .tag {
      display: inline-block;
      padding: 4px 12px;
      background: var(--accent);
      color: white;
      font-size: 0.7rem;
      letter-spacing: 3px;
      text-transform: uppercase;
      margin-bottom: 24px;
    }
    h1 {
      font-family: 'Fraunces', serif;
      font-size: clamp(3.5rem, 6vw, 6rem);
      font-weight: 900;
      line-height: 1;
      letter-spacing: -2px;
    }
    .profession {
      margin-top: 16px;
      font-size: 1.1rem;
      color: var(--accent);
      font-weight: 500;
    }
    .bio {
      font-size: 1rem;
      line-height: 1.9;
      color: #555;
    }
    .contacts { display: flex; flex-direction: column; gap: 8px; }
    .contact-item {
      display: flex; align-items: center; gap: 12px;
      padding: 12px 0;
      border-bottom: 1px solid var(--border);
      text-decoration: none;
      color: var(--text);
      font-size: 0.9rem;
      transition: color 0.2s;
    }
    .contact-item:hover { color: var(--accent); }
    .contact-label { color: var(--muted); font-size: 0.75rem; width: 80px; }

    section {
      padding: 80px;
      border-top: 1px solid var(--border);
    }
    .section-header {
      display: flex; align-items: baseline; gap: 20px;
      margin-bottom: 48px;
    }
    .section-num {
      font-family: 'Fraunces', serif;
      font-size: 4rem;
      font-weight: 900;
      color: var(--border);
      line-height: 1;
    }
    .section-title {
      font-family: 'Fraunces', serif;
      font-size: 2rem;
      font-weight: 700;
    }

    .skills-grid { display: flex; flex-wrap: wrap; gap: 8px; }
    .skill-tag {
      padding: 6px 16px;
      border: 1px solid var(--border);
      font-size: 0.85rem;
      border-radius: 2px;
      transition: all 0.2s;
    }
    .skill-tag:hover { border-color: var(--accent); color: var(--accent); }

    .exp-item {
      display: grid; grid-template-columns: 200px 1fr;
      padding: 24px 0;
      border-bottom: 1px solid var(--border);
      gap: 24px;
    }
    .exp-period { font-size: 0.8rem; color: var(--muted); padding-top: 3px; }
    .exp-role { font-size: 1.05rem; font-weight: 500; }
    .exp-company { font-size: 0.9rem; color: var(--accent); margin-top: 4px; }

    .projects-list { display: flex; flex-direction: column; gap: 0; }
    .project-item {
      display: grid; grid-template-columns: 1fr auto;
      align-items: center;
      padding: 24px 0;
      border-bottom: 1px solid var(--border);
      gap: 20px;
    }
    .project-name {
      font-family: 'Fraunces', serif;
      font-size: 1.3rem;
      font-weight: 700;
    }
    .project-desc { color: var(--muted); font-size: 0.9rem; margin-top: 4px; }
    .project-link {
      padding: 8px 20px;
      border: 1px solid var(--text);
      font-size: 0.8rem;
      text-decoration: none;
      color: var(--text);
      white-space: nowrap;
      transition: all 0.2s;
    }
    .project-link:hover { background: var(--text); color: white; }

    footer {
      padding: 40px 80px;
      border-top: 1px solid var(--border);
      display: flex; justify-content: space-between; align-items: center;
      font-size: 0.8rem; color: var(--muted);
    }

    @media (max-width: 900px) {
      .hero { grid-template-columns: 1fr; }
      .hero-left, .hero-right { padding: 40px; border-right: none; }
      section { padding: 60px 40px; }
      .exp-item { grid-template-columns: 1fr; }
      footer { flex-direction: column; gap: 8px; padding: 40px; }
    }
  </style>
</head>
<body>
  <div class="hero">
    <div class="hero-left">
      <span class="tag">Portfolio</span>
      <h1>{{ full_name }}</h1>
      <p class="profession">{{ profession }}</p>
    </div>
    <div class="hero-right">
      <p class="bio">{{ bio }}</p>
      <div class="contacts">
        {% if email %}<a href="mailto:{{ email }}" class="contact-item"><span class="contact-label">Email</span>{{ email }}</a>{% endif %}
        {% if phone %}<a href="tel:{{ phone }}" class="contact-item"><span class="contact-label">Tel</span>{{ phone }}</a>{% endif %}
        {% if github %}<a href="https://{{ github }}" class="contact-item" target="_blank"><span class="contact-label">GitHub</span>{{ github }}</a>{% endif %}
        {% if linkedin %}<a href="https://{{ linkedin }}" class="contact-item" target="_blank"><span class="contact-label">LinkedIn</span>{{ linkedin }}</a>{% endif %}
      </div>
    </div>
  </div>

  {% if skills %}
  <section>
    <div class="section-header">
      <span class="section-num">01</span>
      <h2 class="section-title">Ko'nikmalar</h2>
    </div>
    <div class="skills-grid">
      {% for skill in skills %}
      <span class="skill-tag">{{ skill }}</span>
      {% endfor %}
    </div>
  </section>
  {% endif %}

  {% if experience %}
  <section>
    <div class="section-header">
      <span class="section-num">02</span>
      <h2 class="section-title">Tajriba</h2>
    </div>
    {% for exp in experience %}
    <div class="exp-item">
      <div class="exp-period">{{ exp.period }}</div>
      <div>
        <div class="exp-role">{{ exp.role }}</div>
        <div class="exp-company">{{ exp.company }}</div>
      </div>
    </div>
    {% endfor %}
  </section>
  {% endif %}

  {% if projects %}
  <section>
    <div class="section-header">
      <span class="section-num">03</span>
      <h2 class="section-title">Loyihalar</h2>
    </div>
    <div class="projects-list">
      {% for p in projects %}
      <div class="project-item">
        <div>
          <div class="project-name">{{ p.name }}</div>
          <div class="project-desc">{{ p.desc }}</div>
        </div>
        {% if p.link %}<a href="https://{{ p.link }}" class="project-link" target="_blank">Ko'rish →</a>{% endif %}
      </div>
      {% endfor %}
    </div>
  </section>
  {% endif %}

  <footer>
    <span>{{ full_name }}</span>
    <span>Made with Portfolio Bot &copy; 2024</span>
  </footer>
</body>
</html>"""


CREATIVE_TEMPLATE = """<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{{ full_name }}</title>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet"/>
  <style>
    :root {
      --bg: #111;
      --yellow: #f5e642;
      --pink: #ff3e9d;
      --blue: #3efff8;
      --text: #f0f0f0;
      --muted: #888;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: var(--bg); color: var(--text); font-family: 'Outfit', sans-serif; }

    /* HERO */
    .hero {
      min-height: 100vh;
      display: flex; flex-direction: column; justify-content: flex-end;
      padding: 60px;
      position: relative; overflow: hidden;
    }
    .hero-bg-text {
      position: absolute;
      top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      font-family: 'Bebas Neue', sans-serif;
      font-size: clamp(8rem, 18vw, 18rem);
      white-space: nowrap;
      color: transparent;
      -webkit-text-stroke: 1px rgba(255,255,255,0.05);
      pointer-events: none;
      user-select: none;
      letter-spacing: -4px;
    }
    .hero-top {
      position: absolute; top: 40px; right: 60px;
      display: flex; gap: 20px;
    }
    .hero-top a {
      color: var(--muted);
      text-decoration: none;
      font-size: 0.8rem;
      transition: color 0.2s;
    }
    .hero-top a:hover { color: var(--yellow); }

    .hero-name {
      font-family: 'Bebas Neue', sans-serif;
      font-size: clamp(5rem, 12vw, 11rem);
      line-height: 0.9;
      letter-spacing: -2px;
      position: relative;
    }
    .hero-name span { color: var(--yellow); }
    .hero-row {
      display: flex; align-items: flex-end; justify-content: space-between;
      flex-wrap: wrap; gap: 20px; margin-top: 20px;
    }
    .hero-profession {
      font-size: 1rem;
      color: var(--pink);
      letter-spacing: 3px;
      text-transform: uppercase;
    }
    .hero-bio {
      max-width: 400px;
      font-size: 0.9rem;
      line-height: 1.8;
      color: var(--muted);
    }

    .scroll-line {
      width: 100%; height: 1px;
      background: linear-gradient(90deg, var(--yellow), var(--pink), var(--blue));
      margin: 60px 0 0;
    }

    /* SECTIONS */
    section { padding: 80px 60px; border-bottom: 1px solid #222; }
    .sec-head {
      display: flex; align-items: center; gap: 20px;
      margin-bottom: 48px;
    }
    .sec-num {
      font-family: 'Bebas Neue', sans-serif;
      font-size: 5rem;
      color: var(--yellow);
      line-height: 1;
    }
    .sec-title {
      font-family: 'Bebas Neue', sans-serif;
      font-size: 3rem;
      letter-spacing: 2px;
    }

    /* SKILLS */
    .skills-wrap { display: flex; flex-wrap: wrap; gap: 12px; }
    .skill {
      padding: 10px 20px;
      border: 1px solid #333;
      font-size: 0.85rem;
      font-weight: 500;
      cursor: default;
      transition: all 0.25s;
      position: relative; overflow: hidden;
    }
    .skill::before {
      content: '';
      position: absolute; inset: 0;
      background: var(--yellow);
      transform: translateY(100%); transition: transform 0.25s;
      z-index: -1;
    }
    .skill:hover { color: #111; border-color: var(--yellow); }
    .skill:hover::before { transform: translateY(0); }

    /* EXP */
    .exp-item {
      display: flex; gap: 40px;
      padding: 28px 0;
      border-bottom: 1px solid #1e1e1e;
    }
    .exp-period {
      font-family: 'Bebas Neue', sans-serif;
      font-size: 1rem;
      color: var(--blue);
      letter-spacing: 2px;
      min-width: 150px;
      padding-top: 4px;
    }
    .exp-role { font-size: 1.15rem; font-weight: 600; }
    .exp-company { color: var(--muted); margin-top: 4px; }

    /* PROJECTS */
    .projects-wrap {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 2px;
    }
    .proj {
      background: #1a1a1a;
      padding: 32px;
      transition: background 0.3s;
      position: relative; overflow: hidden;
    }
    .proj::after {
      content: attr(data-num);
      position: absolute; bottom: -10px; right: 10px;
      font-family: 'Bebas Neue', sans-serif;
      font-size: 5rem;
      color: rgba(255,255,255,0.03);
      line-height: 1;
    }
    .proj:hover { background: #222; }
    .proj-name {
      font-family: 'Bebas Neue', sans-serif;
      font-size: 1.8rem;
      letter-spacing: 1px;
      color: var(--yellow);
      margin-bottom: 8px;
    }
    .proj-desc { color: var(--muted); font-size: 0.9rem; line-height: 1.6; }
    .proj-link {
      display: inline-block;
      margin-top: 20px;
      padding: 8px 18px;
      background: var(--pink);
      color: #fff;
      text-decoration: none;
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 1px;
      text-transform: uppercase;
      transition: opacity 0.2s;
    }
    .proj-link:hover { opacity: 0.8; }

    /* FOOTER */
    footer {
      padding: 40px 60px;
      display: flex; justify-content: space-between; align-items: center;
      flex-wrap: wrap; gap: 12px;
    }
    .footer-name {
      font-family: 'Bebas Neue', sans-serif;
      font-size: 1.5rem;
      letter-spacing: 2px;
      color: var(--yellow);
    }
    .footer-copy { font-size: 0.75rem; color: var(--muted); }

    @media (max-width: 768px) {
      .hero { padding: 40px; }
      section { padding: 60px 40px; }
      .exp-item { flex-direction: column; gap: 8px; }
      footer { padding: 40px; }
    }
  </style>
</head>
<body>
  <div class="hero">
    <div class="hero-bg-text">{{ full_name.upper() }}</div>
    <div class="hero-top">
      {% if github %}<a href="https://{{ github }}" target="_blank">GitHub</a>{% endif %}
      {% if linkedin %}<a href="https://{{ linkedin }}" target="_blank">LinkedIn</a>{% endif %}
      {% if email %}<a href="mailto:{{ email }}">Email</a>{% endif %}
    </div>
    <div class="hero-name">
      {% set parts = full_name.split() %}
      {% if parts|length > 1 %}
        {{ parts[0] }} <span>{{ parts[1:] | join(' ') }}</span>
      {% else %}
        <span>{{ full_name }}</span>
      {% endif %}
    </div>
    <div class="hero-row">
      <p class="hero-profession">{{ profession }}</p>
      <p class="hero-bio">{{ bio }}</p>
    </div>
    <div class="scroll-line"></div>
  </div>

  {% if skills %}
  <section>
    <div class="sec-head">
      <span class="sec-num">01</span>
      <span class="sec-title">Skills</span>
    </div>
    <div class="skills-wrap">
      {% for s in skills %}
      <div class="skill">{{ s }}</div>
      {% endfor %}
    </div>
  </section>
  {% endif %}

  {% if experience %}
  <section>
    <div class="sec-head">
      <span class="sec-num">02</span>
      <span class="sec-title">Tajriba</span>
    </div>
    {% for exp in experience %}
    <div class="exp-item">
      <div class="exp-period">{{ exp.period }}</div>
      <div>
        <div class="exp-role">{{ exp.role }}</div>
        <div class="exp-company">{{ exp.company }}</div>
      </div>
    </div>
    {% endfor %}
  </section>
  {% endif %}

  {% if projects %}
  <section>
    <div class="sec-head">
      <span class="sec-num">03</span>
      <span class="sec-title">Loyihalar</span>
    </div>
    <div class="projects-wrap">
      {% for p in projects %}
      <div class="proj" data-num="{{ loop.index }}">
        <div class="proj-name">{{ p.name }}</div>
        <div class="proj-desc">{{ p.desc }}</div>
        {% if p.link %}<a href="https://{{ p.link }}" class="proj-link" target="_blank">Ko'rish →</a>{% endif %}
      </div>
      {% endfor %}
    </div>
  </section>
  {% endif %}

  <footer>
    <div class="footer-name">{{ full_name }}</div>
    <div class="footer-copy">Made with Portfolio Bot &copy; 2024</div>
  </footer>
</body>
</html>"""


def generate_portfolio(data: dict, output_path: str):
    template_name = data.get("template", "dark")

    if template_name == "light":
        tmpl = LIGHT_TEMPLATE
    elif template_name == "creative":
        tmpl = CREATIVE_TEMPLATE
    else:
        tmpl = DARK_TEMPLATE

    t = Template(tmpl)
    html = t.render(
        full_name=data.get("full_name", ""),
        profession=data.get("profession", ""),
        bio=data.get("bio", ""),
        skills=data.get("skills", []),
        experience=data.get("experience", []),
        projects=data.get("projects", []),
        github=data.get("github", ""),
        linkedin=data.get("linkedin", ""),
        email=data.get("email", ""),
        phone=data.get("phone", ""),
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
