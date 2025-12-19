package com.flightontime.api.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class FlightResponse {
    private String prevision;
    private double probabilidad;
}
