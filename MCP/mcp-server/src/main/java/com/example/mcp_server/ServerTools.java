package com.example.mcp_server;

import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ServerTools {

    // 1. We put the tool in a plain, un-annotated Java class.
    // Because it doesn't have @Configuration, Spring won't wrap it in a proxy!
    public static class MyWeatherService {

        @Tool(description = "Get the current weather for a location")
        public String getWeather(String location) {
            System.out.println("MCP SERVER: getWeather was just called for " + location + "!");
            return "The weather in " + location + " is 22 degrees and sunny!";
        }
    }

    // 2. We explicitly pass a NEW instance of our plain class to the provider
    @Bean
    public ToolCallbackProvider weatherToolProvider() {
        return MethodToolCallbackProvider.builder()
                // FIX: Pass the raw object instead of the 'this' proxy
                .toolObjects(new MyWeatherService())
                .build();
    }
}