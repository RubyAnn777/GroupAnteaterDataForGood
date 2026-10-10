"""Build docs/overnight/REPORT.html and REPORT.md from report_content.md + output/numbers.csv.

Run:  uv run python docs/overnight/build_report.py
Placeholders {{id}} / {{id:fmt}} come from output/numbers.csv (default fmt ",.0f"); unknown ids raise.
"""
from __future__ import annotations
import base64, csv, datetime as dt, html, io, re, subprocess, textwrap
from pathlib import Path
import markdown

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTENT = HERE / "report_content.md"
LOG = HERE / "LOG.md"
NUMBERS = ROOT / "output" / "numbers.csv"

# Free-text placeholders: edit here (e.g. when the Collection 11 per-territory file arrives).
TEXT = {
    "CHECK_BRAZIL_TI": "MISMATCH by collection: platform shows only Collection 11 (Kayapó 2024 = 17,632 ha) vs 18,176 ha in our Col 10.1 file; no Col 11 per-territory file published (checked 2026-10-11)",
    "CHECK_BRAZIL_TI_SHORT": "Kayapó mining 2024 = 18,176 ha (Collection 10.1); platform (Collection 11) shows 17,632 ha (collection difference, no publisher match)",
}

BRIEF_FIG = "![The brief's one figure: new mining area per year, Tambopata and Amarakaeri buffer zones, Tambopata National Reserve, Madre de Dios total and rest](output/fig_brief_main.png)\n**Reading:** [[D]] Tambopata's additions fall after Mercurio (Feb 2019) and return from 2022; Amarakaeri and the rest of Madre de Dios rise. Description only."

# ---------------------------------------------------------------------------------------- next steps
STEPS = [  # (no, lane, step, owner, data)
    (1, "now", "Re-open every cited source and save MAAP pages with \"Save as\"", "each citer", "raw MAAP HTML"),
    (2, "now", "Agree the brief figure (fig_brief_main) and the claim wording", "whole team", "none"),
    (3, "now", "Brazil: switch per-territory series to MapBiomas Collection 11 if available (3 post years, publisher match)", "Brazil analyst", "Col 11 TI file"),
    (4, "l5", "Run the required AI prompt for brief part 4; keep raw + edited", "writer", "none"),
    (5, "l5", "Write brief parts 1–4, 2 pages", "writer + editor", "none"),
    (6, "l5", "Build the replication zip from code/main.py + output/", "data lead", "none"),
    (7, "opt", "Ask FZS/SERNANP for dated patrol / interdiction records per zone", "team lead", "enforcement intensity, Peru"),
    (8, "opt", "Validate AMW vs MapBiomas inside Tambopata BZ; get an official La Pampa polygon", "spatial analyst", "official La Pampa polygon"),
    (9, "opt", "River dredges / mercury: cite MAAP #193 dredge counts; no satellite fix", "writer", "none (cite MAAP #193)"),
]
LANES = {"now": "Now (before Lesson 4)", "l5": "Before Lesson 5", "opt": "Optional / extension"}

# ---------------------------------------------------------------------------------------- numbers
def load_numbers() -> dict[str, dict]:
    with open(NUMBERS, newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}

def fmt_val(v: float, fmt: str, minus: str = "−") -> str:
    s = format(v, fmt)
    return s.replace("-", minus) if s.startswith("-") else s

def fill(text: str, nums: dict, used: list | None = None) -> str:
    def rep(m):
        key, _, fmt = m.group(1).partition(":")
        key = key.strip()
        if key in TEXT:
            return TEXT[key]
        if key not in nums:
            raise KeyError(f"unknown placeholder id: {key}")
        if used is not None:
            used.append(key)
        return fmt_val(float(nums[key]["value"]), fmt or ",.0f")
    return re.sub(r"\{\{\s*([A-Za-z0-9_]+(?::[^}]*)?)\s*\}\}", rep, text)

def nice(v: float) -> str:
    if float(v).is_integer() or abs(v) >= 1000:
        return fmt_val(v, ",.0f")
    return fmt_val(v, ",.1f") if abs(v) >= 10 else fmt_val(v, ".3g")

