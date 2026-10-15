// Word version of the brief, for editing: docs/brief/BRIEF.md -> docs/brief/BRIEF.docx
// Run: cd docs/brief/docx_build && npm install && node make_docx.js
// BRIEF.md is written by docs/walkthrough/build_report.py (numbers already filled in from output/numbers.csv).
// A4, 2 cm margins, Calibri 10 pt; References start on a new page (parts 1-4 = the two graded pages).
const fs = require("fs");
const path = require("path");
const { marked } = require("marked");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, ImageRun, Table, TableRow, TableCell, WidthType,
  ShadingType, BorderStyle, AlignmentType, LevelFormat, ExternalHyperlink, PageBreak,
} = require("docx");

const BRIEF = path.resolve(__dirname, "..");
const SRC = path.join(BRIEF, "BRIEF.md");
const OUT = path.join(BRIEF, "BRIEF.docx");
const INK = "1F2D33", INK2 = "4F5B60", GREEN = "3C7D2C";
const LABEL = { Description: "2B6A8A", Prediction: "8A5F00", Causal: "A42C58" };
const TEXT_W = 11906 - 2 * 1134;                               // A4 width minus 2 cm margins, DXA

let md = fs.readFileSync(SRC, "utf8");
md = md.replace(/\n---\n\*Built [^\n]*\n?$/, "\n");            // drop the build stamp
const tokens = marked.lexer(md);

function runs(inline, style = {}) {
  const out = [];
  for (const t of inline || []) {
    if (t.type === "strong") {
      const lab = /^\[(description|prediction|causal)\]$/i.exec(t.text); if (lab) lab[1] = lab[1][0].toUpperCase() + lab[1].slice(1).toLowerCase();
      if (lab) out.push(new TextRun({ text: ` ${lab[1].toUpperCase()} `, bold: true, size: 15, color: "FFFFFF",
        shading: { type: ShadingType.CLEAR, color: "auto", fill: LABEL[lab[1]] } }));
      else out.push(...runs(t.tokens, { ...style, bold: true }));
    } else if (t.type === "em") out.push(...runs(t.tokens, { ...style, italics: true }));
    else if (t.type === "codespan") out.push(new TextRun({ text: t.text.replace(/&amp;/g, "&"), font: "Consolas", size: 18, ...style }));
    else if (t.type === "link") out.push(new ExternalHyperlink({ link: t.href, children: [new TextRun({ text: t.text, style: "Hyperlink", ...style })] }));
    else if (t.type === "br") out.push(new TextRun({ break: 1 }));
    else if (t.type === "text" && t.tokens) out.push(...runs(t.tokens, style));
    else if (t.type === "escape" || t.type === "text") out.push(new TextRun({ text: decode(t.text), ...style }));
    else if (t.type === "image") continue;
    else out.push(new TextRun({ text: decode(t.raw || ""), ...style }));
  }
  return out;
}
const decode = (s) => s.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'");

function imagePara(tok) {
  const file = path.resolve(BRIEF, tok.href);
  const buf = fs.readFileSync(file);
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);   // PNG header
  const width = 520, height = Math.round((560 * h) / w);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60, after: 40 },
      children: [new ImageRun({ type: "png", data: buf, transformation: { width, height }, altText: { title: "Figure 1", description: tok.text, name: "Figure 1" } })] }),
    new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "Figure 1. ", bold: true, size: 17, color: INK2 }),
      new TextRun({ text: tok.text + ". Source: MapBiomas Peru, Collection 4.", size: 17, color: INK2 })] }),
  ];
}

