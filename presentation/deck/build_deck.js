// Build the FZS talk deck (storyline v3, docs/presentation/STORYLINE.md):  cd presentation/deck && npm install && node build_deck.js
// Design = the walkthrough page's visual language: Roboto Light titles, green kickers with a hairline rule, raspberry
// chapter numbers, framed figure plates on warm off-white, pill claim badges, thin lime numbers on slate. FZS colours,
// no FZS logo (student work). Every content slide puts kicker, title (one line, 28 pt), subtitle (the measure, unit,
// zone and period; up to two lines) and content at the SAME positions.
// Plan v3: ONE measure, net mining additions = new land + re-mined − stopped (ha/yr). Every number is read from
// output/numbers.csv by id (or computed from it); figure titles/subtitles come from output/slides/slide_titles.json,
// computed from the data by code/slides_figures.py. Hand-typed facts are cited external facts.
const fs = require("fs");
const path = require("path");
const React = require("react");
const { renderToStaticMarkup } = require("react-dom/server");
const sharp = require("sharp");
const pptxgen = require("pptxgenjs");
const lu = require("react-icons/lu");
const gi = require("react-icons/gi");

const ROOT = path.resolve(__dirname, "../..");
const OUT = path.join(ROOT, "output");
const SLIDES = path.join(OUT, "slides");
const ANIM = path.join(ROOT, "presentation/animation/out");
const TITLES = JSON.parse(fs.readFileSync(path.join(SLIDES, "slide_titles.json"), "utf8"));

// ------------------------------------------------------------------ numbers
const N = {};
fs.readFileSync(path.join(OUT, "numbers.csv"), "utf8").split("\n").slice(1).forEach((line) => {
  if (!line.trim()) return;
  const [id, value] = line.split(",");
  N[id] = parseFloat(value);
});
const used = new Set();
const need = (id) => { if (!(id in N)) throw new Error(`number ${id} missing from numbers.csv`); used.add(id); return N[id]; };
const ha = (id) => Math.round(need(id)).toLocaleString("en-US").replace("-", "−");
const abs = (id) => Math.abs(Math.round(need(id))).toLocaleString("en-US");
const pct = (id) => `${Math.round(need(id) * 100)}%`;
const p2 = (id) => need(id).toFixed(2);
const int = (id) => `${Math.round(need(id))}`;
const arrow = (...ids) => ids.map(ha).join(" → ");

// ------------------------------------------------------------------ theme + palette
const THEME = {
  name: "FZS student deck", headFontFace: "Roboto Light", bodyFontFace: "Roboto",
  colors: { dk1: "22383F", lt1: "FFFFFF", dk2: "243B42", lt2: "F2EFEA", accent1: "3C7D2C", accent2: "B9C94F",
    accent3: "A42C58", accent4: "D0692F", accent5: "2B74A6", accent6: "858D90", hlink: "2B74A6", folHlink: "6A5ACD" },
};
const X = { bg: "F2EFEA", surface: "FBFAF7", surface2: "E9E4DC", rule: "D9D2C7", rule2: "C9C1B4", ink: "22383F", ink2: "4A5B60",
  muted: "6C7B80", slate: "243B42", slate2: "2E4850", onSlate: "F3F5F2", onSlate2: "C3D0CF", lime: "B9C94F", eyebrow: "3C7D2C",
  accent: "A42C58", accentSoft: "F3E3E9", d: "2B6A8A", p: "8A5F00", orange: "D0692F", blue: "2B74A6",
  // the three parts of net additions (code/common.py C) and net in ink
  new: "9A5520", remined: "D99A1E", stopped: "14998A" };
const CLAIM = { D: ["Description", X.d, null], P: ["Prediction", X.p, null], C: ["Causal · conditional", X.accent, X.accentSoft],
  R: ["Recommendation", X.eyebrow, null] };
const LIGHT = "Roboto Light", BODY = "Roboto", MED = "Roboto Medium";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";                       // 13.333 x 7.5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "When the patrols leave: Operation Mercurio and FZS";
pres.author = "Group Giant Anteater";
pres.company = "Data for Good";
const W = 13.333, H = 7.5, M = 0.55, CW = W - 2 * M;
const G = { kicker: 0.42, title: 0.8, sub: 1.33, top: 1.9, bottom: 6.95, titleSize: 28 };

// ------------------------------------------------------------------ icons (react-icons -> PNG)
const iconCache = {};
async function icon(lib, name, color, px = 256) {
  const key = `${name}-${color}`;
  if (iconCache[key]) return iconCache[key];
  const Comp = (lib === "gi" ? gi : lu)[name];
  if (!Comp) throw new Error(`icon ${name} missing`);
  const svg = renderToStaticMarkup(React.createElement(Comp, { size: px, color: `#${color}` }));
  const png = await sharp(Buffer.from(svg)).png().toBuffer();
  return (iconCache[key] = "image/png;base64," + png.toString("base64"));
}

// ------------------------------------------------------------------ layouts (frame only)
const FOOT = "WHEN THE PATROLS LEAVE  ·  GROUP GIANT ANTEATER  ·  DATA FOR GOOD";
for (const [name, bg, fg] of [["DARK", X.slate, X.onSlate2], ["LIGHT", X.bg, X.muted]]) {
  pres.defineSlideMaster({ title: name, background: { color: bg },
    objects: [{ text: { text: FOOT, options: { x: M, y: H - 0.38, w: 9, h: 0.24, fontFace: MED, fontSize: 9, color: fg, charSpacing: 1.5, margin: 0 } } }],
    slideNumber: { x: W - M - 0.6, y: H - 0.38, w: 0.6, h: 0.24, fontFace: BODY, fontSize: 9, color: fg, align: "right" } });
}

