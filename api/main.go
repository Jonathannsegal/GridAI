package main

import (
	"bufio"
	"bytes"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
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

type Node struct {
	// id       int
	Node     string     `json:"nodeid"`
	Position [2]float64 `json:"coordinates"`
}
type Coords struct {
	Long float32 `json:"long"`
	Lat  float32 `json:"lat"`
}
type Position struct {
	Longitude float64 `json:"lng"`
	Latitude  float64 `json:"lat"`
}
type Anomalies struct {
	Ids []int `json:"anomalies"`
}

type ServiceId int
const (
    Influx ServiceId = iota
    Neo4j
    Anomoly
    Prediction
	NUM_SERVICES
)

type Service struct {
	id      ServiceId
	name    string
	baseurl string
}

services := []Service {
	Service {
		id:      Influx
		name:    "influx"
		baseurl: "https://data-influx-kxcfw5balq-uc.a.run.app"
	}
	Service {
		id:      Neo4j
		name:    "neo4j"
		baseurl: "https://data-neo4j-kxcfw5balq-uc.a.run.app"
	}
	Service {
		id:      Anomoly
		name:    "anomoly"
		baseurl: "https://ml-anomaly-kxcfw5balq-uc.a.run.app"
	}
	Service {
		id:      Prediction
		name:    "prediction"
		baseurl: "https://ml-prediction-kxcfw5balq-uc.a.run.app"
	}
	Service {
		id:      Assistant
		name:    "assistant"
		baseurl: "https://assistant-kxcfw5balq-uc.a.run.app"
	}
}

func main() {
	// ACAO := os.Getenv("ACAO")
	godotenv.Load()

	log.Println("starting API server ")
	//create a new router
	router := mux.NewRouter()
	log.Println("creating routes")
	// fmt.Println("ACAO:", os.Getenv("ACAO"))

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

	router.HandleFunc("/getALl/{busid}", getAll).Methods("GET")
	router.HandleFunc("/getCurrentVoltage/{busid}", getCurrentVoltage).Methods("GET")
	router.HandleFunc("/getCoordinates/{busid}", getCoordinates).Methods("GET")
	router.HandleFunc("/getAllCoordinates", getAllCoordinates).Methods("GET")
	router.HandleFunc("/getNextHourVoltage/{busid}", getNextHourVoltage).Methods("GET")
	router.HandleFunc("/getCurrentAnomalies", getCurrentAnomalies).Methods("GET")
	router.HandleFunc("/sendTextRequest", sendTextRequest).Methods("POST")
	router.HandleFunc("/health-check", HealthCheck).Methods("GET")
	http.Handle("/", router)

	//start and listen to requests
	http.ListenAndServe(":8080", router)

}

func GetNodes(w http.ResponseWriter, r *http.Request) {
	log.Println("Calling neo4j service ")
	w.WriteHeader(http.StatusOK)
	response, err := http.Get(services[Neo4j].baseurl + "/getNodes")

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
	var response := make(map[string]string, len(services))

	for i, service := range services {
		pingurl := service.baseurl + "/ping"

		response, err := http.Get(pingurl)
		if err != nil {
			fmt.Print(err.Error())
			os.Exit(1)
		}

		responseData, err := ioutil.ReadAll(response.Body)
		if err != nil {
			log.Fatal(err)
		}
		if strings.Contains(string(responseData), "pong") {
			response[service.name] = "Live"
		} else {
			response[service.name] = "Down"
		}
	}

	w.Header().Set("Access-Control-Allow-Origin", os.Getenv("ACAO"))
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

func getAll(w http.ResponseWriter, r *http.Request) {
	response, err := http.Get(services[Neo4j].baseurl + "/getCoords")
	if err != nil {
		fmt.Print(err.Error())
		os.Exit(1)
	}

	responseData, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Fatal(err)
	}

	var lines []string
	sc := bufio.NewScanner(strings.NewReader(string(responseData)))
	for sc.Scan() {
		lines = append(lines, sc.Text())
	}
	fmt.Print(lines)

	var Nodes []Node

	for _, i := range lines {
		words := strings.Fields(i)
		var node Node
		node.Node = words[1]
		if s, err := strconv.ParseFloat(words[2], 64); err == nil {
			node.Position[0] = s
		}
		if s, err := strconv.ParseFloat(words[3], 64); err == nil {
			node.Position[1] = s
		}
		Nodes = append(Nodes, node)
	}
	w.Header().Set("Access-Control-Allow-Origin", os.Getenv("ACAO"))
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	jsonResponse, err := json.Marshal(Nodes)
	if err != nil {
		return
	}
	w.Write(jsonResponse)
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
	w.Header().Set("Access-Control-Allow-Origin", os.Getenv("ACAO"))
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
	w.Header().Set("Access-Control-Allow-Origin", os.Getenv("ACAO"))
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		return
	}
	w.Write(jsonResponse)
}

func getAllCoordinates(w http.ResponseWriter, r *http.Request) {
	response, err := http.Get(services[Neo4j].baseurl + "/getCoords")
	if err != nil {
		fmt.Print(err.Error())
		os.Exit(1)
	}

	responseData, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Fatal(err)
	}

	var lines []string
	sc := bufio.NewScanner(strings.NewReader(string(responseData)))
	for sc.Scan() {
		lines = append(lines, sc.Text())
	}
	fmt.Print(lines)

	var Nodes []Node

	for _, i := range lines {
		words := strings.Fields(i)
		var node Node
		node.Node = words[1]
		if s, err := strconv.ParseFloat(words[2], 64); err == nil {
			node.Position[0] = s
		}
		if s, err := strconv.ParseFloat(words[3], 64); err == nil {
			node.Position[1] = s
		}
		Nodes = append(Nodes, node)
	}
	w.Header().Set("Access-Control-Allow-Origin", os.Getenv("ACAO"))
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	jsonResponse, err := json.Marshal(Nodes)
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
	w.Header().Set("Access-Control-Allow-Origin", os.Getenv("ACAO"))
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
	w.Header().Set("Access-Control-Allow-Origin", os.Getenv("ACAO"))
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		return
	}
	w.Write(jsonResponse)
}

func sendTextRequest(w http.ResponseWriter, r *http.Request) {
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		panic(err)
	}
	responseBody := bytes.NewBuffer(body)

	response, err := http.Post(services[Assistant].baseurl + "/text", "application/json", responseBody)
	if err != nil {
		fmt.Print(err.Error())
		os.Exit(1)
	}

	responseData, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Fatal(err)
	}

	w.Header().Set("Access-Control-Allow-Origin", os.Getenv("ACAO"))
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	jsonResponse, err := json.Marshal(responseData)
	if err != nil {
		return
	}
	var input = string(jsonResponse)
	input = input[1 : len(input)-1]

	rawDecodedText, err := base64.StdEncoding.DecodeString(input)
	if err != nil {
		panic(err)
	}

	w.Write(rawDecodedText)
}
