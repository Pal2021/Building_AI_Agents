package com.example.mcp_client.service;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.mcp.SyncMcpToolCallbackProvider;
import org.springframework.stereotype.Service;

@Service
public class ChatService {

    private final ChatClient chatClient;

    // ✅ Put all your context here — never repeat in prompts again
    private static final String SYSTEM_PROMPT = """
            You are a helpful assistant with two capabilities:
            
            1. EMPLOYEE DATA (via employee MCP server):
               - Query employee records from MySQL database
               - Tools: getAllEmployees, getEmployeesByDepartment, 
                 getHighestPaidEmployee, getLowestPaidEmployee,
                 countEmployeesInDepartment, getAverageSalaryByDepartment,
                 getEmployeesWithSalaryGreaterThan, getTopNHighestPaidEmployees,
                 getEmployeesByCity
            
            2. GITHUB OPERATIONS (via GitHub MCP server):
               - GitHub username: pal2021       
               - Default repository: wellfitness.in    
               - Always use these defaults unless user specifies otherwise
               - Tools available: list repos, create/list/close issues,
                 list/merge pull requests, search repos, get user info
            
            RULES:
            - NEVER ask for GitHub username — always use: pal2021
            - NEVER ask for repo name if unclear — use default: wellfitness.in 
            - NEVER say a tool is unavailable — try calling it first
            - If a request is ambiguous, make a reasonable assumption and proceed
            - Always be direct and complete the action without asking for clarification
            """;

    public ChatService(ChatClient.Builder builder, SyncMcpToolCallbackProvider toolCallbackProvider) {
        var tools = toolCallbackProvider.getToolCallbacks();
        System.out.println("Tools loaded from MCP: " + tools.length);

        this.chatClient = builder
                .defaultToolCallbacks(tools)
                .defaultSystem(SYSTEM_PROMPT)
                .build();
    }

    public String chat(String userMessage) {
        return chatClient.prompt()
                .user(userMessage)
                .call()
                .content();
    }
}