import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { Background, FONT, Layer, MapFrame, MapLabel, PANEL, PanelCaption, SourceLine, T, YearKey, clamp, data, easeOut, fadeIn } from "./shared";

// Storyline v3, slide 5: 2010-2025, net mining additions as three flows on the map.
// Each year: brown = land mined for the first time, amber = old pits mined again, teal = pits that stopped
// (left the mining class); grey = land mapped as mining that year. Counter: net = new + re-mined − stopped, per year,
// for La Pampa sector and the corridor across the road (values from zonedata = output/numbers.csv).
const FIRST = 2010;
const LAST = 2025;
const YEARS = Array.from({ length: LAST - FIRST + 1 }, (_, i) => FIRST + i);
const INTRO_S = 2;
const FAST_S = 2;
const SLOW_S = 3.5;
const OUTRO_S = 5;
const secondsFor = (y: number) => (y < 2019 ? FAST_S : SLOW_S);

export const timelineSeconds = () => INTRO_S + YEARS.reduce((a, y) => a + secondsFor(y), 0) + OUTRO_S;

const PINS = [
  { t: 2019 + 1.6 / 12, label: "Mercurio", main: true },
  { t: 2020 + 2 / 12, label: "COVID-19" },
  { t: 2021 + 6 / 12, label: "Restauración" },
  { t: 2023 + 3 / 12, label: "Emergency" },
  { t: 2025 + 2 / 12, label: "Navy out" },
];

type Unit = "lapampa" | "corridor_across";
type Part = "net" | "new" | "remined" | "stopped";
const flow = (y: number, u: Unit) => data.flows[String(y) as YearKey][u] as Record<Part, number>;
const fmt = (v: number) => Math.round(Math.abs(v)).toLocaleString("en-US");
const signed = (v: number) => `${v < 0 ? "−" : "+"}${fmt(v)}`;

const CHAPTERS: { from: number; to: number; eyebrow: string; title: string; note?: string }[] = [
  { from: 2010, to: 2018, eyebrow: "2010–2018", title: "La Pampa grows fast, south of the road", note: "Mostly brown: land mined for the first time" },
  {
    from: 2019,
    to: 2019,
    eyebrow: "2019 · Operation Mercurio",
    title: "New pits keep opening; many pits stop",
    note: `La Pampa: new land ${fmt(flow(2019, "lapampa").new)} ha, stopped ${fmt(flow(2019, "lapampa").stopped)} ha`,
  },
  {
    from: 2020,
    to: 2021,
    eyebrow: "2020–2021 · Mercurio and what followed",
    title: "La Pampa's net additions near zero; across the road they rise",
    note: "COVID-19 from March 2020 · Plan Restauración 2021",
  },
  {
    from: 2022,
    to: 2024,
    eyebrow: "2022–2024 · later years",
    title: "Mining comes back, much of it on old pits",
    note: "Amber: old pits mined again. State of emergency from April 2023",
  },
  {
    from: 2025,
    to: 2025,
    eyebrow: "2025",
    title: "The navy leaves the river posts",
    note: `Net additions inside Tambopata National Reserve: +${fmt(data.reserve_net_2025_ha)} ha in 2025`,
  },
];

const AX_X0 = 130;
const AX_X1 = 1790;
const AX_Y = 990;
const xOf = (t: number) => AX_X0 + ((t - FIRST) / (LAST + 1 - FIRST)) * (AX_X1 - AX_X0);

const PARTS: [Exclude<Part, "net">, string, string][] = [
  ["new", "New land", T.new],
  ["remined", "Re-mined", T.remined],
  ["stopped", "Stopped", T.stopped],
];

