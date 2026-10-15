import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { Background, FONT, Layer, MapFrame, MapLabel, PANEL, PanelCaption, SourceLine, T, YearKey, clamp, data, easeOut, fadeIn } from "./shared";

// Pace: quick through 2008-2018, slower from Mercurio on. Seconds per year.
const FIRST = 2008;
const LAST = 2025;
const YEARS = Array.from({ length: LAST - FIRST + 1 }, (_, i) => FIRST + i);
const INTRO_S = 2;
const FAST_S = 1.6;
const SLOW_S = 3;
const OUTRO_S = 5;
const secondsFor = (y: number) => (y < 2019 ? FAST_S : SLOW_S);

export const timelineSeconds = () => INTRO_S + YEARS.reduce((a, y) => a + secondsFor(y), 0) + OUTRO_S;

// Event pins: fractional year = year + month/12 (months from code/common.py PERU_EVENTS, agent.md, explainer timeline)
const PINS = [
  { t: 2012 + 1 / 12, label: "Legal corridor law", long: "D.L. 1100 corridor, Feb 2012" },
  { t: 2019 + 1.6 / 12, label: "Mercurio", long: "Operation Mercurio, Feb 2019", main: true },
  { t: 2020 + 2 / 12, label: "COVID-19", long: "COVID-19, Mar 2020" },
  { t: 2021 + 6 / 12, label: "Restauración", long: "Plan Restauración, 2021" },
  { t: 2023 + 3 / 12, label: "Emergency", long: "State of emergency, Apr 2023" },
  { t: 2025 + 2 / 12, label: "Navy out", long: "Navy leaves the river posts, 2025" },
];

const fmt = (v: number) => v.toLocaleString("en-US");
const ha = (y: number) => data.first_time_ha[String(y) as YearKey];

const CHAPTERS: { from: number; to: number; eyebrow: string; title: string; note?: string }[] = [
  { from: 2008, to: 2010, eyebrow: "2008–2010", title: "Near La Pampa, most new mining is north of the road" },
  { from: 2011, to: 2018, eyebrow: "2011–2018", title: "New mining moves south of the road, into La Pampa" },
  {
    from: 2019,
    to: 2019,
    eyebrow: "February 2019",
    title: "Operation Mercurio starts in La Pampa",
    note: `First-time mining in La Pampa in 2019: ${fmt(ha(2019).lapampa)} ha`,
  },
  {
    from: 2020,
    to: 2021,
    eyebrow: "2020–2021",
    title: "La Pampa: new mining falls. Across the road: it rises.",
    note: "COVID-19 from March 2020 · Plan Restauración 2021",
  },
  {
    from: 2022,
    to: 2024,
    eyebrow: "2022–2024",
    title: "New mining returns to La Pampa",
    note: "State of emergency from April 2023",
  },
  {
    from: 2025,
    to: 2025,
    eyebrow: "2025",
    title: "Navy leaves the river posts",
    note: `Mining inside Tambopata National Reserve: +${fmt(data.reserve_addition_2025_ha)} ha in 2025`,
  },
];

// Timeline geometry (1920 x 1080 frame)
const AX_X0 = 130;
const AX_X1 = 1790;
const AX_Y = 990;
const xOf = (t: number) => AX_X0 + ((t - FIRST) / (LAST + 1 - FIRST)) * (AX_X1 - AX_X0);