function table(tok) {
  const n = tok.header.length, cw = Math.floor(TEXT_W / n);
  const border = { style: BorderStyle.SINGLE, size: 4, color: "C4C0B6" };
  const cell = (c, head) => new TableCell({ width: { size: cw, type: WidthType.DXA },
    borders: { top: border, bottom: border, left: border, right: border },
    shading: head ? { type: ShadingType.CLEAR, color: "auto", fill: "E9E4DC" } : undefined,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({ children: runs(c.tokens, head ? { bold: true, size: 17 } : { size: 17 }) })] });
  return new Table({ width: { size: cw * n, type: WidthType.DXA }, columnWidths: Array(n).fill(cw),
    rows: [new TableRow({ tableHeader: true, children: tok.header.map((c) => cell(c, true)) }),
           ...tok.rows.map((r) => new TableRow({ children: r.map((c) => cell(c, false)) }))] });
}

function list(tok, level = 0) {
  const out = [];
  for (const it of tok.items) {
    const inner = it.tokens.filter((t) => t.type !== "list");
    const inl = inner.flatMap((t) => (t.tokens ? t.tokens : [{ type: "text", text: t.text || "" }]));
    out.push(new Paragraph({ numbering: { reference: tok.ordered ? "num" : "bullets", level }, spacing: { after: 40 }, children: runs(inl) }));
    for (const sub of it.tokens.filter((t) => t.type === "list")) out.push(...list(sub, level + 1));
  }
  return out;
}

const body = [];
let first = true;
for (const t of tokens) {
  if (t.type === "heading") {
    const txt = t.text;
    if (t.depth === 1) { body.push(new Paragraph({ heading: HeadingLevel.TITLE, children: runs(t.tokens) })); continue; }
    if (t.depth === 2 && /^(References|Appendix A)/.test(txt)) body.push(new Paragraph({ children: [new PageBreak()] }));
    const lvl = { 2: HeadingLevel.HEADING_1, 3: HeadingLevel.HEADING_2 }[t.depth] || HeadingLevel.HEADING_3;
    body.push(new Paragraph({ heading: lvl, children: runs(t.tokens) }));
  } else if (t.type === "paragraph") {
    const img = (t.tokens || []).find((x) => x.type === "image");
    if (img) { body.push(...imagePara(img)); continue; }
    const p = new Paragraph({ spacing: { after: 100 }, children: runs(t.tokens, first ? { color: INK2 } : {}) });
    body.push(p); first = false;
  } else if (t.type === "list") body.push(...list(t));
  else if (t.type === "table") body.push(table(t), new Paragraph({ spacing: { after: 80 }, children: [] }));
  else if (t.type === "blockquote") body.push(new Paragraph({ indent: { left: 360 }, children: runs(t.tokens.flatMap((x) => x.tokens || [])) }));
}

const doc = new Document({
  creator: "Group Giant Anteater", title: "When the patrols leave: what Operation Mercurio tells FZS",
  styles: {
    default: { document: { run: { font: "Calibri", size: 19, color: INK }, paragraph: { spacing: { line: 252 } } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal", run: { size: 34, bold: true, color: INK }, paragraph: { spacing: { after: 60 } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 21, bold: true, color: GREEN, allCaps: true }, paragraph: { keepNext: true, spacing: { before: 200, after: 80 }, outlineLevel: 0,
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "C9C1B4", space: 2 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 20, bold: true }, paragraph: { keepNext: true, spacing: { before: 140, after: 60 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 19, bold: true, color: INK2 }, paragraph: { keepNext: true, spacing: { before: 100, after: 40 }, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [
    { reference: "bullets", levels: [0, 1, 2].map((l) => ({ level: l, format: LevelFormat.BULLET, text: ["•", "–", "·"][l], alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 360 * (l + 1), hanging: 240 } } } })) },
    { reference: "num", levels: [0, 1].map((l) => ({ level: l, format: LevelFormat.DECIMAL, text: `%${l + 1}.`, alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 360 * (l + 1), hanging: 260 } } } })) },
  ] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1020, bottom: 1020, left: 1134, right: 1134 } } },
               children: body }],
});

Packer.toBuffer(doc).then((b) => { fs.writeFileSync(OUT, b); console.log(`wrote ${path.relative(process.cwd(), OUT)} (${(b.length / 1e6).toFixed(2)} MB)`); });
