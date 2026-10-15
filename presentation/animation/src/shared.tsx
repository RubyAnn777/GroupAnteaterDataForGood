import React, { createContext, useContext } from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  continueRender,
  delayRender,
  interpolate,
  staticFile,
} from "remotion";
import { loadFont } from "@remotion/fonts";
import mapData from "../public/map_data.json";

// Fonts: Roboto, the face of the FZS-style pages (code/fonts, Apache 2.0)
const fontHandle = delayRender("Loading Roboto");
Promise.all(
  [300, 400, 500, 700].map((w) =>
    loadFont({
      family: "Roboto",
      url: staticFile(`fonts/Roboto-${w}.ttf`),
      weight: String(w),
    }),
  ),
).then(() => continueRender(fontHandle));

export const data = mapData;
export type YearKey = keyof typeof mapData.flows;

// Palette (code/common.py C + the pages' FZS-like tokens)
export const T = {
  ink: "#1f2d33",
  offwhite: "#fbfaf7",
  slate: "#243b42",
  slatePanel: "rgba(24, 40, 45, 0.86)",
  eyebrow: "#a2cf84", // green eyebrow, light variant for the dark map
  muted: "#c3d0cf",
  lapampa: "#d0692f",
  lapampaBright: "#f08a4b",
  corridor: "#2b74a6",
  corridorBright: "#6fb3e6",
  reserve: "#4e9a3a",
  native: "#e26a9c",
  grey: "#b9c2bf",
  // the three parts of net additions, stepped for the dark map (code/slides_map_export.py FLOW)
  new: "#b5683a",
  remined: "#dba21a",
  stopped: "#1fa595",
};

export const FONT = "Roboto, Helvetica Neue, Arial, sans-serif";
export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const easeOut = Easing.bezier(0.16, 1, 0.3, 1);

export const Layer: React.FC<{ src: string; opacity: number }> = ({ src, opacity }) =>
  opacity <= 0.001 ? null : (
    <Img
      src={staticFile(src)}
      style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080, opacity }}
    />
  );

/** Fade 0 -> 1 starting at frame `at` over `dur` frames. */
export const fadeIn = (frame: number, at: number, dur = 18) =>
  interpolate(frame, [at, at + dur], [0, 1], { ...clamp, easing: easeOut });

/** Map labels live inside MapFrame's scaled box; this factor keeps their on-screen size readable
 *  (on-screen size = size * LABEL_SHRINK, independent of the frame scale). */
export const LabelScale = createContext(1);
export const LABEL_SHRINK = 0.82;

/** Layout: map on the left, side panel on the right, (optional) timeline band below. 1920 x 1080 canvas. */
export const FRAME = { x: 24, y: 24, s: 0.745 };          // map box = 1430 x 805
export const MAP_W = 1920 * FRAME.s;
export const MAP_H = 1080 * FRAME.s;
export const PANEL = { x: FRAME.x + MAP_W + 26, y: FRAME.y, w: 1920 - (FRAME.x + MAP_W + 26) - 24 };

/** The full-extent map (all layers are 1920x1080 on one extent) scaled into the left box. */
export const MapFrame: React.FC<{ children: React.ReactNode; full?: boolean; top?: number }> = ({ children, full, top = FRAME.y }) =>
  full ? (
    <AbsoluteFill>{children}</AbsoluteFill>
  ) : (
    <div
      style={{
        position: "absolute",
        left: FRAME.x,
        top,
        width: MAP_W,
        height: MAP_H,
        overflow: "hidden",
        boxShadow: "0 0 0 1px rgba(255,255,255,0.10)",
      }}
    >
      <div style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080, transform: `scale(${FRAME.s})`, transformOrigin: "0 0" }}>
        <LabelScale.Provider value={LABEL_SHRINK / FRAME.s}>{children}</LabelScale.Provider>
      </div>
    </div>
  );

