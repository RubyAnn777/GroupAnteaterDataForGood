"""Build the team walkthrough and the brief draft from markdown sources + output/numbers.csv.

  docs/overnight/explainer_content.md -> docs/overnight/EXPLAINER.html + EXPLAINER.md  (guided walkthrough)
  docs/brief/brief_content.md         -> docs/brief/BRIEF_DRAFT.html + BRIEF_DRAFT.md   (2-page brief draft)

Run:  uv run python docs/overnight/build_report.py
Placeholders {{id}} / {{id:fmt}} come from output/numbers.csv (default fmt ",.0f"); unknown ids raise.
"""
from __future__ import annotations
import base64, csv, datetime as dt, html, io, re, subprocess, textwrap
from pathlib import Path
import markdown

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTENT = HERE / "explainer_content.md"
BRIEF_DIR = ROOT / "docs" / "brief"
BRIEF_CONTENT = BRIEF_DIR / "brief_content.md"
LOG = HERE / "LOG.md"
NUMBERS = ROOT / "output" / "numbers.csv"

# Free-text placeholders: edit here (e.g. when the Collection 11 per-territory file arrives).
TEXT = {
    "CHECK_BRAZIL_TI": "MISMATCH by collection: platform shows only Collection 11 (Kayapó 2024 = 17,632 ha) vs 18,176 ha in our Col 10.1 file; no Col 11 per-territory file published (checked 2026-10-11)",
    "CHECK_BRAZIL_TI_SHORT": "Kayapó mining 2024 = 18,176 ha (Collection 10.1); platform (Collection 11) shows 17,632 ha (collection difference, no publisher match)",
}


