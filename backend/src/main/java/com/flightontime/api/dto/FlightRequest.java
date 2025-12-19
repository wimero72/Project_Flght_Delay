package com.flightontime.api.dto;

import lombok.Data;

@Data
public class FlightRequest {
    private String aerolinea;
    private String origen;
    private String destino;
    private String fecha_partida;
    private double distancia_km;
}
