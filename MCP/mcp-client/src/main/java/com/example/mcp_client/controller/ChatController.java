package com.example.mcp_client.controller;

import com.example.mcp_client.service.ChatService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/chat")
public class ChatController {

    private final ChatService chatService;

    public ChatController(ChatService chatService) {
        this.chatService = chatService;
    }

    @GetMapping
    public String chat(@RequestParam String message) {

        return chatService.chat(message);
    }
}