/** Text label on the map with a dark halo so it reads on any layer. */
export const MapLabel: React.FC<{
  x: number;
  y: number;
  text: string;
  opacity: number;
  color?: string;
  size?: number;
  weight?: number;
  align?: "left" | "center" | "right";
}> = ({ x, y, text, opacity, color = T.offwhite, size = 34, weight = 500, align = "center" }) => {
  const k = useContext(LabelScale);
  return (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      translate: align === "center" ? "-50% -50%" : align === "right" ? "-100% -50%" : "0 -50%",
      opacity,
      color,
      fontFamily: FONT,
      fontSize: size * k,
      fontWeight: weight,
      whiteSpace: "nowrap",
      textShadow:
        "0 0 6px rgba(10,20,24,0.95), 0 0 14px rgba(10,20,24,0.85), 0 2px 2px rgba(10,20,24,0.9)",
      letterSpacing: 0.2,
    }}
  >
    {text}
  </div>
  );
};

/** Caption in the right-hand side panel (never over the map). */
export const PanelCaption: React.FC<{
  eyebrow: string;
  title: string;
  note?: string;
  opacity: number;
  top?: number;
  titleSize?: number;
}> = ({ eyebrow, title, note, opacity, top = PANEL.y, titleSize = 46 }) =>
  opacity <= 0.001 ? null : (
    <div
      style={{
        position: "absolute",
        left: PANEL.x,
        top,
        width: PANEL.w,
        paddingLeft: 26,
        borderLeft: `6px solid ${T.eyebrow}`,
        opacity,
        translate: `0 ${interpolate(opacity, [0, 1], [12, 0])}px`,
        fontFamily: FONT,
      }}
    >
      <div style={{ color: T.eyebrow, fontSize: 28, fontWeight: 500, letterSpacing: 2.5, textTransform: "uppercase", marginBottom: 12 }}>
        {eyebrow}
      </div>
      <div style={{ color: T.offwhite, fontSize: titleSize, fontWeight: 400, lineHeight: 1.12 }}>{title}</div>
      {note ? <div style={{ color: T.muted, fontSize: 30, fontWeight: 300, lineHeight: 1.3, marginTop: 16 }}>{note}</div> : null}
    </div>
  );

/** Top-left caption panel: green eyebrow + headline (+ optional note). */
export const Caption: React.FC<{
  eyebrow: string;
  title: string;
  note?: string;
  opacity: number;
  width?: number;
}> = ({ eyebrow, title, note, opacity, width = 760 }) => (
  <div
    style={{
      position: "absolute",
      left: 80,
      top: 64,
      width,
      padding: "26px 34px 28px",
      background: T.slatePanel,
      borderLeft: `6px solid ${T.eyebrow}`,
      opacity,
      translate: `0 ${interpolate(opacity, [0, 1], [12, 0])}px`,
      fontFamily: FONT,
    }}
  >
    <div
      style={{
        color: T.eyebrow,
        fontSize: 30,
        fontWeight: 500,
        letterSpacing: 2.5,
        textTransform: "uppercase",
        marginBottom: 10,
      }}
    >
      {eyebrow}
    </div>
    <div style={{ color: T.offwhite, fontSize: 52, fontWeight: 400, lineHeight: 1.12 }}>{title}</div>
    {note ? (
      <div style={{ color: T.muted, fontSize: 32, fontWeight: 300, lineHeight: 1.3, marginTop: 14 }}>{note}</div>
    ) : null}
  </div>
);

export const SourceLine: React.FC<{ text: string; bottom?: number; under?: boolean; top?: number }> = ({
  text,
  bottom = 22,
  under = false,
  top = FRAME.y,
}) => (
  <div
    style={{
      position: "absolute",
      color: T.muted,
      fontFamily: FONT,
      fontWeight: 400,
      ...(under
        ? { left: FRAME.x, top: top + MAP_H + 6, fontSize: 22, padding: "2px 0", background: "none" }
        : { right: 80, bottom, fontSize: 26, padding: "4px 12px", background: "rgba(24, 40, 45, 0.7)" }),
    }}
  >
    {text}
  </div>
);

export const Background: React.FC = () => <AbsoluteFill style={{ backgroundColor: "#1d3036" }} />;
