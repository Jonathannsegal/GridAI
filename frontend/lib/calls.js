/* eslint-disable no-console */
/* eslint-disable import/prefer-default-export */
/* eslint-disable react/prop-types */
/* eslint-disable max-len */
/* eslint-disable no-console */
/* eslint-disable no-return-assign */

// const url = process.env.NEXT_PUBLIC_API_URL;
const url = process.env.NEXT_PUBLIC_API_URL_LOCAL;

// From Influx
export async function getCurrentVoltage() {
  let response1;
  await fetch(`${url}/getCurrentVoltage/1`)
    .then((response) => response.json())
    .then((data) => response1 = data);
  console.log(response1);
  return response1;
}

// From Neo4j
export async function getCoordinates() {
  let response1;
  await fetch(`${url}/getCoordinates/45`)
    .then((response) => response.json())
    .then((data) => response1 = data);
  // This is [long, lat] dummy
  console.log(response1);
  // console.log([{coordinates: [-93.651024,42.027241]}, {coordinates: [-93.7,42.027241]}, {coordinates: [-93.651024,42.03]}])
  // return response;
  return [{ node: 42, coordinates: [-93.651024, 42.027241] }, { node: 53, coordinates: [-93.7, 42.027241] }, { node: 23, coordinates: [-93.651024, 42.03] }];
  // return [{coordinates: [-93.651024,42.027241]}, {coordinates: [-93.7,42.027241]}, {coordinates: [-93.651024,42.03]}];
}

// From Prediction
export function getNextHourVoltage() {
  fetch(`${url}/getNextHourVoltage/45`)
    .then((response) => response.json())
    .then((data) => console.log(data));
}

// From Anomalies
export function getCurrentAnomalies() {
  fetch(`${url}/getCurrentAnomalies`)
    .then((response) => response.json())
    .then((data) => console.log(data));
}

export function sendTextRequest(text) {
  const body = {
    // eslint-disable-next-line comma-dangle
    // eslint-disable-next-line quote-props
    'text': text,
  };
  // let url1 = "https://frontend-next-kxcfw5balq-uc.a.run.app/";
  fetch(`${url}/sendTextRequest`, { method: 'POST', mode: 'no-cors', body: JSON.stringify(body) })
    .then((response) => console.log(response));
  // .then((response) => response.json())
  // .then((data) => console.log(data));
}
