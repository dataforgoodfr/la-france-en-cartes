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
          paint={{
                  "fill-color": [
                    "case",
                    ["==", ["get", "ips_moyen"], null], "#c9c8c3",
                    ["<", ["get", "ips_moyen"], 50], "#86b6ef",
                    ["<", ["get", "ips_moyen"], 80], "#3987e5",
                    ["<", ["get", "ips_moyen"], 100], "#1c5cab",
                    "#0d366b",
                  ],
                }}
        />
      </Source>

    </Map>

  );
}
