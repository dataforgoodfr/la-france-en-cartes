"use client";

import { useState } from "react";
import { addProtocol, setWorkerUrl } from "maplibre-gl";
import { Map, Source, Layer, type MapLayerMouseEvent } from "react-map-gl/maplibre";
import { Protocol } from "pmtiles";
import "maplibre-gl/dist/maplibre-gl.css";

setWorkerUrl(new URL("maplibre-gl/dist/maplibre-gl-worker.mjs", import.meta.url).toString());
addProtocol("pmtiles", new Protocol().tile);

const nombre = new Intl.NumberFormat("fr-FR", { maximumFractionDigits: 1 });

type Survol = { x: number; y: number; nom: string; valeur: number | null };

export default function MapBase() {
  const [survol, setSurvol] = useState<Survol | null>(null);

  const suivre = (e: MapLayerMouseEvent) => {
    const commune = e.features?.[0];
    if (!commune) {
      setSurvol(null);
      return;
    }
    const v = commune.properties.ips_moyen;
    setSurvol({
      x: e.point.x,
      y: e.point.y,
      nom: commune.properties.nom,
      valeur: typeof v === "number" ? v : null,
    });
  };

  return (
    <div className="relative h-full w-full">
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
        interactiveLayerIds={["communes-aplat"]}
        onMouseMove={suivre}
        onClick={suivre}
        onMouseLeave={() => setSurvol(null)}
      >
        <Source id="communes" type="vector" url="pmtiles:///data/ips_lycees_par_commune.pmtiles">
          <Layer
            id="communes-aplat"
            type="fill"
            source-layer="ips_lycees_par_commune"
            paint={{
              "fill-opacity" : 0.7,
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
      {survol && (
        <div
          className="pointer-events-none absolute z-10 rounded bg-white px-2 py-1 text-sm text-neutral-900 shadow"
          style={{ left: survol.x + 12, top: survol.y + 12 }}
        >
          <div className="font-medium">{survol.nom}</div>
          <div>
            {survol.valeur === null
              ? "Donnée indisponible"
              : `IPS moyen : ${nombre.format(survol.valeur)}`}
          </div>
        </div>
      )}
    </div>
  );
}
