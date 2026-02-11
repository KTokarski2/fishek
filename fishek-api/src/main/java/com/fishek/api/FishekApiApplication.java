package com.fishek.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class FishekApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(FishekApiApplication.class, args);
	}

}
