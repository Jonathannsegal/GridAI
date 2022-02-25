/* eslint-disable import/prefer-default-export */

const url = process.env.NEXT_PUBLIC_API_URL;

// From Influx
export function getCurrentVoltage() {
  fetch(`${url}/getCurrentVoltage/1`)
    .then((response) => response.json())
    .then((data) => console.log(data));
}

// From Neo4j
export function getCoordinates() {
  fetch(`${url}/getCoordinates/45`)
    .then((response) => response.json())
    .then((data) => console.log(data));
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

// To Voice Assistant
// TODO: this needs to be fixed
// also need to add a body to send post data not use the url
export function sendTextRequest() {
  fetch(`${url}/sendTextRequest`, { method: 'POST', mode: 'no-cors' })
    .then((response) => console.log(response));
  // .then((response) => response.json())
  // .then((data) => console.log(data));
}