def group_of(i: str) -> str:
    if i.startswith("br_deter"): return "DETER"
    if i.startswith("br_ibama"): return "IBAMA"
    if i.startswith("br_"): return "Brazil"
    if i.startswith("anp_"): return "Peru ANP"
    if i.startswith("robust_"): return "Peru robustness"
    if i.startswith("pe_prod"): return "Production (BCRP/MINEM)"
    if i.startswith("sp_"): return "Spatial (AMW)"
    return "Peru core"
GROUP_ORDER = ["Peru core", "Peru ANP", "Peru robustness", "Production (BCRP/MINEM)", "Brazil", "DETER", "IBAMA", "Spatial (AMW)"]

# ---------------------------------------------------------------------------------------- decisions
def parse_decisions() -> list[list[str]]:
    lines = LOG.read_text(encoding="utf-8").splitlines()
    i = next(k for k, l in enumerate(lines) if l.strip() == "## Decisions")
    rows = []
    for l in lines[i + 1:]:
        if l.startswith("## "): break
        if l.startswith("|"):
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if cells[0] in ("#",) or set(cells[0]) <= set("-: "): continue
            rows.append(cells)
    rows.sort(key=lambda r: int(re.sub(r"\D", "", r[0]) or 0))
    return rows

def inline_md(s: str) -> str:
    out = markdown.markdown(s)
    return re.sub(r"^<p>|</p>$", "", out.strip())

# ---------------------------------------------------------------------------------------- svg diagram
def steps_svg() -> str:
    W, BW, GAP, PADX, LBLW = 1000, 262, 30, 12, 0
    font, lh = 12, 15
    wrap = 36
    y = 10
    parts, boxes = [], {}
    lane_info = []
    for lane in ("now", "l5", "opt"):
        items = [s for s in STEPS if s[1] == lane]
        laid = []
        for no, _, step, owner, data in items:
            t = textwrap.wrap(f"{no}. {step}", wrap)
            o = textwrap.wrap(f"Owner: {owner}", wrap + 4)
            d = textwrap.wrap(f"Needs: {data}", wrap + 4)
            laid.append((no, t, o, d))
        nlines = max(len(t) + len(o) + len(d) for _, t, o, d in laid)
        bh = nlines * lh + 26
        lane_h = bh + 52
        lane_info.append((lane, laid, y, bh, lane_h))
        y += lane_h + 14
    H = y
    parts.append(f'<svg class="flow" viewBox="0 0 {W} {H}" role="img" aria-label="Next steps in three lanes: now, before Lesson 5, optional" xmlns="http://www.w3.org/2000/svg">')
    parts.append('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>')
    for lane, laid, ly, bh, lh_ in lane_info:
        dash = ' stroke-dasharray="6 4"' if lane == "opt" else ""
        parts.append(f'<rect x="2" y="{ly}" width="{W-4}" height="{lh_}" class="lane"{dash}/>')
        parts.append(f'<text x="14" y="{ly+22}" class="lanelbl">{html.escape(LANES[lane])}</text>')
        for k, (no, t, o, d) in enumerate(laid):
            bx = PADX + 6 + k * (BW + GAP + 12)
            by = ly + 36
            boxes[no] = (bx, by, BW + 12, bh)
            parts.append(f'<rect x="{bx}" y="{by}" width="{BW+12}" height="{bh}" rx="3" class="box{" opt" if lane=="opt" else ""}"/>')
            ty = by + 18
            for ln in t:
                parts.append(f'<text x="{bx+9}" y="{ty}" class="t1">{html.escape(ln)}</text>'); ty += lh
            for ln in o:
                parts.append(f'<text x="{bx+9}" y="{ty}" class="t2">{html.escape(ln)}</text>'); ty += lh
            for ln in d:
                parts.append(f'<text x="{bx+9}" y="{ty}" class="t3">{html.escape(ln)}</text>'); ty += lh
    def arrow(a, b, dashed=False):
        ax, ay, aw, ah = boxes[a]; bx, by, bw, bh = boxes[b]
        ds = ' stroke-dasharray="5 4"' if dashed else ""
        if abs(ay - by) < 5:   # same lane: right edge -> left edge
            parts.append(f'<line x1="{ax+aw}" y1="{ay+ah/2}" x2="{bx-1}" y2="{by+bh/2}" class="arrow"{ds} marker-end="url(#arr)"/>')
        else:                  # next lane: elbow from bottom of a down to top of b
            x1, y1 = ax + aw / 2, ay + ah
            x2, y2 = bx + bw / 2, by
            ym = (y1 + y2) / 2 + 4
            parts.append(f'<path d="M{x1} {y1} V{ym} H{x2} V{y2-1}" class="arrow" fill="none"{ds} marker-end="url(#arr)"/>')
    for a, b in [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]:
        arrow(a, b)
    arrow(8, 9, True)  # optional steps are independent; a 2->7 arrow ran through step 5
    parts.append("</svg>")
    return "\n".join(parts)

