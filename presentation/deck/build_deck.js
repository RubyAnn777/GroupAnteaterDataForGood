// Build the FZS talk deck:  cd presentation/deck && npm install && node build_deck.js
// Design = the walkthrough page's visual language (docs/overnight/build_report.py): Roboto Light titles, green kickers
// with a hairline rule, raspberry chapter numbers, framed figure plates on warm off-white, pill claim badges, thin lime
// numbers on slate. FZS colours, no FZS logo (student work).
// Layout rule: every content slide puts kicker, title (one line, 28 pt), subtitle and content at the SAME positions,
// so nothing jumps when clicking through. Text follows Smart Brevity: takeaway titles, short units, details in the notes.
// Every number is read from output/numbers.csv (or computed from it). Hand-typed facts are cited external facts.
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

// ------------------------------------------------------------------ numbers
const N = {};
fs.readFileSync(path.join(OUT, "numbers.csv"), "utf8").split("\n").slice(1).forEach((line) => {
  if (!line.trim()) return;
  const [id, value] = line.split(",");
  N[id] = parseFloat(value);
});
const need = (id) => { if (!(id in N)) throw new Error(`number ${id} missing from numbers.csv`); return N[id]; };
const ha = (id) => Math.round(need(id)).toLocaleString("en-US");
const abs = (id) => Math.abs(Math.round(need(id))).toLocaleString("en-US");
const pct = (id) => `${Math.round(need(id) * 100)}%`;
const p2 = (id) => need(id).toFixed(2);
const int = (id) => `${Math.round(need(id))}`;
const signed = (v, d = 2) => `${v >= 0 ? "+" : "−"}${Math.abs(v).toFixed(d)}`;
const ordinal = (k) => `${k}${({ 1: "st", 2: "nd", 3: "rd" })[k] || "th"}`;
const arrow = (...ids) => ids.map(ha).join(" → ");

// walkthrough captions (read:/take:) for the backup figures
const EXPL = fs.readFileSync(path.join(ROOT, "docs/overnight/explainer_content.md"), "utf8").split("\n");
function walk(fig) {
  const i = EXPL.findIndex((l) => l.startsWith(`:::fig output/${fig}`));
  if (i < 0) return null;
  const read = (EXPL[i + 1] || "").replace(/^read:\s*/, ""), take = (EXPL[i + 2] || "").replace(/^take:\s*/, "");
  return { read: read.includes("{{") ? "" : read, take: take.includes("{{") ? "" : take };
}

// ------------------------------------------------------------------ theme + palette
const THEME = {
  name: "FZS student deck", headFontFace: "Roboto Light", bodyFontFace: "Roboto",
  colors: { dk1: "22383F", lt1: "FFFFFF", dk2: "243B42", lt2: "F2EFEA", accent1: "3C7D2C", accent2: "B9C94F",
    accent3: "A42C58", accent4: "D0692F", accent5: "2B74A6", accent6: "858D90", hlink: "2B74A6", folHlink: "6A5ACD" },
};
const X = { bg: "F2EFEA", surface: "FBFAF7", surface2: "E9E4DC", rule: "D9D2C7", rule2: "C9C1B4", ink: "22383F", ink2: "4A5B60",
  muted: "6C7B80", slate: "243B42", slate2: "2E4850", onSlate: "F3F5F2", onSlate2: "C3D0CF", lime: "B9C94F", eyebrow: "3C7D2C",
  accent: "A42C58", accentSoft: "F3E3E9", d: "2B6A8A", p: "8A5F00", orange: "D0692F", blue: "2B74A6" };
