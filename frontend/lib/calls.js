/* eslint-disable import/prefer-default-export */

const url = 'https://03d8563c-be05-48fc-b7c3-72a89574ac30.mock.pstmn.io';

// From Influx
export function getCurrentVoltage() {
  fetch(`${url}/getCurrentVoltage/45`)
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
export function sendTextRequest() {
  fetch(`${url}/sendTextRequest/getCurrentVoltage/45`, { method: 'POST' })
    .then((response) => response.json())
    .then((data) => console.log(data));
}
