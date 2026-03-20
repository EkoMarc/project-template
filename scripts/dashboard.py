#!/usr/bin/env python3
"""
dashboard.py — Local project documentation site
Serves docs/ as a styled website at http://localhost:3100

Usage: python3 scripts/dashboard.py
"""

import http.server
import re
import sys
import urllib.parse
from pathlib import Path

# Install markdown if missing
try:
    import markdown as md_lib
    MD_AVAILABLE = True
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "markdown", "-q"], check=False)
    try:
        import markdown as md_lib
        MD_AVAILABLE = True
    except ImportError:
        MD_AVAILABLE = False

PORT = 3100
ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"

TOP_LEVEL_PAGES = ["overview", "tasks", "context", "decisions", "stack", "workflows"]
PAGE_LABELS = {
    "overview": "Overview",
    "tasks": "Tasks",
    "context": "Context",
    "decisions": "Decisions",
    "stack": "Stack",
    "workflows": "Workflows",
    "template-context": "About This Template",
}

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS = """
:root {
    --primary: #1a73e8;
    --primary-bg: #e8f0fe;
    --surface: #f8f9fa;
    --surface-2: #ffffff;
    --text: #202124;
    --text-secondary: #5f6368;
    --border: #e0e0e0;
    --radius: 8px;
    --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --mono: 'SF Mono', 'Fira Code', 'Consolas', monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: var(--font);
    color: var(--text);
    background: var(--surface);
    display: flex;
    min-height: 100vh;
}

/* ── Sidebar ── */
nav {
    width: 224px;
    min-width: 224px;
    background: var(--surface-2);
    border-right: 1px solid var(--border);
    padding: 0 0 32px;
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}
.nav-project {
    font-size: 15px;
    font-weight: 600;
    color: var(--text);
    padding: 24px 20px 16px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 8px;
}
.nav-section-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-secondary);
    padding: 16px 20px 4px;
}
nav a {
    display: block;
    padding: 7px 20px;
    color: var(--text);
    text-decoration: none;
    font-size: 14px;
    border-radius: 0 20px 20px 0;
    margin-right: 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
nav a:hover { background: var(--surface); }
nav a.active { background: var(--primary-bg); color: var(--primary); font-weight: 500; }
.nav-secondary a {
    font-size: 13px;
    color: var(--text-secondary);
    padding: 5px 20px 5px 28px;
}
.nav-secondary a.active { color: var(--primary); background: var(--primary-bg); }

/* ── Content ── */
main {
    flex: 1;
    max-width: 860px;
    padding: 48px 56px 80px;
}
main > *:first-child { margin-top: 0; }

h1 { font-size: 28px; font-weight: 600; line-height: 1.2; margin-bottom: 6px; }
h2 { font-size: 20px; font-weight: 600; margin: 40px 0 12px; padding-top: 8px; border-top: 1px solid var(--border); }
h2:first-of-type { border-top: none; margin-top: 24px; }
h3 { font-size: 15px; font-weight: 600; margin: 24px 0 8px; }
p  { line-height: 1.65; margin-bottom: 14px; }
p:last-child { margin-bottom: 0; }

blockquote {
    border-left: 3px solid var(--primary);
    padding: 10px 16px;
    background: var(--primary-bg);
    border-radius: 0 var(--radius) var(--radius) 0;
    margin: 16px 0;
    color: var(--text-secondary);
    font-size: 14px;
    line-height: 1.6;
}
blockquote p { margin-bottom: 6px; }
blockquote p:last-child { margin-bottom: 0; }

code {
    background: #f1f3f4;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 13px;
    font-family: var(--mono);
}
pre {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 16px 20px;
    border-radius: var(--radius);
    overflow-x: auto;
    margin: 16px 0;
    font-size: 13px;
    line-height: 1.5;
}
pre code { background: none; color: inherit; padding: 0; font-size: inherit; }

/* ── Tables ── */
.table-wrap { overflow-x: auto; margin: 16px 0; border-radius: var(--radius); border: 1px solid var(--border); }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
thead { background: var(--surface); }
th {
    text-align: left;
    padding: 10px 14px;
    font-weight: 600;
    font-size: 13px;
    color: var(--text-secondary);
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
}
td { padding: 10px 14px; border-bottom: 1px solid var(--border); vertical-align: top; }
tr:last-child td { border-bottom: none; }
tbody tr:hover { background: var(--surface); }

a { color: var(--primary); text-decoration: none; }
a:hover { text-decoration: underline; }
ul, ol { padding-left: 24px; margin-bottom: 14px; line-height: 1.7; }
li { margin-bottom: 2px; }
hr { border: none; border-top: 1px solid var(--border); margin: 32px 0; }
input[type="checkbox"] { margin-right: 6px; vertical-align: middle; accent-color: var(--primary); }
"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_project_name():
    for fname in ["AGENTS.md", "README.md"]:
        f = ROOT / fname
        if f.exists():
            for line in f.read_text().splitlines():
                if line.startswith("# "):
                    name = line[2:].strip()
                    if name and "[" not in name:
                        return name
    return "Project"

def get_nav_pages():
    """Returns (top_pages, secondary_pages) as lists of (slug, label)."""
    top, secondary = [], []
    for name in TOP_LEVEL_PAGES:
        if (DOCS_DIR / f"{name}.md").exists():
            top.append((name, PAGE_LABELS.get(name, name.title())))
    for path in sorted(DOCS_DIR.glob("*.md")):
        name = path.stem
        if name not in TOP_LEVEL_PAGES:
            label = PAGE_LABELS.get(name, name.replace("-", " ").title())
            secondary.append((name, label))
    return top, secondary

def strip_comments(text):
    """Remove HTML comments (agent-only notes) from markdown before rendering."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip()

