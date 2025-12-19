package com.flightontime.api.controller;

import com.flightontime.api.dto.FlightRequest;
import com.flightontime.api.dto.FlightResponse;
import com.flightontime.api.service.FlightService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/predict")
public class FlightController {

    private final FlightService flightService;

    public FlightController(FlightService flightService) {
        this.flightService = flightService;
    }

    @PostMapping
    public ResponseEntity<FlightResponse> predictDelay(@RequestBody FlightRequest request) {
        // Basic validation could go here
        if (request.getAerolinea() == null || request.getOrigen() == null || request.getDestino() == null) {
            return ResponseEntity.badRequest().build();
        }
        
        try {
            FlightResponse response = flightService.getPrediction(request);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }
}
