package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/gorilla/mux"
)

type Bus struct {
	id          int
	Voltage     Voltage     `json:"voltage"`
	NextVoltage NextVoltage `json:"voltage"`
	Coords      Coords      `json:"coords"`
}
type Voltage struct {
	Voltage int `json:"voltage"`
}
type NextVoltage struct {
	Voltage int `json:"voltage"`
}
type Coords struct {
	Long float32 `json:"long"`
	Lat  float32 `json:"lat"`
}
type Anomalies struct {
	Ids []int `json:"anomalies"`
}

type Health struct {
	id         int
	Neo4j      string `json:"neo4j"`
	Influx     string `json:"influx"`
	Anomoly    string `json:"anomoly"`
	Prediction string `json:"prediction"`
}

func main() {
	log.Println("starting API server ")
	//create a new router
	router := mux.NewRouter()
	log.Println("creating routes")

	//neo4j
	router.HandleFunc("/addNode", GetNodes).Methods("POST")
	router.HandleFunc("/getNodes", GetNodes).Methods("GET")

	//influx
	router.HandleFunc("/writeInflux", GetNodes).Methods("POST")
	router.HandleFunc("/readInflux", GetNodes).Methods("GET")

	//anomaly
	router.HandleFunc("/singlePhaseAnom", GetNodes).Methods("GET", "POST")
	router.HandleFunc("/singlePhaseCTAnom", GetNodes).Methods("GET", "POST")
	router.HandleFunc("/threePhaseAnom", GetNodes).Methods("GET", "POST")
	router.HandleFunc("/allAnom", GetNodes).Methods("GET", "POST")

	//prediction
	router.HandleFunc("/singlePhaseAnom", GetNodes).Methods("GET", "POST")
	router.HandleFunc("/singlePhaseCTAnom", GetNodes).Methods("GET", "POST")
	router.HandleFunc("/threePhaseAnom", GetNodes).Methods("GET", "POST")
	router.HandleFunc("/allAnom", GetNodes).Methods("GET", "POST")

	//assistant
	//TODO

	//firebase
	//TODO

	router.HandleFunc("/getCurrentVoltage/{busid}", getCurrentVoltage).Methods("GET")
	router.HandleFunc("/getCoordinates/{busid}", getCoordinates).Methods("GET")
	router.HandleFunc("/getNextHourVoltage/{busid}", getNextHourVoltage).Methods("GET")
	router.HandleFunc("/getCurrentAnomalies", getCurrentAnomalies).Methods("GET")
	router.HandleFunc("/sendTextRequest", sendTextRequest).Methods("POST")
	router.HandleFunc("/health-check", HealthCheck).Methods("GET")
	http.Handle("/", router)

	//start and listen to requests
	http.ListenAndServe(":8080", router)

}

func GetNodes(w http.ResponseWriter, r *http.Request) {
	log.Println("Calling neo4j service")
	w.WriteHeader(http.StatusOK)
	response, err := http.Get("https://neo4j-kxcfw5balq-uc.a.run.app/getNodes")

	if err != nil {
		fmt.Print(err.Error())
		os.Exit(1)
	}

	responseData, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Fatal(err)
	}

	// fmt.Println(string(responseData))
	// fmt.Fprintf(w, "API is up and running")
	fmt.Fprintf(w, "%+v", string(responseData))
}

