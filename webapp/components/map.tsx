'use client';

import { setWorkerUrl } from "maplibre-gl";
import Map from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";

setWorkerUrl(new URL('maplibre-gl/dist/maplibre-gl-worker.mjs', import.meta.url).toString());

export default function MapBAse() {
  return (
    <Map
      initialViewState={{
          bounds: [
            [-5.2, 41.3],
            [9.6, 51.1],
        ],
        fitBoundsOptions: { padding: 24 },
        }}
      style={{ width: "100%", height: "100%" }}
      mapStyle="https://tiles.openfreemap.org/styles/positron"
    />
  );
}
