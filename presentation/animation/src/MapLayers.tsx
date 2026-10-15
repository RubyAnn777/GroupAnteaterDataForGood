import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { Background, FONT, Layer, MapFrame, MapLabel, PANEL, PanelCaption, SourceLine, T, clamp, fadeIn } from "./shared";

// Five steps, one layer each (STORYLINE.md slide 3). Each step lasts STEP seconds.
export const STEP_SECONDS = 5;
const MAP_TOP = 110; // no timeline here: centre the map vertically

const MINING_TO_2018 = ["mining_pre2008.png", ...Array.from({ length: 11 }, (_, i) => `mining_old_${2008 + i}.png`)];

const CAPTIONS = [
  {
    eyebrow: "1 · Protected areas",
    title: "Tambopata: a reserve ringed by a buffer zone",
    note: "Green: reserves and parks · grey-green: buffer zones · pink: native communities",
  },
  {
    eyebrow: "2 · The road",
    title: "The Interoceanic Highway runs through the buffer zone",
    note: "La Pampa lies along km 98–115 of the highway",
  },
  {
    eyebrow: "3 · Rivers and gold",
    title: "Alluvial gold sits in river floodplains",
    note: "Grey: land mapped as mining by 2018",
  },
  {
    eyebrow: "4 · The law",
    title: "Whether mining is legal depends on where it happens",
    note: "Blue: D.L. 1100 corridor (2012), where small-scale mining can be permitted. Buffer zone, reserve: a crime. Satellites can't tell which.",
  },
  {
    eyebrow: "5 · The target",
    title: "La Pampa: target of Operation Mercurio, Feb 2019",
    note: "Orange: our La Pampa sector (no official boundary exists) · blue outline: the corridor across the road",
  },
];

/** clean = full-bleed map without the caption panel (stills for the flippable deck slides). */
export const MapLayers: React.FC<{ clean?: boolean }> = ({ clean = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const step = STEP_SECONDS * fps;
  const at = (k: number) => k * step; // start frame of step k (0-based)
  const capOpacity = (k: number) =>
    k === CAPTIONS.length - 1
      ? fadeIn(frame, at(k) + 4)
      : Math.min(fadeIn(frame, at(k) + 4), interpolate(frame, [at(k + 1) - 8, at(k + 1)], [1, 0], clamp));
  const lab = (k: number) => fadeIn(frame, at(k) + 14);

  const current = Math.min(CAPTIONS.length - 1, Math.floor(frame / step));

  return (
    <AbsoluteFill>
      <Background />
      <MapFrame full={clean} top={MAP_TOP}>
      <Layer src="layer_base.png" opacity={1} />
      <Layer src="layer_zones.png" opacity={fadeIn(frame, at(0))} />
      <Layer src="layer_highway.png" opacity={fadeIn(frame, at(1))} />
      <Layer src="layer_rivers.png" opacity={0.35 + 0.65 * fadeIn(frame, at(2))} />
      {MINING_TO_2018.map((src) => (
        <Layer key={src} src={src} opacity={fadeIn(frame, at(2) + 20, 24)} />
      ))}
      <Layer src="layer_corridor.png" opacity={fadeIn(frame, at(3))} />
      <Layer src="layer_across.png" opacity={fadeIn(frame, at(4) + 30)} />
      <Layer
        src="layer_lapampa.png"
        opacity={fadeIn(frame, at(4)) * interpolate(Math.sin((frame - at(4)) / 7), [-1, 1], [0.75, 1])}
      />

      {/* step 1 labels */}
      <MapLabel x={1440} y={745} text="Tambopata National Reserve" opacity={lab(0)} />
      <MapLabel x={1410} y={578} text="Tambopata buffer zone" opacity={lab(0)} size={32} />
      <MapLabel x={250} y={540} text="Amarakaeri buffer zone" opacity={lab(0)} />
      <MapLabel x={700} y={900} text="Native community" opacity={lab(0)} color="#f3b2cd" size={32} />
      {/* step 2 */}
      <MapLabel x={180} y={985} text="Interoceanic Highway" opacity={lab(1)} align="left" weight={700} />
      {/* step 4: placed up-left so it never touches "Across the road" (y 512) or "Amarakaeri buffer zone" (y 540) */}
      <MapLabel x={560} y={432} text="Legal mining corridor (D.L. 1100)" opacity={lab(3)} color="#cfe5f5" weight={700} />
      {/* step 5 */}
      <MapLabel x={965} y={650} text="La Pampa" opacity={lab(4)} color="#ffd0b0" size={44} weight={700} />
      <MapLabel x={965} y={512} text="Across the road" opacity={fadeIn(frame, at(4) + 40)} color="#cfe5f5" size={36} weight={700} />

      </MapFrame>

      {clean ? null : (
        <>
          {CAPTIONS.map((c, k) => (
            <PanelCaption key={c.eyebrow} eyebrow={c.eyebrow} title={c.title} note={c.note} opacity={capOpacity(k)} top={MAP_TOP} />
          ))}
          {/* step list: where we are in the build */}
          <div style={{ position: "absolute", left: PANEL.x, top: MAP_TOP + 560, width: PANEL.w, fontFamily: FONT }}>
            {["Protected areas", "The road", "Rivers and gold", "The law", "The target"].map((t, k) => (
              <div
                key={t}
                style={{
                  display: "flex",
                  gap: 16,
                  alignItems: "baseline",
                  fontSize: 30,
                  lineHeight: 1.6,
                  color: k === current ? T.offwhite : k < current ? T.muted : "rgba(195,208,207,0.4)",
                  fontWeight: k === current ? 500 : 400,
                }}
              >
                <span style={{ color: k === current ? T.eyebrow : "inherit", fontVariantNumeric: "tabular-nums" }}>{k + 1}</span>
                <span>{t}</span>
              </div>
            ))}
          </div>
        </>
      )}
      <SourceLine text="MapBiomas Peru Collection 4 (30 m); SERNANP; INGEMMET; RAISG" under={!clean} top={MAP_TOP} />
    </AbsoluteFill>
  );
};