// ------------------------------------------------------------------ building blocks
let n = 0;
const sections = new Set();
const titles = [];
function slide(master, section) {
  if (!sections.has(section)) { pres.addSection({ title: section }); sections.add(section); }
  n += 1;
  return pres.addSlide({ masterName: master, sectionTitle: section });
}
function header(s, { no, label, title, claim, sub, dark = false }) {
  const runs = [];
  if (no) runs.push({ text: `${no}   `, options: { color: dark ? X.lime : X.accent } });
  runs.push({ text: label.toUpperCase(), options: { color: dark ? X.lime : X.eyebrow } });
  const kw = CW - (claim ? 2.6 : 0);
  const tw = Math.min(kw - 0.4, 0.135 * (label.length + (no ? no.length + 3 : 0)) + 0.3);
  s.addText(runs, { x: M, y: G.kicker, w: tw, h: 0.3, fontFace: MED, fontSize: 12, charSpacing: 2.2, margin: 0, isTextBox: true });
  s.addShape(pres.shapes.LINE, { x: M + tw + 0.12, y: G.kicker + 0.15, w: Math.max(0.3, kw - tw - 0.12), h: 0,
    line: { color: dark ? X.lime : X.eyebrow, width: 0.75, transparency: dark ? 30 : 45 } });
  if (claim) pill(s, claim, dark);
  if (title) {
    titles.push([n, title]);
    s.addText(title, { x: M, y: G.title, w: CW, h: 0.52, fontFace: LIGHT, fontSize: G.titleSize, color: dark ? X.onSlate : X.ink,
      margin: 0, valign: "top", isTextBox: true, objectName: "title" });
  }
  if (sub) s.addText(sub, { x: M, y: G.sub, w: CW, h: 0.5, fontFace: BODY, fontSize: 12.5, color: dark ? X.onSlate2 : X.ink2,
    margin: 0, valign: "top", isTextBox: true, objectName: "subtitle" });
}
function pill(s, key, dark = false) {
  const [label, col, fill] = CLAIM[key];
  const solid = dark && key === "C";
  const c = dark && !solid ? X.lime : col;
  s.addText(label.toUpperCase(), { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.17, x: W - M - 2.35, y: G.kicker - 0.04, w: 2.35, h: 0.34,
    align: "center", valign: "middle", fontFace: MED, fontSize: 10.5, charSpacing: 1.5, color: solid ? "FFFFFF" : c,
    fill: solid ? { color: X.accent } : (fill && !dark ? { color: fill } : { type: "none" }), line: { color: solid ? X.accent : c, width: 1 },
    margin: 0, objectName: `claim-${key}` });
}
function plate(s, x, y, w, h) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: X.surface }, line: { color: X.rule, width: 0.75 }, objectName: "plate" });
}
function photo(s, x, y, w, h, label, dark = false) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: dark ? X.slate2 : X.surface2 },
    line: { color: dark ? "3D555D" : X.rule2, width: 1, dashType: "dash" }, objectName: "photo-placeholder" });
  s.addText(`Photo: ${label}`, { x, y: y + h / 2 - 0.3, w, h: 0.6, align: "center", fontFace: BODY, fontSize: 13,
    color: dark ? X.onSlate2 : X.muted, italic: true, isTextBox: true });
}
async function fit(s, file, bx, by, bw, bh) {
  const m = await sharp(file).metadata();
  let w = bw, h = bw * m.height / m.width;
  if (h > bh) { h = bh; w = bh * m.width / m.height; }
  s.addImage({ path: file, x: bx + (bw - w) / 2, y: by + (bh - h) / 2, w, h, altText: path.basename(file) });
}
// figure slide: header + plate; title/subtitle from slide_titles.json unless given
async function figSlide(file, { section, no, label, title, sub, claim = "D", notes, dir = SLIDES }) {
  const key = file.replace(/\.png$/, "");
  const t = TITLES[key] || {};
  const s = slide("LIGHT", section);
  header(s, { no, label, title: title || t.title, claim, sub: sub || t.subtitle });
  plate(s, M, G.top, CW, G.bottom - G.top);
  const f = path.join(dir, file);
  if (fs.existsSync(f)) await fit(s, f, M + 0.06, G.top + 0.05, CW - 0.12, G.bottom - G.top - 0.1);
  else photo(s, M, G.top, CW, G.bottom - G.top, `missing ${file}`);
  s.addNotes(notes);
  return s;
}
function video(s, file, poster, label, top = G.top) {
  const h = G.bottom - top, w = h * 16 / 9, x = (W - w) / 2, y = top;
  const v = path.join(ANIM, file), p = path.join(ANIM, poster);
  if (fs.existsSync(v)) s.addMedia({ type: "video", path: v, x, y, w, h,
    cover: fs.existsSync(p) ? "data:image/png;base64," + fs.readFileSync(p).toString("base64") : undefined });
  else if (fs.existsSync(p)) s.addImage({ path: p, x, y, w, h });
  else photo(s, x, y, w, h, label);
}
function stat(s, x, y, w, { eyebrow, value, label, dark = true, valueSize = 40 }) {
  if (eyebrow) s.addText(eyebrow.toUpperCase(), { x, y, w, h: 0.28, fontFace: MED, fontSize: 11, charSpacing: 2, color: dark ? X.onSlate2 : X.ink2, margin: 0, isTextBox: true });
  s.addText(value, { x, y: y + 0.34, w, h: 0.85, fontFace: LIGHT, fontSize: valueSize, color: dark ? X.lime : X.ink, margin: 0, valign: "top", isTextBox: true });
  s.addText(label, { x, y: y + 1.22, w, h: 0.9, fontFace: BODY, fontSize: 14, color: dark ? X.onSlate2 : X.ink2, margin: 0, valign: "top", isTextBox: true });
}
const vline = (s, x, y, h, dark = true) => s.addShape(pres.shapes.LINE, { x, y, w: 0, h, line: { color: dark ? "FFFFFF" : X.rule, width: 0.75, transparency: dark ? 82 : 0 } });
// one "pixel" square for the definition diagram
function px(s, x, y, size, fill, label, txt = "FFFFFF") {
  s.addText(label, { shape: pres.shapes.RECTANGLE, x, y, w: size, h: size, fill: { color: fill }, line: { color: X.rule2, width: 0.75 },
    align: "center", valign: "middle", fontFace: MED, fontSize: 10, color: txt, margin: 2 });
}

