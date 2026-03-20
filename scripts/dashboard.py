#!/usr/bin/env python3
"""
dashboard.py — Local project documentation site
Serves docs/ as a styled website at http://localhost:3100

Usage: python3 scripts/dashboard.py
"""

import hashlib
import http.server
import re
import socket
import sys
import threading
import time
import urllib.parse
from pathlib import Path

# Install markdown if missing (--user handles externally-managed Python on macOS/Linux)
try:
    import markdown as md_lib
except ImportError:
    import subprocess
    for flags in [["--user"], ["--break-system-packages", "--user"], []]:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "markdown", "-q"] + flags,
            capture_output=True
        )
        if result.returncode == 0:
            break
    try:
        import markdown as md_lib
    except ImportError:
        print("Error: could not install 'markdown'. Run: pip3 install --user markdown")
        sys.exit(1)

PORT_START = 3100
ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"

# ── Live reload state ─────────────────────────────────────────────────────────
_reload_token = str(time.time())
_file_hashes: dict = {}

def _hash_docs():
    h = {}
    for f in DOCS_DIR.glob("*.md"):
        try:
            h[str(f)] = hashlib.md5(f.read_bytes()).hexdigest()
        except OSError:
            pass
    return h

def _watch_loop():
    global _reload_token, _file_hashes
    _file_hashes = _hash_docs()
    while True:
        time.sleep(1)
        current = _hash_docs()
        if current != _file_hashes:
            _file_hashes = current
            _reload_token = str(time.time())

def _find_port(start: int) -> int:
    for port in range(start, start + 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
    return start

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
    html = md_lib.markdown(text, extensions=["tables", "fenced_code"])
    html = rewrite_md_links(html)
    html = wrap_tables(html)
    return html

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

    reload_js = """
<script>
(function(){
  var t = null;
  function check(){
    fetch('/__reload_token__').then(r=>r.text()).then(tok=>{
      if(t === null){ t = tok; } else if(tok !== t){ location.reload(); }
      setTimeout(check, 1200);
    }).catch(()=>{ setTimeout(check, 3000); });
  }
  check();
})();
</script>"""

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
{reload_js}
</body>
</html>"""

# ── Request handler ───────────────────────────────────────────────────────────

class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path.strip("/")

        if path == "__reload_token__":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(_reload_token.encode())
            return

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

    PORT = _find_port(PORT_START)

    threading.Thread(target=_watch_loop, daemon=True).start()

    print(f"Dashboard → http://localhost:{PORT}  (auto-reloads on file save)")
    print("Ctrl+C to stop.")

    server = http.server.HTTPServer(("", PORT), DashboardHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