def steps_md() -> str:
    rows = ["| Step | Lane | Owner (role) | Missing data |", "|---|---|---|---|"]
    for no, lane, step, owner, data in STEPS:
        rows.append(f"| {no}. {step} | {LANES[lane]} | {owner} | {data} |")
    return "\n".join(rows)

# ---------------------------------------------------------------------------------------- numbers table
def numbers_html(nums: dict) -> str:
    groups = {g: [] for g in GROUP_ORDER}
    for r in nums.values():
        groups[group_of(r["id"])].append(r)
    out = ['<div class="nt"><input id="nfilter" type="search" placeholder="Filter numbers (id, description, unit, claim type, function)..." aria-label="Filter numbers">',
           f'<p class="src"><span id="ncount">{len(nums)}</span> of {len(nums)} numbers shown. Source: output/numbers.csv.</p>']
    for g in GROUP_ORDER:
        rows = groups[g]
        if not rows: continue
        out.append(f'<details class="ng" open><summary>{html.escape(g)} <span class="src">({len(rows)})</span></summary><div class="tw"><table class="nums"><thead><tr><th>id</th><th class="r">value</th><th>unit</th><th>description</th><th>claim</th><th>produced by</th></tr></thead><tbody>')
        for r in rows:
            v = nice(float(r["value"]))
            out.append("<tr><td><code>{}</code></td><td class='r num'>{}</td><td>{}</td><td>{}</td><td>{}</td><td><code>{}</code></td></tr>".format(
                html.escape(r["id"]), v, html.escape(r["unit"]), html.escape(r["description"]),
                f'<span class="badge {r["claim_type"][0]}">{r["claim_type"]}</span>', html.escape(r["produced_by"])))
        out.append("</tbody></table></div></details>")
    out.append("</div>")
    return "\n".join(out)

# ---------------------------------------------------------------------------------------- figures
_img_cache: dict[str, str] = {}
def img_data_uri(rel: str) -> str:
    if rel in _img_cache: return _img_cache[rel]
    p = ROOT / rel
    try:
        from PIL import Image
        im = Image.open(p)
        if im.width > 1500:
            im = im.resize((1500, round(im.height * 1500 / im.width)), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "PNG", optimize=True); raw = buf.getvalue()
    except Exception:
        raw = p.read_bytes()
    _img_cache[rel] = "data:image/png;base64," + base64.b64encode(raw).decode()
    return _img_cache[rel]

# ---------------------------------------------------------------------------------------- build
BADGE_NAME = {"D": "description", "P": "prediction", "C": "causal"}

def prepare(text: str, nums: dict) -> tuple[str, list]:
    """Common preprocessing: strip header comment, inject brief figure, fill placeholders."""
    text = re.sub(r"\A\s*<!--.*?-->", "", text, flags=re.S).lstrip()
    # first figure in §5 and start of §9
    text = re.sub(r"(## 5\. Figures\n\n)", lambda m: m.group(1) + BRIEF_FIG + "\n\n", text, count=1)
    text = re.sub(r"(## 9\. Brief skeleton \(draft\)\n\n)", lambda m: m.group(1) + BRIEF_FIG + "\n\n", text, count=1)
    return text, []

