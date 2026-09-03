package com.spring_ai_tools.spring_ai_tools_calling.config;

import org.springframework.ai.tool.execution.ToolExecutionException;
import org.springframework.ai.tool.execution.ToolExecutionExceptionProcessor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ToolConfig {

    @Bean
    public ToolExecutionExceptionProcessor toolExecutionExceptionProcessor() {
        return (exception) -> {
            // Extract the tool name using the clean record-style .name() method
            String toolName = (exception.getToolDefinition() != null)
                    ? exception.getToolDefinition().name() // Fixed here! Changed from getName() to name()
                    : "Unknown Tool";

            // Unpack the real root error thrown inside your Java method
            Throwable rootCause = exception.getCause();
            String errorMessage = (rootCause != null) ? rootCause.getMessage() : exception.getMessage();

            // 1. Handle Invalid Arguments
            if (rootCause instanceof IllegalArgumentException) {
                return "Invalid input provided to " + toolName + ". Please check your request parameters.";
            }

            // 2. Handle System or Network Connection drops
            if (errorMessage != null && errorMessage.contains("Connection")) {
                return "The service dependency for " + toolName + " is currently unavailable. Please try again shortly.";
            }

            // 3. Default fallback error text sent to the LLM
            return "Tool '" + toolName + "' encountered an infrastructure error: " + errorMessage;
        };
    }
}