export const MiningTimeline: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // frame schedule
  const starts: Record<number, number> = {};
  let f = INTRO_S * fps;
  for (const y of YEARS) {
    starts[y] = f;
    f += secondsFor(y) * fps;
  }
  const endYears = f;
  const len = (y: number) => secondsFor(y) * fps;

  // playhead (fractional year)
  let tNow = FIRST;
  for (const y of YEARS) {
    if (frame >= starts[y]) tNow = y + Math.min(1, (frame - starts[y]) / len(y));
  }
  if (frame < starts[FIRST]) tNow = FIRST;
  const curYear = Math.min(LAST, Math.floor(tNow === LAST + 1 ? LAST : tNow));
  const outro = frame >= endYears;

  // layers
  const hotOpacity = (y: number) => {
    const s = starts[y];
    const e = s + len(y);
    if (frame < s) return 0;
    return Math.min(
      interpolate(frame, [s, s + 8], [0, 1], clamp),
      interpolate(frame, [e, e + 1.2 * fps], [1, 0], { ...clamp, easing: easeOut }),
    );
  };
  const oldOpacity = (y: number) => interpolate(frame, [starts[y] + len(y), starts[y] + len(y) + 1.2 * fps], [0, 1], clamp);

  const s19 = starts[2019];
  const lpPulse = frame >= s19 && frame < s19 + 2.4 * fps ? interpolate(Math.sin((frame - s19) / 4), [-1, 1], [0.35, 1]) : 1;
  const lpOpacity = frame < s19 ? 0.45 : lpPulse;
  const acrossOpacity =
    interpolate(frame, [s19 + 1.2 * fps, s19 + 2 * fps], [0, 1], clamp) *
    interpolate(frame, [starts[2022], starts[2022] + fps], [1, 0.65], clamp);

  // chapter captions
  const chapterOpacity = (c: (typeof CHAPTERS)[number]) => {
    if (outro) return 0;
    const s = starts[c.from];
    const e = starts[c.to] + len(c.to);
    return Math.min(interpolate(frame, [s, s + 10], [0, 1], clamp), interpolate(frame, [e - 8, e], [1, 0], clamp));
  };

  // counter values (ease from last year's value over the first 12 frames of the year)
  const v = (key: "lapampa" | "across") => {
    const cur = ha(curYear)[key];
    const prev = curYear > FIRST ? ha(curYear - 1)[key] : 0;
    return interpolate(frame, [starts[curYear], starts[curYear] + 12], [prev, cur], { ...clamp, easing: easeOut });
  };
  const maxV = Math.max(...YEARS.map((y) => Math.max(ha(y).lapampa, ha(y).across)));
  const counterOpacity = fadeIn(frame, starts[FIRST] - 10) * (outro ? interpolate(frame, [endYears, endYears + 10], [1, 0], clamp) : 1);

  return (
    <AbsoluteFill style={{ fontFamily: FONT }}>
      <Background />
      <MapFrame>
      <Layer src="layer_base.png" opacity={1} />
      <Layer src="layer_zones.png" opacity={1} />
      <Layer src="layer_rivers.png" opacity={1} />
      <Layer src="layer_corridor.png" opacity={0.75} />
      <Layer src="layer_highway.png" opacity={1} />
      <Layer src="mining_pre2008.png" opacity={1} />
      {YEARS.map((y) => (
        <React.Fragment key={y}>
          <Layer src={`mining_old_${y}.png`} opacity={oldOpacity(y)} />
          <Layer src={`mining_hot_${y}.png`} opacity={hotOpacity(y)} />
        </React.Fragment>
      ))}
      <Layer src="layer_across.png" opacity={acrossOpacity} />
      <Layer src="layer_lapampa.png" opacity={lpOpacity} />

      <MapLabel x={965} y={655} text="La Pampa" opacity={1} color="#ffd0b0" size={42} weight={700} />
      {/* above the outline (not on its top edge): the label is relatively larger inside the scaled map frame */}
      <MapLabel x={965} y={432} text="Across the road" opacity={acrossOpacity} color="#cfe5f5" size={36} weight={700} />

      <MapLabel x={1440} y={745} text="Tambopata National Reserve" opacity={chapterOpacity(CHAPTERS[CHAPTERS.length - 1])} size={32} />

      </MapFrame>

      {CHAPTERS.map((c) => (
        <PanelCaption key={c.eyebrow} eyebrow={c.eyebrow} title={c.title} note={c.note} opacity={chapterOpacity(c)} titleSize={42} />
      ))}
      <PanelCaption
        eyebrow="What the map can't show"
        title="Satellites can't see river dredges or mercury"
        note="Description, not cause: land mapped as mining, legal and illegal alike"
        opacity={fadeIn(frame, endYears + 6)}
        titleSize={42}
      />

      {/* counter: first-time mining this year */}
      <div
        style={{
          position: "absolute",
          left: PANEL.x,
          top: 500,
          width: PANEL.w,
          padding: "22px 26px 26px",
          background: T.slatePanel,
          opacity: counterOpacity,
          color: T.offwhite,
        }}
      >
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between" }}>
          <div style={{ fontSize: 84, fontWeight: 300, lineHeight: 1, fontVariantNumeric: "tabular-nums" }}>{curYear}</div>
          <div style={{ fontSize: 26, color: T.muted, textAlign: "right", lineHeight: 1.2 }}>
            land mined for
            <br />
            the first time
          </div>
        </div>
        {(
          [
            ["lapampa", "La Pampa", T.lapampaBright],
            ["across", "Across the road", T.corridorBright],
          ] as const
        ).map(([key, name, color]) => (
          <div key={key} style={{ marginTop: 18 }}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 32 }}>
              <span>{name}</span>
              <span style={{ fontWeight: 500, fontVariantNumeric: "tabular-nums" }}>{fmt(Math.round(v(key)))} ha</span>
            </div>
            <div style={{ height: 14, marginTop: 8, background: "rgba(255,255,255,0.10)" }}>
              <div style={{ height: 14, width: `${(100 * v(key)) / maxV}%`, background: color }} />
            </div>
          </div>
        ))}
      </div>

      {/* Zeitstrahl */}
      <div style={{ position: "absolute", left: 24, right: 24, top: 868, bottom: 12, background: T.slatePanel }} />
      <div style={{ position: "absolute", left: AX_X0, width: AX_X1 - AX_X0, top: AX_Y, height: 3, background: "rgba(243,245,242,0.35)" }} />
      <div
        style={{ position: "absolute", left: AX_X0, width: xOf(tNow) - AX_X0, top: AX_Y - 1, height: 5, background: T.offwhite }}
      />
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
        const row = i % 2; // alternate rows so neighbours never overlap
        const top = row === 0 ? 884 : 926;
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
                background: p.main ? T.lapampaBright : T.offwhite,
                opacity: shown * 0.8,
              }}
            />
            <div
              style={{
                position: "absolute",
                left: xOf(p.t),
                top: AX_Y + 1.5,
                translate: "-50% -50%",
                width: 18,
                height: 18,
                borderRadius: 9,
                background: p.main ? T.lapampaBright : T.offwhite,
                scale: interpolate(shown, [0, 1], [0.2, 1]),
                opacity: shown,
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
                color: p.main ? T.lapampaBright : active ? T.offwhite : T.muted,
                opacity: shown,
              }}
            >
              {p.label}
            </div>
          </React.Fragment>
        );
      })}
      {/* playhead */}
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
      <SourceLine text="MapBiomas Peru Collection 4 (30 m); SERNANP; INGEMMET; RAISG · yellow = first mapped as mining that year" under />
    </AbsoluteFill>
  );
};
