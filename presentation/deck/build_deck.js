// Build the FZS talk deck (storyline v3.1, docs/presentation/STORYLINE.md):  cd presentation/deck && npm install && node build_deck.js
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
    objects: [{ text: { text: FOOT, options: { x: M, y: H - 0.38, w: 9, h: 0.24, fontFace: MED, fontSize: 9, color: fg, charSpacing: 1.5, margin: 0 } } },
      // FZS logo (prepared for FZS, who want to use the deck internally); on dark slides on a white plate
      ...(name === "DARK" ? [{ rect: { x: W - M - 1.24, y: H - 0.6, w: 0.5, h: 0.5, fill: { color: "FFFFFF" }, rectRadius: 0.04 } }] : []),
      { image: { x: W - M - 1.2, y: H - 0.56, w: 0.44, h: 0.42, path: path.join(__dirname, "assets", "fzs_logo.png") } }],
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
// no placeholder boxes: a missing image stops the build
function photo(s, x, y, w, h, label) { throw new Error(`missing image: ${label}`); }
// an image cropped (sharp) to exactly fill a box; region = [left, top, width] as shares of the source image
async function cropFill(s, file, x, y, w, h, [l, t, cw], alt) {
  const m = await sharp(file).metadata();
  const width = Math.round(m.width * cw), height = Math.min(m.height - Math.round(m.height * t), Math.round(width * h / w));
  const buf = await sharp(file).extract({ left: Math.round(m.width * l), top: Math.round(m.height * t), width, height }).jpeg({ quality: 88 }).toBuffer();
  s.addImage({ data: "image/jpeg;base64," + buf.toString("base64"), x, y, w, h, altText: alt });
}
const TEAM = "Group Giant Anteater · Ruby Ann Grambauer, Sebastian Schmid, Laurens van der Lely, Omkar Mate, Dhruv Chaudhari";
const ASSETS = path.join(__dirname, "assets");
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
  const ordinal = (k) => `${k}${({ 1: "st", 2: "nd", 3: "rd" })[k] || "th"}`;
  const scaledRank = `${ordinal(Math.round(need("sl_rank_scaled_lo")))}–${ordinal(Math.round(need("sl_rank_scaled_hi")))}`;
  const stopShare = `${pct("tambopata_bz_stopped_share_of_fall_min")}–${pct("tambopata_bz_stopped_share_of_fall_max")}`;

  // ---------------------------------------------------------------- 1 Title (hero layout, as in the 2026-10-13 deck)
  {
    const s = slide("DARK", "Opening");
    header(s, { label: "When the patrols leave · Data for Good · Question 2", dark: true });
    s.addText([
      { text: "A pause, not an end:", options: { color: X.onSlate, breakLine: true } },
      { text: "mining after Operation Mercurio", options: { color: X.lime } },
    ], { x: M, y: 1.2, w: 6.9, h: 2.4, fontFace: LIGHT, fontSize: 46, margin: 0, valign: "top", isTextBox: true, objectName: "title" });
    s.addText("What it means for FZS's work in Tambopata. Prepared for the Frankfurt Zoological Society.",
      { x: M, y: 3.65, w: 6.3, h: 0.6, fontFace: BODY, fontSize: 17, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    s.addShape(pres.shapes.LINE, { x: M, y: 4.95, w: 6.7, h: 0, line: { color: "FFFFFF", width: 0.75, transparency: 82 } });
    [["Feb 2019", "Operation Mercurio starts"], ["30 m", "satellite pixels since 1985"], ["6", "ways we tested for cause"]].forEach(([v, l], i) => {
      const x = M + i * 2.27;
      if (i) vline(s, x - 0.14, 5.05, 1.0);
      s.addText(v, { x, y: 5.08, w: 2.05, h: 0.6, fontFace: LIGHT, fontSize: 28, color: X.lime, margin: 0, isTextBox: true });
      s.addText(l, { x, y: 5.68, w: 2.0, h: 0.4, fontFace: BODY, fontSize: 12, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    });
    await cropFill(s, path.join(ASSETS, "cover_mercurio_2019_afp.jpg"), 7.75, 0.42, W - 7.75 - M, H - 1.32, [0.43, 0, 0.57],
      "Peruvian soldier at an illegal miners' camp in La Pampa during Operation Mercurio, 19 February 2019");
    s.addText("Photo: Operation Mercurio, La Pampa, 19 Feb 2019. Cris Bouroncle / AFP via Getty Images (NBC News, 20 Feb 2019).",
      { x: 7.75, y: H - 0.86, w: W - 7.75 - M, h: 0.3, fontFace: BODY, fontSize: 8, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    s.addText(TEAM, { x: M, y: 4.35, w: 6.7, h: 0.45, fontFace: BODY, fontSize: 12, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    s.addNotes(
      "About 20 seconds. Good morning, we are Group Giant Anteater. We are Ruby Ann Grambauer, Sebastian Schmid, Laurens van der Lely, Omkar Mate and Dhruv Chaudhari.\n\n" +
      "Our title is our main finding: Operation Mercurio bought a pause, not an end. The photo shows La Pampa on 19 February 2019, the first days of Operation Mercurio: soldiers at an illegal miners' camp.\n\n" +
      "Our case is Operation Mercurio, Peru's biggest operation against illegal gold mining, which started in February 2019 in La Pampa, right next to the Tambopata reserve where FZS works. " +
      "We used 30-metre satellite maps for every year since 1985 and tried six ways to test whether the operation caused what we see.");
  }

  // ---------------------------------------------------------------- 2 Anteater facts (as in the 2026-10-13 deck)
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
    await cropFill(s, path.join(ASSETS, "anteater.jpeg"), M + 8.3, G.top, CW - 8.3, 4.1, [0.02, 0, 0.62], "anteater at a termite mound");
    s.addText("Giant anteater at a termite mound", { x: M + 8.3, y: G.top + 4.15, w: CW - 8.3, h: 0.25, fontFace: BODY, fontSize: 10, italic: true, color: X.muted, margin: 0, align: "center", isTextBox: true });
    s.addImage({ path: path.join(ASSETS, "leaf_icon.png"), x: M, y: 6.25, w: 0.55, h: 0.55, altText: "leaf icon" });
    s.addText("Mining in La Pampa did the same: it moved on, then came back.",
      { x: M + 0.7, y: 6.27, w: CW - 0.7, h: 0.5, fontFace: LIGHT, fontSize: 20, color: X.ink, margin: 0, valign: "middle", isTextBox: true });
    s.addNotes(
      "About 30 seconds. Two facts about the giant anteater.\n\n" +
      "One: its tongue is about 60 centimetres long and flicks in and out up to 150 times a minute. That's how it eats up to 35,000 ants and termites a day (Smithsonian's National Zoo; National Geographic).\n\n" +
      "Two, and this is the one to remember: it spends only about a minute at each mound, because the ants fight back. It never destroys the nest. It moves on and comes back later to feed again (National Geographic).\n\n" +
      "Hold on to that habit. It is a good description of what we found for gold mining in La Pampa.");
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
    header(s, { no: "02", label: "Where we are", title: "La Pampa sits one road away from legal mining land", claim: "D",
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

  // ---------------------------------------------------------------- 8 Definition: one measure (after the map steps)
  {
    const s = slide("LIGHT", "Where");
    header(s, { no: "03", label: "What we measure", title: "One measure on every slide: net mining additions", claim: "D",
      sub: "Net additions (ha/yr) = new land + re-mined − stopped · per 30-m pixel, year t vs the years before · MapBiomas Peru Collection 4, 1985–2025" });
    const lx = M, ly = G.top + 0.1, sz = 0.62;
    s.addText("YEAR", { x: lx + 2.55, y: ly, w: 0.8, h: 0.25, fontFace: MED, fontSize: 10, charSpacing: 1.5, color: X.muted, margin: 0, align: "center", isTextBox: true });
    s.addText("t − 1", { x: lx + 2.55, y: ly + 0.25, w: 0.8, h: 0.25, fontFace: BODY, fontSize: 11, color: X.ink2, margin: 0, align: "center", isTextBox: true });
    s.addText("t", { x: lx + 3.75, y: ly + 0.25, w: 0.8, h: 0.25, fontFace: BODY, fontSize: 11, color: X.ink2, margin: 0, align: "center", isTextBox: true });
    const rows = [
      ["New land", "never mined before", X.new, "E7E1D6", "forest", X.new, "mined", "+"],
      ["Re-mined", "out of use a year or more, mined again", X.remined, "E7E1D6", "old pit", X.remined, "mined", "+"],
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
      "We split it into three parts, always in the same colours. Brown: new land, mined for the first time since 1985. Amber: re-mined, old pits that were out of use for at least a year and are mined again. A pit worked in both years is in none of the three flows; it simply stays in the mining area. Teal: stopped, pits that left the mining class, most often because they flooded or started to regrow. Net equals new plus re-mined minus stopped.\n\n" +
      "Why it matters: a fall in net additions can mean fewer new pits, or more pits going out of use. Those are different stories for FZS.\n\n" +
      "And the same zones everywhere: the Tambopata buffer zone as SERNANP draws it, La Pampa as its western part, the strip of legal corridor across the road, the Amarakaeri buffer zone as the less-treated comparison, and the whole department. Hectares measure mining activity, not the number of miners.");
  }
  // ---------------------------------------------------------------- 8 Timeline video
  {
    const s = slide("LIGHT", "Where");
    header(s, { no: "04", label: "2010–2025 in one minute", title: "2010–2025: new pits, old pits re-mined, pits stopping", claim: "D",
      sub: "Net mining additions as three flows on the map: new land (brown), re-mined (amber), stopped (teal) · counter: net ha per year, La Pampa sector and corridor across the road" });
    video(s, "MiningTimeline.mp4", "stills/timeline_2019.png", "mining timeline animation");
    s.addNotes(
      "About 60 seconds, click to play. Each year, brown pixels are land mined for the first time, amber are old pits mined again, teal are pits that stopped; grey is everything mapped as mining that year. On the right, the net additions per year for La Pampa and for the strip across the road, with the three parts.\n\n" +
      `Before 2019, brown dominates in La Pampa, south of the road. Watch 2019, the Mercurio year: new clearing did not stop in 2019 — about ${ha("lapampa_2019_new")} hectares of new land in La Pampa, against ${ha("lapampa_2018_new")} in 2018 — but a lot of land went out of use: ${ha("lapampa_2019_stopped")} hectares stopped. So net additions drop to ${ha("lapampa_2019_net")}.\n\n` +
      "In 2020 and 2021, La Pampa's net additions sit near zero while the strip across the road lights up. In the later years, amber appears: mining comes back, much of it on old pits.\n\n" +
      "The video ends with the caveat we repeat: satellites can't see river dredges or mercury.");
  }

  // ---------------------------------------------------------------- 9–15 What happened (figures; titles from slide_titles.json)
  const what = [
    ["slide_09_net.png", "What happened", "05", "It fell",
      `About 40 seconds. One measure on every chart from here: net mining additions, the mining area this year minus last year, in hectares per year. Zone: the Tambopata buffer zone, exactly as SERNANP draws it.\n\n` +
      `Before the operation, 2016 to 2018, it added about ${ha("tambopata_bz_pre_net")} hectares a year. In 2019 to 2021, Mercurio and what followed, only ${ha("tambopata_bz_during_net")}: a ${pct("sl_net_tambopata_bz_fall_share")} fall. In the later years, 2022 to 2025, it was back at ${ha("tambopata_bz_later_net")}, or ${ha("tambopata_bz_later_ex2023_net")} without 2023, a spike only these maps show.\n\n` +
      `For comparison, the less-treated Amarakaeri buffer zone went the other way over the same years, ${ha("amarakaeri_bz_pre_net")} to ${ha("amarakaeri_bz_during_net")}. All description so far. Other events (COVID in 2020, Plan Restauración in 2021) are in the shaded years; we only mark Mercurio and the 2023 emergency on the charts.`],
    ["slide_10_2019_parts.png", "What happened", "05", "What fell: 2019, year by year",
      `About 50 seconds. Same zone, now split into its three parts, year by year. Brown up is new land, mined for the first time; amber is old pits mined again; teal below zero is stopped land, pits that left the mining class; the black line is net.\n\n` +
      `In 2019 new pits kept opening: ${ha("tambopata_bz_2019_new")} hectares of new land, against ${ha("tambopata_bz_2018_new")} in 2018. But ${ha("tambopata_bz_2019_stopped")} hectares stopped, against ${ha("tambopata_bz_2018_stopped")} in 2018, so net additions fell to ${ha("tambopata_bz_2019_net")}. New land only drops from 2020, which is also the first COVID year.\n\n` +
      `Over 2019 to 2021, more stopping explains ${stopShare} of the fall in net additions, depending on how we count map flicker; ${pct("tambopata_bz_excess_stopped_share_in_2019")} of the extra stopping came in 2019. In Amarakaeri, stopped land stayed flat, ${ha("amarakaeri_bz_pre_stopped")} to ${ha("amarakaeri_bz_during_stopped")} hectares a year.\n\n` +
      "Why it matters for FZS: in the first year of an operation, new pits keep opening at the edges while the targeted pits go quiet. That is why a ring around the operation matters."],
    ["slide_11_region.png", "Where it went", "06", "Where it went",
      `About 40 seconds. Zoom out to the whole department. Net additions in Madre de Dios never fell: ${arrow("mdd_pre_net", "mdd_during_net", "mdd_later_net")} hectares a year across the three periods.\n\n` +
      `Blue is the legal mining corridor: all the land in the D.L. 1100 decree, not only the strip across the road we show next. The percentage is the corridor's share of the department's net additions, summed over each period: ${pct("v2_corridor_share_pre_net")}, then ${pct("v2_corridor_share_during_net")}, then ${pct("v2_corridor_share_later_net")}.\n\n` +
      `Careful: the rise elsewhere in the department was ${need("mdd_rise_elsewhere_vs_tambopata_fall").toFixed(1)} times the size of Tambopata's fall, so this is not just the same miners moving; new entrants and the gold price play a part. MAAP #208 finds the same: most mining deforestation in 2021 to 2024 was inside the corridor.`],
    ["slide_12_across.png", "Where it went", "07", "Across the road",
      `About 40 seconds. Now the strip of legal corridor directly across the highway from La Pampa: up to 10 kilometres north of the road, at La Pampa's longitudes. Blue is that strip, orange is La Pampa itself.\n\n` +
      `Across the road, net additions rose from about ${ha("corridor_across_pre_net")} hectares a year in 2016 to 2018 to ${ha("corridor_across_during_net")} in 2019 to 2021, while La Pampa fell from ${ha("lapampa_pre_net")} to ${ha("lapampa_during_net")}.\n\n` +
      "Independent evidence points the same way: Dethier and colleagues (2023) report most activity abandoned in the targeted zones and faster mining just outside them. But we cannot show it was the same people who crossed the road."],
    ["slide_12b_bands.png", "Where it went", "07", "Across the road: 1-km bands",
      `About 30 seconds. The same story in 1-kilometre bands, at La Pampa's longitudes: orange south of the highway, the La Pampa side; blue north, the corridor side.\n\n` +
      `In 2016 to 2018 nearly all net additions were south of the road: ${ha("sl_band_south_pre_net")} hectares a year south against ${ha("sl_band_north_pre_net")} north. In 2019 to 2021 the south dropped to ${ha("sl_band_south_during_net")} while the north rose to ${ha("sl_band_north_during_net")}, first right next to the road, then deeper in. In the later years both sides grew.\n\n` +
      "Description only: the bands show where mining happened, not who did it."],
    ["slide_13_money.png", "Why it came back", "08", "Why it came back",
      `About 40 seconds. Why did it come back? Three things line up; this is context, not a test.\n\n` +
      `Left: the anti-illegal-mining budget booked in Madre de Dios, programme PP 0128, peaked at about ${Math.round(need("t8_pp0128_mdd_2019") / 1e6)} million soles in 2019 and fell to about ${Math.round(need("t8_pp0128_mdd_2025") / 1e6)} million in 2025; it's a lower bound because national units book in Lima. Middle: the gold price, up ${need("gold_price_ratio_2025_2018").toFixed(1)}-fold from 2018 to 2025. Right: net additions in the Tambopata buffer zone, back up as the money faded and the price rose.\n\n` +
      "We don't show a correlation: eleven years is too few, and money also follows mining."],
    ["slide_14_came_back.png", "Why it came back", "09", "How it came back",
      `About 40 seconds. Back to the parts, 2014 to 2025. In the later years the buffer zone averaged ${ha("tambopata_bz_later_net")} hectares a year net, ${ha("tambopata_bz_later_ex2023_net")} without the 2023 spike.\n\n` +
      `Much of it came back on old pits: re-mined land was ${pct("tambopata_bz_later_remined_share_added")} of the land added, or ${pct("tambopata_bz_later_ex2023_remined_share_added")} without 2023 — a third to a half. Forest-loss alerts miss this, because there is no forest left to lose. MAAP #193 (2023) reports the same return to degraded land.\n\n` +
      "We call 2022 to 2025 'the later years', not 'after enforcement', because enforcement went on in waves: Plan Restauración in 2021 and a state of emergency from April 2023."],
    ["slide_15_reserve.png", "Why it came back", "10", "Inside the reserve",
      `About 30 seconds. This is FZS's core area: the Tambopata National Reserve itself, not the buffer zone.\n\n` +
      `Net additions inside the reserve stayed small or negative for years; in 2019 to 2021 they averaged ${ha("tambopata_nr_during_net")} hectares a year. In 2025 they jumped by ${ha("tambopata_nr_2025_net")} hectares. MAAP #241 (2026) reports about 500 hectares from late 2025 to February 2026, and that the navy withdrew from its Malinowski river posts in 2025 for lack of funds.\n\n` +
      `The 2017 bar, about ${ha("tambopata_nr_2017_net")} hectares, is an earlier jump; treat single years with care.`],
  ];
  for (const [file, section, no, label, notes] of what) await figSlide(file, { section, no, label, notes });

  // ---------------------------------------------------------------- 16 Six methods (old slide 18 grid)
  {
    const s = slide("LIGHT", "Is it causal?");
    header(s, { no: "11", label: "Is it causal?", title: "Six methods: two hold up, none is clean", claim: "C",
      sub: "Each builds a stand-in for the Tambopata buffer zone without Mercurio · all six point down · green = holds up, in net additions, in hectares only" });
    const methods = [
      ["Compare with other zones", "Tambopata vs 14 other Peruvian buffer zones, before and after", true, "Holds up · in hectares only"],
      ["A weighted copy", "a mix of zones built to track Tambopata before 2019", false, "No good copy before 2019"],
      ["Twins in Brazil", "look-alike mining areas picked by fixed rules", false, "Different trends before 2019"],
      ["Either side of the road", "land just north vs just south of the highway", false, "Too noisy to tell"],
      [`Matching, ${need("psm_n_methods").toFixed(0)} ways`, "look-alike areas picked by algorithm", false, "Can't beat chance"],
      ["Weighted zones and years", "zones and years weighted to match Tambopata's past", true, "Holds up · in hectares only"],
    ];
    const icons = ["LuGitCompare", "LuLayers", "LuSearch", "LuSplit", "LuCrosshair", "LuSigma"];
    const gap = 0.25, cw = (CW - 2 * gap) / 3, ch = (G.bottom - G.top - gap) / 2;
    for (let i = 0; i < methods.length; i++) {
      const [name, how, ok, verdict] = methods[i];
      const x = M + (i % 3) * (cw + gap), y = G.top + Math.floor(i / 3) * (ch + gap);
      s.addShape(pres.shapes.RECTANGLE, { x, y, w: cw, h: ch, fill: { color: ok ? "EAF2E4" : X.surface }, line: { color: ok ? X.eyebrow : X.rule, width: ok ? 1.5 : 0.75 } });
      s.addImage({ data: await icon("lu", icons[i], ok ? X.eyebrow : X.muted), x: x + 0.3, y: y + 0.28, w: 0.5, h: 0.5 });
      s.addText(name, { x: x + 0.3, y: y + 0.9, w: cw - 0.6, h: 0.45, fontFace: MED, fontSize: 19, color: ok ? X.ink : X.ink2, margin: 0, isTextBox: true });
      s.addText(how, { x: x + 0.3, y: y + 1.36, w: cw - 0.6, h: 0.6, fontFace: BODY, fontSize: 14, color: X.ink2, margin: 0, valign: "top", isTextBox: true });
      s.addText(verdict.toUpperCase(), { x: x + 0.3, y: y + ch - 0.45, w: cw - 0.6, h: 0.3, fontFace: MED, fontSize: 11.5, charSpacing: 1.5,
        color: ok ? X.eyebrow : X.muted, margin: 0, isTextBox: true });
    }
    s.addNotes(
      "About 45 seconds. Only one area was targeted, so to ask 'did Mercurio cause the fall?' we need a stand-in: what would the Tambopata buffer zone have done without it? We built that stand-in six ways.\n\n" +
      `All six point down; two hold up: comparing with the 14 other Peruvian buffer zones (difference-in-differences with zone and year effects) and weighting zones and years to match Tambopata's past (synthetic difference-in-differences, ${ha("sdid_sdid_ha_during_net")} hectares a year). Both find a fall far bigger than any other zone's, but only in hectares; for its size Tambopata is ordinary.\n\n` +
      `None is clean. A weighted copy (synthetic control) can't track a zone this big before 2019. The Brazilian twins grew at a different pace before 2019, on another product. Either side of the road is too noisy (p = ${p2("rd_road_did_net_p")}). Seven matching methods all find Tambopata slower, but never beyond chance. Details in the backup.`);
  }

  // ---------------------------------------------------------------- 17 The claim (old slide 19, dark)
  {
    const s = slide("DARK", "Is it causal?");
    header(s, { no: "12", label: "The causal claim", title: "What we can say about cause", claim: "C", dark: true });
    s.addText([
      { text: "If the other zones show what Tambopata would have done, ", options: { color: X.onSlate2, italic: true } },
      { text: "Mercurio and the operations that followed lowered net mining additions by ", options: { color: X.onSlate } },
      { text: `${abs("model_m1_during_net")} to ${abs("did_base2014_net")} ha a year`, options: { color: X.lime } },
      { text: " in 2019–21.", options: { color: X.onSlate } },
    ], { x: M, y: G.top, w: 11.8, h: 2.0, fontFace: LIGHT, fontSize: 30, margin: 0, valign: "top", isTextBox: true });
    s.addShape(pres.shapes.LINE, { x: M, y: 4.15, w: CW, h: 0, line: { color: "FFFFFF", width: 0.75, transparency: 82 } });
    [["Hectares only", `Largest fall of ${int("model_m1_n")} zones; for its size, ${scaledRank} of ${int("model_m4_n")}, depending on the scaling.`],
     ["A quarter to a half is pits stopping", `${stopShare} of the fall is more land going out of use, most of it in 2019.`],
     ["COVID overlaps", "New land fell only from 2020, the first COVID year."]].forEach(([v, l], i) => {
      const x = M + i * 4.13;
      if (i) vline(s, x - 0.2, 4.4, 2.1);
      s.addText(v, { x, y: 4.4, w: 3.8, h: 0.95, fontFace: LIGHT, fontSize: 26, color: X.lime, margin: 0, valign: "top", isTextBox: true });
      s.addText(l, { x, y: 5.4, w: 3.7, h: 1.0, fontFace: BODY, fontSize: 15, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    });
    s.addNotes(
      "About 40 seconds. This is the one causal sentence we are willing to make, and it has an 'if'. " +
      `If the other buffer zones show what the Tambopata buffer zone would have done without the operation, then Mercurio and the operations that followed lowered its net mining additions by about ${abs("model_m1_during_net")} to ${abs("did_base2014_net")} hectares a year in 2019 to 2021. ` +
      `The low end compares it with all 14 other Peruvian buffer zones; the high end with Amarakaeri alone, both against a 2014 to 2018 baseline.\n\n` +
      `Three limits. It holds in hectares, not relative to the zone's size: scaled, Tambopata is ${scaledRank} of ${int("model_m4_n")}, nothing special. A quarter to a half of it is pits going out of use rather than fewer new pits. And it coincides with COVID: new land only fell from 2020. Read it as an upper bound.`);
  }

  // ---------------------------------------------------------------- 18 The evidence (old slide 20: raw vs scaled placebo dots)
  await figSlide("slide_18_placebo.png", { section: "Is it causal?", no: "12", label: "The evidence", claim: "C",
    notes: "About 40 seconds. How the test works: we pretend each of the other zones was the one targeted, and compute the same number. If Mercurio mattered, Tambopata's real change should stand out from all the fake ones.\n\n" +
      `Top row, in hectares: the Tambopata buffer zone, the orange dot, is far to the left of every grey dot: ${ordinal(Math.round(need("model_m1_rank")))} of ${int("model_m1_n")}. But it was also first in 2014, before Mercurio: it is simply the biggest zone.\n\n` +
      `Bottom row, the same change scaled to each zone's normal pre-2019 year: Tambopata sits among the others, ${ordinal(Math.round(need("model_m4_rank")))} of ${int("model_m4_n")} here, and ${scaledRank} across the ways of scaling. A big zone falls a lot in hectares just by being big. That is why our claim is in hectares only, and a rank is not a significance test.` });

  // ---------------------------------------------------------------- 19 Limits (old slide 21)
  {
    const s = slide("LIGHT", "Limits");
    header(s, { no: "13", label: "Limits", title: "Most biases make the fall look bigger", claim: "D",
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

  // ---------------------------------------------------------------- 20 For FZS (old slide 22 + ring monitoring)
  {
    const s = slide("DARK", "For FZS");
    header(s, { no: "14", label: "For FZS", title: "Plan for the months after the operation ends", claim: "P", dark: true,
      sub: "Informed expectations from one case, not proven rules · net mining additions, Tambopata buffer zone, corridor across the road, reserve" });
    const recs = [
      ["LuCalendarClock", "Stay after the sweep", arrow("tambopata_bz_during_net", "tambopata_bz_later_net"),
        "ha/yr, 2019–21 → later years, Tambopata buffer zone. Fund presence, not one-off sweeps."],
      ["LuRadar", "Watch the ring around it", arrow("corridor_across_pre_net", "corridor_across_during_net"),
        "ha/yr just across the road. Near-real-time forest-loss alerts on a ring of a few km; add old pits."],
      ["LuShieldCheck", "Guard the reserve's edge and river", pct("rd_reserve_inside_share_1km"),
        "of first-time mining inside the reserve along its buffer-zone border (2000–25) lies within 1 km of the edge."],
    ];
    for (let i = 0; i < recs.length; i++) {
      const [ic, head, v, l] = recs[i], x = M + i * 4.13, y = G.top + 0.15;
      if (i) vline(s, x - 0.2, y, 4.6);
      s.addShape(pres.shapes.OVAL, { x, y, w: 0.8, h: 0.8, fill: { color: X.slate2 }, line: { color: X.lime, width: 1 } });
      s.addImage({ data: await icon("lu", ic, X.lime), x: x + 0.18, y: y + 0.18, w: 0.44, h: 0.44 });
      s.addText(head, { x, y: y + 1.05, w: 3.8, h: 0.8, fontFace: MED, fontSize: 20, color: X.onSlate, margin: 0, valign: "top", isTextBox: true });
      s.addText(v, { x, y: y + 1.9, w: 3.8, h: 0.8, fontFace: LIGHT, fontSize: 40, color: X.lime, margin: 0, isTextBox: true });
      s.addText(l, { x, y: y + 2.8, w: 3.6, h: 1.4, fontFace: BODY, fontSize: 15, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    }
    s.addNotes(
      "About 60 seconds. Three recommendations. They build on this one case, so treat them as informed expectations, not proven rules.\n\n" +
      `One, stay after the sweep. Net additions stayed low only in 2019 to 2021; in the later years the buffer zone was back at about ${ha("tambopata_bz_later_net")} hectares a year (${ha("tambopata_bz_later_ex2023_net")} without 2023). Fund lasting presence, not one-off operations.\n\n` +
      `Two, watch the ring around the operation. In 2019 new pits kept opening while old ones went quiet, and net additions across the road rose from about ${ha("corridor_across_pre_net")} to ${ha("corridor_across_during_net")} hectares a year. Near-real-time forest-loss alerts, like GLAD or MAAP, on a ring of a few kilometres around each operation catch the next pit early. Add old pits to the watch list: alerts miss re-mining.\n\n` +
      `Three, guard the reserve's edge and its river. ${pct("rd_reserve_inside_share_1km")} of the first-time mining inside the reserve along its border with the buffer zone, 2000 to 2025, lies within one kilometre of the edge. Staffed posts on the Malinowski river are a direct shield; MAAP #241 reports that the navy left those posts in 2025.\n\n` +
      "What would let us say more: dated patrol records per zone from SERNANP or FZS, dredge counts, and mercury sampling.");
  }

  // ---------------------------------------------------------------- 21 Thanks
  {
    const s = slide("DARK", "Closing");
    header(s, { label: "Thank you", dark: true });
    s.addText([
      { text: "Questions?", options: { color: X.onSlate, breakLine: true } },
      { text: "Like the anteater: a pause, not an end.", options: { color: X.lime, fontSize: 22 } },
    ], { x: M, y: 1.2, w: 5.4, h: 2.4, fontFace: LIGHT, fontSize: 54, margin: 0, valign: "top", isTextBox: true });
    s.addImage({ data: anteaterLime, x: M, y: 3.9, w: 1.3, h: 1.3 });
    { const mw = 6.6, mh = mw * 9 / 16;
      s.addImage({ path: path.join(ANIM, "stills", "map_step4_clean.png"), x: W - M - mw, y: (H - mh) / 2 - 0.1, w: mw, h: mh, altText: "map: La Pampa and the corridor across the road" }); }
    s.addText(TEAM, { x: M, y: 5.5, w: 5.4, h: 0.5, fontFace: BODY, fontSize: 12, color: X.onSlate2, margin: 0, valign: "top", isTextBox: true });
    s.addNotes("Thank you. Happy to take questions. Backup: six methods in detail, the one causal range, stopped land, road and cells, legality, declared gold, money, risk map, twins, Brazil, the map video and definitions.");
  }

  // ================================================================= Backup
  {
    const s = slide("DARK", "Backup");
    header(s, { label: "Backup", title: "For questions", dark: true,
      sub: "Six methods · one causal range · stopped land · road and cells · legality · declared gold · money · risk map · twins · Brazil · map video · one measure · definitions" });
    s.addNotes("Backup slides, only if asked.");
  }
  {
    const s = slide("LIGHT", "Backup");
    header(s, { label: "Backup · Six methods", title: "Six methods in detail", claim: "C",
      sub: "Net mining additions, Tambopata buffer zone, 2019–21 vs before, ha/yr unless stated · all conditional on the comparison" });
    const rows = [
      ["METHOD: WHAT IT DOES", "RESULT", "VERDICT"],
      ["1  Difference-in-differences: Tambopata's change minus the comparison zones' change",
        `${ha("model_m1_during_net")} (vs 14 zones) to ${ha("did_base2014_net")} (vs Amarakaeri), 2014–18 base; size rank ${scaledRank} of 7`, "Holds up in ha"],
      ["2  Synthetic control: a weighted mix of zones that tracks Tambopata before 2019",
        `${ha("sdid_sc_ha_during_net")}; all weight on Amarakaeri, no pre-2019 fit`, "No good copy"],
      ["3  Rule-based twins: Brazilian areas picked by Ruby's four rules",
        `Tambopata at ${pct("top3_ratio")}–${pct("top3_ratio_excl_unverified")} of their pace (Amazon Mining Watch, another product)`, "Different trends"],
      ["4  Spatial discontinuity: land just north vs just south of the road",
        `${need("rd_road_did_net") >= 0 ? "+" : "−"}${Math.abs(need("rd_road_did_net")).toFixed(1)} pts of land/yr (p = ${p2("rd_road_did_net_p")})`, "Too noisy"],
      [`5  Matching, ${need("psm_n_methods").toFixed(0)} ways: look-alike areas picked by algorithm`,
        `All slower; fake-test p ${p2("psm_p_min")}–${p2("psm_p_max")}; no common support`, "Can't decide"],
      ["6  Synthetic DiD: zones and years weighted to match Tambopata's past",
        `${ha("sdid_sdid_ha_during_net")}; size rank ${int("sdid_sdid_scaled_during_rank")} of ${int("sdid_sdid_scaled_during_n")}`, "Holds up in ha"],
    ];
    const vc = { "Holds up in ha": X.eyebrow, "No good copy": X.p, "Different trends": X.p, "Too noisy": X.p, "Can't decide": X.muted };
    s.addTable(rows.map((r, i) => r.map((c, j) => ({ text: c, options: {
      fontFace: i === 0 || j === 2 ? MED : BODY, fontSize: i === 0 ? 10.5 : 13.5, charSpacing: i === 0 ? 1.5 : 0,
      color: i === 0 ? X.ink2 : (j === 2 ? vc[c] : X.ink), fill: { color: i === 0 ? X.surface2 : X.surface }, valign: "middle", margin: [4, 10, 4, 10] } }))),
      { x: M, y: G.top, w: CW, colW: [5.6, 4.83, 1.8], rowH: [0.4, 0.74, 0.74, 0.74, 0.74, 0.74, 0.74], border: { type: "solid", color: X.rule, pt: 0.75 } });
    s.addNotes("Only the zone-level designs give a large, stable number, and only in hectares: scaled to size Tambopata is ordinary. The raw rank 1 of 15 also appears in 2014, before Mercurio, so it measures size, not significance. Synthetic control cannot fit Tambopata's size before 2019; the twins grew differently before 2019 and use another product (Amazon Mining Watch new area, not net additions); the road discontinuity measures a swing and is too noisy on net additions; matching never beats chance and has no common support.");
  }
  await figSlide("slide_b0_estimates.png", { section: "Backup", label: "Backup · One causal range", claim: "C",
    notes: `The range runs from zone + year effects across all 15 zones (${ha("model_m1_during_net")}) to Tambopata vs Amarakaeri on the 2014–18 baseline (${ha("did_base2014_net")}). Synthetic DiD and the gold-price model fall inside. Two estimates are left out: each zone's own trend (${ha("model_m3_during_net")}) fails the fake-2016 test, and synthetic control (${ha("sdid_sc_ha_during_net")}) puts all weight on Amarakaeri without a pre-2019 fit. All conditional; an upper bound.` });
  const backupFigs = [
    ["slide_b1_stopped_split.png", "Stopped land", null, "D",
      `What 'stopped' means on the ground. Most stopped land becomes water (flooded pits) or regrows; a large share is mapped as mining again within two years: in the Tambopata buffer zone ${pct("tambopata_bz_during_stopped_share_back_within_2y")} for 2019–21. That is classifier flicker or miners returning; we have no image validation sample.`],
  ];
  for (const [file, label, title, claim, notes] of backupFigs)
    await figSlide(file, { section: "Backup", label: `Backup · ${label}`, title: title || undefined, claim, notes,
      dir: file.startsWith("slide_") ? SLIDES : OUT, sub: file.startsWith("slide_") ? undefined : " " });
  {
    const s = slide("LIGHT", "Backup");
    header(s, { label: "Backup · Road and cells", title: "Road and 1-km cell designs: too noisy to tell", claim: "D",
      sub: "Net mining additions · La Pampa longitudes · 2019–21 vs 2014–18 · finer-grained designs, described in one line each" });
    [["Either side of the road", `${need("rd_road_did_net") >= 0 ? "+" : "−"}${Math.abs(need("rd_road_did_net")).toFixed(1)} pts`,
      `of land per year swung north of the road (p = ${p2("rd_road_did_net_p")}; ${p2("rd_road_sens_p_min")}–${p2("rd_road_sens_p_max")} across distances). Compares land just either side of the highway; miners moving across break it, so it is an upper bound.`],
     ["At the reserve edge", `${need("rd_reserve_did_net") >= 0 ? "+" : "−"}${Math.abs(need("rd_reserve_did_net")).toFixed(1)} pts`,
      `no measurable change (p = ${p2("rd_reserve_did_net_p")}). Same comparison, inside vs outside the reserve's border.`],
     ["1-km cells", "≈ before/after", "Each 1-km cell compared with cells of the same year; the comparison cells hold almost no mining, so this is close to a simple before/after."]].forEach(([eb, v, l], i) => {
      const x = M + i * 4.13;
      if (i) vline(s, x - 0.2, G.top, 4.2, false);
      s.addText(eb.toUpperCase(), { x, y: G.top, w: 3.8, h: 0.28, fontFace: MED, fontSize: 11, charSpacing: 2, color: X.ink2, margin: 0, isTextBox: true });
      s.addText(v, { x, y: G.top + 0.4, w: 3.8, h: 0.8, fontFace: LIGHT, fontSize: 36, color: X.ink, margin: 0, isTextBox: true });
      s.addText(l, { x, y: G.top + 1.35, w: 3.75, h: 2.6, fontFace: BODY, fontSize: 15, color: X.ink2, margin: 0, valign: "top", isTextBox: true });
    });
    s.addNotes("Spatial regression discontinuity (rdrobust, difference in discontinuities) at the road and at the reserve edge, and a 1-km cell panel with cell and year effects. Neither is informative on net additions: the road swing is noisy and is an upper bound because displacement breaks the no-spillover assumption; the cell comparison holds almost no mining. Description.");
  }
  const backupFigs2 = [
    ["fig_v2_legality.png", "Legality", "Presumed-illegal new land fell; grey zones grew", "D",
      "Amazon Mining Watch / MAAP legality layer on first-time mining (new land), Madre de Dios. Another product; today's concessions applied to all years. Description."],
    ["fig_peru_gold_definition.png", "Declared gold", "The official gold drop is a definition change", "D",
      "The official Madre de Dios gold series 'fell' in 2020 because the ministry stopped adding its artisanal estimate. Producer-declared gold did not fall. Do not cite it as a production fall. Description."],
    ["fig_v2_economics.png", "Money", "Gold and its damage dwarf enforcement money", "P",
      "Informed speculation from cited parameters, not a finding: gold mined, declared gold, social cost estimates and enforcement money per year, 2022–25, log scale."],
    ["fig_v2_risk_map.png", "Risk map", "Next new mining is likely next to old mining", "P",
      "Prediction, not a causal map: chance of new land per 1-km cell in the next years, from distance to the road, rivers, gold-bearing land and existing mining."],
    ["slide_b2_twins.png", "Twins", null, "D",
      `Rule-based twins (Ruby's design), all chosen by one dating rule. On another product (Amazon Mining Watch new area, comparable to new land, not net additions), the Tambopata buffer zone added new area in 2019–21 at ${pct("top3_ratio")} of the twins' mean pace (${pct("top3_ratio_excl_unverified")} without Munduruku). Before 2019 the twins grew differently, so they can't show the counterfactual.`],
    ["fig_brazil_v2_pixels.png", "Brazil", "Brazil: mining boomed and fell; operations arrived at the peak", "D",
      "Only if asked. In the Yanomami, Munduruku and Kayapó territories mining had boomed for years and fell after 2022. Federal operations arrived at the peak, and Munduruku was already falling before its operation, so our data cannot separate the operations from the end of the boom. A national change in January 2023 (end of the gold 'good faith' rule, electronic invoices) hit all territories at once. Net additions, MapBiomas Brazil Collection 11. Description."],
  ];
  for (const [file, label, title, claim, notes] of backupFigs2)
    await figSlide(file, { section: "Backup", label: `Backup · ${label}`, title: title || undefined, claim, notes,
      dir: file.startsWith("slide_") ? SLIDES : OUT, sub: file.startsWith("slide_") ? undefined : " " });
  {
    const s = slide("LIGHT", "Backup");
    header(s, { label: "Backup · Map video", title: "The map build as one animation", claim: "D",
      sub: "Same four steps as the click-through map slides · protected areas → highway → corridor → La Pampa · click to play" });
    video(s, "MapLayers.mp4", "stills/map_step4.png", "map layers animation");
    s.addNotes("Optional: the same four steps as the click-through map slides, as one video.");
  }
  {
    const s = slide("LIGHT", "Backup");
    header(s, { label: "Backup · Definitions and data", title: "Definitions and data", claim: "D",
      sub: "One outcome, one set of zones, one treatment · every number in this deck comes from our replication code" });
    const rows = [
      ["ITEM", "DEFINITION", "SOURCE"],
      ["Net mining additions", "Mining area in year t − year t−1, ha/yr = new land + re-mined − stopped", "MapBiomas Peru Collection 4 (30 m, class 4.2)"],
      ["New land / re-mined / stopped", "First time since 1985 / mined again after a gap / left the mining class", "Our pixel accounting"],
      ["Tambopata buffer zone", "Official SERNANP polygon, whole (incl. Kotsimba)", "SERNANP"],
      ["La Pampa sector", "Tambopata buffer zone between 70.15° and 69.80° W (no official line)", "Our boundary"],
      ["Corridor across the road", "D.L. 1100 land ≤ 10 km north of the highway, at La Pampa's longitudes", "INGEMMET, RAISG"],
      ["Legal mining corridor", "All D.L. 1100 land in Madre de Dios (native communities excluded); its share = its net additions ÷ the department's, summed over each period", "INGEMMET"],
      ["Treatment and periods", "Mercurio from Feb 2019 (first treated year 2019) · 2016–18 before · 2019–21 Mercurio and what followed · 2022–25 later years (± 2023)", "MAAP #130; course card"],
    ];
    s.addTable(rows.map((r, i) => r.map((c) => ({ text: c, options: {
      fontFace: i === 0 ? MED : BODY, fontSize: i === 0 ? 10.5 : 13, charSpacing: i === 0 ? 1.5 : 0, color: i === 0 ? X.ink2 : X.ink,
      fill: { color: i === 0 ? X.surface2 : X.surface }, valign: "middle", margin: [4, 10, 4, 10] } }))),
      { x: M, y: G.top, w: CW, colW: [2.9, 6.6, 2.73], rowH: [0.36, 0.5, 0.5, 0.5, 0.5, 0.5, 0.78, 0.78], border: { type: "solid", color: X.rule, pt: 0.75 } });
    s.addNotes("Definitions for questions. The course's statistics workbook numbers (1,640 → 163 ha/yr) are reproduced as checks; our numbers come from the rasters on one set of zones.");
  }

  for (const [k, t] of titles) {
    const width = t.length * 0.0066 * G.titleSize;
    if (width > CW) console.warn(`slide ${k}: title may wrap (${t.length} chars): ${t}`);
    if (k > 2 && t.split(/\s+/).length > 10 && k < 22) console.warn(`slide ${k}: title over 10 words: ${t}`);
  }
  const file = path.join(__dirname, "GroupAnteater_FZS_talk.pptx");
  await pres.writeFile({ fileName: file });
  const { applyTheme } = require("./apply_theme.js");
  await applyTheme(file, THEME);
  fs.writeFileSync(path.join(__dirname, "deck_ids_used.txt"), [...used].sort().join("\n") + "\n");
  console.log(`Wrote ${file} (${n} slides, ${used.size} number ids)`);
})();
