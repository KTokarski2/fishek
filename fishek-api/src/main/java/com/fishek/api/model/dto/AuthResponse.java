package com.fishek.api.model.dto;

import lombok.Builder;

@Builder
public record AuthResponse(
        String token
) {}