// =================================================================== the deck
(async () => {
  const anteaterLime = await icon("gi", "GiAnteater", X.lime, 512);

  // ---------------------------------------------------------------- 1 Title + two anteater facts
  {
    const s = slide("DARK", "Opening");
    header(s, { label: "Data for Good · Question 2", dark: true });
    s.addText([
      { text: "When the patrols leave,", options: { color: X.onSlate, breakLine: true } },
      { text: "mining comes back for seconds.", options: { color: X.lime } },
    ], { x: M, y: 0.95, w: 6.95, h: 1.7, fontFace: LIGHT, fontSize: 36, margin: 0, valign: "top", isTextBox: true, objectName: "title" });
    s.addText("Operation Mercurio, La Pampa, from February 2019 · what it means for FZS in Tambopata",
      { x: M, y: 2.95, w: 6.6, h: 0.75, fontFace: BODY, fontSize: 16, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    s.addShape(pres.shapes.LINE, { x: M, y: 3.95, w: 6.7, h: 0, line: { color: "FFFFFF", width: 0.75, transparency: 82 } });
    s.addText("TWO FACTS ABOUT OUR ANIMAL", { x: M, y: 4.12, w: 6.7, h: 0.28, fontFace: MED, fontSize: 11, charSpacing: 2, color: X.lime, margin: 0, isTextBox: true });
    [["35,000", "ants a day, with a 60 cm tongue flicking up to 150 times a minute"],
     ["1 minute", "per mound. It never destroys the nest: it moves on and comes back later"]].forEach(([v, l], i) => {
      const x = M + i * 3.45;
      if (i) vline(s, x - 0.17, 4.55, 1.55);
      s.addText(v, { x, y: 4.5, w: 3.2, h: 0.6, fontFace: LIGHT, fontSize: 30, color: X.lime, margin: 0, isTextBox: true });
      s.addText(l, { x, y: 5.12, w: 3.15, h: 0.95, fontFace: BODY, fontSize: 13, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    });
    s.addText("Smithsonian's National Zoo; National Geographic", { x: M, y: 6.3, w: 6.7, h: 0.25, fontFace: BODY, fontSize: 10, color: X.onSlate2, margin: 0, isTextBox: true });
    photo(s, 7.75, 0.42, W - 7.75 - M, H - 1.0, "giant anteater at a termite mound", true);
    s.addNotes(
      "About 30 seconds. Good morning, we are Group Giant Anteater. [Names.]\n\n" +
      "Two facts about our animal. One: the giant anteater eats up to 35,000 ants and termites a day, with a tongue about 60 centimetres long that flicks up to 150 times a minute (Smithsonian's National Zoo; National Geographic).\n\n" +
      "Two, the one to remember: it spends only about a minute at each mound, never destroys the nest, moves on, and comes back later to feed again (National Geographic).\n\n" +
      "Hold on to that habit. It describes what we found for gold mining in La Pampa: hence the title, mining comes back for seconds.");
  }

  // ---------------------------------------------------------------- 2 The question + the answer up front
  {
    const s = slide("DARK", "Question");
    header(s, { no: "01", label: "The question", title: "FZS pays for operations. What happens when one ends?", dark: true,
      sub: "Net mining additions, ha/yr · Tambopata buffer zone, La Pampa, Madre de Dios · 2016–18 vs 2019–21 vs 2022–25" });
    s.addText("WHAT WE FOUND", { x: M, y: 2.2, w: 4, h: 0.3, fontFace: MED, fontSize: 12, charSpacing: 2.2, color: X.lime, margin: 0, isTextBox: true });
    const items = [
      ["LuTrendingDown", "1 · It fell, locally", arrow("tambopata_bz_pre_net", "tambopata_bz_during_net"),
        `ha/yr, Tambopata buffer zone. ${pct("tambopata_bz_stopped_share_of_fall_min")}–${pct("tambopata_bz_stopped_share_of_fall_max")} of the fall: pits going out of use`],
      ["LuMoveRight", "2 · It moved", arrow("corridor_across_pre_net", "corridor_across_during_net"),
        "ha/yr just across the road, in the legal corridor"],
      ["LuRotateCcw", "3 · It came back", ha("tambopata_bz_later_net"),
        `ha/yr in the later years (2022–25), much of it on old pits`],
    ];
    for (let i = 0; i < items.length; i++) {
      const [ic, eb, v, l] = items[i], x = M + i * 4.13;
      if (i) vline(s, x - 0.2, 2.7, 3.5);
      s.addShape(pres.shapes.OVAL, { x, y: 2.7, w: 0.7, h: 0.7, fill: { color: X.slate2 }, line: { color: X.lime, width: 1 } });
      s.addImage({ data: await icon("lu", ic, X.lime), x: x + 0.16, y: 2.86, w: 0.38, h: 0.38 });
      stat(s, x, 3.6, 3.75, { eyebrow: eb, value: v, label: l, valueSize: 40 });
    }
    s.addText("All three: description. Net additions = new land + re-mined − stopped, from yearly 30-m satellite maps.",
      { x: M, y: 6.45, w: CW, h: 0.3, fontFace: BODY, fontSize: 12, color: X.onSlate2, margin: 0, isTextBox: true });
    s.addNotes(
      "About 40 seconds. FZS supports SERNANP's operations against illegal gold mining around Tambopata. Operations are expensive, and they end. So the practical question: what should FZS expect in the targeted area, and around it, once an operation is over?\n\n" +
      "Three possibilities: mining stops for good (deterrence), it moves next door (displacement), or it waits and comes back (delay). Inside the target alone these look the same, so we compare areas.\n\n" +
      `The answer up front, all description. One: net mining additions in the Tambopata buffer zone fell from about ${ha("tambopata_bz_pre_net")} to ${ha("tambopata_bz_during_net")} hectares a year in 2019 to 2021. But a quarter to a half of that fall is pits going out of use, most of it in 2019; the rest is fewer new pits. ` +
      `Two: just across the road, in the legal corridor, net additions rose from about ${ha("corridor_across_pre_net")} to ${ha("corridor_across_during_net")} hectares a year. ` +
      `Three: in the later years, 2022 to 2025, the buffer zone was back at about ${ha("tambopata_bz_later_net")} hectares a year, much of it on old pits.`);
  }

  // ---------------------------------------------------------------- 3 Definition: one measure
  {
    const s = slide("LIGHT", "Question");
    header(s, { no: "02", label: "One measure", title: "One measure on every slide: net mining additions", claim: "D",
      sub: "Net additions (ha/yr) = new land + re-mined − stopped · per 30-m pixel, year t vs the years before · MapBiomas Peru Collection 4, 1985–2025" });
    const lx = M, ly = G.top + 0.1, sz = 0.62;
    s.addText("YEAR", { x: lx + 2.55, y: ly, w: 0.8, h: 0.25, fontFace: MED, fontSize: 10, charSpacing: 1.5, color: X.muted, margin: 0, align: "center", isTextBox: true });
    s.addText("t − 1", { x: lx + 2.55, y: ly + 0.25, w: 0.8, h: 0.25, fontFace: BODY, fontSize: 11, color: X.ink2, margin: 0, align: "center", isTextBox: true });
    s.addText("t", { x: lx + 3.75, y: ly + 0.25, w: 0.8, h: 0.25, fontFace: BODY, fontSize: 11, color: X.ink2, margin: 0, align: "center", isTextBox: true });
    const rows = [
      ["New land", "never mined before", X.new, "E7E1D6", "forest", X.new, "mined", "+"],
      ["Re-mined", "mined years ago, not last year", X.remined, "E7E1D6", "old pit", X.remined, "mined", "+"],
      ["Stopped", "mined last year, not this year", X.stopped, "8A6B4E", "mined", "DDEFEC", "water / regrowth", "−"],
    ];
    rows.forEach(([name, rule, col, c0, l0, c1, l1, sign], i) => {
      const y = ly + 0.6 + i * 1.05;
      s.addText(sign, { x: lx, y, w: 0.4, h: sz, fontFace: LIGHT, fontSize: 30, color: col, margin: 0, valign: "middle", isTextBox: true });
      s.addText([{ text: name, options: { fontFace: MED, fontSize: 17, color: X.ink, breakLine: true } },
        { text: rule, options: { fontFace: BODY, fontSize: 12, color: X.ink2 } }],
        { x: lx + 0.4, y: y - 0.05, w: 2.1, h: sz + 0.1, margin: 0, valign: "middle", isTextBox: true });
      px(s, lx + 2.64, y, sz, c0, l0, c0 === "E7E1D6" ? X.ink2 : "FFFFFF");
      s.addShape(pres.shapes.LINE, { x: lx + 3.32, y: y + sz / 2, w: 0.48, h: 0, line: { color: X.ink2, width: 1.25, endArrowType: "triangle" } });
      px(s, lx + 3.84, y, sz, c1, l1, c1 === "DDEFEC" ? X.ink2 : "FFFFFF");
    });
    const ey = ly + 3.85;
    s.addShape(pres.shapes.RECTANGLE, { x: lx, y: ey, w: 5.1, h: 0.95, fill: { color: X.surface }, line: { color: X.rule, width: 0.75 } });
    s.addText([
      { text: "Net", options: { color: X.ink, bold: true } }, { text: " = ", options: { color: X.ink2 } },
      { text: "new", options: { color: X.new, bold: true } }, { text: " + ", options: { color: X.ink2 } },
      { text: "re-mined", options: { color: X.remined, bold: true } }, { text: " − ", options: { color: X.ink2 } },
      { text: "stopped", options: { color: X.stopped, bold: true } },
    ], { x: lx + 0.2, y: ey + 0.08, w: 4.8, h: 0.5, fontFace: MED, fontSize: 22, margin: 0, valign: "middle", isTextBox: true });
    s.addText("= mining area this year − last year. Hectares are a proxy for mining activity, not for miners.",
      { x: lx + 0.2, y: ey + 0.55, w: 4.8, h: 0.35, fontFace: BODY, fontSize: 11, color: X.ink2, margin: 0, isTextBox: true });
    // zone map
    const mx = M + 5.5, mw = W - M - mx, mh = mw * 9 / 16;
    const f = path.join(ANIM, "stills", "map_zones_clean.png");
    if (fs.existsSync(f)) s.addImage({ path: f, x: mx, y: G.top, w: mw, h: mh, altText: "zone map" });
    else photo(s, mx, G.top, mw, mh, "zone map");
    s.addText([
      { text: "Same zones everywhere: ", options: { fontFace: MED, color: X.ink } },
      { text: "Tambopata buffer zone (whole, incl. Kotsimba) · La Pampa sector (its 70.15–69.80° W part) · corridor across the road (D.L. 1100, ≤ 10 km north of the highway) · Amarakaeri buffer zone (less treated) · Madre de Dios.", options: { fontFace: BODY, color: X.ink2 } },
    ], { x: mx, y: G.top + mh + 0.12, w: mw, h: 0.85, fontSize: 12, margin: 0, valign: "top", isTextBox: true });
    s.addNotes(
      "About 40 seconds. One measure on every slide from here on: net mining additions, in hectares per year. It is simply the mining area this year minus last year, from the MapBiomas Peru satellite maps at 30 metres.\n\n" +
      "We split it into three parts, always in the same colours. Brown: new land, mined for the first time since 1985. Amber: re-mined, old pits mined again after a gap. Teal: stopped, pits that left the mining class, most often because they flooded or started to regrow. Net equals new plus re-mined minus stopped.\n\n" +
      "Why it matters: a fall in net additions can mean fewer new pits, or more pits going out of use. Those are different stories for FZS.\n\n" +
      "And the same zones everywhere: the Tambopata buffer zone as SERNANP draws it, La Pampa as its western part, the strip of legal corridor across the road, the Amarakaeri buffer zone as the less-treated comparison, and the whole department. Hectares measure mining activity, not the number of miners.");
  }

  // ---------------------------------------------------------------- 4 Map build (part A): four click-through slides
  // Same layout as the 2026-10-13 deck (flippable steps, fixed positions); stills from the v3 map export
  // (presentation/animation/out/stills/map_step{1-4}_clean.png). The video version is in the backup.
  const steps = [
    ["Protected areas", "Tambopata reserve, its buffer zone and the Amarakaeri buffer zone. Pink: communities."],
    ["The Interoceanic Highway", "One road runs along the buffer zone and splits it from the land to the north."],
    ["Where mining can be legal", "The legal mining corridor, north of the road. South of it, in the buffer zone: a crime."],
    ["The target", "La Pampa, Mercurio's target from Feb 2019, and the corridor strip across the road."],
  ];
  const stepNotes = [
    "This is Madre de Dios, in the south-east of the Peruvian Amazon. In green, the protected areas: Tambopata National Reserve in the south, the core FZS helps protect, ringed by its buffer zone. We use the buffer zone exactly as SERNANP draws it, including the Kotsimba native community inside it. West of it the Amarakaeri buffer zone, our less-treated comparison. Pink outlines are native communities.",
    "The white line is the Interoceanic Highway, the paved road from Brazil to the Pacific. It runs right along the edge of the buffer zone. Remember this road: it becomes the border in our story. Blue lines are rivers: the gold here is alluvial, in the floodplains.",
    "The blue area is the mining corridor created by decree in 2012, D.L. 1100. Inside it, small-scale mining can be permitted. South of the road, in the buffer zone, the same work is a crime. Legality is about location: the satellite maps themselves cannot tell legal from illegal mining.",
    "In orange, La Pampa, the target of Operation Mercurio from February 2019. We define it as the buffer zone's part between 70.15 and 69.80 degrees west; there is no official boundary. The blue box just across the road is the part of the legal corridor directly opposite. Watch these two boxes: every number on the next slides is net mining additions in these zones.",
  ];
  for (let k = 0; k < steps.length; k++) {
    const s = slide("LIGHT", "Where");
    header(s, { no: "03", label: "Where we are", title: "La Pampa sits one road away from legal mining land", claim: "D",
      sub: `Madre de Dios, Peru · step ${k + 1} of ${steps.length} · zones as used on every slide` });
    const lx = M, lw = 3.5, rowH = (G.bottom - G.top) / steps.length;
    steps.forEach(([head, text], i) => {
      const on = i === k, past = i < k, y = G.top + i * rowH;
      s.addText(`${i + 1}`, { shape: pres.shapes.OVAL, x: lx, y: y + 0.02, w: 0.36, h: 0.36, align: "center", valign: "middle", fontFace: MED,
        fontSize: 12, color: on ? "FFFFFF" : (past ? X.eyebrow : X.muted), fill: on ? { color: X.eyebrow } : { type: "none" },
        line: { color: on || past ? X.eyebrow : X.rule2, width: 1 }, margin: 0 });
      s.addText(head, { x: lx + 0.5, y, w: lw - 0.5, h: 0.4, fontFace: on ? MED : BODY, fontSize: 16, color: on ? X.ink : (past ? X.ink2 : X.muted),
        margin: 0, valign: "middle", isTextBox: true });
      if (on) s.addText(text, { x: lx + 0.5, y: y + 0.42, w: lw - 0.5, h: rowH - 0.5, fontFace: BODY, fontSize: 13, color: X.ink2, margin: 0, valign: "top", isTextBox: true });
    });
    const clean = path.join(ANIM, "stills", `map_step${k + 1}_clean.png`), cap = path.join(ANIM, "stills", `map_step${k + 1}.png`);
    const f = fs.existsSync(clean) ? clean : cap;
    const mx = M + lw + 0.25, mw = W - M - mx, mh = Math.min(mw * 9 / 16, G.bottom - G.top);
    if (fs.existsSync(f)) s.addImage({ path: f, x: mx, y: G.top, w: mh * 16 / 9, h: mh, altText: `map step ${k + 1}` });
    else photo(s, mx, G.top, mw, mh, `map step ${k + 1}`);
    s.addNotes(`Step ${k + 1} of ${steps.length}, about 12 seconds; click for the next step. ${stepNotes[k]}`);
  }

  // ---------------------------------------------------------------- 5 Timeline (part B)
  {
    const s = slide("LIGHT", "Where");
    header(s, { no: "04", label: "2010–2025 in one minute", title: "2010–2025: new pits, old pits re-mined, pits stopping", claim: "D",
      sub: "Net mining additions as three flows on the map: new land (brown), re-mined (amber), stopped (teal) · counter: net ha per year, La Pampa sector and corridor across the road" });
    video(s, "MiningTimeline.mp4", "stills/timeline_2019.png", "mining timeline animation");
    s.addNotes(
      "About 60 seconds, click to play. Each year, brown pixels are land mined for the first time, amber are old pits mined again, teal are pits that stopped; grey is everything mapped as mining that year. On the right, the net additions per year for La Pampa and for the strip across the road, with the three parts.\n\n" +
      `Before 2019, brown dominates in La Pampa, south of the road. Watch 2019, the Mercurio year: new clearing did not fall in 2019 — about ${ha("lapampa_2019_new")} hectares of new land in La Pampa, against ${ha("lapampa_2018_new")} in 2018 — but land going out of use did: ${ha("lapampa_2019_stopped")} hectares stopped. So net additions drop to ${ha("lapampa_2019_net")}.\n\n` +
      "In 2020 and 2021, La Pampa's net additions sit near zero while the strip across the road lights up. In the later years, amber appears: mining comes back, much of it on old pits. In 2025 the navy leaves the river posts.\n\n" +
      "The video ends with the caveat we repeat: satellites can't see river dredges or mercury.");
  }

  // ---------------------------------------------------------------- 6–11 What happened (figures)
  const what = [
    ["slide_01_net_two_zones.png", "05", "It fell, locally",
      `About 40 seconds. The first comparison, the course's: net mining additions in the Tambopata buffer zone, orange, and in the Amarakaeri buffer zone, green, our less-treated comparison.\n\n` +
      `In 2016 to 2018 Tambopata added about ${ha("tambopata_bz_pre_net")} hectares a year. In 2019 to 2021, Mercurio and what followed, only ${ha("tambopata_bz_during_net")}: a ${pct("sl_net_tambopata_bz_fall_share")} fall. Amarakaeri went the other way, ${ha("amarakaeri_bz_pre_net")} to ${ha("amarakaeri_bz_during_net")}. ` +
      `The simple difference-in-differences is ${ha("did_main_net")} hectares a year: a description, not yet a cause.\n\n` +
      `In the later years Tambopata was back at ${ha("tambopata_bz_later_net")}. The 2023 spike shows up in MapBiomas only, so we also report the later years without it: ${ha("tambopata_bz_later_ex2023_net")}.`],
    ["slide_02_parts_two_zones.png", "06", "What fell",
      `About 50 seconds. Now the same zones, split into the three parts, as period averages. The black bar is net.\n\n` +
      `In Tambopata, new land fell from ${ha("tambopata_bz_pre_new")} to ${ha("tambopata_bz_during_new")} hectares a year: it roughly halved. At the same time stopped land, pits going out of use, nearly doubled, from ${ha("tambopata_bz_pre_stopped")} to ${ha("tambopata_bz_during_stopped")}. ` +
      `Depending on how we count map flicker, between ${pct("tambopata_bz_stopped_share_of_fall_min")} and ${pct("tambopata_bz_stopped_share_of_fall_max")} of the fall in net additions is that extra stopping, and ${pct("tambopata_bz_excess_stopped_share_in_2019")} of the extra stopping happened in 2019.\n\n` +
      `In Amarakaeri, stopped land stayed flat (${ha("amarakaeri_bz_pre_stopped")} to ${ha("amarakaeri_bz_during_stopped")}). Why it matters: a net fall is not the same as fewer new pits. Part of what fell is old pits leaving the mining class.`],
    ["slide_03_lapampa_parts.png", "07", "2019, year by year",
      `About 40 seconds. Zoom into La Pampa itself, year by year. Brown up is new land, amber re-mined, teal down is stopped; the black line is net.\n\n` +
      `New clearing did not fall in 2019; land going out of use did. In 2019 La Pampa still added ${ha("lapampa_2019_new")} hectares of new land, against ${ha("lapampa_2018_new")} in 2018. But ${ha("lapampa_2019_stopped")} hectares stopped, so net additions fell to ${ha("lapampa_2019_net")}. ` +
      `New land only drops from 2020, which is also the first COVID year.\n\n` +
      `Why it matters for FZS: in the first year of an operation, new pits keep opening at the edges while patrolled pits go quiet. That is why a monitoring ring around the operation matters, more on that in the recommendations.`],
    ["slide_04_moved.png", "08", "It moved",
      `About 50 seconds. Left: the strip of legal corridor directly across the road from La Pampa. Net additions rose from about ${ha("corridor_across_pre_net")} hectares a year in 2016 to 2018 to ${ha("corridor_across_during_net")} in 2019 to 2021, mostly new land.\n\n` +
      `Right: the whole department. Madre de Dios never fell: ${arrow("mdd_pre_net", "mdd_during_net", "mdd_later_net")} hectares a year across the three periods. The legal corridor's share of the department's net additions went from ${pct("v2_corridor_share_pre_net")} to ${pct("v2_corridor_share_during_net")}, then ${pct("v2_corridor_share_later_net")} in the later years.\n\n` +
      `Careful: the rise elsewhere in the department was ${need("mdd_rise_elsewhere_vs_tambopata_fall").toFixed(1)} times the size of Tambopata's fall, so this is not just the same miners moving; new entrants and the gold price play a part. We cannot show it was the same people.`],
    ["slide_05_later_old_pits.png", "09", "It came back",
      `About 40 seconds. Back to the whole Tambopata buffer zone, 2010 to 2025. In the later years, 2022 to 2025, net additions were back at ${ha("tambopata_bz_later_net")} hectares a year, ${ha("tambopata_bz_later_ex2023_net")} without the 2023 spike.\n\n` +
      `Much of it came back on old pits: re-mined land averaged ${ha("tambopata_bz_later_remined")} hectares a year, against ${ha("tambopata_bz_pre_remined")} before. Forest-loss alerts do not see this, because there is no forest left to lose. MAAP #193 (2023) reports the same return to degraded land.\n\n` +
      `Note the wording: we call 2022 to 2025 the later years, because enforcement never simply stopped; it went on in waves: Plan Restauración in 2021 and a state of emergency from April 2023.`],
    ["slide_06_reserve.png", "10", "Inside the reserve",
      `About 30 seconds. This is FZS's core area: the Tambopata National Reserve itself, not the buffer zone.\n\n` +
      `Net additions inside the reserve stayed small or negative for years; in 2019 to 2021 they averaged ${ha("tambopata_nr_during_net")} hectares a year. In 2025 they jumped by ${ha("tambopata_nr_2025_net")} hectares, the year the navy left its river posts on the Malinowski for lack of funds. MAAP #241 (2026) reports about 500 hectares from late 2025 to February 2026.\n\n` +
      `The 2017 bar is an earlier jump; treat single years with care.`],
  ];
  for (const [file, no, label, notes] of what) await figSlide(file, { section: "What happened", no, label, notes });

  // ---------------------------------------------------------------- 12 Causal (conditional)
  await figSlide("slide_07_causal.png", { section: "Is it causal?", no: "11", label: "Is it causal?", claim: "C",
    title: TITLES.slide_07_causal.title,
    sub: `If the comparison zones show what Tambopata would have done, Mercurio and what followed lowered net additions by ${abs("model_m1_during_net")}–${abs("did_base2014_net")} ha/yr in 2019–21 (upper bound; part of it pits stopping; coincides with COVID) · Tambopata buffer zone · ha/yr`,
    notes:
      "About 60 seconds. The one causal sentence we are willing to make, and it has an 'if'. " +
      `If the comparison zones show what Tambopata would have done without the operation, then Mercurio and what followed lowered net additions in the buffer zone by about ${abs("model_m1_during_net")} to ${abs("did_base2014_net")} hectares a year in 2019 to 2021. ` +
      `The low end is the model with zone and year effects across ${int("model_m1_n")} Peruvian buffer zones; the high end the two-by-two against Amarakaeri with 2014 to 2018 as the base. Synthetic difference-in-differences lands in between, ${ha("sdid_sdid_ha_during_net")}.\n\n` +
      `The bars show what the estimate is made of: less new land, and more stopped land: about ${abs("model_m1_during_stopped")} hectares a year of the M1 estimate is extra stopping. So part of the 'effect' is pits going out of use.\n\n` +
      `Right side: the ranks are not a significance test. In hectares Tambopata has the biggest fall of ${int("model_m1_n")} zones, but it also has the biggest change in 2014, before Mercurio: the raw rank measures size. Scaled to each zone's own size it ranks ${int("sl_rank_scaled_lo")} to ${int("sl_rank_scaled_hi")} of ${int("model_m4_n")}, nothing special.\n\n` +
      "Read it as an upper bound: La Pampa was targeted at its peak, miners moving into the comparison zones widen the gap, and the fall coincides with COVID." });

  // ---------------------------------------------------------------- 13 What satellites can't see + bias directions
  {
    const s = slide("LIGHT", "Limits");
    header(s, { no: "12", label: "Limits", title: "What satellites cannot see, and which way our biases push", claim: "D",
      sub: "Net mining additions measure land, not people, rivers or mercury · direction of each bias for the 2019–21 fall, Tambopata buffer zone" });
    s.addText("SATELLITES CAN'T SEE", { x: M, y: G.top, w: 5.6, h: 0.3, fontFace: MED, fontSize: 11, charSpacing: 2, color: X.accent, margin: 0, isTextBox: true });
    const cant = [["LuShip", "River dredges", "148 → 598 in La Pampa, 2021–23 (MAAP #193)"], ["LuDroplets", "Mercury", "in rivers and fish"],
      ["LuUsers", "People", "hectares, not miners"], ["LuRefreshCw", "Map flicker", `${pct("tambopata_bz_during_stopped_share_back_within_2y")} of land that stopped in 2019–21 was mined again within 2 years`]];
    const tw = 2.72, th = 2.2, ty = G.top + 0.4;
    for (let i = 0; i < cant.length; i++) {
      const [ic, head, txt] = cant[i], x = M + (i % 2) * (tw + 0.16), y = ty + Math.floor(i / 2) * (th + 0.16);
      plate(s, x, y, tw, th);
      s.addImage({ data: await icon("lu", ic, X.accent), x: x + 0.25, y: y + 0.25, w: 0.5, h: 0.5 });
      s.addText(head, { x: x + 0.25, y: y + 0.9, w: tw - 0.45, h: 0.4, fontFace: MED, fontSize: 18, color: X.ink, margin: 0, isTextBox: true });
      s.addText(txt, { x: x + 0.25, y: y + 1.32, w: tw - 0.45, h: 0.8, fontFace: BODY, fontSize: 13, color: X.ink2, margin: 0, valign: "top", isTextBox: true });
    }
    const rx = M + 2 * tw + 0.16 + 0.55, rw = W - M - rx, cx = rx + rw * 0.5;
    s.addText("EACH BIAS MAKES THE 2019–21 FALL LOOK…", { x: rx, y: G.top, w: rw, h: 0.3, fontFace: MED, fontSize: 11, charSpacing: 2, color: X.d, margin: 0, isTextBox: true });
    s.addText("smaller", { x: rx, y: G.top + 0.42, w: rw / 2 - 0.12, h: 0.3, fontFace: MED, fontSize: 14, color: X.blue, align: "right", margin: 0, isTextBox: true });
    s.addText("bigger", { x: cx + 0.12, y: G.top + 0.42, w: rw / 2 - 0.12, h: 0.3, fontFace: MED, fontSize: 14, color: X.orange, margin: 0, isTextBox: true });
    const biases = [["Targeted at its peak", +1], ["Miners moved into comparison zones", +1], ["Big zones fall more in hectares", +1],
      ["Pits stopping counted as less mining", +1], ["Comparison zones had operations too", -1], ["Yearly maps blur Feb 2019", -1]];
    const rowH = 0.6, ry = G.top + 0.9, len = rw * 0.48;
    s.addShape(pres.shapes.LINE, { x: cx, y: ry - 0.05, w: 0, h: biases.length * rowH, line: { color: X.ink2, width: 1.25 } });
    biases.forEach(([lab, dir], i) => {
      const y = ry + i * rowH;
      s.addShape(pres.shapes.RECTANGLE, { x: dir > 0 ? cx : cx - len, y: y + 0.07, w: len, h: rowH - 0.16, fill: { color: dir > 0 ? "F6E1D3" : "DCE9F3" }, line: { type: "none" } });
      s.addText(lab, { x: dir > 0 ? cx + 0.12 : cx - len + 0.1, y: y + 0.07, w: len - 0.22, h: rowH - 0.16, fontFace: BODY, fontSize: 13,
        color: X.ink, align: dir > 0 ? "left" : "right", valign: "middle", margin: 0, isTextBox: true });
    });
    s.addText("Read the fall as an upper bound, the return as a lower bound.",
      { x: rx, y: ry + biases.length * rowH + 0.2, w: rw, h: 0.5, fontFace: MED, fontSize: 15, color: X.ink, margin: 0, valign: "top", isTextBox: true });
    s.addNotes(
      "About 30 seconds. Every brief must say what satellites can't see. River dredges: MAAP counted 148 rising to 598 in La Pampa between 2021 and 2023. Mercury in rivers and fish. People: hectares measure mining activity, not the number of miners. " +
      `And map flicker: ${pct("tambopata_bz_during_stopped_share_back_within_2y")} of the land that 'stopped' in 2019 to 2021 was mapped as mining again within two years, so some stopping is the classifier, or miners returning.\n\n` +
      "On the right, the direction of each bias. Targeted at its record peak, miners moving into comparison zones, size, and counting pits that stop as less mining all make the fall look bigger. The comparison zones' own operations and yearly maps blurring a February start push the other way.\n\n" +
      "So: read our fall as an upper bound, and the return as a lower bound.");
  }

  // ---------------------------------------------------------------- 14 For FZS (recommendations)
  {
    const s = slide("DARK", "For FZS");
    header(s, { no: "13", label: "For FZS", title: "Stay after the sweep, and watch the ring around it", claim: "P", dark: true,
      sub: "Informed expectations from one case (prediction), not proven rules · net mining additions, Tambopata buffer zone, reserve and corridor" });
    const recs = [
      ["LuCalendarClock", "Stay after the sweep", arrow("tambopata_bz_during_net", "tambopata_bz_later_net"),
        "ha/yr net additions, 2019–21 → later years. Fund presence, not one-off operations."],
      ["LuRadar", "Watch the ring, in near real time", arrow("corridor_across_pre_net", "corridor_across_during_net"),
        "ha/yr just across the road. Forest-loss alerts on a few-km ring around each operation."],
      ["LuShieldCheck", "Hold the reserve's first km and the river", pct("rd_reserve_inside_share_1km"),
        "of first-time mining inside the reserve lies within 1 km of its edge. Staff the Malinowski posts."],
    ];
    for (let i = 0; i < recs.length; i++) {
      const [ic, head, v, l] = recs[i], x = M + i * 4.13, y = G.top + 0.25;
      if (i) vline(s, x - 0.2, y, 4.5);
      s.addShape(pres.shapes.OVAL, { x, y, w: 0.8, h: 0.8, fill: { color: X.slate2 }, line: { color: X.lime, width: 1 } });
      s.addImage({ data: await icon("lu", ic, X.lime), x: x + 0.18, y: y + 0.18, w: 0.44, h: 0.44 });
      s.addText(head, { x, y: y + 1.05, w: 3.8, h: 0.8, fontFace: MED, fontSize: 20, color: X.onSlate, margin: 0, valign: "top", isTextBox: true });
      s.addText(v, { x, y: y + 1.95, w: 3.8, h: 0.8, fontFace: LIGHT, fontSize: 36, color: X.lime, margin: 0, isTextBox: true });
      s.addText(l, { x, y: y + 2.8, w: 3.6, h: 1.2, fontFace: BODY, fontSize: 15, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    }
    s.addNotes(
      "About 50 seconds. Three recommendations. They build on this one case, so treat them as informed expectations, not proven rules.\n\n" +
      `One, stay after the sweep. Net additions stayed low only in 2019 to 2021; in the later years the buffer zone was back at about ${ha("tambopata_bz_later_net")} hectares a year, and the 2025 incursion into the reserve came right after a withdrawal. Fund presence, not one-off operations.\n\n` +
      `Two, watch the ring around the enforcement zone in near real time. In 2019 new pits kept opening in La Pampa while patrolled pits stopped, and new mining rose across the road, from about ${ha("corridor_across_pre_net")} to ${ha("corridor_across_during_net")} hectares a year net. A forest-loss alert system like GLAD or MAAP on a ring of a few kilometres around each operation catches the next pit before it is dug out. Add old pits to the watch list: alerts miss re-mining.\n\n` +
      `Three, hold the reserve's first kilometre and the river. ${pct("rd_reserve_inside_share_1km")} of first-time mining inside the reserve lies within one kilometre of its edge. Staff the Malinowski posts, and push gold traceability in the corridor.\n\n` +
      "What would let us say more: dated patrol records per zone from SERNANP or FZS, dredge counts, and mercury sampling.");
  }

  // ---------------------------------------------------------------- Thanks
  {
    const s = slide("DARK", "Closing");
    header(s, { label: "Thank you", dark: true });
    s.addText([
      { text: "Questions?", options: { color: X.onSlate, breakLine: true } },
      { text: "Like the anteater, mining comes back for seconds.", options: { color: X.lime, fontSize: 22 } },
    ], { x: M, y: 1.2, w: 6.8, h: 2.4, fontFace: LIGHT, fontSize: 54, margin: 0, valign: "top", isTextBox: true });
    s.addImage({ data: anteaterLime, x: M, y: 3.9, w: 1.3, h: 1.3 });
    photo(s, 7.75, 0.42, W - 7.75 - M, H - 1.0, "rangers / Tambopata river", true);
    s.addNotes("Thank you. Happy to take questions. Backup: six attempts, stopped land split, the road and cell designs, twins, Brazil, money and gold, definitions and data, map steps.");
  }

  // ---------------------------------------------------------------- Backup
  {
    const s = slide("DARK", "Backup");
    header(s, { label: "Backup", title: "For questions", dark: true,
      sub: "Six attempts · stopped land · road and cells · twins · Brazil · money and gold · definitions and data · map steps" });
    s.addNotes("Backup slides, only if asked.");
  }
  {
    const s = slide("LIGHT", "Backup");
    header(s, { label: "Backup · Six attempts", title: "Six attempts at cause: two hold in hectares only", claim: "C",
      sub: "Net mining additions, Tambopata buffer zone, 2019–21 vs before, ha/yr unless stated · all conditional on the comparison" });
    const rows = [
      ["METHOD", "COMPARES TAMBOPATA WITH", "RESULT (NET)", "VERDICT"],
      ["1  Zone + year effects (M1–M3)", `${int("model_m1_n") - 1} Peruvian buffer zones`, `${ha("model_m1_during_net")} to ${ha("model_m3_during_net")}; scaled rank ${int("model_m1_rank_scaled")} of ${int("model_m1_n_scaled")}`, "Holds in ha"],
      ["2  Synthetic control", "Weighted mix of zones", `${ha("sdid_sc_ha_during_net")}; no pre-2019 fit in hectares`, "Weak"],
      ["3  Rule-based twins", "Amanã, Tapajós, Munduruku (Brazil)", `${pct("top3_ratio")}–${pct("top3_ratio_excl_unverified")} of their pace (AMW, other measure)`, "Weak"],
      ["4  Spatial RD at the road", "Either side of the highway", `${need("rd_road_did_net") >= 0 ? "+" : "−"}${Math.abs(need("rd_road_did_net")).toFixed(1)} pts of land/yr (p = ${p2("rd_road_did_net_p")})`, "Swing only"],
      ["5  Matching (7 methods)", "Areas picked by algorithm", `All slower; placebo p ${p2("psm_p_min")}–${p2("psm_p_max")}`, "Can't decide"],
      ["6  Synthetic DiD", "Weighted, trend-matched zones", `${ha("sdid_sdid_ha_during_net")}; scaled rank ${int("sdid_sdid_scaled_during_rank")} of ${int("sdid_sdid_scaled_during_n")}`, "Holds in ha"],
    ];
    const vc = { "Holds in ha": X.eyebrow, "Weak": X.p, "Swing only": X.p, "Can't decide": X.muted };
    s.addTable(rows.map((r, i) => r.map((c, j) => ({ text: c, options: {
      fontFace: i === 0 || j === 3 ? MED : BODY, fontSize: i === 0 ? 10.5 : 14, charSpacing: i === 0 ? 1.5 : 0,
      color: i === 0 ? X.ink2 : (j === 3 ? vc[c] : X.ink), fill: { color: i === 0 ? X.surface2 : X.surface }, valign: "middle", margin: [5, 10, 5, 10] } }))),
      { x: M, y: G.top, w: CW, colW: [3.2, 3.2, 4.3, 1.53], rowH: 0.66, border: { type: "solid", color: X.rule, pt: 0.75 } });
    s.addNotes("Only the zone-level designs hold, and only in hectares: scaled to size Tambopata is ordinary. The raw rank 1 of 15 also appears in 2014, before Mercurio, so it measures size, not significance. Synthetic control cannot fit Tambopata's size before 2019; the twins grew differently before 2019 and use another measure (Amazon Mining Watch new area, not net additions); the road discontinuity measures a swing, an upper bound because displacement breaks its no-spillover assumption; matching never beats chance and has no common support.");
  }
  await figSlide("slide_b1_stopped_split.png", { section: "Backup", label: "Backup · Stopped land", claim: "D",
    notes: `What 'stopped' means on the ground. Most stopped land becomes water (flooded pits) or regrows; a large share is mapped as mining again within two years: in the Tambopata buffer zone ${pct("tambopata_bz_during_stopped_share_back_within_2y")} for 2019–21. That is classifier flicker or miners returning; we have no image validation sample.` });
  for (const [file, label, title, notes] of [
    ["fig_v2_rdd.png", "Road and reserve edge", "At the road the gap swung north; at the reserve edge nothing",
      "Spatial regression discontinuity on net additions, as a difference in discontinuities. The road estimate is a swing (north up, south down), an upper bound because displacement breaks the no-spillover assumption. Description."],
    ["fig_v2_stats_event.png", "1-km cells", "Cell panel: close to a before/after, not a clean comparison",
      "1-km cell panel on net additions. The comparison cells hold almost no mining, so this is close to a before/after comparison. Description."],
  ]) await figSlide(file, { section: "Backup", label: `Backup · ${label}`, title, claim: "D", dir: OUT,
    sub: "Net mining additions (and parts where linear) · La Pampa longitudes · 2014–25 · see the methods page for the full setup", notes });
  await figSlide("slide_b2_twins.png", { section: "Backup", label: "Backup · Twins", claim: "D",
    notes: `Rule-based twins (Ruby's design), all chosen by one dating rule. Tambopata added new mining at ${pct("top3_ratio")} of the twins' mean pace in 2019–21 (${pct("top3_ratio_excl_unverified")} without Munduruku). Different measure: Amazon Mining Watch new area, comparable to first-time mining, not net additions. Before 2019 the twins grew differently (pre-trends rejected), so they can't show the counterfactual.` });
  {
    const s = slide("LIGHT", "Backup");
    header(s, { label: "Backup · Brazil", title: "Brazil: a boom, then a fall; operations came at the peak", claim: "D",
      sub: "Net mining additions, ha/yr · MapBiomas Brazil (indigenous lands: Collection 11; staggered DiD: Collection 11 rasters, our pixel accounting)" });
    [["All indigenous lands, artisanal", arrow("br_pack_art_add_mean_2016_2018", "br_pack_art_add_mean_2019_2022", "br_pack_art_add_mean_2023_2025"), "ha/yr net additions, 2016–18 → 2019–22 → 2023–25"],
     ["Yanomami territory", arrow("brv2_yan_net_boom", "brv2_yan_net_later"), "ha/yr net additions, 2019–22 → 2023–25 (operation from Feb 2023)"],
     [`Staggered DiD, ${int("brv2_n_units")} territories`, `${need("brv2_net_did2s") >= 0 ? "+" : "−"}${abs("brv2_net_did2s")}`, `ha/yr net, p = ${p2("brv2_net_did2s_p")}: cannot separate`]].forEach(([eb, v, l], i) => {
      const x = M + i * 4.13;
      if (i) vline(s, x - 0.2, G.top, 2.4, false);
      stat(s, x, G.top, 3.85, { eyebrow: eb, value: v, label: l, dark: false, valueSize: 26 });
    });
    plate(s, M, 4.75, CW, 1.2);
    s.addText("Operations came at the peak of a boom, together with national gold-sale reforms (Jan 2023). Our design cannot separate them.",
      { x: M + 0.25, y: 4.75, w: CW - 0.5, h: 1.2, fontFace: LIGHT, fontSize: 20, color: X.ink, margin: 0, valign: "middle", isTextBox: true });
    s.addNotes("Only if asked. Brazil is the mirror image: weaker federal enforcement in 2019–22, then targeted operations from 2023 (Yanomami from February 2023). Mining in indigenous lands boomed and then fell, but the operations came at the peak, and a national change in January 2023 (end of the gold 'good faith' rule, electronic invoices) hit all territories at once. A territory-level design cannot separate these, and the staggered estimate is not distinguishable from zero. Description.");
  }
  await figSlide("slide_b3_context.png", { section: "Backup", label: "Backup · Money and gold", claim: "D",
    notes: "Context, not a test. The PP 0128 budget booked in Madre de Dios jumped in 2019 and shrank after (a lower bound: national units book in Lima). The gold price rose about 2.7-fold from 2018 to 2025. La Pampa's net additions came back as money faded and the price rose; with 11 years and money that follows mining, we do not test this." });
  {
    const s = slide("LIGHT", "Backup");
    header(s, { label: "Backup · Definitions and data", title: "Definitions and data", claim: "D",
      sub: "One outcome, one zone registry, one treatment (plan v3) · every number in this deck comes from output/numbers.csv" });
    const rows = [
      ["ITEM", "DEFINITION", "SOURCE"],
      ["Net mining additions", "Mining area in year t − year t−1, ha/yr = new land + re-mined − stopped", "MapBiomas Peru Collection 4 rasters (30 m, class 4.2)"],
      ["New land / re-mined / stopped", "First time since 1985 / mined again after a gap / left the mining class", "Our pixel accounting (code/raster_zones.py)"],
      ["Tambopata buffer zone", "Official SERNANP polygon, whole (incl. Kotsimba)", "SERNANP"],
      ["La Pampa sector", "Tambopata buffer zone between 70.15° and 69.80° W (no official line)", "Our boundary"],
      ["Corridor across the road", "D.L. 1100 corridor ≤ 10 km north of the highway, La Pampa longitudes", "INGEMMET, RAISG"],
      ["Treatment", "Operation Mercurio, Feb 2019; first treated year 2019; reference 2018", "MAAP #130; MINAM"],
      ["Periods", "2016–18 before · 2019–21 Mercurio and what followed · 2022–25 later years (± 2023)", "Course card"],
    ];
    s.addTable(rows.map((r, i) => r.map((c) => ({ text: c, options: {
      fontFace: i === 0 ? MED : BODY, fontSize: i === 0 ? 10.5 : 13, charSpacing: i === 0 ? 1.5 : 0, color: i === 0 ? X.ink2 : X.ink,
      fill: { color: i === 0 ? X.surface2 : X.surface }, valign: "middle", margin: [4, 10, 4, 10] } }))),
      { x: M, y: G.top, w: CW, colW: [2.9, 5.9, 3.43], rowH: 0.56, border: { type: "solid", color: X.rule, pt: 0.75 } });
    s.addNotes("Definitions for questions. The course's statistics workbook numbers (1,640 → 163 ha/yr) are reproduced as checks; our numbers come from the rasters on one zone registry and differ in the last digit.");
  }
  {
    const s = slide("LIGHT", "Backup");
    header(s, { label: "Backup · Map video", title: "The map build as one animation", claim: "D",
      sub: "Same four steps as the click-through map slides · protected areas → highway → corridor → La Pampa · click to play (21 s)" });
    video(s, "MapLayers.mp4", "stills/map_step4.png", "map layers animation");
    s.addNotes("Optional: the same four steps as the click-through map slides, as one video.");
  }

  for (const [k, t] of titles) {
    const width = t.length * 0.0066 * G.titleSize;
    if (width > CW) console.warn(`slide ${k}: title may wrap (${t.length} chars): ${t}`);
  }
  const file = path.join(__dirname, "GroupAnteater_FZS_talk.pptx");
  await pres.writeFile({ fileName: file });
  const { applyTheme } = require("./apply_theme.js");
  await applyTheme(file, THEME);
  fs.writeFileSync(path.join(__dirname, "deck_ids_used.txt"), [...used].sort().join("\n") + "\n");
  console.log(`Wrote ${file} (${n} slides, ${used.size} number ids)`);
})();
