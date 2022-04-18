/* eslint-disable linebreak-style */
/* eslint-disable react/prop-types */
/* eslint-disable max-len */
/* eslint-disable no-console */
/* eslint-disable import/no-extraneous-dependencies */
import DeckGL from '@deck.gl/react';
import { useState } from 'react';
import MapGL from 'react-map-gl';
import {
  getLineLayer, getIconLayer,
} from '../lib/calls';

function IconWithConnectionMap() {
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

  // const data = getConnections();
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
  const lineLayer = getLineLayer();

  const [hoverInfo, iconLayer] = getIconLayer();

  const layers = [
    iconLayer, lineLayer,
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
      {hoverInfo.object && (
        // <div style={{position: 'absolute', zIndex: 1, pointerEvents: 'none', left: hoverInfo.x, top: hoverInfo.y}}>
        <div style={{
          position: 'absolute', zIndex: 1, pointerEvents: 'none', left: 0, top: 0,
        }}
        >
          <div className="max-w-md py-4 px-8 bg-white shadow-lg rounded-lg my-20">
            <div>
              <h2 className="text-gray-800 text-3xl font-semibold">
                Node id:
                { hoverInfo.object.nodeid }
              </h2>
            </div>
          </div>
        </div>
      )}
    </DeckGL>
  );
}

export default IconWithConnectionMap;
