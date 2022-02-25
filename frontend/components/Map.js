/* eslint-disable import/no-extraneous-dependencies */
/* eslint-disable max-len */
/* eslint-disable react/prop-types */
import * as React from 'react';
import { useState } from 'react';
import MapGL from 'react-map-gl';
import DeckGL from '@deck.gl/react';
import { IconLayer } from '@deck.gl/layers';

function Map() {
  const MAPBOX_TOKEN = 'pk.eyJ1IjoibWFyaXNzYWciLCJhIjoiY2t6aXZ5M2FkNGZiNTJ3bmZ1Ymx4cXEzaSJ9.oxEaAW-mjM0Cc9NDNfDQPg'; // Set your mapbox token here

  // Viewport settings
  const INITIAL_VIEW_STATE = {
    longitude: -93.6422,
    latitude: 42.0281,
    zoom: 12,
    pitch: 0,
    bearing: 0,
  };

  const ICON_MAPPING = {
    marker: {
      x: 0, y: 0, width: 128, height: 128, mask: true,
    },
  };
  // Data to be used by the LineLayer
  // 42.027241, -93.651024
  const data = [{ coordinates: [-93.651024, 42.027241] }, { coordinates: [-93.7, 42.027241] }, { coordinates: [-93.651024, 42.03] }];

  const [viewport, setViewport] = useState({
    latitude: 42.0281,
    longitude: -93.6422,
    zoom: 12,
    bearing: 0,
    pitch: 0,
  });
  const layers = [
    new IconLayer({
      id: 'icon-layer',
      data,
      pickable: true,
      // iconAtlas and iconMapping are required
      // getIcon: return a string
      iconAtlas: 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.png',
      iconMapping: ICON_MAPPING,
      getIcon: () => 'marker',

      sizeScale: 15,
      getPosition: (d) => d.coordinates,
      getSize: () => 5,
      getColor: (d) => [Math.sqrt(d.exits), 140, 0],
    }),
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
