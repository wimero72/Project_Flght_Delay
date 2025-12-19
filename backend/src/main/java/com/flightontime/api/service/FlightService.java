package com.flightontime.api.service;

import com.flightontime.api.dto.FlightRequest;
import com.flightontime.api.dto.FlightResponse;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class FlightService {

    private final WebClient webClient;

    public FlightService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.baseUrl("http://localhost:8000").build();
    }

    public FlightResponse getPrediction(FlightRequest request) {
        // Map request to Python API format (snake_case)
        PythonFlightRequest pythonRequest = new PythonFlightRequest();
        pythonRequest.setAirline(request.getAerolinea());
        pythonRequest.setOrigin(request.getOrigen());
        pythonRequest.setDestination(request.getDestino());
        pythonRequest.setDepartureDate(request.getFecha_partida());
        pythonRequest.setDistance(request.getDistancia_km());

        PythonFlightResponse response = webClient.post()
                .uri("/predict_model")
                .bodyValue(pythonRequest)
                .retrieve()
                .bodyToMono(PythonFlightResponse.class)
                .block(); // Blocking for MVP simplicity, better to use Mono/Flux in real reactive app

        if (response != null) {
            return new FlightResponse(response.getPrediction(), response.getProbability());
        } else {
            throw new RuntimeException("Failed to get prediction from DS service");
        }
    }

    @Data
    private static class PythonFlightRequest {
        private String airline;
        private String origin;
        private String destination;
        @JsonProperty("departure_date")
        private String departureDate;
        private double distance;
    }

    @Data
    private static class PythonFlightResponse {
        private String prediction;
        private double probability;
    }
}