def section_split(text: str):
    parts = re.split(r"(?m)^(?=## )", text)
    head = parts[0]
    secs = [p for p in parts[1:]]
    return head, secs

def build_html(text: str, nums: dict, decisions, build_info: str) -> str:
    used: list = []
    text, _ = prepare(text, nums)
    stash: dict[str, str] = {}
    def stash_put(html_s: str) -> str:
        k = f"@@STASH{len(stash)}@@"; stash[k] = html_s; return k
    text = text.replace("{{DECISIONS_TABLE}}", stash_put(
        '<div class="tw"><table class="dec"><thead><tr><th>#</th><th>Decision</th><th>Alternatives</th><th>Why</th></tr></thead><tbody>' +
        "".join("<tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in r[:4]) + "</tr>" for r in decisions) + "</tbody></table></div>"))
    text = text.replace("{{NUMBERS_TABLE}}", stash_put(numbers_html(nums)))
    text = text.replace("{{NEXT_STEPS_DIAGRAM}}", stash_put('<div class="figure svgwrap">' + steps_svg() + "</div>"))
    text = fill(text, nums, used)
    # figures
    def fig(m):
        cap, rel = m.group(1), m.group(2)
        return stash_put(f'<figure><img src="{img_data_uri(rel)}" alt="{html.escape(cap)}" loading="lazy"><figcaption>{html.escape(cap)}</figcaption></figure>')
    text = re.sub(r"(?m)^!\[([^\]]*)\]\(([^)]+)\)\s*$", fig, text)
    text = re.sub(r"\[\[([DPC])\]\]", lambda m: f'<span class="badge {m.group(1).lower()}">{BADGE_NAME[m.group(1)]}</span>', text)
    # DRAFT banner = first callout
    m = re.search(r"(?m)^> (.*)$", text)
    banner = ""
    if m:
        banner = m.group(1)
        text = text.replace(m.group(0), "", 1)
    head, secs = section_split(text)
    md = markdown.Markdown(extensions=["tables", "sane_lists"])
    h1m = re.search(r"(?m)^# (.*)$", head)
    title = h1m.group(1) if h1m else "Report"
    toc, body = [], []
    for s in secs:
        hm = re.match(r"## (.*)\n", s)
        name = hm.group(1)
        sid = "s" + (re.match(r"(\d+)\.", name).group(1) if re.match(r"\d+\.", name) else str(len(toc)))
        toc.append(f'<a href="#{sid}">{html.escape(name)}</a>')
        inner = md.reset().convert(s[hm.end():])
        inner = re.sub(r"<p>\s*(@@STASH\d+@@)\s*</p>", r"\1", inner)
        body.append(f'<section id="{sid}"><h2>{html.escape(name)}</h2>\n{inner}</section>')
    page = "\n".join(body)
    for _ in range(3):  # stashes may sit inside stashes? no, but replace until stable
        for k, v in stash.items():
            page = page.replace(k, v)
    page = page.replace("<blockquote>", '<blockquote class="callout">')
    banner_html = inline_md(re.sub(r"\[\[([DPC])\]\]", "", banner))
    assert "{{" not in page and "[[" not in page, "leftover placeholder"
    return HTML_TEMPLATE.format(title=html.escape(title), css=CSS, js=JS, toc="\n".join(toc),
                                h1=html.escape(title), banner=banner_html, body=page, build=build_info)

def build_md(text: str, nums: dict, decisions, build_info: str) -> str:
    used: list = []
    text, _ = prepare(text, nums)
    text = fill(text.replace("{{NUMBERS_TABLE}}", "@@NUMS@@").replace("{{DECISIONS_TABLE}}", "@@DEC@@")
                .replace("{{NEXT_STEPS_DIAGRAM}}", "@@STEPS@@"), nums, used)
    # headline numbers = those used in section 1
    sec1 = re.search(r"(?s)## 1\..*?(?=\n## 2\.)", text)
    s1_used: list = []
    fill(re.search(r"(?s)## 1\..*?(?=\n## 2\.)", prepare(CONTENT.read_text(encoding="utf-8"), nums)[0]).group(0), nums, s1_used)
    seen, head_rows = set(), ["| id | value | unit | description |", "|---|---:|---|---|"]
    for i in s1_used:
        if i in seen: continue
        seen.add(i); r = nums[i]
        head_rows.append(f"| `{i}` | {nice(float(r['value']))} | {r['unit']} | {r['description']} |")
    nums_md = (f"All {len(nums)} numbers, with unit, description, claim type and producing function: "
               f"[`output/numbers.csv`](../../output/numbers.csv). Headline numbers used in section 1:\n\n" + "\n".join(head_rows))
    dec_md = "| # | Decision | Alternatives | Why |\n|---|---|---|---|\n" + "\n".join(
        "| " + " | ".join(c.replace("|", "\\|") for c in r[:4]) + " |" for r in decisions)
    text = text.replace("@@NUMS@@", nums_md).replace("@@DEC@@", dec_md).replace("@@STEPS@@", steps_md())
    text = re.sub(r"\[\[([DPC])\]\]", lambda m: f"**[{BADGE_NAME[m.group(1)]}]**", text)
    text = re.sub(r"(?m)^(!\[[^\]]*\]\()output/", r"\1../../output/", text)
    text = text.replace("](output/", "](../../output/")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.rstrip() + f"\n\n---\n*{build_info}*\n"

def main():
    nums = load_numbers()
    decisions = parse_decisions()
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or "unknown"
    except Exception:
        commit = "unknown"
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    info = f"Built {stamp} from git commit {commit} (working tree may contain uncommitted changes). Numbers from output/numbers.csv ({len(nums)} rows)."
    text = CONTENT.read_text(encoding="utf-8")
    h = build_html(text, nums, decisions, info)
    (HERE / "REPORT.html").write_text(h, encoding="utf-8")
    m = build_md(text, nums, decisions, info)
    assert "{{" not in m, "leftover placeholder in md"
    (HERE / "REPORT.md").write_text(m, encoding="utf-8")
    print(f"REPORT.html {len(h)/1e6:.2f} MB, REPORT.md {len(m)/1e3:.0f} kB")

# ---------------------------------------------------------------------------------------- template
CSS = r"""
:root{--paper:#f3efeb;--card:#ffffff;--tint:#e8e2db;--rule:#d9d1c8;--teal:#1b3f44;--on-teal:#fff;--on-teal-2:#c9dcdc;
--ink:#1b3f44;--ink-2:#4b5f61;--ink-3:#6f7f80;--rasp:#c2185b;--no:#b3261e;--no-soft:#f6dcd9;--maybe:#a86400;--maybe-soft:#f6e6c8;--yes:#2f7f32;--yes-soft:#e1eedd;--blue:#2a78d6;
--sans:"Roboto",system-ui,-apple-system,"Segoe UI",Arial,sans-serif;--mono:"Roboto Mono",ui-monospace,"SF Mono",Menlo,monospace;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#11201f;--card:#1d3236;--tint:#24393d;--rule:#33494c;--teal:#0c2326;--on-teal-2:#a9c3c3;--ink:#eef4f3;--ink-2:#bccbcb;--ink-3:#8fa3a3;--rasp:#e0558f;--no:#ef8077;--no-soft:#3d2220;--maybe:#e9a845;--maybe-soft:#3a2e15;--yes:#7fc37c;--yes-soft:#1f3624;--blue:#4d94e8;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#11201f;--card:#1d3236;--tint:#24393d;--rule:#33494c;--teal:#0c2326;--on-teal-2:#a9c3c3;--ink:#eef4f3;--ink-2:#bccbcb;--ink-3:#8fa3a3;--rasp:#e0558f;--no:#ef8077;--no-soft:#3d2220;--maybe:#e9a845;--maybe-soft:#3a2e15;--yes:#7fc37c;--yes-soft:#1f3624;--blue:#4d94e8;color-scheme:dark}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:70px}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16.5px;line-height:1.6;margin:0}
.draft{position:sticky;top:0;z-index:50;background:#b3201a;color:#fff;font-weight:900;letter-spacing:.06em;text-transform:uppercase;font-size:.85rem;padding:8px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px}
.draft button{font:inherit;font-size:.75rem;background:transparent;color:#fff;border:1px solid rgba(255,255,255,.7);padding:3px 10px;cursor:pointer;text-transform:none;letter-spacing:0;font-weight:500}
.hero{background:var(--teal);color:var(--on-teal)}
.hero .in{max-width:1200px;margin:0 auto;padding:36px 20px 30px}
.hero .kicker{font-size:.78rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#f48fb1}
h1{font-size:clamp(1.7rem,4vw,2.6rem);font-weight:900;line-height:1.15;letter-spacing:-.01em;margin:8px 0 0;text-wrap:balance}
.layout{max-width:1200px;margin:0 auto;padding:0 20px;display:grid;grid-template-columns:230px minmax(0,1fr);gap:40px}
nav.toc{position:sticky;top:48px;align-self:start;max-height:calc(100vh - 60px);overflow:auto;padding:24px 0;font-size:.88rem}
nav.toc a{display:block;color:var(--ink-2);text-decoration:none;padding:5px 10px;border-left:3px solid var(--rule)}
nav.toc a:hover,nav.toc a.on{color:var(--rasp);border-left-color:var(--rasp)}
main{padding-bottom:60px;min-width:0}
section{padding-top:44px}
h2{font-size:clamp(1.35rem,3vw,1.8rem);font-weight:900;margin:0 0 14px;line-height:1.2}
p{margin:0 0 12px;max-width:74ch}
ul,ol{margin:0 0 14px;padding-left:1.4em;max-width:80ch}
li{margin-bottom:8px}
a{color:var(--rasp)}
code{font-family:var(--mono);font-size:.84em;background:var(--tint);padding:1px 5px;overflow-wrap:anywhere}
em{color:var(--ink-2)}
.num{font-variant-numeric:tabular-nums}.src{font-size:.8rem;color:var(--ink-3)}
blockquote.callout,.callout{background:var(--maybe-soft);border-left:5px solid var(--maybe);margin:0 0 16px;padding:12px 16px;max-width:none}
blockquote.callout p{margin:0}
.draftbox{background:var(--no-soft);border:2px solid var(--no);border-left-width:8px;color:var(--ink);padding:14px 18px;margin:26px 0 0}
.draftbox b{color:var(--no);text-transform:uppercase;letter-spacing:.06em}
.badge{display:inline-block;font-size:.68rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:1px 8px;vertical-align:1px;white-space:nowrap}
.badge.d{background:var(--yes-soft);color:var(--yes)}.badge.p{background:var(--maybe-soft);color:var(--maybe)}.badge.c{background:var(--no-soft);color:var(--no)}
figure{margin:18px 0 6px;background:var(--card);border:1px solid var(--rule);padding:12px}
figure img{width:100%;height:auto;display:block;background:#fff}
figcaption{font-size:.84rem;color:var(--ink-2);padding-top:8px}
.tw{overflow-x:auto;margin:0 0 16px}
table{border-collapse:collapse;font-size:.88rem;background:var(--card);border:1px solid var(--rule);width:100%}
th,td{padding:7px 10px;text-align:left;border-bottom:1px solid var(--rule);vertical-align:top}
th{background:var(--tint);font-size:.76rem;text-transform:uppercase;letter-spacing:.05em;position:sticky;top:0}
td.r,th.r{text-align:right}
section>table{display:block;overflow-x:auto}
details.ng{margin:10px 0;border:1px solid var(--rule);background:var(--card)}
details.ng>summary{cursor:pointer;font-weight:700;padding:8px 12px;background:var(--tint)}
details.ng .tw{margin:0;max-height:520px;overflow:auto}
table.nums td:first-child code{overflow-wrap:normal;white-space:nowrap;font-size:.78em}
table.nums td:nth-child(4){min-width:240px}
table.nums td:last-child code{overflow-wrap:normal;white-space:nowrap}
#nfilter{width:100%;max-width:520px;font:inherit;padding:8px 12px;background:var(--card);color:var(--ink);border:1px solid var(--rule)}
.figure{background:var(--card);border:1px solid var(--rule);padding:12px}.svgwrap{overflow-x:auto}
svg.flow{width:100%;min-width:760px;height:auto;display:block;color:var(--ink-2);font-family:var(--sans)}
svg.flow .lane{fill:var(--tint);fill-opacity:.55;stroke:var(--rule);stroke-width:1}
svg.flow .lanelbl{fill:var(--rasp);font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
svg.flow .box{fill:var(--card);stroke:var(--ink-3);stroke-width:1.2}svg.flow .box.opt{stroke-dasharray:5 3}
svg.flow .t1{fill:var(--ink);font-size:12px;font-weight:700}svg.flow .t2{fill:var(--ink-2);font-size:11.5px}svg.flow .t3{fill:var(--yes);font-size:11.5px}
svg.flow .arrow{stroke:currentColor;stroke-width:1.5}
footer{border-top:1px solid var(--rule);color:var(--ink-3);font-size:.8rem;padding:20px;text-align:center}
@media (max-width:900px){.layout{grid-template-columns:1fr;gap:0}nav.toc{position:static;max-height:none;padding:14px 0;display:flex;flex-wrap:wrap;gap:6px}nav.toc a{border:1px solid var(--rule);border-left:1px solid var(--rule)}}
@media print{.draft button,nav.toc{display:none}.draft{position:static}.layout{display:block}body{background:#fff;color:#000;font-size:11pt}figure,table,.box{break-inside:avoid}details.ng .tw{max-height:none}details.ng:not([open])>*:not(summary){display:block}section{padding-top:20px}a{color:inherit}}
"""

JS = r"""
(function(){var r=document.documentElement,k='report-theme',s=localStorage.getItem(k);if(s)r.setAttribute('data-theme',s);
document.getElementById('theme').addEventListener('click',function(){var dark=r.getAttribute('data-theme')?r.getAttribute('data-theme')==='dark':matchMedia('(prefers-color-scheme:dark)').matches;var n=dark?'light':'dark';r.setAttribute('data-theme',n);localStorage.setItem(k,n)});
var f=document.getElementById('nfilter');if(f){f.addEventListener('input',function(){var q=f.value.toLowerCase(),n=0;document.querySelectorAll('table.nums tbody tr').forEach(function(tr){var m=tr.textContent.toLowerCase().indexOf(q)>-1;tr.style.display=m?'':'none';if(m)n++});document.getElementById('ncount').textContent=n;document.querySelectorAll('details.ng').forEach(function(d){var any=d.querySelector('tbody tr:not([style*="none"])');d.style.display=any?'':'none';if(q&&any)d.open=true})})}
var links=[].slice.call(document.querySelectorAll('nav.toc a'));var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'-20% 0px -70% 0px'});document.querySelectorAll('main section').forEach(function(s){io.observe(s)});
window.addEventListener('beforeprint',function(){document.querySelectorAll('details.ng').forEach(function(d){d.open=true})});})();
"""

HTML_TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DRAFT, not reviewed: {title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&family=Roboto+Mono:wght@400;500&display=swap">
<style>{css}</style></head><body>
<div class="draft"><span>DRAFT for the team — not reviewed</span><button id="theme" type="button">Light / dark</button></div>
<header class="hero"><div class="in"><div class="kicker">Group Giant Anteater · Question 2 · Peru and Brazil</div><h1>{h1}</h1>
<div class="draftbox"><b>Draft.</b> {banner}</div></div></header>
<div class="layout"><nav class="toc" aria-label="Contents">
{toc}
</nav><main>
{body}
</main></div>
<footer>{build}</footer>
<script>{js}</script></body></html>
"""

if __name__ == "__main__":
    main()