export const MiningTimeline: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const starts: Record<number, number> = {};
  let f = INTRO_S * fps;
  for (const y of YEARS) {
    starts[y] = f;
    f += secondsFor(y) * fps;
  }
  const endYears = f;
  const len = (y: number) => secondsFor(y) * fps;

  let tNow = FIRST;
  for (const y of YEARS) if (frame >= starts[y]) tNow = y + Math.min(1, (frame - starts[y]) / len(y));
  const curYear = Math.min(LAST, Math.floor(tNow));
  const outro = frame >= endYears;

  // grey stock: crossfade from last year's to this year's
  const stockOpacity = (y: number) => {
    if (y === FIRST - 1) return frame < starts[FIRST] + 8 ? 1 : 0;
    const s = starts[y];
    const nextStart = y < LAST ? starts[y + 1] : Infinity;
    if (frame < s) return 0;
    return Math.min(interpolate(frame, [s, s + 8], [0, 1], clamp), frame >= nextStart + 8 ? 0 : 1);
  };
  // this year's flows: on for the year, fade at the end
  const flowOpacity = (y: number) => {
    const s = starts[y];
    const e = s + len(y);
    if (frame < s) return 0;
    return Math.min(interpolate(frame, [s, s + 8], [0, 1], clamp), interpolate(frame, [e - 4, e + 0.5 * fps], [1, 0], { ...clamp, easing: easeOut }));
  };

  const chapterOpacity = (c: (typeof CHAPTERS)[number]) => {
    if (outro) return 0;
    const s = starts[c.from];
    const e = starts[c.to] + len(c.to);
    return Math.min(interpolate(frame, [s, s + 10], [0, 1], clamp), interpolate(frame, [e - 8, e], [1, 0], clamp));
  };

  const v = (u: Unit, p: Part) => {
    const cur = flow(curYear, u)[p];
    const prev = curYear > FIRST ? flow(curYear - 1, u)[p] : 0;
    return interpolate(frame, [starts[curYear], starts[curYear] + 12], [prev, cur], { ...clamp, easing: easeOut });
  };
  const maxV = Math.max(...YEARS.flatMap((y) => (["lapampa", "corridor_across"] as Unit[]).flatMap((u) => PARTS.map(([p]) => flow(y, u)[p]))));
  const counterOpacity = fadeIn(frame, starts[FIRST] - 10) * (outro ? interpolate(frame, [endYears, endYears + 10], [1, 0], clamp) : 1);
  const BAR_W = PANEL.w - 2 * 22 - 150;

  return (
    <AbsoluteFill style={{ fontFamily: FONT }}>
      <Background />
      <MapFrame>
        <Layer src="layer_base.png" opacity={1} />
        <Layer src="layer_zones.png" opacity={0.85} />
        <Layer src="layer_rivers.png" opacity={0.9} />
        <Layer src="layer_corridor.png" opacity={0.55} />
        <Layer src="layer_highway.png" opacity={1} />
        <Layer src={`stock_${FIRST - 1}.png`} opacity={stockOpacity(FIRST - 1)} />
        {YEARS.map((y) => (
          <React.Fragment key={y}>
            <Layer src={`stock_${y}.png`} opacity={stockOpacity(y)} />
            <Layer src={`flows_${y}.png`} opacity={flowOpacity(y)} />
          </React.Fragment>
        ))}
        <Layer src="layer_across_w.png" opacity={0.9} />
        <Layer src="layer_lapampa_w.png" opacity={0.9} />
        <MapLabel x={965} y={655} text="La Pampa" opacity={1} size={42} weight={700} />
        <MapLabel x={965} y={432} text="Across the road" opacity={1} color="#cfe5f5" size={36} weight={700} />
        <MapLabel x={1440} y={745} text="Tambopata National Reserve" opacity={chapterOpacity(CHAPTERS[CHAPTERS.length - 1])} size={32} />
      </MapFrame>

      {CHAPTERS.map((c) => (
        <PanelCaption key={c.eyebrow} eyebrow={c.eyebrow} title={c.title} note={c.note} opacity={chapterOpacity(c)} titleSize={38} />
      ))}
      <PanelCaption
        eyebrow="What the map can't show"
        title="Satellites can't see river dredges or mercury"
        note="Description, not cause: land mapped as mining, legal and illegal alike"
        opacity={fadeIn(frame, endYears + 6)}
        titleSize={40}
      />

      {/* counter: net additions this year = new + re-mined − stopped */}
      <div
        style={{
          position: "absolute",
          left: PANEL.x,
          top: 372,
          width: PANEL.w,
          padding: "18px 22px 18px",
          background: T.slatePanel,
          opacity: counterOpacity,
          color: T.offwhite,
        }}
      >
        <div style={{ fontSize: 72, fontWeight: 300, lineHeight: 1, fontVariantNumeric: "tabular-nums" }}>{curYear}</div>
        <div style={{ fontSize: 21, color: T.muted, lineHeight: 1.25, marginTop: 6, whiteSpace: "nowrap" }}>
          Net additions, ha = new + re-mined − stopped
        </div>
        {(
          [
            ["lapampa", "La Pampa"],
            ["corridor_across", "Across the road"],
          ] as const
        ).map(([u, name]) => (
          <div key={u} style={{ marginTop: 14 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", fontSize: 26 }}>
              <span>{name}</span>
              <span style={{ fontSize: 32, fontWeight: 500, fontVariantNumeric: "tabular-nums" }}>net {signed(v(u, "net"))}</span>
            </div>
            {PARTS.map(([p, label, color]) => (
              <div key={p} style={{ display: "flex", alignItems: "center", height: 26, marginTop: 4, fontSize: 20, color: T.muted }}>
                <span style={{ width: 96 }}>{label}</span>
                <div style={{ width: BAR_W, height: 14, background: "rgba(255,255,255,0.08)" }}>
                  <div style={{ height: 14, width: `${(100 * v(u, p)) / maxV}%`, background: color }} />
                </div>
                <span style={{ width: 70, textAlign: "right", fontVariantNumeric: "tabular-nums", color: T.offwhite }}>
                  {p === "stopped" ? "−" : "+"}
                  {fmt(v(u, p))}
                </span>
              </div>
            ))}
          </div>
        ))}
      </div>

      {/* Zeitstrahl */}
      <div style={{ position: "absolute", left: 24, right: 24, top: 868, bottom: 12, background: T.slatePanel }} />
      <div style={{ position: "absolute", left: AX_X0, width: AX_X1 - AX_X0, top: AX_Y, height: 3, background: "rgba(243,245,242,0.35)" }} />
      <div style={{ position: "absolute", left: AX_X0, width: xOf(tNow) - AX_X0, top: AX_Y - 1, height: 5, background: T.offwhite }} />
      {YEARS.map((y) => (
        <div
          key={y}
          style={{
            position: "absolute",
            left: xOf(y + 0.5),
            top: AX_Y + 16,
            translate: "-50% 0",
            fontSize: 28,
            fontWeight: y === curYear ? 700 : 400,
            color: y === curYear ? T.offwhite : y <= curYear ? T.muted : "rgba(195,208,207,0.45)",
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {y}
        </div>
      ))}
      {PINS.map((p, i) => {
        const shown = interpolate(tNow, [p.t, p.t + 0.12], [0, 1], clamp);
        const top = i % 2 === 0 ? 884 : 926;
        const active = tNow >= p.t && tNow < p.t + 1.3;
        return (
          <React.Fragment key={p.label}>
            <div
              style={{
                position: "absolute",
                left: xOf(p.t) - 1.5,
                top: top + 38,
                height: AX_Y - top - 38,
                width: 3,
                background: p.main ? T.offwhite : T.muted,
                opacity: shown * 0.8,
              }}
            />
            <div
              style={{
                position: "absolute",
                left: xOf(p.t),
                top,
                translate: "-50% 0",
                whiteSpace: "nowrap",
                fontSize: 30,
                fontWeight: active || p.main ? 700 : 400,
                color: p.main || active ? T.offwhite : T.muted,
                opacity: shown,
              }}
            >
              {p.label}
            </div>
          </React.Fragment>
        );
      })}
      {/* legend for the map flows, left of the axis start */}
      <div style={{ position: "absolute", left: 40, top: 880, display: "flex", gap: 22, fontSize: 24, color: T.offwhite }}>
        {PARTS.map(([p, label, color]) => (
          <div key={p} style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <div style={{ width: 20, height: 20, background: color, borderRadius: 3 }} />
            {label}
          </div>
        ))}
        <div style={{ display: "flex", alignItems: "center", gap: 8, color: T.muted }}>
          <div style={{ width: 20, height: 20, background: T.grey, opacity: 0.6, borderRadius: 3 }} />
          mining that year
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          left: xOf(tNow),
          top: AX_Y + 1.5,
          translate: "-50% -50%",
          width: 26,
          height: 26,
          borderRadius: 13,
          border: `4px solid ${T.offwhite}`,
          background: T.slate,
        }}
      />
      <SourceLine text="MapBiomas Peru Collection 4 (30 m, class 4.2 mining); SERNANP; INGEMMET; RAISG · our pixel accounting (code/raster_zones.py)" under />
    </AbsoluteFill>
  );
};
