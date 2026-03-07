package com.fishek.api.rest.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fishek.api.config.JpaConfig;
import com.fishek.api.config.JwtAuthFilter;
import com.fishek.api.config.SecurityConfig;
import com.fishek.api.config.UserDetailsServiceConfig;
import com.fishek.api.exception.EmailAlreadyExistsException;
import com.fishek.api.model.dto.AuthResponse;
import com.fishek.api.model.dto.LoginRequest;
import com.fishek.api.model.dto.RegisterRequest;
import com.fishek.api.repository.UserRepository;
import com.fishek.api.rest.exception.GlobalExceptionHandler;
import com.fishek.api.service.AuthService;
import com.fishek.api.service.JwtService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.jackson.autoconfigure.JacksonAutoConfiguration;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(AuthController.class)
@Import({SecurityConfig.class, UserDetailsServiceConfig.class, GlobalExceptionHandler.class})
class AuthControllerTest {

    private static final String REGISTER_URL = "/api/v1/auth/register";
    private static final String LOGIN_URL = "/api/v1/auth/login";
    private static final String USER_EMAIL = "user@test.com";
    private static final String INVALID_EMAIL = "not-an-email";
    private static final String PASSWORD = "password123";
    private static final String JWT_TOKEN = "jwt-token";
    private static final String TOKEN_JSON_PATH = "$.token";
    private static final String EMAIL_ALREADY_IN_USE = "Email already in use";

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Autowired MockMvc mockMvc;

    @MockitoBean AuthService authService;
    @MockitoBean JwtAuthFilter jwtAuthFilter;
    @MockitoBean JwtService jwtService;
    @MockitoBean UserDetailsService userDetailsService;
    @MockitoBean UserRepository userRepository;

    @BeforeEach
    void setUp() throws Exception {
        doAnswer(invocation -> {
            invocation.getArgument(2, jakarta.servlet.FilterChain.class)
                    .doFilter(
                            invocation.getArgument(0, jakarta.servlet.ServletRequest.class),
                            invocation.getArgument(1, jakarta.servlet.ServletResponse.class)
                    );
            return null;
        }).when(jwtAuthFilter).doFilter(any(), any(), any());
    }

    @Test
    void shouldReturn201OnRegister() throws Exception {
        when(authService.register(any())).thenReturn(new AuthResponse(JWT_TOKEN));

        mockMvc.perform(post(REGISTER_URL)
                        .with(csrf())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(
                                new RegisterRequest(USER_EMAIL, PASSWORD)
                        )))
                .andExpect(status().isCreated())
                .andExpect(jsonPath(TOKEN_JSON_PATH).value(JWT_TOKEN));
    }

    @Test
    void shouldReturn400WhenEmailInvalid() throws Exception {
        mockMvc.perform(post(REGISTER_URL)
                        .with(csrf())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(
                                new RegisterRequest(INVALID_EMAIL, PASSWORD)
                        )))
                .andExpect(status().isBadRequest());
    }

    @Test
    void shouldReturn409WhenEmailAlreadyExists() throws Exception {
        when(authService.register(any()))
                .thenThrow(new EmailAlreadyExistsException(EMAIL_ALREADY_IN_USE));

        mockMvc.perform(post(REGISTER_URL)
                        .with(csrf())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(
                                new RegisterRequest(USER_EMAIL, PASSWORD)
                        )))
                .andExpect(status().isConflict());
    }

    @Test
    void shouldReturn200OnLogin() throws Exception {
        when(authService.login(any())).thenReturn(new AuthResponse(JWT_TOKEN));

        mockMvc.perform(post(LOGIN_URL)
                        .with(csrf())
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(
                                new LoginRequest(USER_EMAIL, PASSWORD)
                        )))
                .andExpect(status().isOk())
                .andExpect(jsonPath(TOKEN_JSON_PATH).value(JWT_TOKEN));
    }
}