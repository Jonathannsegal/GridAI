/* eslint-disable linebreak-style */
/* eslint-disable react/prop-types */
/* eslint-disable max-len */
/* eslint-disable no-console */
/* eslint-disable import/no-extraneous-dependencies */
/* eslint-disable react/jsx-boolean-value */
/* eslint-disable no-plusplus */
/* eslint-disable prefer-destructuring */
import React from 'react';
import { StaticMap } from 'react-map-gl';
import { AmbientLight, PointLight, LightingEffect } from '@deck.gl/core';
import { HexagonLayer } from '@deck.gl/aggregation-layers';
import DeckGL from '@deck.gl/react';
import {
  getCoordinatesGeneration,
} from '../lib/calls';

const MAPBOX_TOKEN = 'pk.eyJ1IjoibWFyaXNzYWciLCJhIjoiY2t6aXZ5M2FkNGZiNTJ3bmZ1Ymx4cXEzaSJ9.oxEaAW-mjM0Cc9NDNfDQPg'; // Set your mapbox token here

const ambientLight = new AmbientLight({
  color: [255, 255, 255],
  intensity: 1.0,
});

const pointLight1 = new PointLight({
  color: [255, 255, 255],
  intensity: 0.8,
  position: [-0.144528, 49.739968, 80000],
});

const pointLight2 = new PointLight({
  color: [255, 255, 255],
  intensity: 0.8,
  position: [-3.807751, 54.104682, 8000],
});

const lightingEffect = new LightingEffect({ ambientLight, pointLight1, pointLight2 });

const material = {
  ambient: 0.64,
  diffuse: 0.6,
  shininess: 32,
  specularColor: [51, 51, 51],
};

const INITIAL_VIEW_STATE = {
  longitude: -112.3373,
  latitude: 33.745,
  zoom: 13.5,
  minZoom: 0,
  maxZoom: 15,
  pitch: 40.5,
  bearing: -27,
};

// Comment for rerun
// const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json';
const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json';

export const colorRange = [
  [153, 221, 200],
  [149, 191, 116],
  [101, 155, 94],
  [85, 111, 68],
  [40, 63, 59],
  [243, 247, 240],
];

function getTooltip1({ object }) {
  if (!object) {
    return null;
  }
  const lat = object.position[1];
  const lng = object.position[0];
  let point = object.points[0];
  for (let i = 1; i < object.points.length; i++) {
    if (object.points[i].source.active > point.source.active) {
      point = object.points[i];
    }
  }
  const generation = point.source.generated;
  const date = point.source.date;
  const nodeid = point.source.nodeid;
  return `\
    Node Id: ${nodeid};
    Date: ${date};
    Power: ${generation};
    Coordinates: ${lat}, ${lng}`;
}

// function getTooltip2({ object }) {
//   if (!object) {
//     return null;
//   }else{
//     console.log(object);
//   }
//   const lat = object.position[1];
//   const lng = object.position[0];
//   if(object.nodeid.charAt(0) === 'S'){
//     const count = 1;
//   }else{
//     const count = 0;
//   }

//   return `\
//     latitude: ${Number.isFinite(lat) ? lat.toFixed(6) : ''}
//     longitude: ${Number.isFinite(lng) ? lng.toFixed(6) : ''}
//     ${count} Buses`;
// }

// Inspo: https://deck.gl/examples/hexagon-layer/
// Control panel: https://deck.gl/gallery/hexagon-layer
/* eslint-disable react/no-deprecated */
export default function HexagonMap({
  mapStyle = MAP_STYLE,
  radius = 2,
  upperPercentile = 100,
  coverage = 7,
}) {
  const data = getCoordinatesGeneration();
  // console.log(data)
  const layers = [
    new HexagonLayer({
      id: 'heatmap',
      colorRange,
      coverage,
      data,
      elevationRange: [0, 50],
      // elevationScale: data && data.length ? 50 : 0,
      elevationScale: 10,
      extruded: true,
      getPosition: (d) => d.coordinates,
      getElevation: (d) => 10 * d.active,
      pickable: true,
      radius,
      upperPercentile,
      material,

      transitions: {
        elevationScale: 50,
      },
    }),
  ];

  return (
    <DeckGL
      layers={layers}
      effects={[lightingEffect]}
      initialViewState={INITIAL_VIEW_STATE}
      controller={true}
      getTooltip={getTooltip1}
    >
      <StaticMap reuseMaps mapStyle={mapStyle} preventStyleDiffing={true} mapboxApiAccessToken={MAPBOX_TOKEN} />
    </DeckGL>
  );
}
