package com.fishek.api.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.test.util.ReflectionTestUtils;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class JwtServiceTest {

    private static final String SECRET = "dGVzdC1zZWNyZXQta2V5LXRoYXQtaXMtbG9uZy1lbm91Z2gtZm9yLUhTMjU2";
    private static final long EXPIRATION = 86400000L;
    private static final long EXPIRED = -1000L;
    private static final String USER_EMAIL = "user@test.com";
    private static final String OTHER_EMAIL = "other@test.com";
    private static final String PASSWORD = "pass";
    private static final String SECRET_FIELD = "secret";
    private static final String EXPIRATION_FIELD = "expiration";

    private JwtService jwtService;

    @BeforeEach
    void setUp() {
        jwtService = new JwtService();
        ReflectionTestUtils.setField(jwtService, SECRET_FIELD, SECRET);
        ReflectionTestUtils.setField(jwtService, EXPIRATION_FIELD, EXPIRATION);
    }

    private UserDetails userDetails(String email) {
        return User.withUsername(email).password(PASSWORD).authorities(List.of()).build();
    }

    @Test
    void shouldGenerateToken() {
        String token = jwtService.generateToken(userDetails(USER_EMAIL));
        assertThat(token).isNotBlank();
    }

    @Test
    void shouldExtractEmailFromToken() {
        UserDetails user = userDetails(USER_EMAIL);
        String token = jwtService.generateToken(user);

        assertThat(jwtService.extractEmail(token)).isEqualTo(USER_EMAIL);
    }

    @Test
    void shouldValidateTokenForCorrectUser() {
        UserDetails user = userDetails(USER_EMAIL);
        String token = jwtService.generateToken(user);

        assertThat(jwtService.isTokenValid(token, user)).isTrue();
    }

    @Test
    void shouldRejectTokenForDifferentUser() {
        String token = jwtService.generateToken(userDetails(USER_EMAIL));
        UserDetails otherUser = userDetails(OTHER_EMAIL);

        assertThat(jwtService.isTokenValid(token, otherUser)).isFalse();
    }

    @Test
    void shouldRejectExpiredToken() {
        ReflectionTestUtils.setField(jwtService, EXPIRATION_FIELD, EXPIRED);
        String token = jwtService.generateToken(userDetails(USER_EMAIL));

        ReflectionTestUtils.setField(jwtService, EXPIRATION_FIELD, EXPIRATION);
        UserDetails user = userDetails(USER_EMAIL);

        assertThatThrownBy(() -> jwtService.isTokenValid(token, user))
                .isInstanceOf(Exception.class);
    }
}