// course claim labels + "Recommendation" for advice built on our predictions
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
// fixed grid (inches): the same on every content slide
const G = { kicker: 0.42, title: 0.8, sub: 1.38, top: 1.85, bottom: 6.95, titleSize: 28 };

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
const titles = [];                                    // collected for the one-line check at the end
function slide(master, section) {
  if (!sections.has(section)) { pres.addSection({ title: section }); sections.add(section); }
  n += 1;
  return pres.addSlide({ masterName: master, sectionTitle: section });
}
// header = kicker (chapter no. + label + hairline) + one-line title + optional claim pill + optional subtitle, fixed grid
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
  if (sub) s.addText(sub, { x: M, y: G.sub, w: CW, h: 0.3, fontFace: BODY, fontSize: 14, color: dark ? X.onSlate2 : X.ink2,
    margin: 0, isTextBox: true, objectName: "subtitle" });
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
// figure slide: header + plate filling the fixed content box
async function figSlide(file, { section, no, label, title, sub, claim = "D", notes, dir = SLIDES }) {
  const s = slide("LIGHT", section);
  header(s, { no, label, title, claim, sub });
  plate(s, M, G.top, CW, G.bottom - G.top);
  const f = path.join(dir, file);
  if (fs.existsSync(f)) await fit(s, f, M + 0.06, G.top + 0.05, CW - 0.12, G.bottom - G.top - 0.1);
  else photo(s, M, G.top, CW, G.bottom - G.top, `missing ${file}`);
  s.addNotes(notes);
  return s;
}
function video(s, file, poster, label) {
  const h = G.bottom - G.top, w = h * 16 / 9, x = (W - w) / 2, y = G.top;
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

// =================================================================== the deck
(async () => {
  const anteaterLime = await icon("gi", "GiAnteater", X.lime, 512);
  const anteaterInk = await icon("gi", "GiAnteater", X.eyebrow, 512);

  // ---------------------------------------------------------------- 1 Title (hero layout, the one exception to the grid)
  {
    const s = slide("DARK", "Opening");
    header(s, { label: "Data for Good · Question 2", dark: true });
    s.addText([
      { text: "When the patrols leave,", options: { color: X.onSlate, breakLine: true } },
      { text: "mining comes back for seconds.", options: { color: X.lime } },
    ], { x: M, y: 1.2, w: 6.9, h: 2.4, fontFace: LIGHT, fontSize: 46, margin: 0, valign: "top", isTextBox: true, objectName: "title" });
    s.addText("What Operation Mercurio means for FZS's work in Tambopata.",
      { x: M, y: 3.65, w: 6.3, h: 0.6, fontFace: BODY, fontSize: 17, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    s.addShape(pres.shapes.LINE, { x: M, y: 4.95, w: 6.7, h: 0, line: { color: "FFFFFF", width: 0.75, transparency: 82 } });
    [["Feb 2019", "Operation Mercurio starts"], ["30 m", "satellite pixels since 1985"], ["6", "tests for cause"]].forEach(([v, l], i) => {
      const x = M + i * 2.27;
      if (i) vline(s, x - 0.14, 5.05, 1.0);
      s.addText(v, { x, y: 5.08, w: 2.05, h: 0.6, fontFace: LIGHT, fontSize: 28, color: X.lime, margin: 0, isTextBox: true });
      s.addText(l, { x, y: 5.68, w: 2.0, h: 0.4, fontFace: BODY, fontSize: 12, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    });
    photo(s, 7.75, 0.42, W - 7.75 - M, H - 1.0, "giant anteater", true);
    s.addNotes(
      "About 30 seconds. Good morning, we are Group Giant Anteater. [Names.]\n\n" +
      "Our title is a small pun you'll understand in a minute: when enforcement leaves, mining comes back for seconds, the way our animal comes back to the same termite mound.\n\n" +
      "We looked at one question FZS faces every year: what do you get for the money you put into enforcement? Our case is Operation Mercurio, Peru's biggest operation against illegal gold mining, which started in February 2019 in La Pampa, right next to the Tambopata reserve where FZS works. " +
      "We used 30-metre satellite maps for every year since 1985 and tested in six ways whether the operation caused what we see.");
  }

  // ---------------------------------------------------------------- 2 Anteater facts
  {
    const s = slide("LIGHT", "Opening");
    header(s, { no: "00", label: "Two facts about our animal", title: "Anteaters eat 35,000 ants a day, and never destroy a nest" });
    [["60 cm", "of tongue", "Flicks up to 150 times a minute.", "Smithsonian's National Zoo; National Geographic"],
     ["1 minute", "per mound", "Then it moves on, and comes back later.", "National Geographic"]].forEach(([big, unit, text, src], i) => {
      const x = M + i * 4.15, y = G.top, w = 3.9, h = 4.1;
      plate(s, x, y, w, h);
      s.addText(big, { x: x + 0.35, y: y + 0.35, w: w - 0.7, h: 1.0, fontFace: LIGHT, fontSize: 50, color: X.eyebrow, margin: 0, isTextBox: true });
      s.addText(unit.toUpperCase(), { x: x + 0.35, y: y + 1.4, w: w - 0.7, h: 0.3, fontFace: MED, fontSize: 12, charSpacing: 2, color: X.ink2, margin: 0, isTextBox: true });
      s.addText(text, { x: x + 0.35, y: y + 1.85, w: w - 0.7, h: 1.2, fontFace: BODY, fontSize: 18, color: X.ink, margin: 0, valign: "top", isTextBox: true });
      s.addText(src, { x: x + 0.35, y: y + h - 0.5, w: w - 0.7, h: 0.3, fontFace: BODY, fontSize: 10, color: X.muted, margin: 0, isTextBox: true });
    });
    photo(s, M + 8.3, G.top, CW - 8.3, 4.1, "anteater at a termite mound");
    s.addImage({ data: anteaterInk, x: M, y: 6.25, w: 0.55, h: 0.55 });
    s.addText("Mining in La Pampa did the same: it moved on, then came back.",
      { x: M + 0.7, y: 6.27, w: CW - 0.7, h: 0.5, fontFace: LIGHT, fontSize: 20, color: X.ink, margin: 0, valign: "middle", isTextBox: true });
    s.addNotes(
      "About 30 seconds. Two facts about the giant anteater.\n\n" +
      "One: its tongue is about 60 centimetres long and flicks in and out up to 150 times a minute. That's how it eats up to 35,000 ants and termites a day (Smithsonian's National Zoo; National Geographic).\n\n" +
      "Two, and this is the one to remember: it spends only about a minute at each mound, because the ants fight back. It never destroys the nest. It moves on and comes back later to feed again (National Geographic).\n\n" +
      "Hold on to that habit. It is a good description of what we found for gold mining in La Pampa.");
  }

  // ---------------------------------------------------------------- 3 Question + results
  {
    const s = slide("DARK", "Question");
    header(s, { label: "The question", title: "What happens when an enforcement operation ends?", dark: true,
      sub: "Operation Mercurio, La Pampa, Madre de Dios · from February 2019" });
    s.addShape(pres.shapes.LINE, { x: M, y: 2.35, w: CW, h: 0, line: { color: "FFFFFF", width: 0.75, transparency: 82 } });
    s.addText("WHAT WE FOUND", { x: M, y: 2.55, w: 4, h: 0.3, fontFace: MED, fontSize: 12, charSpacing: 2.2, color: X.lime, margin: 0, isTextBox: true });
    [["1 · It fell", `${ha("mean_add_tambopata_2016_18")} → ${ha("mean_add_tambopata_2019_21")}`, "ha/yr net new mining, Tambopata buffer zone"],
     ["2 · It moved", `${pct("t1_road_north_share_2016_18")} → ${pct("t1_road_north_share_2019_21")}`, "of new mining near La Pampa north of the road"],
     ["3 · It came back", ha("mean_add_tambopata_2022_25"), "ha/yr in 2022–25, much of it on old pits"]].forEach(([eb, v, l], i) => {
      const x = M + i * 4.13;
      if (i) vline(s, x - 0.2, 3.15, 2.6);
      stat(s, x, 3.15, 3.75, { eyebrow: eb, value: v, label: l, valueSize: 48 });
    });
    s.addText("All three: description, 2016–18 vs 2019–21 vs 2022–25.", { x: M, y: 6.3, w: CW, h: 0.3, fontFace: BODY, fontSize: 12, color: X.onSlate2, margin: 0, isTextBox: true });
    s.addNotes(
      "About 45 seconds. FZS supports SERNANP's operations against illegal mining around Tambopata. Operations are expensive and they end. So the practical question is: what should FZS expect in the targeted area, and around it, once an operation is over?\n\n" +
      "There are three possibilities. Mining stops for good: deterrence. It moves next door: displacement. Or it waits and comes back: delay. Inside the target alone these look the same, which is why we compare areas.\n\n" +
      "The answer up front, all three are descriptions, not yet causes. One: net new mining in the buffer zone fell from about 1,640 to about 160 hectares a year. Two: new mining moved north of the highway, from about a quarter to two thirds. Three: it came back, to over 1,800 hectares a year in 2022 to 2025.");
  }

  // ---------------------------------------------------------------- 4–8 Where we are (flippable map steps, fixed positions)
  const steps = [
    ["Protected areas", "Tambopata reserve, its buffer zone, Amarakaeri. Pink: native land."],
    ["The Interoceanic Highway", "One road splits the buffer zone from the land to the north."],
    ["Rivers and old mining", "Alluvial gold sits in floodplains. Grey: mined by 2018."],
    ["Where mining can be legal", "D.L. 1100 corridor, north of the road. South of it: a crime."],
    ["The target", "La Pampa, target of Operation Mercurio from Feb 2019."],
  ];
  const stepNotes = [
    "This is Madre de Dios, in the south-east of the Peruvian Amazon. In green, the protected areas: Tambopata National Reserve in the south, the core area FZS helps protect, with its buffer zone around it. West of it the Amarakaeri buffer zone, east the Bahuaja-Sonene park. Pink outlines are native communities.",
    "The white line is the Interoceanic Highway, paved road from Brazil to the Pacific. It runs right along the edge of the buffer zone. Remember this road: it becomes the border in our story.",
    "The blue lines are rivers. Gold here is alluvial: it sits in the sediments of river floodplains, so mining follows the rivers. The grey patches are land already mapped as mining by 2018: that is La Pampa, Peru's largest illegal mining area.",
    "The blue area is the mining corridor created by decree in 2012, D.L. 1100. Inside it small-scale mining can be permitted. South of the road, in the buffer zone, the same work is a crime. Important for later: legality is about location. The satellite maps themselves cannot tell legal from illegal mining.",
    "And this orange box is La Pampa, the target of Operation Mercurio from February 2019: over a thousand police and soldiers, with rotating commanders against corruption. The box is our boundary; there is no official one. The blue box just across the road is the part of the legal corridor directly opposite. Watch these two boxes.",
  ];
  for (let k = 0; k < steps.length; k++) {
    const s = slide("LIGHT", "Context");
    header(s, { no: "01", label: "Where we are", title: "La Pampa: one road away from land where mining is legal", claim: "D" });
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
    s.addNotes(`Step ${k + 1} of 5, about 12 seconds. ${stepNotes[k]}`);
  }

  // ---------------------------------------------------------------- 9 Animation
  {
    const s = slide("LIGHT", "Context");
    header(s, { no: "02", label: "2008–2025 in one minute", title: "Where land was mined for the first time, 2008–2025", claim: "D" });
    video(s, "MiningTimeline.mp4", "stills/timeline_2020.png", "mining timeline animation");
    s.addNotes(
      "About 75 seconds. Click to play. Each year, yellow pixels are land mapped as mining for the first time; they then fade to grey.\n\n" +
      "Before 2019 the yellow concentrates in La Pampa, south of the road. Watch the Mercurio pin in February 2019. In 2019 itself La Pampa is still busy; clearing went on that year. From 2020 La Pampa goes quiet and the yellow appears north of the road, in the corridor box. 2020 is also COVID: police and soldiers were pulled away.\n\n" +
      "From 2022 new mining returns in La Pampa, much of it on old, grey pits. 2023 brings a state of emergency; in 2025 the navy leaves its river posts.\n\n" +
      "The video ends with the caveat we'll repeat: satellites can't see river dredges or mercury.");
  }

  // ---------------------------------------------------------------- What happened: figure slides (deck owns short titles)
  const what = [
    ["slide_01_tambopata_net.png", "03", "What happened in the target",
      `Net new mining in Tambopata fell ${pct("sl_tam_net_fall_share")}, then came back`,
      "Tambopata buffer zone · net new mining, ha per year · bars = period averages",
      "About 45 seconds. This is the course's measure: the mapped mining area this year minus last year, in the Tambopata buffer zone.\n\n" +
      `Before the operation, 2016 to 2018, it added about ${ha("mean_add_tambopata_2016_18")} hectares a year. In 2019 to 2021 only about ${ha("mean_add_tambopata_2019_21")}: a 90 percent drop. In 2022 to 2025 it was back at about ${ha("mean_add_tambopata_2022_25")}.\n\n` +
      "Two things to note. The timing: the fall shows from 2020, the first COVID year, not straight away in 2019. And 2023 spikes everywhere in the region, which may partly be a map artefact, so don't read too much into that single year."],
    ["slide_02a_zones.png", "04", "Where it went", "La Pampa: first-time mining halved in 2019–21",
      "Land mined for the first time, ha per year · orange = La Pampa, grey = rest of Madre de Dios",
      "About 20 seconds. From here we switch to a sharper measure from the pixel maps: land mined for the very first time. Net additions can hide miners returning to old pits; this measure can't.\n\n" +
      `In La Pampa, first-time mining went from about ${ha("sl_new_lapampa_2016_18")} to ${ha("sl_new_lapampa_2019_21")} hectares a year: it halved, not the 90 percent of the net measure. The grey is everything else in Madre de Dios. Next click: we colour it in.`],
    ["slide_02b_zones.png", "04", "Where it went", "The region kept growing, mostly in the legal corridor",
      `All Madre de Dios, first-time mining: ${arrow("v2_new_total_2016_18", "v2_new_total_2019_21", "v2_new_total_2022_25")} ha/yr`,
      "About 40 seconds. Same bars, now coloured by zone. Blue is the legal mining corridor; dark blue at the bottom is the part directly across the road from La Pampa.\n\n" +
      `The department as a whole did not fall at all: ${ha("v2_new_total_2016_18")} hectares a year before, ${ha("v2_new_total_2019_21")} during, ${ha("v2_new_total_2022_25")} after. The legal corridor's share went from about half to almost three quarters.\n\n` +
      "Careful: the corridor grew by far more than La Pampa lost. So this is not just the same miners moving; new entrants and the gold price play a part. MAAP finds the same: 74 percent of mining deforestation in 2021 to 2024 was inside the corridor."],
    ["slide_03_road_share.png", "05", "Across the road", `New mining near La Pampa moved north of the road: ${pct("t1_road_north_share_2016_18")} → ${pct("t1_road_north_share_2019_21")}`,
      "Share of first-time mining north of the Interoceanic Highway, La Pampa's longitudes",
      "About 40 seconds. Now zoom in to La Pampa's stretch of the highway. The line is the share of new mining north of the road, on the legal side.\n\n" +
      `Before the operation, about ${pct("t1_road_north_share_2016_18")}. During, ${pct("t1_road_north_share_2019_21")}. No other start year gives a bigger jump north.\n\n` +
      `Honest history: the road was crossed before. In 2008, during the Guacamayo boom, ${pct("t1_road_north_share_2008")} of new mining was north of it. Independent evidence agrees: Dethier and colleagues (2023) found that after Mercurio pond colour, a sign of active mining, faded across La Pampa except in its northwest, where it rose 43 percent. We can't show it was the same people who moved.`],
    ["slide_03b_road_bands.png", "05", "Across the road", "In 2019–21 new mining piled up just north of the road",
      "First-time mining per 1-km strip, ha/yr · blue = north (legal side), orange = south (buffer zone)",
      "About 30 seconds. The same story as a picture. Each bar is a one-kilometre strip parallel to the highway; the thick line is the road.\n\n" +
      "Before the operation the mass sits south, in the buffer zone. In 2019 to 2021 it sits in the first few kilometres north of the road. By 2022 to 2025 it has spread deeper into the corridor, and the south has partly come back."],
    ["slide_04_context.png", "06", "Why it came back", `Money faded after 2019, while gold rose ${need("sl_gold_ratio_2025_2018").toFixed(1)}-fold`,
      "Enforcement spending, Madre de Dios · gold price · La Pampa first-time mining",
      "About 45 seconds. Why did it come back? Three things line up.\n\n" +
      "Left: the anti-illegal-mining budget booked in Madre de Dios jumped in 2019 and then shrank year after year; it's a lower bound because national units book in Lima. Middle: the gold price, up 2.7-fold from 2018 to 2025. Right: La Pampa's first-time mining, which came back as the money faded and the price rose.\n\n" +
      `And La Pampa had not run out of gold: by 2018 only ${pct("gold_broad_lapampasector_depleted_2018")} of its gold-bearing land had been mined.\n\n` +
      `If asked about a correlation: the yearly gap and spending correlate at r = ${p2("ctx_dose_corr")} over 11 years. That is weak, and money also follows mining, so it is not a causal test.`],
    ["slide_05_old_pits.png", "07", "How it came back", `In 2023, ${pct("sl_lp_oldpit_share_2023")} of new mining in La Pampa was on old pits`,
      "La Pampa, ha per year · dark = new land · light = old pits mined again",
      "About 30 seconds. How it came back matters for monitoring. Dark orange is land mined for the first time; light orange is old pits that were abandoned and mined again.\n\n" +
      "In 2023, two thirds of La Pampa's new mining was on old pits. Forest-loss alerts never see this, because there is no forest left to lose. MAAP #193 reports the same return to degraded land. Small old-pit counts include some map flicker, so trust the 2023 jump, not small changes."],
    ["slide_06_reserve.png", "08", "Inside the reserve", `In 2025, mining inside the reserve jumped by ${ha("anp_tam_nr_addition_2025")} ha`,
      "Tambopata National Reserve · net new mining, ha per year",
      "About 40 seconds. This is FZS's core area. The course data stop at the buffer zone, so we downloaded the protected-area statistics ourselves.\n\n" +
      `Inside Tambopata National Reserve, mining stayed small for years. In 2025 it jumped by ${ha("anp_tam_nr_addition_2025")} hectares, to ${ha("anp_level_tam_nr_2025")} in total. MAAP #241 reports about 500 hectares from late 2025 to February 2026, after the navy left its river posts on the Malinowski for lack of funds.\n\n` +
      "The 2017 bar is partly a map reclassification, not real mining."],
  ];
  for (const [file, no, label, title, sub, notes] of what) await figSlide(file, { section: "What happened", no, label, title, sub, notes });

  // ---------------------------------------------------------------- Is it causal? 1: six methods
  {
    const s = slide("LIGHT", "Is it causal?");
    header(s, { no: "09", label: "Is it causal?", title: "We tried six methods. Two held up", claim: "C",
      sub: "Each builds a stand-in for Tambopata without Mercurio" });
    const methods = [
      ["Difference-in-differences", "vs 14 other Peruvian buffer zones", true, "Held up · in hectares"],
      ["Synthetic control", "a weighted copy of Tambopata", false, "No good copy"],
      ["Rule-based twins", "look-alike areas in Brazil", false, "Different trends before 2019"],
      ["Spatial discontinuity", "just north vs just south of the road", false, `Borderline · p = ${p2("rd_road_did_p")}`],
      ["Matching, 7 ways", "areas picked by algorithm", false, "Can't beat chance"],
      ["Synthetic DiD", "weighted zones and years", true, "Held up · in hectares"],
    ];
    const icons = ["LuGitCompare", "LuLayers", "LuSearch", "LuSplit", "LuCrosshair", "LuSigma"];
    const gap = 0.25, cw = (CW - 2 * gap) / 3, ch = (G.bottom - G.top - gap) / 2;
    for (let i = 0; i < methods.length; i++) {
      const [name, how, ok, verdict] = methods[i];
      const x = M + (i % 3) * (cw + gap), y = G.top + Math.floor(i / 3) * (ch + gap);
      s.addShape(pres.shapes.RECTANGLE, { x, y, w: cw, h: ch, fill: { color: ok ? "EAF2E4" : X.surface }, line: { color: ok ? X.eyebrow : X.rule, width: ok ? 1.5 : 0.75 } });
      s.addImage({ data: await icon("lu", icons[i], ok ? X.eyebrow : X.muted), x: x + 0.3, y: y + 0.3, w: 0.5, h: 0.5 });
      s.addText(name, { x: x + 0.3, y: y + 0.95, w: cw - 0.6, h: 0.45, fontFace: MED, fontSize: 19, color: ok ? X.ink : X.ink2, margin: 0, isTextBox: true });
      s.addText(how, { x: x + 0.3, y: y + 1.4, w: cw - 0.6, h: 0.4, fontFace: BODY, fontSize: 14, color: X.ink2, margin: 0, isTextBox: true });
      s.addText(verdict.toUpperCase(), { x: x + 0.3, y: y + ch - 0.5, w: cw - 0.6, h: 0.3, fontFace: MED, fontSize: 11, charSpacing: 1.5,
        color: ok ? X.eyebrow : X.muted, margin: 0, isTextBox: true });
    }
    s.addNotes(
      "About 45 seconds. Only one area was targeted, so to ask 'did Mercurio cause the fall?' we need a stand-in: what would Tambopata have done without it? We built that stand-in six ways.\n\n" +
      "Two held up: difference-in-differences against the other 14 Peruvian buffer zones, and synthetic difference-in-differences, which weights zones and years to match Tambopata's past. Both find a fall far bigger than chance, but only in hectares.\n\n" +
      "The other four are weaker. A synthetic copy can't match a zone this big. The Brazilian twins grew at a different pace before 2019, so they fail the basic test. The road comparison is borderline. And seven matching methods all find Tambopata slower, but never beyond chance. Details are in the backup.");
  }
  // ---------------------------------------------------------------- Is it causal? 2: the claim
  {
    const s = slide("DARK", "Is it causal?");
    header(s, { no: "10", label: "The causal claim", title: "What we can say about cause", claim: "C", dark: true });
    s.addText([
      { text: "If the other zones show what Tambopata would have done, ", options: { color: X.onSlate2, italic: true } },
      { text: "Mercurio and the operations after it cut net new mining by ", options: { color: X.onSlate } },
      { text: `${abs("sdid_sc_ha_during")}\u00a0to\u00a0${abs("model_m3_during")}\u00a0ha a year`, options: { color: X.lime } },
      { text: " in 2019–21.", options: { color: X.onSlate } },
    ], { x: M, y: G.top, w: 11.8, h: 2.0, fontFace: LIGHT, fontSize: 30, margin: 0, valign: "top", isTextBox: true });
    s.addShape(pres.shapes.LINE, { x: M, y: 4.15, w: CW, h: 0, line: { color: "FFFFFF", width: 0.75, transparency: 82 } });
    [["Hectares only", `Largest fall of ${int("model_m1_n")} zones; for its size, ${ordinal(Math.round(need("model_m4_rank")))} of ${int("model_m4_n")}.`],
     [`p = ${p2("model_m1_ri_p")}`, `The best possible with one target among ${int("model_m1_n")}.`],
     ["COVID overlaps", "Nothing fell in 2019. The fall came in 2020–21."]].forEach(([v, l], i) => {
      const x = M + i * 4.13;
      if (i) vline(s, x - 0.2, 4.4, 1.9);
      s.addText(v, { x, y: 4.4, w: 3.8, h: 0.7, fontFace: LIGHT, fontSize: 30, color: X.lime, margin: 0, isTextBox: true });
      s.addText(l, { x, y: 5.15, w: 3.7, h: 1.0, fontFace: BODY, fontSize: 15, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    });
    s.addNotes(
      "About 40 seconds. This is the one causal sentence we are willing to make, and it has an 'if'. If the other buffer zones show what Tambopata would have done without the operation, then Mercurio and the operations that followed cut net new mining by roughly 400 to 1,900 hectares a year in 2019 to 2021. The low end comes from the synthetic control, the high end from the model with each zone's own trend.\n\n" +
      "Three limits. It holds in hectares, not relative to the zone's size: scaled, Tambopata is third of seven, nothing special. With one target among fifteen zones, 0.07 is the smallest p-value this test can produce. And the fall coincides with COVID: nothing fell in 2019 itself.");
  }
  await figSlide("slide_07_causal.png", { section: "Is it causal?", no: "10", label: "The evidence", claim: "C",
    title: "In hectares the fall stands out. For its size, it doesn't",
    sub: "Orange = Tambopata's real 2019–21 change · grey = other zones given a fake operation",
    notes: "About 40 seconds. How the test works: we pretend each of the other zones was the one targeted, and compute the same number. If Mercurio mattered, Tambopata's real change should stand out from all the fake ones.\n\n" +
      `Top row, in hectares: Tambopata, the orange dot, is far to the left of every grey dot. First of ${int("model_m1_n")}.\n\n` +
      `Bottom row, the same thing scaled to each zone's normal year: Tambopata sits among the others, ${ordinal(Math.round(need("model_m4_rank")))} of ${int("model_m4_n")}. A big zone falls a lot in hectares just by being big. That is why our claim is in hectares only.` });

  // ---------------------------------------------------------------- Limits
  {
    const s = slide("LIGHT", "Limits");
    header(s, { no: "11", label: "Limits", title: "Most biases make the fall look bigger", claim: "D" });
    s.addText("SATELLITES CAN'T SEE", { x: M, y: G.top, w: 5.6, h: 0.3, fontFace: MED, fontSize: 11, charSpacing: 2, color: X.accent, margin: 0, isTextBox: true });
    const cant = [["LuShip", "River dredges", "148 → 598 in La Pampa, 2021–23 (MAAP #193)"], ["LuDroplets", "Mercury", "in rivers and fish"],
      ["LuUsers", "People", "hectares, not miners"], ["LuScale", "Legality", "legal and illegal look alike"]];
    const tw = 2.72, th = 2.2, ty = G.top + 0.4;
    for (let i = 0; i < cant.length; i++) {
      const [ic, head, txt] = cant[i], x = M + (i % 2) * (tw + 0.16), y = ty + Math.floor(i / 2) * (th + 0.16);
      plate(s, x, y, tw, th);
      s.addImage({ data: await icon("lu", ic, X.accent), x: x + 0.25, y: y + 0.25, w: 0.55, h: 0.55 });
      s.addText(head, { x: x + 0.25, y: y + 1.0, w: tw - 0.45, h: 0.4, fontFace: MED, fontSize: 18, color: X.ink, margin: 0, isTextBox: true });
      s.addText(txt, { x: x + 0.25, y: y + 1.42, w: tw - 0.45, h: 0.65, fontFace: BODY, fontSize: 13, color: X.ink2, margin: 0, valign: "top", isTextBox: true });
    }
    const rx = M + 2 * tw + 0.16 + 0.55, rw = W - M - rx, cx = rx + rw * 0.5;
    s.addText("EACH BIAS MAKES THE 2019–21 FALL LOOK…", { x: rx, y: G.top, w: rw, h: 0.3, fontFace: MED, fontSize: 11, charSpacing: 2, color: X.d, margin: 0, isTextBox: true });
    s.addText("smaller", { x: rx, y: G.top + 0.42, w: rw / 2 - 0.12, h: 0.3, fontFace: MED, fontSize: 14, color: X.blue, align: "right", margin: 0, isTextBox: true });
    s.addText("bigger", { x: cx + 0.12, y: G.top + 0.42, w: rw / 2 - 0.12, h: 0.3, fontFace: MED, fontSize: 14, color: X.orange, margin: 0, isTextBox: true });
    const biases = [["Picked at its peak", +1], ["Hectares, not people", +1], ["Miners moved into comparison zones", +1], ["Big zones fall more in hectares", +1],
      ["Comparison zones had operations too", -1], ["Yearly maps blur Feb 2019", -1]];
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
      "About 40 seconds. Every brief must say what satellites can't see. On the left: river dredges, which MAAP counted rising from 148 to 598 in La Pampa between 2021 and 2023; mercury in rivers and fish; people, because we count hectares, not miners; and legality, because legal and illegal mining look the same from space.\n\n" +
      "More useful for FZS is the direction of each bias, on the right. La Pampa was targeted at its record peak, so part of the fall may be a return to normal. Hectares understate activity on old pits and rivers. Miners moving into comparison zones widen the gap. A big zone falls more in hectares. All of these make the fall look bigger. Two push the other way: the comparison zones had their own operations, and yearly maps blur a February start.\n\n" +
      "So: read our fall as an upper bound, and the return as a lower bound.");
  }

  // ---------------------------------------------------------------- For FZS (recommendations)
  {
    const s = slide("DARK", "For FZS");
    header(s, { no: "12", label: "For FZS", title: "Plan for the months after the operation ends", claim: "R", dark: true });
    const recs = [
      ["LuCalendarClock", "Stay after the sweep", "2019–21", "the only years with a fall. Fund lasting presence, not one-off raids."],
      ["LuShieldCheck", "Guard the reserve's edge and river", pct("rd_reserve_inside_share_1km"), "of new mining inside the reserve is within 1 km of its edge."],
      ["LuBinoculars", "Watch the legal side and old pits", arrow("v2_new_corridoracrosstheroa_2016_18", "v2_new_corridoracrosstheroa_2019_21"), "ha/yr of new mining just across the road."],
    ];
    for (let i = 0; i < recs.length; i++) {
      const [ic, head, v, l] = recs[i], x = M + i * 4.13, y = G.top + 0.25;
      if (i) vline(s, x - 0.2, y, 4.5);
      s.addShape(pres.shapes.OVAL, { x, y, w: 0.8, h: 0.8, fill: { color: X.slate2 }, line: { color: X.lime, width: 1 } });
      s.addImage({ data: await icon("lu", ic, X.lime), x: x + 0.18, y: y + 0.18, w: 0.44, h: 0.44 });
      s.addText(head, { x, y: y + 1.05, w: 3.8, h: 0.8, fontFace: MED, fontSize: 20, color: X.onSlate, margin: 0, valign: "top", isTextBox: true });
      s.addText(v, { x, y: y + 1.95, w: 3.8, h: 0.8, fontFace: LIGHT, fontSize: 40, color: X.lime, margin: 0, isTextBox: true });
      s.addText(l, { x, y: y + 2.8, w: 3.6, h: 1.0, fontFace: BODY, fontSize: 15, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    }
    s.addNotes(
      "About 60 seconds. Three recommendations. They build on one case, so treat them as informed expectations, not proven rules.\n\n" +
      "One, stay after the sweep. The fall lasted only through 2021, and the 2025 incursion into the reserve came right after the navy left its river posts. A permanent presence protects more than another one-off operation.\n\n" +
      `Two, guard the reserve's edge and its river. ${pct("rd_reserve_inside_share_1km")} of all first-time mining inside the reserve lies within one kilometre of its edge. Staffed posts on the Malinowski river are a direct shield.\n\n` +
      "Three, watch the legal side of the boundary and the old pits. New mining just across the road jumped from about 70 to over 460 hectares a year. Old pits don't show up in forest-loss alerts. And push for proof of gold origin in the corridor; Brazil's 2023 reforms are a model.\n\n" +
      "What would let us say more: dated patrol records per zone from SERNANP or FZS, dredge counts, and mercury sampling.");
  }

  // ---------------------------------------------------------------- Thanks (hero layout)
  {
    const s = slide("DARK", "Closing");
    header(s, { label: "Thank you", dark: true });
    s.addText([
      { text: "Questions?", options: { color: X.onSlate, breakLine: true } },
      { text: "Like the anteater, we'll come back for more.", options: { color: X.lime, fontSize: 22 } },
    ], { x: M, y: 1.2, w: 6.8, h: 2.4, fontFace: LIGHT, fontSize: 54, margin: 0, valign: "top", isTextBox: true });
    s.addImage({ data: anteaterLime, x: M, y: 3.9, w: 1.3, h: 1.3 });
    photo(s, 7.75, 0.42, W - 7.75 - M, H - 1.0, "rangers / Tambopata river", true);
    s.addNotes("Thank you. Happy to take questions. Backup slides: methods table, range of estimates, placebo tests, timing, depth, legality, declared gold, money, risk map, Brazil, and the map as one video.");
  }

  // ---------------------------------------------------------------- Backup
  {
    const s = slide("DARK", "Backup");
    header(s, { label: "Backup", title: "For questions", dark: true,
      sub: "Methods · estimates · placebos · timing · depth · legality · declared gold · money · risk map · Brazil · map video" });
  }
  {
    const s = slide("LIGHT", "Backup");
    header(s, { label: "Backup · Six methods", title: "Six methods in detail", claim: "C" });
    const rows = [
      ["METHOD", "COMPARES TAMBOPATA WITH", "RESULT", "VERDICT"],
      ["1  Difference-in-differences", "14 Peruvian buffer zones", `${ha("model_m1_during")} to ${ha("model_m3_during")} ha/yr; rank 1 of ${int("model_m1_n")}`, "Held up"],
      ["2  Synthetic control", "Weighted mix of zones", `${ha("sdid_sc_ha_during")} ha/yr; no pre-2019 fit`, "Weak"],
      ["3  Rule-based twins", "Amanã and Tapajós (Brazil)", `${pct("top3_median_ratio")} of the twins' pace; different pre-trends`, "Weak"],
      ["4  Spatial discontinuity", "Either side of the road", `+${need("rd_road_did").toFixed(1)} pts north (p = ${p2("rd_road_did_p")})`, "Borderline"],
      ["5  Matching (7 methods)", "Areas picked by algorithm", `All slower; placebo p ${p2("psm_p_min")}–${p2("psm_p_max")}`, "Can't decide"],
      ["6  Synthetic DiD", "Weighted, trend-matched zones", `${ha("sdid_sdid_ha_during")} ha/yr; scaled rank ${int("sdid_sdid_scaled_during_rank")} of ${int("sdid_sdid_scaled_during_n")}`, "Held up"],
    ];
    const vc = { "Held up": X.eyebrow, "Weak": X.p, "Borderline": X.p, "Can't decide": X.muted };
    s.addTable(rows.map((r, i) => r.map((c, j) => ({ text: c, options: {
      fontFace: i === 0 || j === 3 ? MED : BODY, fontSize: i === 0 ? 10.5 : 14, charSpacing: i === 0 ? 1.5 : 0,
      color: i === 0 ? X.ink2 : (j === 3 ? vc[c] : X.ink), fill: { color: i === 0 ? X.surface2 : X.surface }, valign: "middle", margin: [5, 10, 5, 10] } }))),
      { x: M, y: G.top, w: CW, colW: [3.2, 3.3, 4.2, 1.53], rowH: 0.66, border: { type: "solid", color: X.rule, pt: 0.75 } });
    s.addNotes("Only the zone-level designs clear their placebo floor, and only in hectares. Synthetic control can't fit Tambopata's size before 2019; the Brazilian twins fail the pre-trend test (p < 0.001); the road discontinuity is borderline across bandwidths; matching never beats chance and has no common support.");
  }
  await figSlide("slide_07b_estimates.png", { section: "Backup", label: "Backup · Estimates", title: "Five estimates, one conditional range", claim: "C",
    sub: "Change in net new mining, Tambopata buffer zone, 2019–21, ha/yr",
    notes: "The conditional range runs from the synthetic control (low end) to the model with each zone's own trend (high end). All estimates are conditional on the comparison zones being a fair stand-in." });
  const backups = [
    ["fig_placebo_explainer.png", "Placebo tests", "How a fake test shows if the real result stands out", "D"],
    ["fig_v2_glad_quarterly.png", "Timing", "Clearing in La Pampa went on through 2019", "D"],
    ["fig_v2_depth.png", "Depth", "New mining hugged the road, then spread deeper", "D"],
    ["fig_v2_legality.png", "Legality", "Presumed-illegal new mining fell; grey zones grew", "D"],
    ["fig_peru_gold_definition.png", "Declared gold", "The official gold drop is a definition change", "D"],
    ["fig_v2_economics.png", "Money", "Gold and its damage dwarf enforcement money", "P"],
    ["fig_v2_risk_map.png", "Risk map", "Next new mining is likely next to old mining", "P"],
  ];
  for (const [file, label, title, claim] of backups) {
    const w = walk(file) || { read: "", take: "" };
    await figSlide(file, { section: "Backup", label: `Backup · ${label}`, title, claim, dir: OUT,
      notes: `${w.read} ${w.take}${claim === "P" ? " Informed expectation from cited parameters, not a finding." : ""}` });
  }
  await figSlide("slide_08_brazil_twins.png", { section: "Backup", label: "Backup · Brazil twins", title: "The Brazilian twins fail the pre-trend test",
    sub: "Mining area before 2019 (index 2018 = 100) · new mining 2019–21, % of 2018 area",
    notes: "Rule-based twins (Ruby's design): Amanã and Tapajós. Tambopata grew faster than both before 2019 (pre-trend p < 0.001), so they can't show what Tambopata would have done. Description only." });
  {
    const s = slide("LIGHT", "Backup");
    header(s, { label: "Backup · Brazil", title: "Brazil: falls, but not after each operation", claim: "D" });
    [["Yanomami, first-time mining", arrow("brv2_yan_new_2019_22", "brv2_yan_new_2023_25"), "ha/yr, 2019–22 → 2023–25"],
     [`Staggered DiD, ${int("brv2_n_units")} territories`, signed(need("brv2_did2s_treat")), `log points, p = ${p2("brv2_did2s_treat_p")}: wrong sign`],
     ["National reforms, Jan 2023", "All at once", "new rules on gold sales hit every territory"]].forEach(([eb, v, l], i) => {
      const x = M + i * 4.13;
      if (i) vline(s, x - 0.2, G.top, 2.4, false);
      stat(s, x, G.top, 3.75, { eyebrow: eb, value: v, label: l, dark: false, valueSize: 40 });
    });
    plate(s, M, 4.75, CW, 1.2);
    s.addText("Consistent with 'enforcement plus gold tracing goes with less mining'. Our test can't confirm it.",
      { x: M + 0.25, y: 4.75, w: CW - 0.5, h: 1.2, fontFace: LIGHT, fontSize: 20, color: X.ink, margin: 0, valign: "middle", isTextBox: true });
    s.addNotes("Only if asked. MapBiomas Brazil Collection 11, same pixel method as Peru. A national change in January 2023 (new government, end of the gold 'good faith' rule, electronic gold invoices) hit all territories at once, which a territory-level design can't separate.");
  }
  {
    const s = slide("LIGHT", "Backup");
    header(s, { label: "Backup · Map video", title: "The five map layers as one video", claim: "D" });
    video(s, "MapLayers.mp4", "stills/map_step5.png", "map layers animation");
    s.addNotes("The same five layers as the 'Where we are' slides, as one 26-second video.");
  }

  // one-line check: every title must fit one line at 28 pt (Roboto Light, ~0.0066 in per char per pt, measured)
  for (const [k, t] of titles) {
    const width = t.length * 0.0066 * G.titleSize;
    if (width > CW) console.warn(`slide ${k}: title may wrap (${t.length} chars): ${t}`);
  }
  const file = path.join(__dirname, "GroupAnteater_FZS_talk.pptx");
  await pres.writeFile({ fileName: file });
  const { applyTheme } = require("./apply_theme.js");     // copied from the pptx skill: writes THEME into the theme part
  await applyTheme(file, THEME);
  console.log(`Wrote ${file} (${n} slides)`);
})();
