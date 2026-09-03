package com.spring_ai_tools.spring_ai_tools_calling.service;

import com.spring_ai_tools.spring_ai_tools_calling.Tools.EmployeeTools;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Service;

@Service
public class ChatService {
    private final ChatClient chatClient;
    private final EmployeeTools employeeTools;

    public ChatService(ChatClient.Builder chatClient, EmployeeTools employeeTools) {
        this.chatClient = chatClient.build();
        this.employeeTools = employeeTools;
    }
    public String chat(String userMessage) {
        return chatClient.prompt()
                .user(userMessage)
                .tools(employeeTools)    // all @Tool methods in this class get registered
                .call()
                .content();
    }
}
