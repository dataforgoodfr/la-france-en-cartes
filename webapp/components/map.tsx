'use client';

import { setWorkerUrl, addProtocol,  removeProtocol} from "maplibre-gl";
import { Map, Source, Layer } from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";
import { Protocol } from 'pmtiles';
import { useEffect } from 'react';

setWorkerUrl(new URL('maplibre-gl/dist/maplibre-gl-worker.mjs', import.meta.url).toString());
addProtocol("pmtiles", new Protocol().tile);


export default function MapBase() {
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
      >
      <Source id="communes" type="vector" url="pmtiles:///data/ips_lycees_par_commune.pmtiles">
        <Layer
          id="communes-aplat"
          type="fill"
          source-layer="ips_lycees_par_commune"
          paint={{ "fill-color": "#3987e5", "fill-opacity": 0.8 }}
        />
      </Source>

    </Map>

  );
}
