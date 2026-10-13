import React from "react";
import { Composition } from "remotion";
import { MapLayers } from "./MapLayers";
import { MiningTimeline } from "./MiningTimeline";

// Slide 3: the map built layer by layer (5 steps x 5 s + 1 s hold) = 780 frames.
// Slide 4: 2008-2025, first-time mining year by year, with the Zeitstrahl = 1368 frames (45.6 s).
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MapLayers"
        component={MapLayers}
        durationInFrames={780}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="MiningTimeline"
        component={MiningTimeline}
        durationInFrames={1368}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
