package com.example.mcp_server;

import com.example.mcp_server.tools.EmployeeTools;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class McpServerApplication {

	public static void main(String[] args) {
		SpringApplication.run(McpServerApplication.class, args);
	}
	// This bean tells Spring AI MCP:
	// "These are the tools to expose over MCP protocol"
	@Bean
	public ToolCallbackProvider employeeToolCallbackProvider(EmployeeTools employeeTools) {
		return MethodToolCallbackProvider.builder()
				.toolObjects(employeeTools)
				.build();
	}

}
