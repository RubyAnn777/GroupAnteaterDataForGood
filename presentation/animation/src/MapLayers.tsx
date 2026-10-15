import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { Background, FONT, Layer, MapFrame, MapLabel, PANEL, PanelCaption, SourceLine, T, clamp, fadeIn } from "./shared";

// Storyline v3, slide 4: four steps, one layer each: zones -> highway -> corridor -> La Pampa. STEP seconds each.
export const STEP_SECONDS = 5;
const STEPS = 4;
export const MAP_LAYERS_FRAMES = (STEPS * STEP_SECONDS + 1) * 30;
const MAP_TOP = 110; // no timeline here: centre the map vertically

const CAPTIONS = [
  {
    eyebrow: "1 · Protected areas",
    title: "Tambopata: a reserve ringed by its buffer zone",
    note: "Green: reserves and parks · grey-green: buffer zones, whole (Tambopata's includes Kotsimba) · pink: native communities",
  },
  {
    eyebrow: "2 · The road",
    title: "The Interoceanic Highway runs along the buffer zone",
    note: "Blue lines: rivers. Alluvial gold sits in their floodplains.",
  },
  {
    eyebrow: "3 · The law",
    title: "Whether mining is legal depends on where it happens",
    note: "Blue: D.L. 1100 corridor (2012), where small-scale mining can be permitted. Buffer zone, reserve: a crime. Satellites can't tell which.",
  },
  {
    eyebrow: "4 · The target",
    title: "La Pampa: one road away from legal mining land",
    note: "Orange: La Pampa sector, the buffer zone's 70.15–69.80° W part (our boundary) · blue outline: corridor across the road · grey: mined by 2018",
  },
];

/** clean = full-bleed map without the caption panel (stills for the deck). */
export const MapLayers: React.FC<{ clean?: boolean }> = ({ clean = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const step = STEP_SECONDS * fps;
  const at = (k: number) => k * step;
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
        <Layer src="layer_rivers.png" opacity={0.35 + 0.65 * fadeIn(frame, at(1))} />
        <Layer src="layer_zones.png" opacity={fadeIn(frame, at(0))} />
        <Layer src="layer_highway.png" opacity={fadeIn(frame, at(1))} />
        <Layer src="layer_corridor.png" opacity={fadeIn(frame, at(2))} />
        <Layer src="mining_by2018.png" opacity={fadeIn(frame, at(3) + 10, 24)} />
        <Layer src="layer_across.png" opacity={fadeIn(frame, at(3) + 30)} />
        <Layer
          src="layer_lapampa.png"
          opacity={fadeIn(frame, at(3)) * interpolate(Math.sin((frame - at(3)) / 7), [-1, 1], [0.75, 1])}
        />

        <MapLabel x={1440} y={745} text="Tambopata National Reserve" opacity={lab(0)} />
        <MapLabel x={1410} y={578} text="Tambopata buffer zone" opacity={lab(0)} size={32} />
        <MapLabel x={250} y={540} text="Amarakaeri buffer zone" opacity={lab(0)} />
        <MapLabel x={700} y={900} text="Native community" opacity={lab(0)} color="#f3b2cd" size={32} />
        <MapLabel x={180} y={985} text="Interoceanic Highway" opacity={lab(1)} align="left" weight={700} />
        <MapLabel x={560} y={432} text="Legal mining corridor (D.L. 1100)" opacity={lab(2)} color="#cfe5f5" weight={700} />
        <MapLabel x={965} y={650} text="La Pampa" opacity={lab(3)} color="#ffd0b0" size={44} weight={700} />
        <MapLabel x={965} y={512} text="Across the road" opacity={fadeIn(frame, at(3) + 40)} color="#cfe5f5" size={36} weight={700} />
      </MapFrame>

      {clean ? null : (
        <>
          {CAPTIONS.map((c, k) => (
            <PanelCaption key={c.eyebrow} eyebrow={c.eyebrow} title={c.title} note={c.note} opacity={capOpacity(k)} top={MAP_TOP} />
          ))}
          <div style={{ position: "absolute", left: PANEL.x, top: MAP_TOP + 600, width: PANEL.w, fontFamily: FONT }}>
            {["Protected areas", "The road", "The law", "The target"].map((t, k) => (
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
