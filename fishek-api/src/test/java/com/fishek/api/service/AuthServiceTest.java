package com.fishek.api.service;

import com.fishek.api.exception.EmailAlreadyExistsException;
import com.fishek.api.model.dto.AuthResponse;
import com.fishek.api.model.dto.LoginRequest;
import com.fishek.api.model.dto.RegisterRequest;
import com.fishek.api.model.persistance.User;
import com.fishek.api.repository.UserRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    private static final String USER_EMAIL = "user@test.com";
    private static final String UNKNOWN_EMAIL = "unknown@test.com";
    private static final String PASSWORD = "password123";
    private static final String HASHED_PASSWORD = "hashed";
    private static final String JWT_TOKEN = "jwt-token";
    private static final String EMAIL_ALREADY_IN_USE = "Email already in use";

    @Mock private UserRepository userRepository;
    @Mock private PasswordEncoder passwordEncoder;
    @Mock private JwtService jwtService;
    @Mock private AuthenticationManager authenticationManager;

    @InjectMocks
    private AuthService authService;

    @Test
    void shouldRegisterNewUser() {
        RegisterRequest request = new RegisterRequest(USER_EMAIL, PASSWORD);

        when(userRepository.findByEmail(USER_EMAIL)).thenReturn(Optional.empty());
        when(passwordEncoder.encode(PASSWORD)).thenReturn(HASHED_PASSWORD);
        when(userRepository.save(any(User.class))).thenAnswer(i -> i.getArgument(0));
        when(jwtService.generateToken(any())).thenReturn(JWT_TOKEN);

        AuthResponse response = authService.register(request);

        assertThat(response.token()).isEqualTo(JWT_TOKEN);
        verify(userRepository).save(any(User.class));
    }

    @Test
    void shouldThrowWhenEmailAlreadyExists() {
        RegisterRequest request = new RegisterRequest(USER_EMAIL, PASSWORD);
        when(userRepository.findByEmail(USER_EMAIL)).thenReturn(Optional.of(new User()));

        assertThatThrownBy(() -> authService.register(request))
                .isInstanceOf(EmailAlreadyExistsException.class)
                .hasMessageContaining(EMAIL_ALREADY_IN_USE);

        verify(userRepository, never()).save(any());
    }

    @Test
    void shouldLoginAndReturnToken() {
        LoginRequest request = new LoginRequest(USER_EMAIL, PASSWORD);
        User user = User.builder().email(USER_EMAIL).password(HASHED_PASSWORD).build();

        when(userRepository.findByEmail(USER_EMAIL)).thenReturn(Optional.of(user));
        when(jwtService.generateToken(user)).thenReturn(JWT_TOKEN);

        AuthResponse response = authService.login(request);

        assertThat(response.token()).isEqualTo(JWT_TOKEN);
        verify(authenticationManager).authenticate(any(UsernamePasswordAuthenticationToken.class));
    }

    @Test
    void shouldThrowWhenUserNotFoundOnLogin() {
        LoginRequest request = new LoginRequest(UNKNOWN_EMAIL, PASSWORD);
        when(userRepository.findByEmail(UNKNOWN_EMAIL)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> authService.login(request))
                .isInstanceOf(Exception.class);
    }
}