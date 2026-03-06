package com.fishek.api.service;

import com.fishek.api.exception.EmailAlreadyExistsException;
import com.fishek.api.model.dto.AuthResponse;
import com.fishek.api.model.dto.LoginRequest;
import com.fishek.api.model.dto.RegisterRequest;
import com.fishek.api.model.persistance.User;
import com.fishek.api.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;

    public static final String ERROR_EMAIL_ALREADY_IN_USE = "Email already in use";
    public static final String ERROR_INVALID_LOGIN = "Username not found or incorrect password";

    public AuthResponse register(RegisterRequest request) {
        if (userRepository.findByEmail(request.email()).isPresent()) {
            throw new EmailAlreadyExistsException(ERROR_EMAIL_ALREADY_IN_USE);
        }
        User user = User.builder()
                .email(request.email())
                .password(passwordEncoder.encode(request.password()))
                .build();
        userRepository.save(user);
        return AuthResponse.builder()
                .token(jwtService.generateToken(user))
                .build();
    }

    public AuthResponse login(LoginRequest request) {
        authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(request.email(), request.password())
        );
        User user = userRepository.findByEmail(request.email())
                .orElseThrow(() -> new UsernameNotFoundException(ERROR_INVALID_LOGIN));
        return AuthResponse.builder()
                .token(jwtService.generateToken(user))
                .build();
    }
}
