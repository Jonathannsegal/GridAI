/* eslint-disable linebreak-style */
/* eslint-disable react/prop-types */
/* eslint-disable max-len */
/* eslint-disable no-console */
/* eslint-disable import/no-extraneous-dependencies */
import DeckGL from '@deck.gl/react';
import { useState } from 'react';
import { LineLayerComp } from 'LineLayer';
import MapGL from 'react-map-gl';

function ConnectionMap() {
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

  /**
   * Data format:
   * [
   *   {
   *     inbound: 72633,
   *     outbound: 74735,
   *     from: {
   *       name: '19th St. Oakland (19TH)',
   *       coordinates: [-122.269029, 37.80787]
   *     },
   *     to: {
   *       name: '12th St. Oakland City Center (12TH)',
   *       coordinates: [-122.271604, 37.803664]
   *   },
   *   ...
   * ]
   */
  const layer = LineLayerComp();

  return (
    <DeckGL
      initialViewState={INITIAL_VIEW_STATE}
      controller
      layers={layer}
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

export default ConnectionMap;
