/* eslint-disable linebreak-style */
/* eslint-disable import/no-extraneous-dependencies */
/* eslint-disable max-len */
/* eslint-disable react/prop-types */
/* eslint-disable max-len */
/* eslint-disable no-console */
import * as React from 'react';
import { useState } from 'react';
import MapGL from 'react-map-gl';
import DeckGL from '@deck.gl/react';
import {
  getIconLayer,
} from '../lib/calls';

// Reference from : https://github.com/visgl/deck.gl/blob/master/docs/api-reference/layers/icon-layer.md
// Reference from : https://deck.gl/docs/developer-guide/interactivity
function Map() {
  const MAPBOX_TOKEN = 'pk.eyJ1IjoibWFyaXNzYWciLCJhIjoiY2t6aXZ5M2FkNGZiNTJ3bmZ1Ymx4cXEzaSJ9.oxEaAW-mjM0Cc9NDNfDQPg'; // Set your mapbox token here

  // Viewport settings
  const INITIAL_VIEW_STATE = {
    longitude: -112.337088,
    latitude: 33.75363564,
    zoom: 12,
    pitch: 0,
    bearing: 0,
  };

  const [viewport, setViewport] = useState({
    latitude: 42.0281,
    longitude: -93.6422,
    zoom: 12,
    bearing: 0,
    pitch: 0,
  });
  const iconlayer = getIconLayer();

  const layers = [
    iconlayer,
  ];

  return (
    <DeckGL
      initialViewState={INITIAL_VIEW_STATE}
      controller
      layers={layers}
    >
      <MapGL
        className="rounded-lg"
        {...viewport}
        width="100%"
        height="30em"
        mapStyle="mapbox://styles/mapbox/light-v10"
        onViewportChange={setViewport}
        mapboxApiAccessToken={MAPBOX_TOKEN}
      />
    </DeckGL>
  );
}

export default Map;