# ---------------------------------------------------------------------------------------- next steps
STEPS = [  # (no, lane, step, owner, data)
    (1, "now", "Share the walkthrough page with the team (it is private until shared)", "Sebastian", "none"),
    (2, "now", "Ruby checks step 8: her four rules and the cut-offs", "Ruby", "none"),
    (3, "now", "Agree the claim wording, esp. the one conditional causal sentence", "whole team", "none"),
    (4, "now", "Re-open every cited source; save MAAP pages with \"Save as\"", "each citer", "raw MAAP HTML"),
    (5, "l5", "Fill in TEAM_PLAN.docx (members, roles)", "team lead", "none"),
    (6, "l5", "Edit the brief (section 15) to final; keep or re-run the AI prompt", "writer + editor", "none"),
    (7, "l5", "Build the replication zip; make slides from the walkthrough figures", "data lead", "none"),
    (8, "opt", "Ask FZS/SERNANP for dated patrol / interdiction records per zone", "team lead", "enforcement intensity"),
    (9, "opt", "Brazil: search Munduruku operations 2019-21; Col 11 territory file", "Brazil analyst", "news, MapBiomas"),
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
    """{{id}}, {{id:fmt}}, {{id:fmt|abs}} (absolute value, for "fell by 1,454" instead of "by −1,454").
    p-values that round to zero print as "< 0.01" / "< 0.001"; "p = < 0.01" is then tidied to "p < 0.01"."""
    def rep(m):
        key, _, fmt = m.group(1).partition(":")
        key = key.strip()
        fmt, _, mod = fmt.partition("|")
        if key in TEXT:
            return TEXT[key]
        if key not in nums:
            raise KeyError(f"unknown placeholder id: {key}")
        if used is not None:
            used.append(key)
        v = float(nums[key]["value"])
        if mod.strip() == "abs":
            v = abs(v)
        fmt = fmt or ",.0f"
        if nums[key].get("unit") == "p-value" and float(format(v, fmt)) == 0:
            return "< " + format(10 ** -int(fmt.strip(".f") or 2), f".{int(fmt.strip('.f') or 2)}f")
        return fmt_val(v, fmt)
    out = re.sub(r"\{\{\s*([A-Za-z0-9_]+(?::[^}]*)?)\s*\}\}", rep, text)
    return re.sub(r"= < ", "< ", out)

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

PIPELINE = [("Raw files", "data_raw/"), ("Checks", "against publisher numbers"), ("Measures", "new mining per area-year"),
            ("Models", "DiD, event study, twins"), ("Figures", "and tables in output/"), ("numbers.csv", "every cited number"),
            ("Pages", "walk-through, methods, brief")]

def pipeline_html() -> str:
    """Static flow diagram (no JS, no CDN): an ordered list styled as boxes with arrows; wraps on narrow screens."""
    items = "".join(f'<li><b>{html.escape(a)}</b><span>{html.escape(b)}</span></li>' for a, b in PIPELINE)
    return f'<ol class="pipe" aria-label="Pipeline from raw files to pages">{items}</ol>'

def pipeline_md() -> str:
    return " → ".join(f"**{a}** ({b})" for a, b in PIPELINE)

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
_img_cache: dict[str, tuple[str, int, int]] = {}
def img_data_uri(rel: str, max_w: int = 1600, quality: int = 80) -> tuple[str, int, int]:
    """PNG from output/ -> WebP data URI (keeps the page light). Returns (uri, width, height)."""
    key = f"{rel}|{max_w}|{quality}"
    if key in _img_cache: return _img_cache[key]
    from PIL import Image
    im = Image.open(ROOT / rel).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=quality, method=6)
    _img_cache[key] = ("data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode(), im.width, im.height)
    return _img_cache[key]

# ---------------------------------------------------------------------------------------- page syntax
BADGE_NAME = {"D": "description", "P": "prediction", "C": "causal"}

def badges(s: str) -> str:
    return re.sub(r"\[\[([DPC])\]\]", lambda m: f'<span class="badge {m.group(1).lower()}">{BADGE_NAME[m.group(1)]}</span>', s)

def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def prepare(text: str) -> str:
    return fix_lists(re.sub(r"\A\s*<!--.*?-->", "", text, flags=re.S).lstrip())

def fix_lists(text: str) -> str:
    """Python-Markdown needs a blank line before a list; insert one after any non-list, non-table line."""
    out, prev = [], ""
    item = re.compile(r"^\s*(- |\d+\. )")
    for line in text.split("\n"):
        if item.match(line) and prev.strip() and not item.match(prev) and not prev.lstrip().startswith(("|", ">", ":::")):
            out.append("")
        out.append(line); prev = line
    return "\n".join(out)

def md_block(s: str) -> str:
    h = markdown.markdown(s, extensions=["tables", "sane_lists"])
    h = re.sub(r"<p>\s*(@@S\d+@@)\s*</p>", r"\1", h)
    h = h.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    h = re.sub(r"<p><strong>Why it matters:</strong>\s*(\w)", lambda m: '<p class="why"><strong>Why it matters</strong>' + m.group(1).upper(), h)
    return h

BLOCK = re.compile(r"(?ms)^:::(stats|beats|fig|note)[ \t]*([^\n]*)\n(.*?)\n:::[ \t]*$")
MORE = re.compile(r"(?ms)^:::more[ \t]*([^\n]*)\n(.*?)\n:::[ \t]*$")

class Page:
    """Turns the content markdown (see the header comment of explainer_content.md) into page parts."""
    def __init__(self, text: str, nums: dict, extra: dict[str, str]):
        self.stash: dict[str, str] = {}
        self.nfig = 0
        self.hero_stats = ""
        text = prepare(text)
        for k, v in extra.items():
            text = text.replace("{{" + k + "}}", self.put(v))
        text = badges(fill(text, nums))
        text = BLOCK.sub(self.block, text)
        self.text = MORE.sub(self.more, text)

    def put(self, h: str) -> str:
        k = f"@@S{len(self.stash)}@@"; self.stash[k] = h; return k

    def unstash(self, h: str) -> str:
        for _ in range(4):
            if "@@S" not in h: break
            h = re.sub(r"@@S\d+@@", lambda m: self.stash[m.group(0)], h)
        return h

    def block(self, m) -> str:
        kind, arg, body = m.group(1), m.group(2).strip(), m.group(3)
        lines = [l.strip() for l in body.split("\n") if l.strip()]
        if kind == "stats":
            tiles = "".join(f'<div class="stat"><div class="stat-v">{inline_md(v.strip())}</div><div class="stat-l">{inline_md(l.strip())}</div></div>'
                            for v, l in (ln.split("||", 1) for ln in lines))
            h = f'<div class="stats">{tiles}</div>'
            if not self.hero_stats:
                self.hero_stats = h; return ""
            return self.put(h)
        if kind == "beats":
            items = []
            for i, ln in enumerate(lines, 1):
                lab, txt, href = [x.strip() for x in ln.split("||")]
                items.append(f'<li class="beat beat-{slug(lab)}"><span class="beat-n">{i:02d}</span><span class="beat-l">{html.escape(lab)}</span>'
                             f'<span class="beat-t">{badges(inline_md(txt))}</span><a class="beat-go" href="{href}">Evidence <span aria-hidden="true">→</span></a></li>')
            return self.put(f'<ol class="beats">{"".join(items)}</ol>')
        if kind == "note":
            return self.put(f'<aside class="note">{md_block(body)}</aside>')
        # figure
        self.nfig += 1
        meta = {}
        for ln in lines:
            k, _, v = ln.partition(":")
            meta[k.strip().lower()] = v.strip()
        uri, w, hgt = img_data_uri(arg)
        n = self.nfig
        alt = html.escape(meta.get("alt") or meta.get("take", f"Figure {n}"))
        cap = ""
        if meta.get("read") or meta.get("take"):
            cap = ('<figcaption>'
                   + (f'<div class="fc fc-read"><span class="lbl">How to read it</span><p>{inline_md(meta["read"])}</p></div>' if meta.get("read") else "")
                   + (f'<div class="fc fc-take"><span class="lbl">Takeaway</span><p>{inline_md(meta["take"])}</p></div>' if meta.get("take") else "")
                   + '</figcaption>')
        return self.put(f'<figure class="fig" id="fig-{n}"><div class="fig-bar"><span class="fig-no">Figure {n}</span>'
                        f'<button class="fig-zoom" type="button" data-fig="{n}" aria-label="Enlarge figure {n}">Enlarge</button></div>'
                        f'<div class="plate"><img src="{uri}" width="{w}" height="{hgt}" alt="{alt}" loading="lazy" decoding="async"></div>{cap}</figure>')

    def more(self, m) -> str:
        summary, body = m.group(1).strip() or "More detail", m.group(2)
        return self.put(f'<details class="more"><summary><span class="more-ic" aria-hidden="true"></span><span class="more-k">Go deeper</span>'
                        f'<span class="more-s">{html.escape(summary)}</span></summary><div class="more-b">{md_block(body)}</div></details>')

    def structure(self):
        """-> title, lede, [(part_name, [(id, eyebrow, headline, html)])]"""
        t = self.text
        title = re.search(r"(?m)^# (.*)$", t).group(1).strip()
        lm = re.search(r"(?m)^> (.*)$", t)
        lede = lm.group(1).strip() if lm else ""
        start = re.search(r"(?m)^(@part |## )", t)
        body = t[start.start():] if start else ""
        parts, cur = [], None
        chunks = re.split(r"(?m)^(@part .*|## .*)$", body)
        pending = None
        for c in chunks:
            if c.startswith("@part "):
                cur = (c[6:].strip(), []); parts.append(cur)
            elif c.startswith("## "):
                pending = c[3:].strip()
            elif pending is not None:
                eb, _, hl = pending.partition("|")
                eb, hl = (eb.strip(), hl.strip()) if hl else ("", eb.strip())
                if cur is None:
                    cur = ("", []); parts.append(cur)
                cur[1].append((slug(eb or hl), eb, hl, md_block(c.strip())))
                pending = None
        return title, lede, parts

def render_page(page: Page, kind: str, page_title: str, build_info: str, links: dict) -> str:
    title, lede, parts = page.structure()
    toc, body, n = [], [], 0
    ids = set()
    for pi, (pname, chapters) in enumerate(parts, 1):
        pid = "part-" + slug(pname or str(pi))
        if pname:
            toc.append(f'<li class="toc-part"><a href="#{pid}">{html.escape(pname)}</a><ol>')
            body.append(f'<div class="part" id="{pid}"><span class="part-k">Part {pi}</span><span class="part-n">{html.escape(pname)}</span></div>')
        for cid, eb, hl, inner in chapters:
            n += 1
            assert cid not in ids, f"duplicate chapter id {cid}"; ids.add(cid)
            toc.append(f'<li><a href="#{cid}"><span class="toc-no">{n:02d}</span>{html.escape(eb or hl)}</a></li>')
            inner = re.sub(r"\A<p><strong>", '<p class="lede"><strong>', inner, count=1)
            body.append(f'<section class="ch" id="{cid}" aria-labelledby="{cid}-h"><header class="ch-head"><div class="ch-eb"><span class="ch-no">{n:02d}</span>{html.escape(eb)}</div>'
                        f'<h2 id="{cid}-h">{badges(inline_md(hl))}</h2></header>{inner}</section>')
        if pname:
            toc.append("</ol></li>")
    main = page.unstash("\n".join(body))
    for a in set(re.findall(r'href="#([^"]+)"', main)):
        assert a in ids or a.startswith(("part-", "fig-")), f"broken internal link #{a}"
    assert "{{" not in main and "[[" not in main and "@@S" not in main, "leftover placeholder"
    nav = "".join(f'<a href="{html.escape(u)}"{" aria-current=\"page\"" if k == kind else ""}>{html.escape(lbl)}</a>' for k, (lbl, u) in links.items())
    toc_html = "\n".join(toc)
    hero_stats = page.unstash(page.hero_stats)
    kicker = {"walk": "Data for Good · Group Giant Anteater · Question 2", "methods": "Data for Good · Group Giant Anteater · Methods"}[kind]
    return PAGE.format(title=html.escape(page_title), css=CSS, js=JS, nav=nav, kicker=kicker, h1=badges(inline_md(title)),
                       lede=inline_md(lede), stats=hero_stats, toc=toc_html, main=main, build=html.escape(build_info),
                       nfig=page.nfig, fonts=FONTS)

# ---------------------------------------------------------------------------------------- markdown mirror
def to_markdown(text: str, nums: dict, extra_md: dict[str, str], build_info: str) -> str:
    """Plain Markdown mirror of a page (for GitHub / diffs): blocks flattened, figures linked."""
    t = prepare(text)
    for k, v in extra_md.items():
        t = t.replace("{{" + k + "}}", v)
    t = fill(t, nums)
    def blk(m):
        kind, arg, body = m.group(1), m.group(2).strip(), m.group(3)
        lines = [l.strip() for l in body.split("\n") if l.strip()]
        if kind == "stats":
            return "\n".join(f"- **{v.strip()}** {l.strip()}" for v, l in (ln.split("||", 1) for ln in lines))
        if kind == "beats":
            return "\n".join(f"{i}. **{a.strip()}:** {b.strip()}" for i, (a, b, _) in enumerate((ln.split("||") for ln in lines), 1))
        if kind == "note":
            return "\n".join("> " + l for l in body.split("\n"))
        meta = {k.strip().lower(): v.strip() for k, _, v in (ln.partition(":") for ln in lines)}
        return f"![{meta.get('take', '')}](../../{arg})\n\n*How to read it:* {meta.get('read', '')}\n\n*Takeaway:* {meta.get('take', '')}"
    t = BLOCK.sub(blk, t)
    t = MORE.sub(lambda m: f"<details><summary>Go deeper: {m.group(1).strip()}</summary>\n\n{m.group(2)}\n\n</details>", t)
    t = re.sub(r"(?m)^@part (.*)$", r"---\n\n**Part: \1**", t)
    t = re.sub(r"(?m)^## ([^|\n]*)\|\s*(.*)$", r"## \2", t)
    t = re.sub(r"\[\[([DPC])\]\]", lambda m: f"**[{BADGE_NAME[m.group(1)]}]**", t)
    return re.sub(r"\n{3,}", "\n\n", t).rstrip() + f"\n\n---\n*{build_info}*\n"

# ---------------------------------------------------------------------------------------- brief
def brief_html(nums: dict) -> str:
    text = prepare_brief()
    text = fill(text, nums)
    def fig(m):
        uri, w, h = img_data_uri(m.group(2), 1500, 88)
        return (f'<figure><img src="{uri}" width="{w}" height="{h}" alt="{html.escape(m.group(1))}">'
                f'<figcaption><b>Figure 1.</b> {html.escape(m.group(1))}. Source: MapBiomas Peru, Collection 4.</figcaption></figure>')
    text = re.sub(r"(?m)^!\[([^\]]*)\]\(([^)]+)\)\s*$", fig, text)
    body = markdown.markdown(badges(text), extensions=["tables", "sane_lists"])
    body = body.replace("<h2>References</h2>", '<h2 class="pb">References</h2>')
    body = re.sub(r"(<h1>.*?</h1>)\s*<p>(.*?)</p>", r'<header class="b-head">\1<p class="b-meta">\2</p></header>', body, count=1, flags=re.S)
    return body

def write_brief_numbers(text: str, nums: dict) -> None:
    """output/brief_numbers.csv: every registered number in the brief, in order of appearance (course rule: the
    replication output lists the brief's numbers in the order they appear). The figure's own numbers (fig_brief_*,
    title and subtitle) are listed where the figure stands."""
    head = text.split("## References")[0]
    used: list[str] = []
    for i, part in enumerate(re.split(r"(?m)^!\[[^\]]*\]\(output/fig_brief_main\.png\)\s*$", head)):
        if i == 1:
            used += sorted(k for k in nums if k.startswith("fig_brief_"))
        fill(part, nums, used)
    rows, seen = [], set()
    for k in used:
        if k in seen:
            continue
        seen.add(k)
        r = nums[k]
        rows.append({"order": len(rows) + 1, "id": k, "value": r["value"], "unit": r.get("unit", ""),
                     "measure": r.get("measure", ""), "zone": r.get("zone", ""), "period": r.get("period", ""),
                     "claim_type": r.get("claim_type", ""), "description": r.get("description", "")})
    out = ROOT / "output" / "brief_numbers.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["order", "id"])
        w.writeheader(); w.writerows(rows)
    print(f"Saved output/brief_numbers.csv ({len(rows)} numbers, order of appearance)")

def ai_raw_md() -> str:
    """The raw AI answer for brief Appendix B1, verbatim, with its headings demoted below the appendix heading."""
    raw = (ROOT / "docs" / "brief" / "ai_part4_raw.md").read_text(encoding="utf-8")
    raw = raw.split("## Raw answer", 1)[1].strip()
    return re.sub(r"(?m)^#{1,3} ", "#### ", raw)

def prepare_brief() -> str:
    return prepare(BRIEF_CONTENT.read_text(encoding="utf-8")).replace("{{TEXT:ai_part4_raw}}", ai_raw_md())

def build_brief(nums: dict, build_info: str, links: dict) -> tuple[str, str, str]:
    text = prepare_brief()
    write_brief_numbers(text, nums)
    text = fill(text, nums)
    md_text = re.sub(r"\[\[([DPC])\]\]", lambda m: f"**[{BADGE_NAME[m.group(1)]}]**", text)
    md_text = md_text.replace("](output/", "](../../output/") + f"\n\n---\n*{build_info}*\n"
    body = brief_html(nums)
    nav = "".join(f'<a href="{html.escape(u)}"{" aria-current=\"page\"" if k == "brief" else ""}>{html.escape(lbl)}</a>' for k, (lbl, u) in links.items())
    frag = BRIEF_PAGE.format(css=CSS_BRIEF, body=body, build=html.escape(build_info), nav=nav, fonts=FONTS, js=JS_THEME)
    assert "{{" not in frag and "[[" not in frag, "leftover placeholder in brief"
    return md_text, frag, as_document(localize(frag, "brief"))

def brief_body_html(nums: dict, fig_width: str = "60%") -> str:   # kept for other scripts
    return brief_html(nums)

# ---------------------------------------------------------------------------------------- output
def as_document(fragment: str) -> str:
    """Local, self-contained HTML document from an artifact fragment (artifact pages get their skeleton at publish)."""
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>\n' + fragment + "\n</body></html>\n")

ART = HERE / "_artifact"          # artifact fragments (git-ignored); published with the Artifact tool

def main(only_brief: bool = False):
    nums = load_numbers()
    decisions = parse_decisions()
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or "unknown"
    except Exception:
        commit = "unknown"
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    info = f"Built {stamp} from git commit {commit} (working tree may contain uncommitted changes). Numbers from output/numbers.csv ({len(nums)} rows)."
    links = {"walk": ("Walkthrough", URLS["walk"]), "methods": ("Methods", URLS["methods"]), "brief": ("Brief draft", URLS["brief"])}
    def link(k, label): return f'<a href="{html.escape(URLS[k])}">{html.escape(label)}</a>'
    extra = {
        "DECISIONS_TABLE": '<div class="tw"><table class="dec"><thead><tr><th>#</th><th>Decision</th><th>Alternatives</th><th>Why</th></tr></thead><tbody>' +
                           "".join("<tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in r[:4]) + "</tr>" for r in decisions) + "</tbody></table></div>",
        "NUMBERS_TABLE": numbers_html(nums),
        "NEXT_STEPS_DIAGRAM": '<div class="svgwrap">' + steps_svg() + "</div>",
        "PIPELINE_DIAGRAM": pipeline_html(),
        "BRIEF_LINK": link("brief", "Brief draft"), "METHODS_LINK": link("methods", "Methods page"), "WALK_LINK": link("walk", "Walkthrough"),
    }
    extra_md = {"DECISIONS_TABLE": "See `docs/overnight/LOG.md`.", "NUMBERS_TABLE": "See [`output/numbers.csv`](../../output/numbers.csv).",
                "NEXT_STEPS_DIAGRAM": steps_md(), "PIPELINE_DIAGRAM": pipeline_md(), "BRIEF_LINK": "[the brief draft](../brief/BRIEF_DRAFT.md)",
                "METHODS_LINK": "[METHODS.html](METHODS.html)", "WALK_LINK": "[EXPLAINER.html](EXPLAINER.html)"}
    ART.mkdir(exist_ok=True)
    out = {}
    for kind, src, page_title, dst in (() if only_brief else (("walk", CONTENT, "Mercurio Team Walkthrough", "EXPLAINER"),
                                       ("methods", HERE / "methods_content.md", "Mercurio Methods Guide", "METHODS"))):
        text = src.read_text(encoding="utf-8")
        frag = render_page(Page(text, nums, extra), kind, page_title, info, links)
        (ART / f"{dst.lower()}.html").write_text(frag, encoding="utf-8")
        (HERE / f"{dst}.html").write_text(as_document(localize(frag, "overnight")), encoding="utf-8")
        md = to_markdown(text, nums, extra_md, info)
        assert "{{" not in md, f"leftover placeholder in {dst}.md"
        (HERE / f"{dst}.md").write_text(md, encoding="utf-8")
        out[dst] = len(frag)
    bm, bfrag, bdoc = build_brief(nums, info, links)
    (BRIEF_DIR / "BRIEF_DRAFT.md").write_text(bm, encoding="utf-8")
    (BRIEF_DIR / "BRIEF_DRAFT.html").write_text(bdoc, encoding="utf-8")
    (ART / "brief.html").write_text(bfrag, encoding="utf-8")
    print(", ".join(f"{k}.html {v/1e6:.2f} MB" for k, v in out.items()) + f" BRIEF_DRAFT.html {len(bdoc)/1e6:.2f} MB")

# ---------------------------------------------------------------------------------------- templates
# Design: the partner's visual language (FZS): Roboto, light display weight, slate-teal bands, warm off-white,
# lime/green uppercase eyebrows with a rule, big thin numbers. No FZS logo or branding: this is a student team's page.
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Mono:wght@400;500&display=swap">')

CSS = r"""
/* Layout: slate hero with thin big numbers, then a two-column reading layout (sticky contents | 760px text column,
   figures up to 920px). Chapters carry a numbered eyebrow and a claim headline; detail hides in "Go deeper". */
:root{
  --bg:#f2efea; --surface:#fbfaf7; --surface-2:#e9e4dc; --rule:#d9d2c7; --rule-2:#c9c1b4;
  --ink:#22383f; --ink-2:#4a5b60; --muted:#6c7b80;
  --slate:#243b42; --slate-2:#2e4850; --on-slate:#f3f5f2; --on-slate-2:#c3d0cf;
  --lime:#b9c94f; --eyebrow:#3c7d2c; --accent:#a42c58; --accent-soft:#f3e3e9;
  --d:#2b6a8a; --p:#8a5f00; --c:#a42c58; --plate:#fbfaf7;
  --sans:"Roboto",system-ui,-apple-system,"Segoe UI",Arial,sans-serif; --mono:"Roboto Mono",ui-monospace,Menlo,monospace;
  --col:760px; --wide:920px;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#15242a; --surface:#1c2f35; --surface-2:#23383f; --rule:#31474e; --rule-2:#3d555d;
  --ink:#e8eeeb; --ink-2:#bccac9; --muted:#93a5a7; --slate:#0f1c20; --slate-2:#172a30; --on-slate:#eef2ef; --on-slate-2:#aebfbf;
  --lime:#c3d35c; --eyebrow:#a2cf84; --accent:#ec84a9; --accent-soft:#3a2430; --d:#8cc0de; --p:#e2b64e; --c:#ef8db0; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#15242a; --surface:#1c2f35; --surface-2:#23383f; --rule:#31474e; --rule-2:#3d555d;
  --ink:#e8eeeb; --ink-2:#bccac9; --muted:#93a5a7; --slate:#0f1c20; --slate-2:#172a30; --on-slate:#eef2ef; --on-slate-2:#aebfbf;
  --lime:#c3d35c; --eyebrow:#a2cf84; --accent:#ec84a9; --accent-soft:#3a2430; --d:#8cc0de; --p:#e2b64e; --c:#ef8db0; color-scheme:dark}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:72px;-webkit-text-size-adjust:100%}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:17px;line-height:1.65;font-weight:400;margin:0}
a{color:var(--accent);text-underline-offset:2px}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
code{font-family:var(--mono);font-size:.82em;background:var(--surface-2);padding:1px 5px;border-radius:3px;overflow-wrap:anywhere}
strong{font-weight:500;color:var(--ink)}
em{font-style:italic}
.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:8px;z-index:100;background:var(--surface);padding:8px 12px}

/* top bar */
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:40;background:var(--slate);color:var(--on-slate);border-bottom:1px solid rgba(255,255,255,.08)}
.top .in{max-width:1280px;margin:0 auto;padding:0 20px;height:52px;display:flex;align-items:center;gap:20px}
.brand{font-weight:500;letter-spacing:.08em;text-transform:uppercase;font-size:.74rem;white-space:nowrap;color:var(--on-slate)}
.brand b{color:var(--lime);font-weight:500}
.pages{display:flex;gap:4px;margin-left:auto}
.pages a{color:var(--on-slate-2);text-decoration:none;font-size:.86rem;padding:6px 10px;border-radius:3px}
.pages a:hover{color:var(--on-slate);background:rgba(255,255,255,.07)}
.pages a[aria-current="page"]{color:var(--on-slate);box-shadow:inset 0 -2px 0 var(--lime);border-radius:0}
.pill{font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--lime);color:var(--lime);padding:2px 8px;border-radius:999px;white-space:nowrap}
.theme{font:inherit;font-size:.82rem;color:var(--on-slate-2);background:transparent;border:1px solid rgba(255,255,255,.25);border-radius:3px;padding:5px 10px;cursor:pointer;min-height:32px}
.theme:hover{color:var(--on-slate);border-color:var(--on-slate-2)}

/* hero */
.hero{background:var(--slate);color:var(--on-slate)}
.hero .in{max-width:1280px;margin:0 auto;padding:56px 20px 48px}
.kicker{display:flex;align-items:center;gap:18px;color:var(--lime);font-size:.8rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase}
.kicker::after{content:"";flex:1;height:1px;background:var(--lime);opacity:.7}
.hero h1{font-weight:300;font-size:clamp(2.1rem,5.2vw,3.7rem);line-height:1.08;letter-spacing:-.01em;margin:22px 0 18px;max-width:24ch;text-wrap:balance}
.hero .lede{color:var(--on-slate-2);font-size:1.12rem;line-height:1.6;max-width:66ch;margin:0}
.hero .lede code{background:rgba(255,255,255,.1);color:var(--on-slate)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(200px,100%),1fr));gap:0;margin:44px 0 0;border-top:1px solid rgba(255,255,255,.14)}
.stat{padding:22px 24px 4px 0;border-right:1px solid rgba(255,255,255,.14);margin-right:24px;min-width:0}
.stat:last-child{border-right:0;margin-right:0}
.stat-v{font-weight:300;font-size:clamp(1.9rem,3vw,2.6rem);line-height:1.05;color:var(--lime);font-variant-numeric:lining-nums;letter-spacing:-.01em}
.stat-l{color:var(--on-slate-2);font-size:.9rem;line-height:1.45;margin-top:10px;max-width:30ch}
.main .stats{border-top:1px solid var(--rule);margin:24px 0}
.main .stat{border-right-color:var(--rule)}.main .stat-v{color:var(--ink)}.main .stat-l{color:var(--ink-2)}

/* layout */
.shell{max-width:1280px;margin:0 auto;padding:0 20px;display:grid;grid-template-columns:232px minmax(0,1fr);gap:64px}
nav.toc{position:sticky;top:76px;align-self:start;max-height:calc(100vh - 96px);overflow:auto;padding:40px 0 24px;font-size:.86rem}
nav.toc ol{list-style:none;margin:0;padding:0}
nav.toc .toc-part{margin:0 0 18px}
nav.toc .toc-part>a{display:block;color:var(--eyebrow);font-weight:500;font-size:.7rem;letter-spacing:.11em;text-transform:uppercase;text-decoration:none;margin-bottom:6px}
nav.toc li li a{display:flex;gap:10px;color:var(--ink-2);text-decoration:none;padding:4px 0 4px 10px;border-left:2px solid var(--rule);line-height:1.35}
nav.toc li li a:hover{color:var(--ink);border-left-color:var(--rule-2)}
nav.toc li li a.on{color:var(--ink);border-left-color:var(--accent);font-weight:500}
.toc-no{color:var(--muted);font-variant-numeric:tabular-nums;font-size:.78rem;padding-top:1px}
.toc-tools{display:flex;gap:8px;margin-top:22px}
.toc-tools button{font:inherit;font-size:.78rem;color:var(--ink-2);background:transparent;border:1px solid var(--rule-2);border-radius:3px;padding:5px 9px;cursor:pointer;min-height:32px}
.toc-tools button:hover{color:var(--ink);border-color:var(--ink-2)}
details.mtoc{display:none}
.main{min-width:0;padding:8px 0 80px}
.main>*{max-width:var(--wide)}

/* parts and chapters */
.part{display:flex;align-items:center;gap:16px;margin:84px 0 0;color:var(--eyebrow);font-size:.8rem;font-weight:500;letter-spacing:.11em;text-transform:uppercase}
.part::after{content:"";flex:1;height:1px;background:currentColor;opacity:.55}
.part-k{color:var(--muted)}
.ch{padding-top:44px}
.ch-head{margin-bottom:18px;max-width:var(--col)}
.ch-eb{display:flex;align-items:baseline;gap:12px;color:var(--ink-2);font-size:.78rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase}
.ch-no{color:var(--accent);font-variant-numeric:tabular-nums}
.ch h2{font-weight:300;font-size:clamp(1.65rem,3.1vw,2.35rem);line-height:1.15;letter-spacing:-.005em;margin:8px 0 0;text-wrap:balance;color:var(--ink)}
.ch p,.ch ul,.ch ol:not(.beats){max-width:var(--col)}
.ch p{margin:0 0 14px}
.ch ul,.ch ol{padding-left:1.25em;margin:0 0 16px}
.ch li{margin-bottom:7px}
.ch li::marker{color:var(--muted)}
p.lede{font-size:1.17rem;line-height:1.55;color:var(--ink);margin-bottom:18px}
p.lede strong{font-weight:500}
p.why{border-top:1px solid var(--rule);padding-top:12px;margin-top:20px;color:var(--ink)}
p.why strong:first-child{display:block;font-size:.72rem;letter-spacing:.11em;text-transform:uppercase;color:var(--eyebrow);font-weight:500;margin-bottom:2px}

/* badges */
.badge{display:inline-block;font-size:.66rem;font-weight:500;letter-spacing:.07em;text-transform:uppercase;line-height:1.5;padding:0 7px;border:1px solid currentColor;border-radius:999px;vertical-align:2px;white-space:nowrap}
.badge.d{color:var(--d)}.badge.p{color:var(--p)}.badge.c{color:var(--c);background:var(--accent-soft)}

/* story beats */
ol.beats{list-style:none;padding:0;margin:26px 0 26px;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px;max-width:var(--wide)}
.beat{display:flex;flex-direction:column;gap:8px;background:var(--surface);border:1px solid var(--rule);border-top:3px solid var(--rule-2);padding:14px 14px 12px;min-width:0}
.beat-before,.beat-during,.beat-after{border-top-color:#d0692f}.beat-next-door{border-top-color:#2b74a6}.beat-region{border-top-color:#a9a8a2}
.beat-n{font-size:.72rem;color:var(--muted);font-variant-numeric:tabular-nums}
.beat-l{font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;font-weight:500;color:var(--ink)}
.beat-t{font-size:.92rem;line-height:1.5;color:var(--ink-2);flex:1}
.beat-go{font-size:.82rem;text-decoration:none;font-weight:500}

/* figures */
figure.fig{margin:26px 0 22px;background:var(--surface);border:1px solid var(--rule);max-width:var(--wide)}
.fig-bar{display:flex;align-items:center;justify-content:space-between;padding:9px 14px;border-bottom:1px solid var(--rule)}
.fig-no{font-size:.72rem;letter-spacing:.11em;text-transform:uppercase;color:var(--ink-2);font-weight:500}
.fig-zoom{font:inherit;font-size:.78rem;color:var(--accent);background:transparent;border:0;padding:6px 4px;cursor:zoom-in;min-height:32px}
.plate{background:var(--plate);padding:10px}
.plate img{display:block;width:100%;height:auto;cursor:zoom-in}
figure.fig figcaption{display:grid;grid-template-columns:1fr 1fr;gap:0;border-top:1px solid var(--rule)}
.fc{padding:12px 16px 14px;min-width:0}
.fc+.fc{border-left:1px solid var(--rule)}
.fc .lbl{display:block;font-size:.68rem;letter-spacing:.11em;text-transform:uppercase;color:var(--muted);font-weight:500;margin-bottom:3px}
.fc p{margin:0;font-size:.9rem;line-height:1.5;color:var(--ink-2)}
.fc-take p{color:var(--ink);font-weight:500}
dialog.lb{border:0;padding:0;background:transparent;max-width:min(1600px,96vw);max-height:94vh}
dialog.lb::backdrop{background:rgba(9,18,21,.88)}
dialog.lb img{display:block;max-width:min(1600px,96vw);max-height:88vh;width:auto;height:auto;background:#fbfaf7}
dialog.lb button{position:fixed;top:12px;right:16px;font:inherit;color:#fff;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.4);border-radius:3px;padding:6px 12px;cursor:pointer}

/* go deeper */
details.more{margin:22px 0 8px;border-top:1px solid var(--rule-2);border-bottom:1px solid var(--rule-2);max-width:var(--wide)}
details.more>summary{list-style:none;display:flex;align-items:baseline;gap:12px;padding:13px 4px;cursor:pointer;min-height:44px}
details.more>summary::-webkit-details-marker{display:none}
details.more>summary:hover{background:var(--surface)}
.more-ic{flex:none;width:18px;height:18px;border:1px solid var(--ink-2);border-radius:50%;position:relative;top:3px}
.more-ic::before,.more-ic::after{content:"";position:absolute;left:4px;right:4px;top:8px;height:1px;background:var(--ink-2)}
.more-ic::after{transform:rotate(90deg);transition:transform .2s ease}
details.more[open] .more-ic::after{transform:rotate(0)}
.more-k{flex:none;font-size:.72rem;letter-spacing:.11em;text-transform:uppercase;color:var(--accent);font-weight:500}
.more-s{color:var(--ink);font-weight:500;font-size:.98rem}
.more-b{padding:6px 4px 18px 30px}
.more-b p,.more-b ul{font-size:.95rem}
.more-b figure.fig{margin-left:0}

/* tables */
.tw{overflow-x:auto;margin:14px 0 20px;max-width:var(--wide)}
table{border-collapse:collapse;width:100%;font-size:.88rem;font-variant-numeric:tabular-nums;background:var(--surface)}
th,td{padding:8px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--rule)}
th{font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2);font-weight:500;border-bottom:1px solid var(--ink-2);background:var(--surface)}
tbody tr:last-child td{border-bottom:0}
td code{white-space:nowrap}
table.dec td:nth-child(2),table.dec td:nth-child(3),table.dec td:nth-child(4){min-width:200px}
aside.note{background:var(--surface);border:1px solid var(--rule);padding:14px 18px;margin:18px 0;max-width:var(--col)}

/* numbers table */
.nt input{width:100%;max-width:520px;font:inherit;padding:9px 12px;background:var(--surface);color:var(--ink);border:1px solid var(--rule-2);border-radius:3px}
.nt .src{font-size:.8rem;color:var(--muted)}
details.ng{margin:10px 0;border:1px solid var(--rule)}
details.ng>summary{cursor:pointer;font-weight:500;padding:9px 12px;background:var(--surface-2)}
details.ng .tw{margin:0;max-height:520px;overflow:auto}
table.nums td:nth-child(4){min-width:240px}
.r{text-align:right}

/* next steps diagram */
.svgwrap{overflow-x:auto;background:var(--surface);border:1px solid var(--rule);padding:12px;margin:12px 0}
svg.flow{width:100%;min-width:760px;height:auto;display:block;color:var(--ink-2);font-family:var(--sans)}
svg.flow .lane{fill:var(--surface-2);fill-opacity:.6;stroke:var(--rule);stroke-width:1}
svg.flow .lanelbl{fill:var(--eyebrow);font-size:13px;font-weight:500;letter-spacing:.08em;text-transform:uppercase}
svg.flow .box{fill:var(--surface);stroke:var(--rule-2);stroke-width:1.2}svg.flow .box.opt{stroke-dasharray:5 3}
svg.flow .t1{fill:var(--ink);font-size:12px;font-weight:500}svg.flow .t2{fill:var(--ink-2);font-size:11.5px}svg.flow .t3{fill:var(--d);font-size:11.5px}
svg.flow .arrow{stroke:currentColor;stroke-width:1.5}

/* pipeline flow (methods page): static boxes + arrows, wraps on narrow screens */
ol.pipe{list-style:none;padding:0;margin:20px 0 22px;display:flex;flex-wrap:nowrap;align-items:stretch;gap:10px 18px;max-width:var(--wide)}
ol.pipe li{position:relative;flex:1 1 0;min-width:0;max-width:100%;background:var(--surface);border:1px solid var(--rule-2);border-top:3px solid var(--eyebrow);padding:8px 7px;margin:0;font-size:.8rem;line-height:1.35}
ol.pipe li b{display:block;font-weight:500;color:var(--ink)}
ol.pipe li span{color:var(--ink-2);font-size:.76rem;overflow-wrap:break-word;hyphens:auto}
ol.pipe li:not(:last-child)::after{content:"→";position:absolute;right:-15px;top:50%;transform:translateY(-50%);color:var(--muted);font-size:1rem}

/* never wider than the screen: grid/flex children may shrink, media and long tokens wrap */
.hero .in>*,.main>*,.ch>*,.more-b>*,.stat,.beat,.fc,.pages,.top .in>*{min-width:0}
.hero h1,.hero .lede,.stat-l,.beat-t,.ch h2,p.lede{overflow-wrap:break-word}
img,svg,video{max-width:100%}
.ch p,.ch li{overflow-wrap:break-word}

footer.foot{background:var(--slate);color:var(--on-slate-2);font-size:.8rem;margin-top:40px}
footer.foot .in{max-width:1280px;margin:0 auto;padding:28px 20px;display:flex;flex-wrap:wrap;gap:8px 28px;justify-content:space-between}

/* narrow screens */
@media (max-width:1080px){
  .shell{grid-template-columns:minmax(0,1fr);gap:0}
  nav.toc{display:none}
  details.mtoc{display:block;margin:20px 0 0;border:1px solid var(--rule);background:var(--surface)}
  details.mtoc>summary{cursor:pointer;padding:12px 14px;font-weight:500;min-height:44px}
  details.mtoc nav.toc{display:block;position:static;max-height:none;padding:4px 14px 14px}
  ol.beats{grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}
}
@media (max-width:720px){
  body{font-size:16px}
  .top .in{gap:10px;padding:0 16px}.brand{display:none}.pill{display:none}
  .pages{margin-left:0}.pages a{padding:6px 7px;font-size:.82rem}.theme{margin-left:auto}
  .hero .in{padding:36px 16px 32px}.shell{padding:0 16px}
  .stat{border-right:0;margin-right:0;border-bottom:1px solid rgba(255,255,255,.14);padding:16px 0}
  .main .stat{border-bottom-color:var(--rule)}
  figure.fig figcaption{grid-template-columns:1fr}.fc+.fc{border-left:0;border-top:1px solid var(--rule)}
  .plate{padding:4px}
  .more-b{padding-left:4px}
  ol.beats{grid-template-columns:1fr}
  .pages{flex:0 1 auto;min-width:0;overflow-x:auto}.theme{flex:none;padding:5px 8px}
  ol.pipe{flex-direction:column;gap:22px}ol.pipe li{flex:none}
  ol.pipe li:not(:last-child)::after{content:"↓";right:auto;left:50%;top:auto;bottom:-21px;transform:none}
}
@media print{
  .top,nav.toc,details.mtoc,.fig-zoom,.toc-tools{display:none}.shell{display:block}
  body{background:#fff}details.more>.more-b{display:block}figure,table{break-inside:avoid}
}
"""

JS_THEME = r"""
(function(){var r=document.documentElement,k='mercurio-theme',b=document.getElementById('theme');
try{var s=localStorage.getItem(k);if(s)r.setAttribute('data-theme',s)}catch(e){}
function dark(){var t=r.getAttribute('data-theme');return t?t==='dark':matchMedia('(prefers-color-scheme: dark)').matches}
function label(){if(b)b.textContent=dark()?'Light mode':'Dark mode'}
label();if(b)b.addEventListener('click',function(){var n=dark()?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem(k,n)}catch(e){}label()});
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',label);})();
"""

JS = JS_THEME + r"""
(function(){
var links=[].slice.call(document.querySelectorAll('.shell>nav.toc li li a'));
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'-15% 0px -75% 0px'});
document.querySelectorAll('section.ch').forEach(function(s){io.observe(s)});
function openTo(id){var el=id&&document.getElementById(id);if(!el)return;var d=el.closest('details');while(d){d.open=true;d=d.parentElement.closest('details')}}
openTo(location.hash.slice(1));window.addEventListener('hashchange',function(){openTo(location.hash.slice(1))});
document.querySelectorAll('details.mtoc a').forEach(function(a){a.addEventListener('click',function(){a.closest('details').open=false})});
var all=function(o){document.querySelectorAll('details.more').forEach(function(d){d.open=o})};
document.querySelectorAll('[data-all]').forEach(function(b){b.addEventListener('click',function(){all(b.getAttribute('data-all')==='open')})});
var lb=document.getElementById('lb'),li=lb&&lb.querySelector('img');
function show(fig){var im=fig.querySelector('.plate img');if(!lb||!im)return;li.src=im.src;li.alt=im.alt;if(lb.showModal)lb.showModal();else lb.setAttribute('open','')}
document.querySelectorAll('figure.fig').forEach(function(f){f.querySelector('.fig-zoom').addEventListener('click',function(){show(f)});f.querySelector('.plate img').addEventListener('click',function(){show(f)})});
if(lb){lb.addEventListener('click',function(){lb.close()});}
var f=document.getElementById('nfilter');if(f){f.addEventListener('input',function(){var q=f.value.toLowerCase(),n=0;document.querySelectorAll('table.nums tbody tr').forEach(function(tr){var m=tr.textContent.toLowerCase().indexOf(q)>-1;tr.hidden=!m;if(m)n++});document.getElementById('ncount').textContent=n;document.querySelectorAll('details.ng').forEach(function(d){var any=d.querySelector('tbody tr:not([hidden])');d.hidden=!any;if(q&&any)d.open=true})})}
window.addEventListener('beforeprint',function(){all(true)});
})();
"""

PAGE = """<title>{title}</title>
{fonts}
<style>{css}</style>
<a class="skip" href="#main">Skip to content</a>
<div class="top"><div class="in"><span class="brand"><b>Giant Anteater</b> · Question 2</span><nav class="pages" aria-label="Pages">{nav}</nav><span class="pill">Team draft</span><button id="theme" class="theme" type="button">Dark mode</button></div></div>
<header class="hero"><div class="in"><div class="kicker">{kicker}</div><h1>{h1}</h1><p class="lede">{lede}</p>{stats}</div></header>
<div class="shell">
<nav class="toc" aria-label="Contents"><ol>{toc}</ol><div class="toc-tools"><button type="button" data-all="open">Expand all</button><button type="button" data-all="close">Collapse all</button></div></nav>
<main class="main" id="main">
<details class="mtoc"><summary>Contents</summary><nav class="toc" aria-label="Contents (mobile)"><ol>{toc}</ol></nav></details>
{main}
</main></div>
<footer class="foot"><div class="in"><span>Group Giant Anteater · Data for Good, October 2026 · {nfig} figures · satellites cannot see river dredges or mercury</span><span>{build}</span></div></footer>
<dialog id="lb" class="lb" aria-label="Enlarged figure"><button type="button">Close</button><img alt=""></dialog>
<script>{js}</script>
"""

CSS_BRIEF = r"""
:root{--bg:#e9e4dc;--paper:#ffffff;--ink:#1d2e33;--ink-2:#4a5b60;--rule:#d9d2c7;--slate:#243b42;--on-slate:#f3f5f2;--on-slate-2:#c3d0cf;--lime:#b9c94f;
--d:#2b6a8a;--p:#8a5f00;--c:#a42c58;--accent:#a42c58;--sans:"Roboto",system-ui,-apple-system,"Segoe UI",Arial,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15242a;--slate:#0f1c20;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#15242a;--slate:#0f1c20;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);margin:0;font-family:var(--sans)}
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--slate);color:var(--on-slate)}
.top .in{max-width:1100px;margin:0 auto;padding:0 20px;height:52px;display:flex;align-items:center;gap:16px}
.brand{font-weight:500;letter-spacing:.08em;text-transform:uppercase;font-size:.74rem}.brand b{color:var(--lime);font-weight:500}
.pages{display:flex;gap:4px;margin-left:auto}.pages a{color:var(--on-slate-2);text-decoration:none;font-size:.86rem;padding:6px 10px}
.pages a[aria-current="page"]{color:var(--on-slate);box-shadow:inset 0 -2px 0 var(--lime)}
.theme{font:inherit;font-size:.82rem;color:var(--on-slate-2);background:transparent;border:1px solid rgba(255,255,255,.25);border-radius:3px;padding:5px 10px;cursor:pointer}
.note{max-width:210mm;margin:22px auto 0;padding:0 16px;font-size:.86rem;color:var(--ink-2)}
:root[data-theme="dark"] .note{color:#bccac9}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .note{color:#bccac9}}
.sheet{background:var(--paper);color:var(--ink);max-width:210mm;margin:14px auto 48px;padding:16mm 17mm;box-shadow:0 1px 2px rgba(0,0,0,.08),0 10px 30px rgba(0,0,0,.08);
  font-size:10pt;line-height:1.38;color-scheme:light}
.sheet .b-head{border-bottom:2px solid var(--slate);padding-bottom:6px;margin-bottom:8px}
.sheet h1{font-size:15pt;font-weight:500;margin:0 0 2px;line-height:1.2;color:var(--slate);text-wrap:balance}
.sheet .b-meta{color:#5d6b70;margin:0;font-size:8.6pt;letter-spacing:.02em}
.sheet h2{font-size:10.5pt;font-weight:500;margin:9px 0 3px;color:#3c7d2c;text-transform:uppercase;letter-spacing:.07em;display:flex;align-items:center;gap:8px}
.sheet h2::after{content:"";flex:1;height:1px;background:#3c7d2c;opacity:.5}
.sheet p{margin:0 0 5px}.sheet ul{margin:0 0 5px;padding-left:1.2em}.sheet li{margin:0 0 2px}
.sheet strong{font-weight:500}
.sheet a{color:var(--accent);overflow-wrap:anywhere}
.sheet figure{margin:4px 0 6px;text-align:center}.sheet figure img{width:72%;height:auto}
.sheet figcaption{font-size:8pt;color:#5d6b70;text-align:left}
.sheet code{font-size:8.5pt;font-family:"Roboto Mono",ui-monospace,monospace}
.badge{font-size:6.6pt;font-weight:500;letter-spacing:.06em;text-transform:uppercase;padding:0 5px;border:1px solid currentColor;border-radius:999px;white-space:nowrap}
.badge.d{color:var(--d)}.badge.p{color:var(--p)}.badge.c{color:var(--c);background:#f3e3e9}
.pb{break-before:page}
.foot{max-width:210mm;margin:0 auto 40px;padding:0 16px;color:#7a878b;font-size:.75rem}
@media screen and (max-width:820px){.sheet{padding:22px 18px;margin:12px 12px 32px;font-size:15px}.sheet figure img{width:100%}.brand{display:none}}
@page{size:A4;margin:16mm 17mm}
@media print{body{background:#fff}.top,.note,.foot{display:none}.sheet{box-shadow:none;margin:0;padding:0;max-width:none}}
"""

BRIEF_PAGE = """<title>Mercurio Brief Draft</title>
{fonts}
<style>{css}</style>
<div class="top"><div class="in"><span class="brand"><b>Giant Anteater</b> · Question 2</span><nav class="pages" aria-label="Pages">{nav}</nav><button id="theme" class="theme" type="button">Dark mode</button></div></div>
<p class="note">Draft for the team. Parts 1–4 fit on two A4 pages; references and appendix follow. Every number comes from <code>output/numbers.csv</code>; edit the text in <code>docs/brief/brief_content.md</code>.</p>
<article class="sheet">{body}</article>
<p class="foot">{build}</p>
<script>{js}</script>
"""

# Published artifact URLs (the three pages link to each other). New artifacts, created 12 Oct 2026; republish the
# fragments in docs/overnight/_artifact/ to these URLs. Local HTML files get relative links instead (localize()).
URLS = {"walk": "https://claude.ai/artifact/VT9wkZqxhH8WAHU4v36mg6",
        "methods": "https://claude.ai/artifact/83ZeCu4frkocBDJ46RV1pA",
        "brief": "https://claude.ai/artifact/NRjV7R75F8Wvogn6Bs3ycJ"}
LOCAL = {"overnight": {"walk": "EXPLAINER.html", "methods": "METHODS.html", "brief": "../brief/BRIEF_DRAFT.html"},
         "brief": {"walk": "../overnight/EXPLAINER.html", "methods": "../overnight/METHODS.html", "brief": "BRIEF_DRAFT.html"}}

def localize(frag: str, where: str) -> str:
    for k, u in URLS.items():
        frag = frag.replace(f'href="{u}"', f'href="{LOCAL[where][k]}"')
    return frag

if __name__ == "__main__":
    import sys
    main(only_brief="--brief" in sys.argv)