func HealthCheck(w http.ResponseWriter, r *http.Request) {
	var response Health
	influx_response, err := http.Get("https://influx-kxcfw5balq-uc.a.run.app/ping")
	neo4j_response, err := http.Get("https://neo4j-kxcfw5balq-uc.a.run.app/ping")
	prediction_response, err := http.Get("https://prediction-kxcfw5balq-uc.a.run.app/ping")
	anomoly_response, err := http.Get("https://anomaly-kxcfw5balq-uc.a.run.app/ping")
	if err != nil {
		fmt.Print(err.Error())
		os.Exit(1)
	}
	influx_responseData, err := ioutil.ReadAll(influx_response.Body)
	neo4j_responseData, err := ioutil.ReadAll(neo4j_response.Body)
	prediction_responseData, err := ioutil.ReadAll(prediction_response.Body)
	anomoly_responseData, err := ioutil.ReadAll(anomoly_response.Body)
	if err != nil {
		log.Fatal(err)
	}
	if strings.Contains(string(influx_responseData), "pong") {
		response.Influx = "Live"
	} else {
		response.Influx = "Down"
	}
	if strings.Contains(string(neo4j_responseData), "pong") {
		response.Neo4j = "Live"
	} else {
		response.Neo4j = "Down"
	}
	if strings.Contains(string(prediction_responseData), "pong") {
		response.Anomoly = "Live"
	} else {
		response.Anomoly = "Down"
	}
	if strings.Contains(string(anomoly_responseData), "pong") {
		response.Prediction = "Live"
	} else {
		response.Prediction = "Down"
	}
	w.Header().Set("Access-Control-Allow-Origin", "http://localhost:3000")
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		return
	}
	w.Write(jsonResponse)
}

func prepareResponse() []Bus {
	var Buses []Bus

	var bus Bus
	bus.id = 1
	bus.Voltage.Voltage = 42
	bus.NextVoltage.Voltage = 45
	bus.Coords.Long = 42.0308946
	bus.Coords.Lat = -93.6391486
	Buses = append(Buses, bus)

	bus.id = 2
	bus.Voltage.Voltage = 21
	bus.NextVoltage.Voltage = 23
	bus.Coords.Long = 42.0216387
	bus.Coords.Lat = 93.4512314
	Buses = append(Buses, bus)

	bus.id = 3
	bus.Voltage.Voltage = 97
	bus.NextVoltage.Voltage = 103
	bus.Coords.Long = 42.0554932
	bus.Coords.Lat = -93.8679897
	Buses = append(Buses, bus)
	return Buses
}

func getCurrentVoltage(w http.ResponseWriter, r *http.Request) {
	var response Voltage
	buses := prepareResponse()
	vars := mux.Vars(r)
	intVar, err := strconv.Atoi(vars["busid"])
	for i := range buses {
		if buses[i].id == intVar {
			response = buses[i].Voltage
		}
	}
	w.Header().Set("Access-Control-Allow-Origin", "http://localhost:3000")
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		return
	}
	w.Write(jsonResponse)
}

func getCoordinates(w http.ResponseWriter, r *http.Request) {
	var response Coords
	buses := prepareResponse()
	vars := mux.Vars(r)
	intVar, err := strconv.Atoi(vars["busid"])
	for i := range buses {
		if buses[i].id == intVar {
			response = buses[i].Coords

		}
	}
	w.Header().Set("Access-Control-Allow-Origin", "http://localhost:3000")
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		return
	}
	w.Write(jsonResponse)
}

func getNextHourVoltage(w http.ResponseWriter, r *http.Request) {
	var response NextVoltage
	buses := prepareResponse()
	vars := mux.Vars(r)
	intVar, err := strconv.Atoi(vars["busid"])
	for i := range buses {
		if buses[i].id == intVar {
			response = buses[i].NextVoltage
		}
	}
	w.Header().Set("Access-Control-Allow-Origin", "http://localhost:3000")
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		return
	}
	w.Write(jsonResponse)
}

func getCurrentAnomalies(w http.ResponseWriter, r *http.Request) {
	var response Anomalies
	ids := []int{1, 2, 3}
	response.Ids = ids
	w.Header().Set("Access-Control-Allow-Origin", "http://localhost:3000")
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		return
	}
	w.Write(jsonResponse)
}

func sendTextRequest(w http.ResponseWriter, r *http.Request) {
	var response Voltage
	buses := prepareResponse()
	response = buses[1].Voltage
	w.Header().Set("Access-Control-Allow-Origin", "http://localhost:3000")
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		return
	}
	w.Write(jsonResponse)
}
