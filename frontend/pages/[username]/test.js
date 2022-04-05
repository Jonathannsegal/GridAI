// /* eslint-disable react/prop-types */
/* eslint-disable no-trailing-spaces */
/* eslint-disable no-multiple-empty-lines */
/* eslint-disable max-len */
/* eslint-disable indent */
/* eslint-disable no-unused-vars */
// import { getUserWithUsername} from '../../lib/firebase';
// // import {GeoJsonLayer, ArcLayer} from 'deck.gl';

// /**
//  * Look at index.js for examples with MapBox, also w react example: https://docs.mapbox.com/help/tutorials/use-mapbox-gl-js-with-react/
//  * Kinda want this look: https://docs.mapbox.com/help/tutorials/create-interactive-hover-effects-with-mapbox-gl-js/
//  * Geojason: {"type":"FeatureCollection","features":[{"type":"Point","coordinates":[85.3235970368767,23.317724598996193]}},{"type":"Point","coordinates":[85.3235970368767,23.317724598996193]}}]}
//  * @param {*} param0 
//  * @returns 
//  */
// export async function getServerSideProps({ query }) {
//   const { username } = query;

//   const userDoc = await getUserWithUsername(username);

//   // If no user, short circuit to 404 page
//   if (!userDoc) {
//     return {
//       notFound: true,
//     };
//   }

//   // JSON serializable data
//   let user = null;

//   if (userDoc) {
//     user = userDoc.data();
//   }

//   return {
//     props: { user },
//   };
// }

// export default function UserProfilePage() {
//   // const AIR_PORTS =
//   // 'https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_10m_airports.geojson';

// // const INITIAL_VIEW_STATE = {
// //   latitude: 51.47,
// //   longitude: 0.45,
// //   zoom: 4,
// //   bearing: 0,
// //   pitch: 30
// // };

// // const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/positron-nolabels-gl-style/style.json';
// // const NAV_CONTROL_STYLE = {
// //   position: 'absolute',
// //   top: 10,
// //   left: 10
// // };

  const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/positron-nolabels-gl-style/style.json';
  const NAV_CONTROL_STYLE = {
    position: 'absolute',
    top: 10,
    left: 10,
  };

//   // const onClick = info => {
//   //   if (info.object) {
//   //     // eslint-disable-next-line
//   //     alert(`${info.object.properties.name} (${info.object.properties.abbrev})`);
//   //   }
//   // };

//   // const layers = [
//   //   new GeoJsonLayer({
//   //     id: 'airports',
//   //     data: AIR_PORTS,
//   //     // Styles
//   //     filled: true,
//   //     pointRadiusMinPixels: 2,
//   //     pointRadiusScale: 2000,
//   //     getPointRadius: f => 11 - f.properties.scalerank,
//   //     getFillColor: [200, 0, 80, 180],
//   //     // Interactive props
//   //     pickable: true,
//   //     autoHighlight: true,
//   //     onClick
//   //   }),
//   //   new ArcLayer({
//   //     id: 'arcs',
//   //     data: AIR_PORTS,
//   //     dataTransform: d => d.features.filter(f => f.properties.scalerank < 4),
//   //     // Styles
//   //     getSourcePosition: [-0.4531566, 51.4709959], // London
//   //     getTargetPosition: f => f.geometry.coordinates,
//   //     getSourceColor: [0, 128, 200],
//   //     getTargetColor: [200, 0, 80],
//   //     getWidth: 1
//   //   })
//   // ];

//   var codeBlock = '<html lang="en">' +
//   '<head>'+
//     '<meta charset="utf-8" />'+
//     '<title>Create interactive hover effects with Mapbox GL JS</title>'+
//     '<meta name="viewport" content="width=device-width, initial-scale=1" />'+
//     '<script src="https://api.tiles.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.js"></script>'+
//     '<link href="https://api.tiles.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.css" rel="stylesheet" />'+
//     '<style>'+
//       'body {'+
//         'margin: 0;'+
//         'padding: 0;'+
//       '}'+
//       '#map {'+
//         'position: absolute;'+
//         'top: 0;'+
//         'bottom: 0;'+
//         'width: 100%;'+
//       '}'+
//     '</style>'+
//   '</head>'+
//   '<body>'+
//     '<div id="map"></div>'+
//     '<script>'+
//       'mapboxgl.accessToken = "pk.eyJ1IjoibWFyaXNzYWciLCJhIjoiY2t6aXZ5M2FkNGZiNTJ3bmZ1Ymx4cXEzaSJ9.oxEaAW-mjM0Cc9NDNfDQPg";'+
//       'const map = new mapboxgl.Map({'+
//         'container: "map", // Specify the container ID'+
//         'style: "mapbox://styles/mapbox/outdoors-v11", // Specify which map style to use'+
//         'center: [-122.44121, 37.76132], // Specify the starting position [lng, lat]'+
//         'zoom: 3.5 // Specify the starting zoom'+
//       '});'+
//     '</script>'+
  
//   '</body>'+
//   '</html>'

//   // var doc = document.getElementById("wrapper").innerHTML = codeBlock
//   return( codeBlock
//   );
// }