def rewrite_md_links(html):
    """Rewrite links like href="tasks.md" → href="/tasks" so wiki links work."""
    def repl(m):
        href = m.group(1)
        if href.endswith(".md") and not href.startswith("http"):
            slug = href[:-3].lstrip("./")
            return f'href="/{slug}"'
        return m.group(0)
    return re.sub(r'href="([^"]+)"', repl, html)

def wrap_tables(html):
    """Wrap tables in a scroll container for overflow handling."""
    return html.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")

def preprocess_tasklists(text):
    """Convert - [ ] and - [x] to HTML checkboxes before markdown parsing."""
    text = re.sub(r"^(\s*)-\s+\[x\]\s+", r"\1- <input type='checkbox' checked disabled> ", text, flags=re.MULTILINE)
    text = re.sub(r"^(\s*)-\s+\[ \]\s+", r"\1- <input type='checkbox' disabled> ", text, flags=re.MULTILINE)
    return text

def render_md(text):
    text = strip_comments(text)
    text = preprocess_tasklists(text)
    if MD_AVAILABLE:
        # Note: no nl2br — it inserts <br> tags that break list parsing
        html = md_lib.markdown(text, extensions=["tables", "fenced_code"])
    else:
        html = _fallback_render(text)
    html = rewrite_md_links(html)
    html = wrap_tables(html)
    return html

def _fallback_render(text):
    """Minimal renderer used only when the markdown package is unavailable."""
    lines = text.splitlines()
    out = []
    in_table = False
    in_pre = False
    buf = []

    def flush_para():
        if buf:
            content = " ".join(buf).strip()
            if content:
                out.append(f"<p>{inline(content)}</p>")
            buf.clear()

    def inline(s):
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        return s

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            flush_para()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            out.append(f"<pre><code>{chr(10).join(code_lines)}</code></pre>")
            i += 1
            continue

        if line.startswith("# "):
            flush_para(); out.append(f"<h1>{inline(line[2:])}</h1>"); i += 1; continue
        if line.startswith("## "):
            flush_para(); out.append(f"<h2>{inline(line[3:])}</h2>"); i += 1; continue
        if line.startswith("### "):
            flush_para(); out.append(f"<h3>{inline(line[4:])}</h3>"); i += 1; continue
        if line.startswith("> "):
            flush_para(); out.append(f"<blockquote><p>{inline(line[2:])}</p></blockquote>"); i += 1; continue
        if line.startswith("---"):
            flush_para(); out.append("<hr>"); i += 1; continue
        if line.startswith("| "):
            flush_para()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[-| :]+\|$", lines[i]):
                    rows.append(lines[i])
                i += 1
            if rows:
                th_cells = [f"<th>{inline(c.strip())}</th>" for c in rows[0].split("|")[1:-1]]
                table_html = f"<table><thead><tr>{''.join(th_cells)}</tr></thead><tbody>"
                for row in rows[1:]:
                    td_cells = [f"<td>{inline(c.strip())}</td>" for c in row.split("|")[1:-1]]
                    table_html += f"<tr>{''.join(td_cells)}</tr>"
                table_html += "</tbody></table>"
                out.append(table_html)
            continue
        if line.strip() == "":
            flush_para(); i += 1; continue

        buf.append(line)
        i += 1

    flush_para()
    return "\n".join(out)

def render_page(slug, content_html, project_name):
    top_pages, secondary_pages = get_nav_pages()

    nav_top = ""
    for name, label in top_pages:
        cls = "active" if name == slug else ""
        nav_top += f'<a href="/{name}" class="{cls}">{label}</a>\n'

    nav_secondary = ""
    if secondary_pages:
        nav_secondary = '<div class="nav-section-label">More</div><div class="nav-secondary">'
        for name, label in secondary_pages:
            cls = "active" if name == slug else ""
            nav_secondary += f'<a href="/{name}" class="{cls}">{label}</a>\n'
        nav_secondary += "</div>"

    all_pages = top_pages + secondary_pages
    page_label = dict(all_pages).get(slug, slug.replace("-", " ").title())

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_label} — {project_name}</title>
<style>{CSS}</style>
</head>
<body>
<nav>
  <div class="nav-project">{project_name}</div>
  {nav_top}
  {nav_secondary}
</nav>
<main>
{content_html}
</main>
</body>
</html>"""

# ── Request handler ───────────────────────────────────────────────────────────

class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path.strip("/")
        if not path:
            path = "overview"

        md_file = DOCS_DIR / f"{path}.md"
        project_name = get_project_name()

        if md_file.exists():
            raw = md_file.read_text(encoding="utf-8")
            content = render_md(raw)
            html = render_page(path, content, project_name)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        else:
            # Try to find close match
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                f"<html><body style='font-family:sans-serif;padding:48px'>"
                f"<h2>Page not found: {path}</h2>"
                f"<p><a href='/overview' style='color:#1a73e8'>← Back to Overview</a></p>"
                f"</body></html>".encode()
            )

# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not DOCS_DIR.exists():
        print(f"Error: docs/ folder not found at {DOCS_DIR}")
        sys.exit(1)

    print(f"Dashboard → http://localhost:{PORT}")
    print("Ctrl+C to stop.")

    server = http.server.HTTPServer(("", PORT), DashboardHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
