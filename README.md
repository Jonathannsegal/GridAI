# GridAI

GridAI is a comprehensive platform for monitoring, analyzing, and interacting with power grid data. It combines real-time data visualization, machine learning for anomaly detection and prediction, and a voice-activated assistant for natural language queries.

## 🚀 Features

*   **Interactive Dashboard:** A Next.js-based frontend for visualizing power grid topology, consumption, and generation data.
*   **AI Assistant:** A Python-based service that integrates with Google Assistant to answer natural language queries about the grid status.
*   **Machine Learning:** Dedicated modules for anomaly detection and load prediction.
*   **Robust Backend:**
    *   **API:** A Go REST API for efficient data retrieval.
    *   **Data Stores:** Uses InfluxDB for time-series data and Neo4j for topological graph data.

## 📂 Repository Structure

*   `api/`: Go REST API service. Contains the backend logic and Swagger documentation.
*   `assistant/`: Python service acting as a webhook for Google Assistant. Handles voice commands and NLP.
*   `data/`: Configuration and scripts for InfluxDB (time-series) and Neo4j (graph) databases.
*   `documentation/`: Project documentation and OpenDSS datasets (`PowerGridDataSets`).
*   `frontend/`: A Next.js (React) web application for the user interface.
*   `ml/`: Machine learning components for anomaly detection and prediction.

## 💻 Development & Deployment

This project relies on Docker for containerization. Each major component (`api`, `assistant`, `frontend`, `data/influx`, `data/neo4j`) contains its own `Dockerfile` for easier deployment.

### Frontend
Located in `frontend/`.
To run locally:
```bash
cd frontend
npm install
npm run dev
```
See `frontend/README.md` for detailed instructions on Docker and Google Cloud Run deployment.

### Assistant
Located in `assistant/`.
Designed to be deployed as a webhook for [Actions on Google](https://developers.google.com/assistant/conversational/overview).

### API
Located in `api/`.
A Go service that acts as the interface between the data layers and the frontend/assistant.

## 🤝 Contributing

1.  Clone the repository:
    ```bash
    git clone https://github.com/Jonathannsegal/GridAI.git
    cd GridAI
    ```
2.  Create a feature branch: `git checkout -b my-new-feature`
3.  Commit your changes: `git commit -am 'Add some feature'`
4.  Push to the branch: `git push origin my-new-feature`
5.  Open a pull request.
