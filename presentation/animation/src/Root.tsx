import React from "react";
import { Composition } from "remotion";
import { MapLayers, MAP_LAYERS_FRAMES } from "./MapLayers";
import { MiningTimeline, timelineSeconds } from "./MiningTimeline";

// Storyline v3, slide 4: the map built layer by layer (zones -> highway -> corridor -> La Pampa).
// Slide 5: 2010-2025, net mining additions as three flows on the map (new land, re-mined, stopped) + a net counter.
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="MapLayers" component={MapLayers} durationInFrames={MAP_LAYERS_FRAMES} fps={30} width={1920} height={1080} />
      <Composition
        id="MiningTimeline"
        component={MiningTimeline}
        durationInFrames={Math.round(timelineSeconds() * 30)}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
